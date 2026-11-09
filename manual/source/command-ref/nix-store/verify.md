# Name

`nix-store --verify` - 校验 Nix 数据库的一致性

# 概要

`nix-store` `--verify` [`--check-contents`] [`--repair`]

# 描述

`--verify` 操作校验 Nix 数据库的内部一致性，以及 Nix 数据库与 Nix store 之间的一致性。遇到的任何不一致都会被自动修复。不一致通常是由于 Nix store 或数据库被非 Nix 工具修改，或 Nix 自身的 bug 导致的。

该操作具有以下选项：

- `--check-contents`

  通过计算内容的 SHA-256 哈希并与构建时存储在 Nix 数据库中的哈希进行比较，检查每个有效路径的内容是否被改动过。被修改的路径会被打印出来。对于大型 store 来说，`--check-contents` 显然相当慢。

- `--repair`

  如果某个有效路径在 store 中缺失，或者（如果给定了
  `--check-contents`）某个有效路径的内容被修改过，则尝试通过重新下载来修复该路径。详见 `nix-store --repair-path`。

{{#include ./opt-common.md}}

{{#include ../opt-common.md}}

{{#include ../env-common.md}}
