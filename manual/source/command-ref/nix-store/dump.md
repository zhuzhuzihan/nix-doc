# Name

`nix-store --dump` - 将单个路径写入 [Nix Archive]

## 概要

`nix-store` `--dump` *path*

## 描述

`--dump` 操作生成一个 [Nix 归档](@docroot@/glossary.md#gloss-nar)（NAR）文件，其中包含以 *path* 为根的文件系统树的内容。该归档被写入标准输出。

NAR 归档类似于 TAR 或 Zip 归档，但它只包含 Nix 认为重要的信息。例如，时间戳会被省略，因为 Nix store 中所有文件的时间戳本来就被设为 0。同样，除了可执行位之外，所有权限都会被省略，因为 Nix store 中所有文件的权限都是 444 或 555。

此外，NAR 归档是*规范化的*（canonical），这意味着"相同"的路径总是生成相同的 NAR 归档。例如，目录条目总是经过排序，因此磁盘上的实际顺序不会影响结果。这意味着一个路径的 NAR 转储的加密哈希可以用作该路径内容的指纹。事实上，存储在 Nix 数据库中的存储路径哈希（参见 `nix-store --query
--hash`）就是每个存储路径的 NAR 转储的 SHA-256 哈希。

NAR 归档支持无限长度的文件名和 64 位文件大小。它们可以包含普通文件、目录和符号链接，但不能包含其他类型的文件（如设备节点）。

可以使用 [`nix-store --restore`](@docroot@/command-ref/nix-store/restore.md) 解包 Nix 归档。

[Nix Archive]: @docroot@/store/file-system-object/content-address.md#serial-nix-archive

{{#include ./opt-common.md}}

{{#include ../opt-common.md}}

{{#include ../env-common.md}}
