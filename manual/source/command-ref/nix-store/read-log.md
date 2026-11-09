# Name

`nix-store --read-log` - 打印构建日志

# 概要

`nix-store` {`--read-log` | `-l`} *paths…*

# 描述

`--read-log` 操作在标准输出上打印指定存储路径的构建日志。构建日志是 derivation 的 builder 写入标准输出和标准错误的所有内容。如果某个存储路径不是 derivation，则使用该存储路径的 deriver。

构建日志保存在 `/nix/var/log/nix/drvs` 中。然而，并不能保证任何特定的存储路径都有可用的构建日志。例如，如果路径是通过 substitute 从预构建的二进制文件下载的，那么日志就不可用。

{{#include ./opt-common.md}}

{{#include ../opt-common.md}}

{{#include ../env-common.md}}

# 示例

```console
$ nix-store --read-log $(which ktorrent)
building /nix/store/dhc73pvzpnzxhdgpimsd9sw39di66ph1-ktorrent-2.2.1
unpacking sources
unpacking source archive /nix/store/p8n1jpqs27mgkjw07pb5269717nzf5f8-ktorrent-2.2.1.tar.gz
ktorrent-2.2.1/
ktorrent-2.2.1/NEWS
...
```
