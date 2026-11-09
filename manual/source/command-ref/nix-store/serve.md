# Name

`nix-store --serve` - 通过 SSH 提供 Nix store 服务

# 概要

`nix-store` `--serve` [`--write`]

# 描述

`--serve` 操作通过标准输入和标准输出提供对 Nix store 的访问，旨在用于向受限的 ssh 用户授予 Nix store 访问权限。

可以使用以下标志：

- `--write`

  允许连接的客户端请求实化 derivation。实际上，这可以用来让主机充当远程构建器（remote builder）。

{{#include ./opt-common.md}}

{{#include ../opt-common.md}}

{{#include ../env-common.md}}

# 示例

要将一台主机变成构建服务器，可以使用 `authorized_keys` 文件为给定的 SSH 公钥授予构建权限：

```console
$ cat <<EOF >>/root/.ssh/authorized_keys
command="nice -n20 nix-store --serve --write" ssh-rsa AAAAB3NzaC1yc2EAAAA...
EOF
```
