# Name

`nix-store --load-db` - 导入 Nix 数据库

# 概要

`nix-store` `--load-db`

# 描述

`--load-db` 操作从标准输入读取由 `--dump-db` 创建的 Nix 数据库转储，并将其加载到 Nix 数据库中。

{{#include ./opt-common.md}}

{{#include ../opt-common.md}}

{{#include ../env-common.md}}
