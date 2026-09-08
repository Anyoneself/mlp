"""启动用于 Linux 进程与网络排障练习的本地测试服务。"""

from __future__ import annotations

import argparse
import json
import multiprocessing
import signal
import socket
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from multiprocessing.connection import Connection
from pathlib import Path
from threading import Event
from typing import Sequence


class HealthHandler(BaseHTTPRequestHandler):
    """返回固定健康检查响应，避免诊断结果受业务逻辑影响。"""

    def do_GET(self) -> None:  # noqa: N802
        body = b"ok\n"
        self.send_response(200)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format: str, *args: object) -> None:
        del format, args


def reset_termination_signals() -> None:
    """避免 fork 启动的 Worker 继承 Parent 的优雅退出处理器。"""
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    signal.signal(signal.SIGTERM, signal.SIG_DFL)


def burn_cpu() -> None:
    """持续进行整数运算，提供可观测但内存稳定的 CPU 负载。"""
    reset_termination_signals()
    value = 1
    while True:
        value = (value * 1_664_525 + 1_013_904_223) & 0xFFFFFFFF


def serve_http(port: int, ready_sender: Connection) -> None:
    """绑定回环地址并向父进程报告当前 Worker 的启动结果。"""
    reset_termination_signals()
    try:
        server = ThreadingHTTPServer(("127.0.0.1", port), HealthHandler)
    except OSError as error:
        ready_sender.send(("error", str(error)))
        ready_sender.close()
        raise
    ready_sender.send(("ready", ""))
    ready_sender.close()
    server.serve_forever()


def wait_for_http(
    port: int,
    process: multiprocessing.Process,
    ready_receiver: Connection,
) -> None:
    """等待当前 HTTP Worker 完成端口绑定和健康检查。"""
    # 先通过 Pipe 确认绑定者是当前 Worker，避免误连到占用同一端口的旧服务。
    if not ready_receiver.poll(5):
        if not process.is_alive():
            raise RuntimeError("HTTP Worker 在报告就绪前退出")
        raise TimeoutError("HTTP Worker 未能在 5 秒内报告就绪")

    status, detail = ready_receiver.recv()
    if status != "ready":
        raise RuntimeError(f"HTTP 服务启动失败: {detail}")

    deadline = time.monotonic() + 5
    while time.monotonic() < deadline:
        if not process.is_alive():
            raise RuntimeError("HTTP Worker 在健康检查完成前退出")
        try:
            with socket.create_connection(("127.0.0.1", port), timeout=0.1):
                return
        except OSError:
            time.sleep(0.05)
    raise TimeoutError(f"HTTP 服务未能在 5 秒内监听端口 {port}")


def stop_process(process: multiprocessing.Process) -> None:
    """终止并回收子进程，超时后使用强制终止兜底。"""
    if not process.is_alive():
        process.join()
        return
    process.terminate()
    process.join(timeout=2)
    # 子进程忽略 SIGTERM 时不能让父进程无限等待。
    if process.is_alive():
        process.kill()
        process.join()


def write_state(
    state_file: Path,
    cpu_process: multiprocessing.Process,
    http_process: multiprocessing.Process,
    port: int,
) -> None:
    """写入诊断脚本需要的 PID 与端口信息。"""
    state = {
        "parent_pid": multiprocessing.current_process().pid,
        "cpu_pid": cpu_process.pid,
        "http_pid": http_process.pid,
        "port": port,
    }
    state_file.write_text(
        json.dumps(state, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    """解析服务端口和可选状态文件路径。"""
    parser = argparse.ArgumentParser(
        description="启动 CPU 负载进程和仅监听本机的 HTTP 测试服务。",
    )
    parser.add_argument("--port", type=int, default=18080)
    parser.add_argument("--state-file", type=Path)
    args = parser.parse_args(argv)
    if not 1 <= args.port <= 65535:
        parser.error("--port 必须在 1 到 65535 之间")
    return args


def main(argv: Sequence[str] | None = None) -> None:
    """启动测试 Worker，等待终止信号并完成资源清理。"""
    args = parse_args(argv)
    stop_event = Event()

    def handle_signal(signum: int, frame: object) -> None:
        del frame
        print(
            f"received_signal={signal.Signals(signum).name}",
            flush=True,
        )
        stop_event.set()

    signal.signal(signal.SIGINT, handle_signal)
    signal.signal(signal.SIGTERM, handle_signal)

    cpu_process = multiprocessing.Process(target=burn_cpu, name="cpu-worker")
    ready_receiver, ready_sender = multiprocessing.Pipe(duplex=False)
    http_process = multiprocessing.Process(
        target=serve_http,
        args=(args.port, ready_sender),
        name="http-worker",
    )
    cpu_process.start()
    http_process.start()
    ready_sender.close()

    try:
        wait_for_http(args.port, http_process, ready_receiver)
        assert cpu_process.is_alive(), "CPU Worker 必须保持运行"
        assert http_process.is_alive(), "HTTP Worker 必须保持运行"
        if args.state_file is not None:
            write_state(args.state_file, cpu_process, http_process, args.port)
        print(
            f"parent_pid={multiprocessing.current_process().pid} "
            f"cpu_pid={cpu_process.pid} "
            f"http_pid={http_process.pid} "
            f"port={args.port}",
            flush=True,
        )
        stop_event.wait()
    finally:
        ready_receiver.close()
        stop_process(http_process)
        stop_process(cpu_process)


if __name__ == "__main__":
    main()
