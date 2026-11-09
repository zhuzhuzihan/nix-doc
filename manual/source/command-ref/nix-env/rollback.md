# Name

`nix-env --rollback` - 将用户环境切换到上一个 generation（代）

概要

`nix-env` `--rollback`

# 描述

该操作切换到当前激活 profile 的"上一个" generation，即编号小于当前 generation 的最大编号 generation（如果存在）。
它只是 `--list-generations` 和 `--switch-generation` 的一个便捷封装。

{{#include ./opt-common.md}}

{{#include ../opt-common.md}}

{{#include ./env-common.md}}

{{#include ../env-common.md}}

# 示例

```console
$ nix-env --rollback
switching from generation 92 to 91
```

```console
$ nix-env --rollback
error: no generation older than the current (91) exists
```
