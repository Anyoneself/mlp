# Linux 进程与网络排障

**阶段：** 基础补齐  
**建议时间：** 第 1 周前半段  
**前置条件：** Linux 主机或 Linux 容器

## 目标

掌握从进程、文件描述符、端口和系统负载四个方向定位服务异常。

## 实现说明

- `main.py` 使用父进程启动 CPU Worker 和 HTTP Worker，输出 PID，并负责
  信号处理与子进程清理。
- `diagnose.sh` 以 PID 和端口为线索，采集进程、负载、文件描述符和网络状态，
  再验证端口冲突与退出清理。
- `diagnostics.md` 保存环境、关键输出和判断依据，使排障过程可以被复查。

核心流程：

1. Parent 启动持续整数运算的 CPU Worker 和本地 HTTP Worker。
2. HTTP Worker 绑定端口后，通过单向 Pipe 向 Parent 报告启动结果。
3. Parent 完成健康检查、输出三个 PID，并等待 `SIGINT` 或 `SIGTERM`。
4. 诊断脚本根据 PID 和端口执行观测，最后触发信号并确认端口释放。

关键技术选择：

- HTTP 服务只绑定 `127.0.0.1`，避免将练习端口暴露到外部网络。
- Pipe 用于确认成功绑定的是当前 HTTP Worker，避免端口冲突时误连到旧服务。
- Worker 恢复默认终止信号处理，只有 Parent 负责优雅退出和统一清理。
- 诊断脚本使用临时目录和 `trap`，成功或失败时都不会遗留进程和日志。

## 学习与复现

### 1. 环境准备

依赖 Python 3，以及 `procps`、`sysstat`、`lsof`、`iproute2` 和 `curl`
提供的诊断命令。进入项目根目录后，以 Ubuntu 为例安装：

```bash
sudo apt-get update
sudo apt-get install -y python3 procps sysstat lsof iproute2 curl
```

没有 Linux 主机时，也可以使用 Docker 或 Colima。首次运行需要联网拉取镜像和
Alpine 软件包：

```bash
docker run --rm \
  -v "$PWD":/workspace:ro \
  alpine:3.22.2 \
  sh -c 'apk add --no-cache bash python3 curl procps sysstat lsof iproute2 >/dev/null &&
    /workspace/example/01_linux_process_network/diagnose.sh'
```

#### 交互式 Linux 容器

需要逐条练习 Linux 命令时，可以使用两个终端进入同一个容器。先在终端一进入
项目根目录。使用 Colima 时启动运行时；使用 Docker Desktop 时跳过
`colima start`：

```bash
cd /Users/yuanzhi.liu/Desktop/code/mlp
colima start

docker run --rm -it \
  --name linux-process-lab \
  -v "$PWD":/workspace:ro \
  -w /workspace \
  alpine:3.22.2 sh
```

进入容器后安装诊断工具并切换到 Bash：

```bash
apk add --no-cache bash python3 curl procps sysstat lsof iproute2
bash
```

在终端一的容器内启动测试服务：

```bash
python3 example/01_linux_process_network/main.py \
  --port 18080 \
  --state-file /tmp/linux-process-network.json
```

保持服务运行，打开终端二并进入同一个容器：

```bash
docker exec -it linux-process-lab bash
cd /workspace
```

读取 CPU Worker 和 HTTP Worker 的 PID：

```bash
cat /tmp/linux-process-network.json

CPU_PID="$(python3 -c \
  'import json; print(json.load(open("/tmp/linux-process-network.json"))["cpu_pid"])')"
HTTP_PID="$(python3 -c \
  'import json; print(json.load(open("/tmp/linux-process-network.json"))["http_pid"])')"
```

此时可以在终端二执行后文的 `ps`、`top`、`pidstat`、`lsof`、`ss`、
`vmstat`、`free` 和 `df` 命令。完成后：

1. 在终端二执行 `exit`，退出诊断 Shell。
2. 在终端一按 `Ctrl+C` 停止测试服务。
3. 在终端一执行 `exit` 退出容器；`--rm` 会自动删除容器。
4. 不再需要 Colima 时，在宿主机执行 `colima stop`。

### 2. 自动复现

在项目根目录执行：

```bash
chmod +x example/01_linux_process_network/diagnose.sh
example/01_linux_process_network/diagnose.sh
```

预期最后输出：

```text
端口 18080 已释放

所有诊断检查通过。
```

### 3. 手动学习

在项目根目录的第一个终端启动服务，并将 PID 写入临时状态文件：

```bash
python3 example/01_linux_process_network/main.py \
  --port 18080 \
  --state-file /tmp/linux-process-network.json
```

在第二个终端读取 PID 并执行诊断：

下面这组命令使用 Linux 参数，完整验收应在 Linux 主机或前述容器中执行。
macOS 的 `top`、内存和网络工具参数不同，不能直接复制这组命令。

```bash
CPU_PID="$(python3 -c \
  'import json; print(json.load(open("/tmp/linux-process-network.json"))["cpu_pid"])')"
HTTP_PID="$(python3 -c \
  'import json; print(json.load(open("/tmp/linux-process-network.json"))["http_pid"])')"

ps -o pid,ppid,stat,pcpu,comm,args -p "${CPU_PID},${HTTP_PID}"
top -b -n 1 -p "${CPU_PID}"
pidstat -p "${CPU_PID}" 1 1
lsof -nP -a -p "${HTTP_PID}" -iTCP:18080 -sTCP:LISTEN
ss -ltnp '( sport = :18080 )'
vmstat 1 2
free -h
df -h /
```

如果只想在 macOS 上快速观察同一个测试服务，可以执行：

```bash
ps -o pid,ppid,stat,pcpu,comm,args -p "${CPU_PID},${HTTP_PID}"
top -l 1 -pid "${CPU_PID}" -stats pid,ppid,state,cpu,mem,time,command
lsof -nP -a -p "${HTTP_PID}" -iTCP:18080 -sTCP:LISTEN
vm_stat
memory_pressure
df -h /
```

macOS 默认没有 Linux 的 `pidstat`、`ss` 和 `free`。其中 `lsof` 可以同时完成
PID 查端口和端口查 PID，`vm_stat` 与 `memory_pressure` 用于观察内存状态。

回到第一个终端按 `Ctrl+C`，再在第二个终端确认端口已经释放：

```bash
ss -ltn '( sport = :18080 )'
```

### 4. 命令与参数说明

#### `ps`：查看指定进程

```bash
ps -o pid,ppid,stat,pcpu,comm,args -p "${CPU_PID},${HTTP_PID}"
```

- `-o`：指定输出列；`pid` 是进程 ID，`ppid` 是父进程 ID，`stat` 是进程状态，
  `pcpu` 是 CPU 使用率，`comm` 是程序名称，`args` 是完整启动命令。
- `-p`：只查看后面给出的 PID；两个变量展开后类似 `-p 41286,41287`。
- 观察重点：两个 Worker 应拥有相同的 PPID；CPU Worker 通常为 `R`，HTTP
  Worker 通常为 `S`。

#### `top`：获取 CPU 使用快照

```bash
top -b -n 1 -p "${CPU_PID}"
```

- `-b`：使用非交互的批处理模式，适合脚本采集。
- `-n 1`：刷新一次后退出。
- `-p`：只显示 CPU Worker。
- 观察重点：`%CPU`、`%MEM`、进程状态和累计 CPU 时间。这里使用的是 Linux
  `top` 参数，macOS 的参数不同。

macOS 对应命令为：

```bash
top -l 1 -pid "${CPU_PID}" -stats pid,ppid,state,cpu,mem,time,command
```

- `-l 1`：采集 1 次后退出。
- `-pid`：只观察指定 PID。
- `-stats`：指定要显示的字段。

#### `pidstat`：按时间采样进程 CPU

```bash
pidstat -p "${CPU_PID}" 1 1
```

- `-p`：指定要采样的进程 PID。
- 第一个 `1`：采样间隔为 1 秒；第二个 `1`：只采样 1 次。
- 观察重点：`%usr` 是用户态 CPU，`%system` 是内核态 CPU，`%wait` 是等待
  CPU 的比例，`%CPU` 是总 CPU 使用率。

#### `lsof`：从 PID 查询监听端口

```bash
lsof -nP -a -p "${HTTP_PID}" -iTCP:18080 -sTCP:LISTEN
```

- `-n`：不把 IP 解析为主机名；`-P`：不把端口转换为服务名称。
- `-a`：要求后续筛选条件同时满足，而不是取并集。
- `-p`：限定 HTTP Worker PID。
- `-iTCP:18080`：限定 TCP 端口 `18080`。
- `-sTCP:LISTEN`：只显示处于监听状态的 TCP Socket。
- 预期结果：HTTP Worker 持有 `127.0.0.1:18080` 的监听文件描述符。

#### `ss`：从端口反查进程

```bash
ss -ltnp '( sport = :18080 )'
```

- `-l`：只显示监听 Socket；`-t`：只显示 TCP；`-n`：显示数字地址和端口；
  `-p`：显示关联进程与 PID。
- `sport = :18080`：只保留本地端口为 `18080` 的 Socket。
- 观察重点：`users` 字段中的 PID 应与 `HTTP_PID` 相同。

服务退出后执行的 `ss -ltn '( sport = :18080 )'` 没有 `-p`，因为此时只需确认
端口是否仍处于监听状态，不需要查询进程信息。

#### `vmstat`：查看系统整体状态

```bash
vmstat 1 2
```

- `1`：每隔 1 秒采样；`2`：总共输出 2 次。
- `r` 是运行或等待 CPU 的进程数，`b` 是不可中断等待的进程数。
- `si/so` 是 Swap 读写，`bi/bo` 是块设备读写。
- `us`、`sy`、`id`、`wa` 分别表示用户态、内核态、空闲和 I/O 等待比例。
- 第一行通常是开机以来的平均值，第二行更接近当前状态。

#### `free`：查看内存

```bash
free -h
```

- `-h`：使用 MiB、GiB 等易读单位。
- 观察重点：`available` 表示考虑可回收缓存后的可用内存，`buff/cache` 表示
  缓存占用，`Swap` 表示交换空间。判断内存压力时不能只看 `free`。

#### `df`：查看文件系统容量

```bash
df -h /
```

- `-h`：使用 MiB、GiB 等易读单位。
- `/`：只查看根目录所在的文件系统。
- 观察重点：`Size` 是总容量，`Used` 是已用容量，`Avail` 是剩余容量，`Use%`
  是使用率，`Mounted on` 是挂载位置。

### 5. 观察点

- `ps` 中两个 Worker 的 PPID 相同；CPU Worker 通常为运行态，HTTP Worker
  通常为睡眠态。
- `top` 和 `pidstat` 中 CPU Worker 主要消耗用户态 CPU。
- `lsof` 从 HTTP Worker PID 找到 `18080`，`ss` 从 `18080` 反查到相同 PID。
- `vmstat` 应重点比较第二次采样，`free` 应关注 `available`，`df` 应同时关注
  `Use%` 和 `Avail`。
- Parent 收到信号后退出码为 0，随后 `ss` 不再显示监听端口。

### 6. 扩展实验

使用环境变量改为另一个端口运行自动验收：

```bash
PORT=18081 example/01_linux_process_network/diagnose.sh
```

运行前先预测 `lsof` 和 `ss` 中哪些字段会变化；运行后确认 PID 和端口虽然改变，
但父子进程关系、CPU 特征和端口释放结论保持一致。

## 验收标准

- 能从端口反查进程，也能从 PID 找到监听端口。
- 能区分 CPU 饱和、内存不足、磁盘不足和端口冲突。
- 能整理一份包含命令、现象和判断依据的排障记录。

## 预期产出

- `diagnostics.md`：命令输出摘要与故障判断。
- `main.py`：可重复启动并能响应终止信号的测试服务。
- `diagnose.sh`：覆盖正常路径和端口冲突路径的自动验收脚本。
