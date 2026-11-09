# Name

`nix-env --set` - 将 profile 设置为只包含指定的 derivation（派生）

概要

`nix-env` `--set` *drvname*

## 描述

`--set` 操作修改 profile 的当前 generation，使其恰好包含指定的 derivation，而不包含其他任何内容。

{{#include ./opt-common.md}}

{{#include ../opt-common.md}}

{{#include ./env-common.md}}

{{#include ../env-common.md}}

## 示例

以下命令更新一个 profile，使其当前 generation 只包含 Firefox：

```console
$ nix-env --profile /nix/var/nix/profiles/browser --set firefox
```
