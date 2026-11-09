# Name

`nix-store --restore` - 解包 Nix 归档

## 概要

`nix-store` `--restore` *path*

## 描述

`--restore` 操作将 [Nix Archive (NAR)][Nix Archive] 解包到 *path*，该路径必须尚不存在。归档从标准输入读取。

[Nix Archive]: @docroot@/store/file-system-object/content-address.md#serial-nix-archive

{{#include ./opt-common.md}}

{{#include ../opt-common.md}}

{{#include ../env-common.md}}
