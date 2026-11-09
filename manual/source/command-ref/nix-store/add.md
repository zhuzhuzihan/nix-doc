# Name

`nix-store --add` - 将路径添加到 Nix store

# 概要

`nix-store` `--add` *paths…*

# 描述

`--add` 操作将指定路径添加到 Nix store，并在标准输出上打印生成的存储路径。

指向符号链接的 *paths* 不会被解引用，而是以符号链接的形式添加到 store 中，其目标保持不变。

{{#include ./opt-common.md}}

{{#include ../opt-common.md}}

{{#include ../env-common.md}}

# 示例

```console
$ nix-store --add ./foo.c
/nix/store/m7lrha58ph6rcnv109yzx1nk1cj7k7zf-foo.c
```
