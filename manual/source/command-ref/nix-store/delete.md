# Name

`nix-store --delete` - 删除 store 路径

# 概要

`nix-store` `--delete` [`--ignore-liveness`] *paths…*

# 描述

`--delete` 操作从 Nix store 中删除存储路径 *paths*，但仅在安全的情况下才会删除；也就是说，只有当该路径从垃圾回收器的某个 root 不可达时才会删除。这意味着你只能删除那些同样会被 `nix-store --gc` 删除的路径。因此，`--delete` 是 `--gc` 的一个更有针对性的版本。

使用选项 `--ignore-liveness` 时，将忽略从 root 出发的可达性。然而，如果 store 中还有其他路径引用它（即依赖它），该路径仍然不会被删除。

{{#include ./opt-common.md}}

{{#include ../opt-common.md}}

{{#include ../env-common.md}}

# 示例

```console
$ nix-store --delete /nix/store/gjak3al7lj61x4gj6rln4f5pc5v0f67n-mesa-6.4
0 bytes freed (0.00 MiB)
error: cannot delete path `/nix/store/gjak3al7lj61x4gj6rln4f5pc5v0f67n-mesa-6.4' since it is still alive
```
