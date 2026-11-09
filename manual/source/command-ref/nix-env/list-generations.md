# Name

`nix-env --list-generations` - 列出 profile 的 generation（代）

概要

`nix-env` `--list-generations`

# 描述

该操作打印当前激活 profile 的所有现存 generation 的列表。
可以使用 `--switch-generation` 操作切换到这些 generation。
它还会打印每个 generation 的创建日期，并标明当前 generation。

{{#include ./opt-common.md}}

{{#include ../opt-common.md}}

{{#include ./env-common.md}}

{{#include ../env-common.md}}

# 示例

```console
$ nix-env --list-generations
  95   2004-02-06 11:48:24
  96   2004-02-06 11:49:01
  97   2004-02-06 16:22:45
  98   2004-02-06 16:24:33   (current)
```
