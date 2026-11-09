# Name

`nix-store --export` - 将存储路径导出为 [Nix Archive]

## 概要

`nix-store` `--export` *paths…*

## 描述

`--export` 操作将给定 [store 对象](@docroot@/glossary.md#gloss-store-object) 的序列化结果写入标准输出，其格式可以通过 [`nix-store --import`](./import.md) 导入到另一个 [Nix store](@docroot@/store/index.md) 中。

> **警告**
>
> 此命令*不会*生成指定存储路径的[闭包](@docroot@/glossary.md#gloss-closure)。
> 尝试导入一个引用了目标 Nix store 中不存在的存储路径的 store 对象将会失败。
>
> 使用 [`nix-store --query`](@docroot@/command-ref/nix-store/query.md) 来获取某个存储路径的闭包。

此命令不同于 [`nix-store --dump`](./dump.md)，后者生成的 [Nix 归档](@docroot@/glossary.md#gloss-nar)*不*包含给定存储路径的[引用](@docroot@/glossary.md#gloss-reference)集合。

> **注意**
>
> 若要通过 SSH 高效地向远程机器传输闭包，请使用 [`nix-copy-closure`](@docroot@/command-ref/nix-copy-closure.md)。

[Nix Archive]: @docroot@/store/file-system-object/content-address.md#serial-nix-archive

{{#include ./opt-common.md}}

{{#include ../opt-common.md}}

{{#include ../env-common.md}}

# 示例

> **示例**
>
> 通过 U 盘将 GNU Hello 部署到一台物理隔离（airgapped）的机器上。
>
> 在一台有网络连接的机器上，将闭包写入块设备：
>
> ```shell-session
> [alice@itchy]$ storePath=$(nix-build '<nixpkgs>' -I nixpkgs=channel:nixpkgs-unstable -A hello --no-out-link)
> [alice@itchy]$ nix-store --export $(nix-store --query --requisites $storePath) | sudo dd of=/dev/usb
> ```
>
> 在没有网络连接的机器上，从块设备读取闭包：
>
> ```shell-session
> [bob@scratchy]$ hello=$(sudo dd if=/dev/usb | nix-store --import | tail -1)
> [bob@scratchy]$ $hello/bin/hello
> Hello, world!
> ```
