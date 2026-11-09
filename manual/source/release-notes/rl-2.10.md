# Release 2.10 (2022-07-11)

* `nix repl` 现在可以在命令行上接受 installable，统一了它与其它使用 `--file` 和 `--expr` 的命令的用法。主要的破坏性变更影响 `nix repl '<nixpkgs>'` 这一常见用法，可以用 `nix repl --file '<nixpkgs>'` 或 `nix repl --expr 'import <nixpkgs>{}'` 来恢复原有行为。

  该变更目前由 `repl-flake` 实验性特性守护。

* 新函数 `builtins.traceVerbose` 可用。当 `trace-verbose` 设置为 true 时它类似于 `builtins.trace`，否则是一个空操作（no-op）。

* `nix search` 新增标志 `--exclude`，用于过滤掉软件包。

* 在 Linux 上，如果 `/nix` 不存在且无法创建，而你又不是以 root 运行，Nix 会自动使用 `~/.local/share/nix/root` 作为 chroot store。这使得非 root 用户可以下载静态链接的 Nix 二进制文件并开箱即用，例如

  ```
  # ~/nix run nixpkgs#hello
  warning: '/nix' does not exists, so Nix will use '/home/ubuntu/.local/share/nix/root' as a chroot store
  Hello, world!
  ```

* `flake-registry.json` 现在从 `channels.nixos.org` 获取。

* Nix 现在可以通过向 `configure` 传递 `--enable-lto` 来以 LTO 构建。LTO 目前仅在使用 GCC 构建时受支持。
