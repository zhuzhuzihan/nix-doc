# Name

`nix-store --add-fixed` - 使用指定的哈希算法将路径添加到 store

## 概要

`nix-store` `--add-fixed` [`--recursive`] *algorithm* *paths…*

## 描述

`--add-fixed` 操作将指定路径添加到 Nix store。与 `--add` 不同，路径会以指定的哈希算法注册，从而得到与固定输出 derivation（派生）相同的输出路径。这可用于那些无法从公开 URL 获取、或自下载表达式编写以来已失效的源码。

该操作具有以下选项：

- `--recursive`

  使用递归模式而非扁平哈希模式，用于将目录添加到 store。

  指向符号链接的 *paths* 不会被解引用，而是以符号链接的形式添加到 store 中，其目标保持不变。

{{#include ./opt-common.md}}

{{#include ../opt-common.md}}

{{#include ../env-common.md}}

## 示例

```console
$ nix-store --add-fixed sha256 ./hello-2.10.tar.gz
/nix/store/8alrpdaasjd1x6g1fczchmzbpqm936a3-hello-2.10.tar.gz
```
