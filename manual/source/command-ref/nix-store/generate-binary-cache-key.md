# Name

`nix-store --generate-binary-cache-key` - 生成用于二进制缓存的密钥对

## 概要

`nix-store` `--generate-binary-cache-key` *key-name* *secret-key-file* *public-key-file*

## 描述

此命令生成一个 [Ed25519 密钥对](http://ed25519.cr.yp.to/)，可用于创建带签名的二进制缓存。它接受三个必需参数：

1.  密钥名称，例如 `cache.example.org-1`，客户端在验证签名时用它来查找密钥。它可以是任何内容，但建议使用你的缓存的主机名（例如 `cache.example.org`）加上一个表示密钥编号的后缀（每次需要吊销密钥时递增）。

2.  用于存储私钥的文件名。

3.  用于存储公钥的文件名。

{{#include ./opt-common.md}}

{{#include ../opt-common.md}}

{{#include ../env-common.md}}
