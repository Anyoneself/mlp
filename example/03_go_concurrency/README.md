# Go 并发 Worker Pool

**阶段：** 基础补齐  
**建议时间：** 第 2 周前半段  
**前置条件：** Go 开发环境

## 目标

实现支持并发上限、超时、取消和错误收集的 Go Worker Pool。

## 实现说明

- 使用任务输入 channel 和结果 channel 解耦生产者、Worker 与结果收集器。
- 每个 Worker 共享父 `context.Context`，单任务通过派生 context 设置超时。
- 用 `sync.WaitGroup` 管理退出，用结构化结果同时返回任务 ID、值、错误和耗时。

## 学习与复现

1. 定义任务输入、结果和错误结构。
2. 使用 goroutine 与 channel 实现固定数量 Worker。
3. 使用 `context.Context` 支持整体取消和单任务超时。
4. 注入慢任务与失败任务，验证资源能够回收。
5. 编写并发数、取消和错误路径测试。
6. 扩展实验：将 Worker 数从 1 调到 8，记录吞吐和取消延迟。

## 验收标准

- 实际并发数不超过配置上限。
- 取消后不再接收新任务，现有 goroutine 能退出。
- `go test -race ./...` 不报告数据竞争。

## 产出

- 可运行的 Go Worker Pool。
- 单元测试和简短设计说明。
