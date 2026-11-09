# Name

`nix-prefetch-url` - 将 URL 指向的文件复制进 store 并打印其哈希

# 概要

`nix-prefetch-url` *url* [*hash*]
  [`--type` *hashAlgo*]
  [`--print-path`]
  [`--unpack`]
  [`--name` *name*]

# 描述

命令 `nix-prefetch-url` 下载 URL *url* 引用的文件，打印其密码学哈希，并将其复制进 Nix store。文件在 store 中的名称为 `hash-baseName`，其中 *baseName* 是 *url* 中最后一个斜杠之后的所有内容。

这个命令只是为 Nix 表达式编写者提供的便利工具。通常，Nix 表达式会通过 Nixpkgs 中的 `fetchurl` 表达式从网络获取某个源代码发行包。然而，`fetchurl` 需要一个密码学哈希。如果你不知道哈希值，就得先下载该文件，然后 `fetchurl` 在你构建 Nix 表达式时会再下载一次。由于 `fetchurl` 为下载的文件使用与 `nix-prefetch-url` 相同的名称，因此可以避免这种冗余下载。

如果指定了 *hash*，那么当 Nix store 中已经存在具有相同哈希和基本名称的文件时，就不会执行下载。否则，文件会被下载，如果文件的实际哈希与指定的哈希不匹配，则报错。

该命令将哈希打印到标准输出。除非指定 `--type md5`（此时以 base-16 打印），否则哈希使用 [Nix32](@docroot@/protocols/nix32.md) 打印。此外，如果使用了选项 `--print-path`，则还会打印下载文件在 Nix store 中的路径。

# 选项

- `--type` *hashAlgo*

  使用指定的密码学哈希算法，
  可以是 `blake3`、`md5`、`sha1`、`sha256` 和 `sha512` 之一。
  默认值为 `sha256`。

- `--print-path`

  将下载文件的存储路径打印到标准输出。

- `--unpack`

  解压归档（必须是 tarball 或 zip 文件）并将结果添加到 Nix store。所得的哈希可以配合 Nixpkgs 的 `fetchzip` 或 `fetchFromGitHub` 等函数使用。

- `--executable`

  为下载的文件设置可执行位。

- `--name` *name*

  覆盖文件在 Nix store 中的名称。默认情况下，这是
  `hash-basename`，其中 *basename* 是 *url* 的最后一个组成部分。
  当 *basename* 包含 Nix store 路径中不允许的字符时，
  需要覆盖该名称。

# 示例

```console
$ nix-prefetch-url ftp://ftp.gnu.org/pub/gnu/hello/hello-2.10.tar.gz
0ssi1wpaf7plaswqqjwigppsg5fyh99vdlb9kzl7c9lng89ndq1i
```

```console
$ nix-prefetch-url --print-path mirror://gnu/hello/hello-2.10.tar.gz
0ssi1wpaf7plaswqqjwigppsg5fyh99vdlb9kzl7c9lng89ndq1i
/nix/store/8alrpdaasjd1x6g1fczchmzbpqm936a3-hello-2.10.tar.gz
```

```console
$ nix-prefetch-url --unpack --print-path https://github.com/NixOS/patchelf/archive/0.8.tar.gz
079agjlv0hrv7fxnx9ngipx14gyncbkllxrp9cccnh3a50fxcmy7
/nix/store/19zrmhm3m40xxaw81c8cqm6aljgrnwj2-0.8.tar.gz
```
