# Linux 进程与网络排障记录

**验收日期：** 2026-09-07  
**测试入口：** `example/01_linux_process_network/diagnose.sh`

## 执行环境

- 容器运行时：Colima 与 Docker。
- 操作系统：Alpine Linux 3.22.2。
- Python：3.12.14。
- 内核与架构：Linux 6.8.0-64-generic，aarch64。
- 资源：2 个逻辑 CPU，约 1.9 GiB 内存，无 GPU。
- 网络：测试服务只监听容器内的 `127.0.0.1`，不访问公网。

## 完整命令

基线实验：

```bash
docker run --rm \
  -v "$PWD":/workspace:ro \
  alpine:3.22.2 \
  sh -c 'apk add --no-cache bash python3 curl procps sysstat lsof iproute2 >/dev/null &&
    /workspace/example/01_linux_process_network/diagnose.sh'
```

端口参数扩展实验：

```bash
docker run --rm \
  -v "$PWD":/workspace:ro \
  -e PORT=18081 \
  alpine:3.22.2 \
  sh -c 'apk add --no-cache bash python3 curl procps sysstat lsof iproute2 >/dev/null &&
    /workspace/example/01_linux_process_network/diagnose.sh'
```

## 实际结果摘要

- CPU Worker 在 `top` 和 `pidstat` 中稳定占用 100% 的一个逻辑 CPU，
  主要消耗在用户态。
- `lsof` 显示 HTTP Worker 监听 `127.0.0.1:18080`，`ss` 从同一端口反查到
  相同 PID。
- 容器可用内存约 1.2 GiB、无 swap；根文件系统剩余约 2.7 GiB，使用率 97%，
  已属于需要关注但尚未写满的状态。
- 相同端口重复启动以退出码 1 失败。
- Parent 收到 `SIGTERM` 后记录该信号并以退出码 0 完成清理，端口随后释放。
- 使用 `PORT=18081` 重跑后，`lsof` 和 `ss` 显示新端口，父子进程关系、CPU
  负载特征、端口冲突和退出清理结论均保持一致。

两次运行的结尾均为：

```text
端口 <PORT> 已释放

所有诊断检查通过。
```

## 命令与判断依据

| 观察方向 | 命令 | 关键现象 | 判断依据 |
|---|---|---|---|
| 进程关系 | `ps -o pid,ppid,stat,pcpu,comm,args -p ...` | Parent 下存在 CPU 和 HTTP 两个 Worker | PPID 能还原父子进程关系，`STAT` 可识别运行、睡眠或僵尸状态 |
| CPU 负载 | `top -b -n 1 -p <CPU_PID>` | CPU Worker 持续占用一个逻辑 CPU | 单进程 `%CPU` 长期接近一个逻辑核上限，说明负载集中在该进程 |
| CPU 采样 | `pidstat -p <CPU_PID> 1 1` | `%usr` 明显高于 `%system` 和 `%wait` | 用户态计算造成 CPU 饱和，而不是内核调用或 I/O 等待 |
| PID 查端口 | `lsof -nP -a -p <HTTP_PID> -iTCP:18080 -sTCP:LISTEN` | HTTP Worker 持有 TCP LISTEN 文件描述符 | 指定 PID 的 FD 与监听地址、端口相互对应 |
| 端口查 PID | `ss -ltnp '( sport = :18080 )'` | `users` 字段包含 HTTP Worker PID | 可以从监听端口反查占用进程 |
| 系统负载 | `vmstat 1 2` | 可同时观察 runnable、free、swap、I/O、CPU idle/wait | 第二次采样比启动以来的平均值更适合判断当前状态 |
| 内存 | `free -h` | `available` 表示考虑可回收缓存后的可用内存 | `available` 持续很低且 swap 活跃时，才支持内存压力判断 |
| 磁盘 | `df -h /` | 根文件系统仍有可用空间 | `Use%` 接近 100% 或 `Avail` 过低支持磁盘容量不足判断 |
| 端口冲突 | 在服务存活时用相同端口再次启动 | 第二个进程非零退出并报告端口可能被占用 | 同一地址和端口无法重复绑定 |
| 信号退出 | `kill -TERM <PARENT_PID>` 后 `wait` | 服务记录 `received_signal=SIGTERM` 并以 0 退出 | Parent 捕获信号并完成子进程清理，属于正常的优雅退出 |
| 端口释放 | 服务退出后再次执行 `ss` | 端口不再处于 LISTEN | HTTP Worker 已退出，监听文件描述符已关闭 |

## 四类常见故障

### CPU 饱和

- 现象：`top` 或 `pidstat` 中一个或多个进程的 `%CPU` 长期接近可用逻辑核上限，
  `vmstat` 的 runnable 数量持续偏高且 CPU idle 很低。
- 定位：先用系统级指标确认整体压力，再按 PID 找到热点进程，区分用户态计算、
  内核态开销和 I/O wait。

### 内存不足

- 现象：`free` 的 `available` 持续很低，swap 持续增长；严重时进程被 OOM Killer
  终止。
- 定位：不能只看 `free` 列，因为 Linux 会把空闲内存用于缓存；应结合
  `available`、swap、进程 RSS 和内核日志判断。

### 磁盘不足

- 现象：`df` 的 `Use%` 接近 100%，写文件出现 `No space left on device`。
- 定位：容量正常但仍无法创建文件时，还应使用 `df -i` 检查 inode 是否耗尽。

### 端口冲突

- 现象：服务绑定端口时出现 `Address already in use` 或本示例的
  “端口可能已被占用”错误。
- 定位：使用 `ss -ltnp` 从端口反查 PID，再用 `ps` 确认进程身份；不要直接终止
  未确认归属的进程。

## 结论

自动验收覆盖了正常启动、HTTP 健康检查、CPU 负载观测、PID 与端口双向追踪、
相同端口重复绑定失败、`SIGTERM` 优雅退出及端口释放。脚本不会连接公网，测试
服务只监听 `127.0.0.1`。
