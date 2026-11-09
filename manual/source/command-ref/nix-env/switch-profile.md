# Name

`nix-env --switch-profile` - 将用户环境切换到给定的 profile

概要

`nix-env` {`--switch-profile` | `-S`} *path*

# 描述

该操作使 *path* 成为该用户的当前 profile。
也就是说，符号链接 `~/.nix-profile` 会被指向 *path*。

{{#include ./opt-common.md}}

{{#include ../opt-common.md}}

{{#include ./env-common.md}}

{{#include ../env-common.md}}

# 示例

```console
$ nix-env --switch-profile ~/my-profile
```
