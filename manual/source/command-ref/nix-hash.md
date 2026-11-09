# Name

`nix-hash` - 计算路径的密码学哈希

# 概要

`nix-hash` [`--flat`] [`--base32`] [`--truncate`] [`--type` *hashAlgo*] *path…*

`nix-hash` [`--to-base16`|`--to-base32`|`--to-base64`|`--to-sri`] [`--type` *hashAlgo*] *hash…*

# 描述

命令 `nix-hash` 计算每个 *path* 内容的密码学哈希并将其打印到标准输出。默认情况下，它计算
MD5 哈希，但也可以使用其他哈希算法。哈希
以十六进制打印。要生成与
`nix-prefetch-url` 相同的哈希，你必须指定多个参数，示例见下文。

哈希是对每个路径的*序列化（serialisation）*计算的：即以该路径为根的文件系统树的转储。这使得目录和
符号链接也可以像普通文件一样被哈希。转储采用 [`nix-store
--dump`](@docroot@/command-ref/nix-store/dump.md) 生成的 *[Nix Archive (NAR)][Nix Archive] 格式*。因此，`nix-hash path`
产生的密码学哈希与 `nix-store --dump path |
md5sum` 相同。

[Nix Archive]: @docroot@/store/file-system-object/content-address.md#serial-nix-archive

# 选项

- `--flat`

  打印每个普通文件 *path* 内容的密码学哈希。
  也就是说，不再计算 *path* 的
  [Nix Archive (NAR)](@docroot@/store/file-system-object/content-address.md#serial-nix-archive) 的哈希，
  而是[直接按原样哈希](@docroot@/store/file-system-object/content-address.md#serial-flat) *path*。
  这要求 *path* 解析为普通文件而非目录。
  结果与 GNU 命令
  `md5sum` 和 `sha1sum` 产生的结果相同。

- `--base16`

  以十六进制表示打印哈希（默认）。

- `--base32`

  以 [Nix32](@docroot@/protocols/nix32.md) 表示而非十六进制打印哈希。
  这种表示更紧凑，并且可以用在 Nix
  表达式中（例如在 `fetchurl` 的调用中）。

- `--base64`

  类似于 `--base32`，但以 [Base64](https://en.wikipedia.org/wiki/Base64) 表示打印哈希，
  比 Nix32 更紧凑。

- `--sri`

  以带 Base64 编码的 [SRI](@docroot@/glossary.md#gloss-sri) 格式打印哈希。
  哈希算法类型会附加在哈希字符串之前，
  后跟一个连字符（-）和 Base64 哈希主体。

- `--truncate`

  将超过 160 位（例如 SHA-256）的哈希截断为 160 位。

- `--type` *hashAlgo*

  使用指定的密码学哈希算法，可以是
  `blake3`、`md5`、`sha1`、`sha256` 和 `sha512` 之一。

- `--to-base16`

  不做任何哈希，而是将 [Nix32](@docroot@/protocols/nix32.md) 哈希表示
  *hash* 转换为十六进制。

- `--to-base32`

  不做任何哈希，而是将十六进制哈希表示
  *hash* 转换为 [Nix32](@docroot@/protocols/nix32.md)。

- `--to-base64`

  不做任何哈希，而是将十六进制哈希表示
  *hash* 转换为 Base64。

- `--to-sri`

  不做任何哈希，而是将十六进制哈希表示
  *hash* 转换为 SRI。

# 示例

计算与 `nix-prefetch-url` 相同的哈希：

```console
$ nix-prefetch-url file://<(echo test)
1lkgqb6fclns49861dwk9rzb6xnfkxbpws74mxnx01z9qyv1pjpj
$ nix-hash --type sha256 --flat --base32 <(echo test)
1lkgqb6fclns49861dwk9rzb6xnfkxbpws74mxnx01z9qyv1pjpj
```

计算哈希：

```console
$ mkdir test
$ echo "hello" > test/world

$ nix-hash test/ (MD5 hash; default)
8179d3caeff1869b5ba1744e5a245c04

$ nix-store --dump test/ | md5sum (for comparison)
8179d3caeff1869b5ba1744e5a245c04  -

$ nix-hash --type sha1 test/
e4fd8ba5f7bbeaea5ace89fe10255536cd60dab6

$ nix-hash --type sha1 --base16 test/
e4fd8ba5f7bbeaea5ace89fe10255536cd60dab6

$ nix-hash --type sha1 --base32 test/
nvd61k9nalji1zl9rrdfmsmvyyjqpzg4

$ nix-hash --type sha1 --base64 test/
5P2Lpfe76upazon+ECVVNs1g2rY=

$ nix-hash --type sha1 --sri test/
sha1-5P2Lpfe76upazon+ECVVNs1g2rY=

$ nix-hash --type sha256 --flat test/
error: reading file `test/': Is a directory

$ nix-hash --type sha256 --flat test/world
5891b5b522d5df086d0ff0b110fbd9d21bb4fc7163af34d08286a2e846f6be03
```

在十六进制、Nix32、Base64 和 SRI 之间转换：

```console
$ nix-hash --type sha1 --to-base32 e4fd8ba5f7bbeaea5ace89fe10255536cd60dab6
nvd61k9nalji1zl9rrdfmsmvyyjqpzg4

$ nix-hash --type sha1 --to-base16 nvd61k9nalji1zl9rrdfmsmvyyjqpzg4
e4fd8ba5f7bbeaea5ace89fe10255536cd60dab6

$ nix-hash --type sha1 --to-base64 e4fd8ba5f7bbeaea5ace89fe10255536cd60dab6
5P2Lpfe76upazon+ECVVNs1g2rY=

$ nix-hash --type sha1 --to-sri nvd61k9nalji1zl9rrdfmsmvyyjqpzg4
sha1-5P2Lpfe76upazon+ECVVNs1g2rY=

$ nix-hash --to-base16 sha1-5P2Lpfe76upazon+ECVVNs1g2rY=
e4fd8ba5f7bbeaea5ace89fe10255536cd60dab6
```
