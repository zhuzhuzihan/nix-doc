# Release 2.22.0 (2024-04-23)

### 显著变更

- 移除实验性的 repl-flake [#10103](https://github.com/NixOS/nix/issues/10103) [#10299](https://github.com/NixOS/nix/pull/10299)

  `repl-flake` 实验特性已被移除。`nix repl` 命令现在的行为与新 CLI 的其他部分一致：`nix repl {path}` 会尝试在 `{path}` 处加载一个 Flakes（若未启用 `flakes` 实验特性则会失败）。

### 其他变更

- `nix eval` 将 derivation 打印为 `.drv` 路径 [#10200](https://github.com/NixOS/nix/pull/10200)

  `nix eval` 现在会将 derivation（派生）打印为其 `.drv` 路径，而不是属性集。这使 `nix eval nixpkgs#bash` 这类命令能够正常终止，而不会因递归自引用属性陷入无限循环：

  ```ShellSession
  $ nix eval nixpkgs#bash
  «derivation /nix/store/m32cbgbd598f4w299g0hwyv7gbw6rqcg-bash-5.2p26.drv»
  ```
