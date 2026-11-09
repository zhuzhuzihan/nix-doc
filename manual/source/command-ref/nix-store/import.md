# Name

`nix-store --import` - 将 [Nix Archive] 导入 store

[Nix Archive]: @docroot@/store/file-system-object/content-address.md#serial-nix-archive

# 概要

`nix-store` `--import`

# 描述

`--import` 操作从标准输入读取由 [`nix-store --export`](./export.md) 生成的一组 [store 对象](@docroot@/glossary.md#gloss-store-object)的序列化结果，并将这些 store 对象添加到指定的 [Nix store](@docroot@/store/index.md) 中。
目标 Nix store 中已存在的路径会被忽略。
如果某个路径[引用](@docroot@/glossary.md#gloss-reference)了目标 Nix store 中不存在的另一个路径，导入将失败。

> **注意**
>
> 若要通过 SSH 高效地向远程机器传输闭包，请使用 [`nix-copy-closure`](@docroot@/command-ref/nix-copy-closure.md)。

{{#include ./opt-common.md}}

{{#include ../opt-common.md}}

{{#include ../env-common.md}}

# 示例

> **示例**
>
> 假设已将 GNU Hello 的闭包保存为一个文件：
>
> ```shell-session
> $ storePath="$(nix-build '<nixpkgs>' -I nixpkgs=channel:nixpkgs-unstable -A hello --no-out-link)"
> $ nix-store --export $(nix-store --query --requisites $storePath) > hello.closure
> ```
>
> 使用 [`--store`](@docroot@/command-ref/conf-file.md#conf-store) 选项将该闭包导入一个[远程 SSH store](@docroot@/store/types/ssh-store.md)：
>
> ```console
> $ nix-store --import --store ssh://alice@itchy.example.org < hello.closure
> ```
