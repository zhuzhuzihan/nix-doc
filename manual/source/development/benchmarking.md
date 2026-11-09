# 运行基准测试

本指南介绍如何在 Nix 代码库中构建和运行性能基准测试。

## 概述

Nix 使用 [Google Benchmark](https://github.com/google/benchmark) 框架进行性能测试。基准测试有助于度量和跟踪关键操作（如 derivation（派生）解析）的性能。

## 构建基准测试

基准测试默认是禁用的，必须在构建配置阶段显式启用。为获得准确的结果，请使用调试优化的 release 构建。

### 搭建开发环境

首先，进入包含必要依赖的开发 shell：

```bash
nix develop .#native-ccacheStdenv
```

### 配置启用基准测试的构建

在项目根目录下，配置启用基准测试和优化的构建：

```bash
cd build
meson configure -Dbenchmarks=true -Dbuildtype=debugoptimized
```

`debugoptimized` 构建类型提供：
- 编译器优化，用于真实的性能测量
- 调试符号，用于性能剖析和分析
- 性能与可调试性之间的平衡

### 构建基准测试

构建包含基准测试的项目：

```bash
ninja
```

这会在构建目录中创建基准测试可执行文件。当前可用的有：
- `build/src/libstore-tests/nix-store-benchmarks` - store 相关的性能基准测试

随着更多基准测试被加入代码库，还会创建更多的基准测试可执行文件。

## 运行基准测试

### 基本用法

直接运行基准测试可执行文件。例如，运行 store 基准测试：

```bash
./build/src/libstore-tests/nix-store-benchmarks
```

随着更多基准测试可执行文件的加入，可以用同样的方式在各自对应的构建目录中运行它们。

### 过滤基准测试

使用正则表达式模式运行特定的基准测试：

```bash
# 只运行 derivation 解析器基准测试
./build/src/libstore-tests/nix-store-benchmarks --benchmark_filter="derivation.*"

# 只运行 hello.drv 相关的基准测试
./build/src/libstore-tests/nix-store-benchmarks --benchmark_filter=".*hello.*"
```

### 输出格式

以不同格式生成基准测试结果：

```bash
# JSON 输出
./build/src/libstore-tests/nix-store-benchmarks --benchmark_format=json > results.json

# CSV 输出
./build/src/libstore-tests/nix-store-benchmarks --benchmark_format=csv > results.csv
```

### 高级选项

```bash
# 多次运行基准测试以获得更好的统计数据
./build/src/libstore-tests/nix-store-benchmarks --benchmark_repetitions=10

# 设置最短基准测试时间（对微基准测试很有用）
./build/src/libstore-tests/nix-store-benchmarks --benchmark_min_time=2

# 与基线进行比较
./build/src/libstore-tests/nix-store-benchmarks --benchmark_baseline=baseline.json

# 以自定义单位显示时间
./build/src/libstore-tests/nix-store-benchmarks --benchmark_time_unit=ms
```

## 编写新的基准测试

要添加新的基准测试：

1. 在相应的 `*-tests` 目录中创建一个新的 `.cc` 文件
2. 包含基准测试头文件：
   ```cpp
   #include <benchmark/benchmark.h>
   ```

3. 编写基准测试函数：
   ```cpp
   static void BM_YourBenchmark(benchmark::State & state)
   {
       // Setup code here

       for (auto _ : state) {
           // Code to benchmark
       }
   }
   BENCHMARK(BM_YourBenchmark);
   ```

4. 将该文件添加到对应的 `meson.build` 中：
   ```meson
   benchmarks_sources = files(
       'your-benchmark.cc',
       # existing benchmarks...
   )
   ```

## 使用基准测试进行性能剖析

要进行更深入的性能分析，可以将基准测试与剖析工具结合使用：

```bash
# 使用 Linux perf
perf record ./build/src/libstore-tests/nix-store-benchmarks
perf report
```

### 使用 Valgrind Callgrind

Valgrind 的 callgrind 工具提供详细的剖析信息，可以用 kcachegrind 进行可视化：

```bash
# 使用 callgrind 进行剖析
valgrind --tool=callgrind ./build/src/libstore-tests/nix-store-benchmarks

# 用 kcachegrind 可视化结果
kcachegrind callgrind.out.*
```

这可以提供：
- 函数调用图
- 指令级别的剖析
- 源代码标注
- 性能瓶颈的交互式可视化

## 持续性能测试

```bash
# 保存基线结果
./build/src/libstore-tests/nix-store-benchmarks --benchmark_format=json > baseline.json

# 在 CI 中与基线进行比较
./build/src/libstore-tests/nix-store-benchmarks --benchmark_baseline=baseline.json
```

## 故障排除

### 基准测试未构建

确保基准测试已启用：
```bash
meson configure build | grep benchmarks
# Should show: benchmarks true
```

### 结果不一致

- 确保你的系统没有处于高负载状态
- 禁用 CPU 频率调节以获得一致的结果
- 使用 `--benchmark_repetitions` 多次运行基准测试

## 另请参阅

- [Google Benchmark 文档](https://github.com/google/benchmark/blob/main/docs/user_guide.md)
