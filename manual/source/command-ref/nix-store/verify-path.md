# Name

`nix-store --verify-path` - 对照 Nix 数据库校验路径内容

## 概要

`nix-store` `--verify-path` *paths…*

## 描述

`--verify-path` 操作将给定存储路径的内容与 Nix 数据库中存储的加密哈希进行比较。对于每一个发生变化的路径，它都会打印一条警告消息。如果没有路径发生变化，退出状态为 0，否则为 1。

{{#include ./opt-common.md}}

{{#include ../opt-common.md}}

{{#include ../env-common.md}}

## 示例

校验 `svn` 命令及其全部依赖的完整性：

```console
$ nix-store --verify-path $(nix-store --query --requisites $(which svn))
```
