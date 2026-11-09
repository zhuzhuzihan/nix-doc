# 运行测试

## 覆盖率分析

[覆盖率分析报告]可在线查阅。
你也可以自行构建：

[coverage analysis report]: https://hydra.nixos.org/job/nix/master/coverage/latest/download-by-type/report/coverage

```
# nix build .#hydraJobs.coverage
# xdg-open ./result/index.html
```

[大量构建指标的记录](https://hydra.nixos.org/job/nix/master/coverage#tabs-charts)，例如随时间变化的测试覆盖率，也可在线查阅。

## 单元测试

单元测试使用 [googletest] 和 [rapidcheck] 框架定义。

[googletest]: https://google.github.io/googletest/
[rapidcheck]: https://github.com/emil-e/rapidcheck
[property testing]: https://en.wikipedia.org/wiki/Property_testing

### 源码与头文件布局

> 一些文件的示例，展示了下文描述的大部分内容
>
> ```
> src
> ├── libexpr
> │   ├── meson.build
> │   ├── include/nix/expr/value/context.hh
> │   ├── value/context.cc
> │   …
> │
> ├── libutil-tests
> │   ├── meson.build
> │   …
> │   ├── data
> │   │   ├── git/tree.txt
> │       …
> │
> ├── libexpr-test-support
> │   ├── meson.build
> │   ├── include/nix/expr
> │   │   ├── meson.build
> │   │   └── tests
> │   │       ├── value/context.hh
> │   │       …
> │   ├── tests
> │       ├── value/context.cc
> │       …
> │
> ├── libexpr-tests
> │   ├── meson.build
> │   ├── value/context.cc
> │    …
> …
> ```

每个 Nix 库（`libnixexpr`、`libnixstore` 等）的测试都位于 `src/${library_name_without-nix}-test` 目录中。
给定原始库中的一对接口（头文件）与实现，例如 `src/libexpr/include/nix/expr/value/context.hh` 和 `src/libexpr/value/context.cc`，我们在 `src/libexpr-tests/value/context.cc` 中为它编写测试，并（可能）在 `src/libexpr-test-support/include/nix/expr/tests/value/context.hh` 和 `src/libexpr-test-support/tests/value/context.cc` 中为测试目的声明/定义额外的接口。

单元测试的数据存储在每个单元测试可执行文件所在目录的 `data` 子目录中。
例如，`libnixstore` 的代码在 `src/libstore`，其测试数据在 `src/libstore-tests/data`。
`src/${library_name_without-nix}-test/data` 目录的路径通过环境变量 `_NIX_TEST_UNIT_DATA` 传给单元测试可执行文件。
注意，每个可执行文件只会拿到它自己测试所需的数据。

单元测试库位于 `src/${library_name_without-nix}-test-support`。
所有头文件都放在 `tests` 子目录中，因此可以用 `#include "nix/tests/"` 包含它们。

单元测试使用这些相互独立的目录看起来可能不太方便，例如测试并没有“紧挨着”它们所测试的代码。
但以这种方式组织测试有一个很大的好处：
库的构建系统通配符不会有任何风险误拾取那些不应被构建并作为库的一部分安装的测试代码。

### 运行测试

你可以在 Meson 构建目录中用 `meson test` 运行整个测试套件，或者用 `meson test nix-store-tests` 运行特定组件的测试。
Google Test 接受的环境变量也值得了解：

1. [`GTEST_FILTER`](https://google.github.io/googletest/advanced.html#running-a-subset-of-the-tests)

   用于更细粒度地过滤要运行哪些测试。


2. [`GTEST_BRIEF`](https://google.github.io/googletest/advanced.html#suppressing-test-passes)

   用于避免记录通过的测试。

3. [`GTEST_BREAK_ON_FAILURE`](https://google.github.io/googletest/advanced.html#turning-assertion-failures-into-break-points)

   用于在断言失败发生时创建一个调试器断点。

把前两者结合起来，可以运行

```bash
GTEST_BRIEF=1 GTEST_FILTER='ErrorTraceTest.*' meson test nix-expr-tests -v
```

以获得简短而全面的输出。

### 需要 root 权限的单元测试

在 `nix-util-tests` 中，以 `Root` 开头的测试套件需要 root 权限，默认被排除。
在 macOS 上运行它们：

```bash
nix build .#nix-util-tests
sudo ./result/bin/nix-util-tests --gtest_filter='Root*'
```

### 调试测试

对于调试，把上面的第三个选项与 Meson 的 [`--gdb`](https://mesonbuild.com/Unit-tests.html#other-test-options) 标志结合起来会很有用：

```bash
GTEST_BRIEF=1 GTEST_FILTER='Group.my-failing-test' meson test nix-expr-tests --gdb
```

这将会：

1. 在 GDB 下运行单元测试

2. 只运行 `Group.my-failing-test`

3. 在测试失败时停下程序，让用户随后可以向 GDB 发出任意命令。

### 特征化测试（characterisation testing）{ #characterisation-testing-unit }

关于特征化测试更广泛的讨论，参见[功能特征化测试](#characterisation-testing-functional)。

与功能特征化一样，这里也使用 `_NIX_TEST_ACCEPT=1`。
例如：
```shell-session
$ _NIX_TEST_ACCEPT=1 meson test nix-store-tests -v
...
[  SKIPPED ] WorkerProtoTest.string_read
[  SKIPPED ] WorkerProtoTest.string_write
[  SKIPPED ] WorkerProtoTest.storePath_read
[  SKIPPED ] WorkerProtoTest.storePath_write
...
```
会重新生成 `libnixstore` 特征化测试的“黄金标准”（golden master）期望结果。
特征化测试会把自己标记为“跳过”，因为它们重新生成了期望结果，而不是实际测试任何东西。

### JSON Schema 测试

在 `doc/manual/source/protocols/json/` 中，我们有许多由 [JSON Schema](https://json-schema.org/) 生成的手册页。
这些 JSON schema 会针对 [特征化测试](#characterisation-testing-unit )中用于 JSON (反)序列化的 JSON 文件测试数据进行检验，代码位于 `src/json-schema-checks`。
通过 JSON (反)序列化测试，以及对同一数据的 schema 检验，我们确保手册、实现和机器可读的 schema 三者保持同步。

### 单元测试支持库

有一些头文件和代码不仅用于测试相关库本身，还被下游库使用。
例如，我们使用 [rapidcheck] 库进行[性质测试]（property testing）。
这需要编写 `Arbitrary` “实例”，用于描述如何为运行性质测试生成给定类型的值。
由于类型中包含其他类型，某个类型的 `Arbitrary` “实例”不仅对测试该类型有用，对任何包含它的其他类型也有用。
下游类型经常包含上游类型，因此共享这些 arbitrary 实例非常重要，这样下游库的性质测试也能使用它们。

重要的是，这些测试支持库自身不得包含任何实际的测试。
在某些平台上，它们会作为每个使用它们的测试可执行文件的一部分运行，这是冗余的。
在其他平台上，它们则完全不会运行。

## 功能测试

功能测试位于 `tests/functional` 目录下，并在 `tests/functional/meson.build` 中列出。
每个测试都是一个 bash 脚本。

功能测试在 `nix` 软件包构建期间的 `installCheck` 阶段运行，也会独立于构建在 VM 测试中运行。

### 运行整个测试套件

整个测试套件（功能测试和单元测试）可以用以下命令运行：

```shell-session
$ checkPhase
```

### 测试分组

有时把相关的测试编成组很有用，这样无需运行整个测试套件就能轻松地一起运行它们。
每个测试组位于 `tests` 的一个子目录中。
例如，`tests/functional/ca/meson.build` 为内容寻址的 derivation 输出定义了一个 `ca` 测试组。

该测试组可以这样运行：

```shell-session
$ meson test --suite ca
ninja: Entering directory `/home/jcericson/src/nix/master/build'
ninja: no work to do.
[1-20/20] 🌑 nix-functional-tests:ca / ca/why-depends                                1/20 nix-functional-tests:ca / ca/nix-run                                  OK               0.16s
[2-20/20] 🌒 nix-functional-tests:ca / ca/why-depends                                2/20 nix-functional-tests:ca / ca/import-derivation                        OK               0.17s
```

### 运行单个测试

可以用 `meson` 运行单个测试：

```shell-session
$ meson test --verbose ${testName}
ninja: Entering directory `/home/jcericson/src/nix/master/build'
ninja: no work to do.
1/1 nix-functional-tests:main / ${testName}        OK               0.41s

Ok:                 1
Expected Fail:      0
Fail:               0
Unexpected Pass:    0
Skipped:            0
Timeout:            0

Full log written to /home/jcericson/src/nix/master/build/meson-logs/testlog.txt
```

`--verbose` 标志会让 Meson 同时显示每个测试的控制台输出，便于调试。
测试脚本随后会以 `set -x` 进行跟踪并实时显示输出，
无论测试成功还是失败。

测试也可以不通过 `meson` 直接运行：

```shell-session
$ TEST_NAME=${testName} NIX_REMOTE='' PS4='+(${BASH_SOURCE[0]-$0}:$LINENO) tests/functional/${testName}.sh
+(${testName}.sh:1) foo
output from foo
+(${testName}.sh:2) bar
output from bar
...
```

### 调试失败的功能测试

功能测试失败时，通常失败发生在脚本的中间某处。

要弄清哪里出了问题，一个便利的做法是：先照常运行测试直到失败的 `nix` 命令处，然后用 GDB 之类的调试器运行该命令。

例如，如果脚本如下：

```bash
foo
nix blah blub
bar
```

把它改成这样：

```diff
 foo
-nix blah blub
+gdb --args nix blah blub
 bar
```

然后，用 [`--interactive`](https://mesonbuild.com/Unit-tests.html#other-test-options) 运行测试可以防止 Meson 抢占终端，这样一旦脚本执行到该处，你就会被带入 GDB：

```shell-session
$ meson test ${testName} --interactive
...
+ gdb blash blub
GNU gdb (GDB) 12.1
...
(gdb)
```

你可以用所有惯常的方式调试 Nix 调用。
例如，输入 `run` 来启动该 Nix 调用。

### 特征化测试（characterisation testing）{ #characterisation-testing-functional }

偶尔，Nix 会在功能测试中使用一种叫做[特征化测试](https://en.wikipedia.org/wiki/Characterization_test)的技术。
这种技术是把 Nix 某个旧版本的确切输出/行为纳入测试，以检验 Nix 在未来继续保持相同的行为。

例如，语言测试就使用了这一技术，既检查求值成功时打印的最终值，也检查遇到的任何错误和警告。

重新生成期望输出往往很有用。
为此，用 `_NIX_TEST_ACCEPT=1` 重新运行失败的测试即可。
例如：
```bash
_NIX_TEST_ACCEPT=1 meson test lang
```
这一约定也与[特征化单元测试](#characterisation-testing-unit)共用。

一个值得记录的有趣情形是这些测试被“过拟合”的情况。
语言测试再次成为了这样的例子。
求值的期望成功输出应当高度稳定——我们不打算对 Nix 语言的（稳定部分）做破坏性更改。
然而，求值期间（无论成功与否）的错误和警告并不具有这种稳定性。
我们可以随时更改它们的展示方式。

我们竟然要测试诊断输出这类非规范性行为，这也许令人意外。
诊断输出确实不是稳定接口，但它们对用户仍然很重要。
通过记录期望输出，测试套件可以防范意外的变更，并确保诊断代码路径的*结果*（而不仅仅是实现它的代码）处于代码评审之下。
回归会被捕获，改进也总是会在代码评审中显现。

为确保特征化测试不至于让有意更改这些接口变得更困难，必须始终存在一种轻松重新生成期望输出的方式，就像我们用 `_NIX_TEST_ACCEPT=1` 所做的那样。

### 在 NixOS 上运行功能测试

我们不仅在构建中运行功能测试，也在 VM 测试中运行。
这帮助我们确保 Nix 在 NixOS 上正常工作，也在那些在构建环境中难以复现的类似特性环境中正常工作。

可以用以下命令运行：

```shell
nix build .#hydraJobs.tests.functional_user
```

通常这个构建就足够了，但在 nightly 或 CI 中我们还会测试 `functional_root` 和 `functional_trusted` 属性，在其中测试套件以不同的授权级别运行。

## 集成测试

集成测试定义在 Nix flake 的 `hydraJobs.tests` 属性下。
这些测试包括一切需要与外部服务交互或在非平凡分布式设置中运行 Nix 的内容。
由于这些测试代价高昂，且需要的资源超出标准 github-actions 配置所能提供，它们中的大多数只在 master 分支上运行（在 <https://hydra.nixos.org/jobset/nix/master>）。

你可以用 `nix build .#hydraJobs.tests.{testName}` 或 `nix-build -A hydraJobs.tests.{testName}` 手动运行它们。

## 模糊测试（Fuzzing）

本项目使用 [`libFuzzer`](https://llvm.org/docs/LibFuzzer.html) 和 LLVM 覆盖率插桩来对敏感代码片段进行模糊测试。
测试驱动（harness）位于对应的 `-tests` 子项目中（例如 `src/libutil-tests/fuzz`）。
`fuzzers` 选项独立于 `unit-tests` 构建 harness；若要只构建 fuzzer，可设置 `unit-tests=false`。
`fuzzing-engine` 选项接受一个用于链接外部模糊测试引擎的编译器驱动参数。
如果 `fuzzing-engine` 为空，Meson 要求使用 Clang 并在 `b_sanitize` 中包含 `fuzzer-no-link`。
编译器驱动随后会把 harness 与 libFuzzer 和 libstdc++ 链接起来。

```shell
nix develop .#native-clangStdenv
appendToVar mesonFlags "-Dunit-tests=false"
appendToVar mesonFlags "-Dfuzzers=true"
appendToVar mesonFlags "-Db_sanitize=address,undefined,fuzzer-no-link"
# Clang sanitizer/shared-library workaround: https://github.com/mesonbuild/meson/issues/764
appendToVar mesonFlags "-Db_lundef=false"
appendToVar mesonFlags "-Dlibexpr:gc=disabled" # Because Boehm doesn't play well with ASan
configurePhase
buildPhase
```

要使用外部模糊测试引擎，请设置 `fuzzing-engine`：

```shell
mesonFlagsArray+=(
  "-Dunit-tests=false"
  "-Dfuzzers=true"
  "-Dfuzzing-engine=$LIB_FUZZING_ENGINE"
)
```

Nix 将该值作为一个编译器驱动参数传入。
调用者还必须选择兼容的编译器和 C++ 运行时，并提供任何所需的插桩和 sanitizer 标志。

如果你想收集覆盖率指标，还需要在运行 `configurePhase` 之前指定以下编译器标志：

```shell
export CXXFLAGS="-fprofile-instr-generate -fcoverage-mapping"
export CCFLAGS="-fprofile-instr-generate -fcoverage-mapping"
```

目前，这些测试用例大多还很简陋，主要用于捕获内存安全 bug，但模糊测试对于验证不变量同样至关重要。
欢迎贡献改进 harness 以及语料库/字典的工作。

要运行 harness（例如 NAR 反序列化的），可以执行以下操作：

```shell
export LLVM_PROFILE_FILE="default.%p.profraw"
mkdir /tmp/parse-dump
build/src/libutil-tests/fuzz/harnesses/fuzz-parse-dump -runs=1000000 -max_len=65536 -dict=./src/libutil-tests/fuzz/data/nars.dict /tmp/parse-dump ./src/libutil-tests/fuzz/data/nars
```

注意，要获得更好的结果，可能需要调整 `libFuzzer` 参数或改进初始语料库和字典。更多信息请查阅 [libFuzzer 手册](https://llvm.org/docs/LibFuzzer.html)。

如果你想查看覆盖率，请等待 harness 运行完毕（中途打断不会生成非空的 `.profraw` 文件），然后汇总最终的覆盖率报告：

```
llvm-profdata merge -sparse *.profraw -o default.profdata
llvm-cov show build/src/libutil/libnixutil.so -instr-profile=default.profdata -format=html -output-dir cov-html
xdg-open cov-html/index.html
```

如果你通过模糊测试发现了内存安全问题，并认为它与安全相关，请考虑[私下报告](https://github.com/NixOS/nix/security/)。

### 妨碍模糊测试的检查

模糊测试对验证不变量至关重要，但有少数不变量是 fuzzer 永远无法满足的。
检查某字段是否等于其他字段的密码学散列就是典型情况：要通过该检查需要一个哈希原像（preimage），因此该检查之下的代码对 fuzzer 来说变得*不可达*，而不仅仅是难以到达。
这与那些只是难以满足的检查不同——键已排序、分隔符配对、没有冗余转义——覆盖制导的 fuzzer 会自己学会绕过它们。
只有前者才应当被门控。

此类检查会在 `FUZZING_BUILD_MODE_UNSAFE_FOR_PRODUCTION` 下被编译掉，例如：

```c++
#ifndef FUZZING_BUILD_MODE_UNSAFE_FOR_PRODUCTION
    if (path != computedPath)
        throw FormatError(...);
#endif
```

该宏名是 [OSS-Fuzz](https://google.github.io/oss-fuzz/) 和 libFuzzer 的一个约定。
当 `b_sanitize` 中含有 `fuzzer-no-link` 时——也就是正在构建 fuzzer 插桩版本时——`nix-meson-build-support/common/meson.build` 会为每个子项目定义它。
使用外部 `fuzzing-engine` 的构建应自行传入该宏，正如 OSS-Fuzz 所做的那样。

以这种方式门控的任何内容都不再被 fuzzer 执行，因此必须改由单元测试覆盖。
关于这两方面的示例，参见 `parseOutput` 中的 fixed-output derivation 路径检查（`src/libstore/derivation/aterm.cc`）及其测试 `CAFixedPathMismatch`。

## 安装器测试

Nix 仓库中的 GitHub Actions CI 也会在 PR 上测试安装器。它不需要额外配置，利用 [GHA Artifacts](https://docs.github.com/en/actions/tutorials/store-and-share-data)，并且可以在任何 Nix 仓库 fork 中运行。

- `tests` 任务为以下平台生成安装器并作为 artifact 上传：
  - `x86_64-linux`
  - `aarch64-darwin`

- `installer_test` 任务（在 Linux 和 macOS 上运行）会尝试用缓存的安装器安装 Nix 并运行一个简单的 Nix 命令。
- 脚本式安装器和[独立的基于 Rust 的安装器](https://github.com/NixOS/nix-installer)都会被测试。

你可以通过运行 `nix build .#hydraJobs.installerScriptForGHA.<system-double>` 手动生成安装器 tarball 和脚本。

## 编写文档

### 使用 CI 生成的安装器进行手动测试

CI 运行完成后，你可以查看其输出以提取安装器 artifact：
1. 点击进入该 CI 运行的详细视图。
2. 向下滚动到 `Artifacts` 部分。
3. 下载相应的安装器 artifact（`aarch64-darwin` 对应 `installer-darwin`，`x86_64-linux` 对应 `installer-linux`）。
4. 解压下载的 `.zip` artifact。
5. 要生成安装命令，把解压后 artifact 的路径代入这个模板：

    ```console
    sh <path/to/artifact>/install --tarball-url-prefix file://<path/to/artifact>
    ```
