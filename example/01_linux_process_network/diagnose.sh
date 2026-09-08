#!/usr/bin/env bash

# 自动完成 Linux 进程、端口和系统负载诊断，并验证异常与清理路径。
set -eu

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PORT="${PORT:-18080}"
TMP_DIR="$(mktemp -d)"
STATE_FILE="${TMP_DIR}/state.json"
SERVICE_LOG="${TMP_DIR}/service.log"
SERVICE_PID=""

# 无论脚本在哪一步退出，都回收测试服务和临时诊断文件。
cleanup() {
    if [ -n "${SERVICE_PID}" ] && kill -0 "${SERVICE_PID}" 2>/dev/null; then
        kill -TERM "${SERVICE_PID}"
        wait "${SERVICE_PID}" || true
    fi
    rm -rf "${TMP_DIR}"
}
trap cleanup EXIT

require_command() {
    if ! command -v "$1" >/dev/null 2>&1; then
        echo "缺少命令: $1" >&2
        exit 1
    fi
}

if [ "$(uname -s)" != "Linux" ]; then
    echo "此脚本需要 Linux 主机或 Linux 容器。" >&2
    exit 1
fi

for command in python3 curl ps top pidstat lsof ss vmstat free df; do
    require_command "${command}"
done

python3 "${SCRIPT_DIR}/main.py" \
    --port "${PORT}" \
    --state-file "${STATE_FILE}" \
    >"${SERVICE_LOG}" 2>&1 &
SERVICE_PID=$!

# 状态文件由服务就绪后原子步骤写出，可同时用于判断启动失败。
for _ in $(seq 1 100); do
    if [ -s "${STATE_FILE}" ]; then
        break
    fi
    if ! kill -0 "${SERVICE_PID}" 2>/dev/null; then
        cat "${SERVICE_LOG}" >&2
        exit 1
    fi
    sleep 0.05
done

if [ ! -s "${STATE_FILE}" ]; then
    echo "服务未在 5 秒内就绪" >&2
    exit 1
fi

CPU_PID="$(python3 -c \
    'import json, sys; print(json.load(open(sys.argv[1]))["cpu_pid"])' \
    "${STATE_FILE}")"
HTTP_PID="$(python3 -c \
    'import json, sys; print(json.load(open(sys.argv[1]))["http_pid"])' \
    "${STATE_FILE}")"

test "$(curl --fail --silent "http://127.0.0.1:${PORT}/")" = "ok"

echo "== 进程状态: ps =="
ps -o pid,ppid,stat,pcpu,comm,args \
    -p "${SERVICE_PID},${CPU_PID},${HTTP_PID}"

echo
echo "== CPU 快照: top =="
top -b -n 1 -p "${CPU_PID}" | head -n 12

echo
echo "== CPU 采样: pidstat =="
pidstat -p "${CPU_PID}" 1 1

echo
echo "== 从 PID 查看监听端口: lsof =="
lsof -nP -a -p "${HTTP_PID}" -iTCP:"${PORT}" -sTCP:LISTEN

echo
echo "== 从端口反查 PID: ss =="
SS_OUTPUT="$(ss -ltnp "( sport = :${PORT} )")"
echo "${SS_OUTPUT}"
echo "${SS_OUTPUT}" | grep -q "pid=${HTTP_PID},"

echo
echo "== 系统负载: vmstat =="
vmstat 1 2

echo
echo "== 内存: free =="
free -h

echo
echo "== 根文件系统: df =="
df -h /

echo
echo "== 端口冲突验证 =="
# 第二个服务必须因相同地址和端口无法重复绑定而快速失败。
set +e
python3 "${SCRIPT_DIR}/main.py" --port "${PORT}" \
    >"${TMP_DIR}/conflict.log" 2>&1
CONFLICT_STATUS=$?
set -e
test "${CONFLICT_STATUS}" -ne 0
echo "重复启动退出码: ${CONFLICT_STATUS}"
CONFLICT_OUTPUT="$(grep -E \
    "Address already in use|HTTP 服务启动失败" \
    "${TMP_DIR}/conflict.log" || true)"
test -n "${CONFLICT_OUTPUT}"
echo "${CONFLICT_OUTPUT}" | tail -n 1

echo
echo "== SIGTERM 与端口释放验证 =="
kill -TERM "${SERVICE_PID}"
set +e
wait "${SERVICE_PID}"
SERVICE_STATUS=$?
set -e
SERVICE_PID=""
echo "服务退出码: ${SERVICE_STATUS}"
grep "received_signal=SIGTERM" "${SERVICE_LOG}"
test "${SERVICE_STATUS}" -eq 0

# SIGTERM 完成后轮询监听状态，避免把异步释放误判为失败。
for _ in $(seq 1 40); do
    if ! ss -ltn "( sport = :${PORT} )" | grep -q LISTEN; then
        break
    fi
    sleep 0.05
done

if ss -ltn "( sport = :${PORT} )" | grep -q LISTEN; then
    echo "端口 ${PORT} 未释放" >&2
    exit 1
fi

echo "端口 ${PORT} 已释放"
echo
echo "所有诊断检查通过。"
