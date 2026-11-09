# Name

`nix-env --switch-generation` - 将用户环境切换到给定的 profile generation（代）

概要

`nix-env` {`--switch-generation` | `-G`} *generation*

# 描述

该操作使编号为 *generation* 的 generation 成为当前激活 profile 的当前 generation。
也就是说，如果 `profile` 是当前激活 profile 的路径，那么符号链接 `profile` 会被指向
`profile-generation-link`，而后者又是指向 Nix store 中实际用户环境的符号链接。

如果指定的 generation 不存在，切换会失败。

{{#include ./opt-common.md}}

{{#include ../opt-common.md}}

{{#include ./env-common.md}}

{{#include ../env-common.md}}

# 示例

```console
$ nix-env --switch-generation 42
switching from generation 50 to 42
```
