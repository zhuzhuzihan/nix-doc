# Name

`nix-env --uninstall` - 从用户环境中移除软件包

概要

`nix-env` {`--uninstall` | `-e`} *drvnames…*

# 描述

uninstall 操作基于当前激活 profile 的当前 generation 创建一个新的用户环境，并从中移除由符号名称 *drvnames* 指定的存储路径。

{{#include ./opt-common.md}}

{{#include ../opt-common.md}}

{{#include ./env-common.md}}

{{#include ../env-common.md}}

# 示例

```console
$ nix-env --uninstall gcc
$ nix-env --uninstall '.*' (remove everything)
```
