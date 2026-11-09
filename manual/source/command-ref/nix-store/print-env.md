# Name

`nix-store --print-env` - 打印 derivation（派生）的构建环境

## 概要

`nix-store` `--print-env` *drvpath*

## 描述

`--print-env` 操作以可被 shell 求值的格式打印 derivation 的环境。builder 的命令行参数会被放入变量 `_args` 中。

{{#include ./opt-common.md}}

{{#include ../opt-common.md}}

{{#include ../env-common.md}}

## 示例

```console
$ nix-store --print-env $(nix-instantiate '<nixpkgs>' -A firefox)
…
export src; src='/nix/store/plpj7qrwcz94z2psh6fchsi7s8yihc7k-firefox-12.0.source.tar.bz2'
export stdenv; stdenv='/nix/store/7c8asx3yfrg5dg1gzhzyq2236zfgibnn-stdenv'
export system; system='x86_64-linux'
export _args; _args='-e /nix/store/9krlzvny65gdc8s7kpb6lkx8cd02c25c-default-builder.sh'
```
