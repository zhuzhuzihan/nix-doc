# Name

`nix-store --optimise` - 减少磁盘空间占用

## 概要

`nix-store` `--optimise`

## 描述

`--optimise` 操作通过在 store 中查找相同文件并将它们互相硬链接来减少 Nix store 的磁盘空间占用。它通常可将 store 的大小减少约 25-35%。只有普通文件和符号链接会以这种方式进行硬链接。当文件具有相同的 [Nix Archive (NAR)][Nix Archive] 序列化结果时，即被视为相同：也就是说，普通文件必须具有相同的内容和权限（可执行或不可执行），符号链接必须具有相同的目标。

完成后或命令被中断时，会在标准错误上打印一份关于所节省空间的报告。

使用 `-vv` 或 `-vvv` 可以获得一些进度提示。

{{#include ./opt-common.md}}

{{#include ../opt-common.md}}

{{#include ../env-common.md}}

## 示例

```console
$ nix-store --optimise
hashing files in `/nix/store/qhqx7l2f1kmwihc9bnxs7rc159hsxnf3-gcc-4.1.1'
...
541838819 bytes (516.74 MiB) freed by hard-linking 54143 files;
there are 114486 files with equal contents out of 215894 files in total
```

[Nix Archive]: @docroot@/store/file-system-object/content-address.md#serial-nix-archive
