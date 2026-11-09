# Name

`nix-store --dump-db` - 导出 Nix 数据库

# 概要

`nix-store` `--dump-db` [*paths…*]

# 描述

`--dump-db` 操作将 Nix 数据库的转储（dump）写入标准输出。它可以通过 `--load-db` 加载到一个空的 Nix store 中。这对于制作备份以及迁移到不同的数据库模式很有用。

默认情况下，`--dump-db` 会转储整个 Nix 数据库。当传入一个或多个存储路径时，只会转储这些存储路径对应的 Nix 数据库子集。与 `--export` 一样，用户需要自行传入一个闭包中的全部存储路径。示例参见 `--export`。

{{#include ./opt-common.md}}

{{#include ../opt-common.md}}

{{#include ../env-common.md}}
