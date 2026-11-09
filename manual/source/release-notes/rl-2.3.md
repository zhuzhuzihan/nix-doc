# Release 2.3 (2019-09-04)

这主要是一个缺陷修复版本，但也包含了一些不兼容的变更：

  - Nix 现在使用 BSD 文件锁而不是 POSIX 文件锁。因此，请不要在同一个 Nix store 上同时使用 Nix 2.3 与更早的版本。

它还包含以下变更：

  - `builtins.fetchGit` 的 `ref` 参数现在允许指定远程的绝对 ref。只有当 `ref` 不以 `refs/` 开头时，Nix 才会自动为 `ref` 加上 `refs/heads` 前缀。

  - 在 Linux 上，当系统具备必要的内核支持时，安装程序现在默认启用沙箱。

  - `max-jobs` 设置现在默认为 1。

  - 新增内建函数：`builtins.isPath`、`builtins.hashFile`。

  - `nix` 命令新增 `--print-build-logs`（`-L`）标志，用于将构建日志输出到 stderr，而不是在进度条中只显示最后一行日志。为了区分并发进行的多个构建，日志行会以软件包名称作为前缀。

  - 构建现在在伪终端中执行，并且 `TERM` 环境变量会被设置为 `xterm-256color`。这使得许多程序（例如 `gcc`、`clang`、`cmake`）能够打印带颜色的日志输出。

  - 新增 `--no-net` 便捷标志。该标志会禁用 substituter；将 `tarball-ttl` 设置设为无穷大（确保任何先前下载的文件都被视为最新）；禁用下载重试，并将连接超时设为最小值。当不存在任何已配置的非回环网络接口时，该标志会自动启用。

  - 新增 `post-build-hook` 设置，用于在构建成功后运行一个程序。

  - 新增 `trace-function-calls` 设置，用于将 Nix 函数调用的耗时记录到 stderr。
