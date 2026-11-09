# 静态分析

Nix 使用 [clang-tidy](https://clang.llvm.org/extra/clang-tidy/) 对 C++ 代码进行静态分析。
这有助于发现 bug、执行编码规范并保持代码质量。

## 在本地运行 clang-tidy

在开发 shell 中对整个代码库运行 clang-tidy：

```console
$ nix develop .#native-clangStdenv
$ configurePhase
$ meson compile -C build clang-tidy
```

这会分析所有 C++ 源文件并报告所有警告。

要自动修复某些警告：

```console
$ meson compile -C build clang-tidy-fix
```

> **警告**
>
> 提交之前请审阅变更，因为自动修复并不总是正确。

## CI 集成

clang-tidy 通过 GitHub Actions 在每个 pull request 上自动运行。
CI 任务会构建 `.#hydraJobs.clangTidy.x86_64-linux`，它会：

1. 以 debug 模式构建所有组件（编译更快）
2. 对每个组件运行 clang-tidy
3. 发现任何警告即失败（警告被视为错误）

## 配置

clang-tidy 的配置位于仓库根目录的 `.clang-tidy`（符号链接自 `nix-meson-build-support/common/clang-tidy/.clang-tidy`）。

### 抑制警告

如果某个警告是误报，可以通过几种方式抑制它：

1. **行内抑制**（针对具体情况首选）：
   ```cpp
   // NOLINTBEGIN(bugprone-some-check)
   ... code ...
   // NOLINTEND(bugprone-some-check)
   ```
   或者对单行：
   ```cpp
   int x = something(); // NOLINT(bugprone-some-check)
   ```

2. **配置文件**（用于项目级抑制）：
   将该检查加入 `.clang-tidy` 的禁用列表：
   ```yaml
   Checks:
     - -bugprone-some-check  # Reason for disabling
   ```

3. **检查选项**（用于配置检查行为）：
   ```yaml
   CheckOptions:
     bugprone-reserved-identifier.AllowedIdentifiers: '__some_identifier'
   ```

### 添加新检查

要启用更多检查：

1. 编辑 `nix-meson-build-support/common/clang-tidy/.clang-tidy`
2. 将该检查添加到 `Checks` 列表
3. 在本地运行 clang-tidy 查看影响
4. 修复所有新警告，或视需要禁用特定的子检查

## 自定义 clang-tidy 插件

Nix 项目在 `src/clang-tidy-plugin/` 中提供了自定义 clang-tidy 检查的基础设施。
这些检查可以强制执行标准 clang-tidy 检查未覆盖的 Nix 特定编码模式。

要添加新的自定义检查：

1. 在 `src/clang-tidy-plugin/` 中添加检查实现
2. 在 `nix-clang-tidy-checks.cc` 中注册它
3. 在 `.clang-tidy` 中以 `nix-` 前缀启用它
