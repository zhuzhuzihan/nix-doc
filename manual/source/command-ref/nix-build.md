# Name

`nix-build` - 构建 Nix 表达式

# 概要

`nix-build` [*paths…*]
  [`--arg` *name* *value*]
  [`--argstr` *name* *value*]
  [{`--attr` | `-A`} *attrPath*]
  [`--no-out-link`]
  [`--dry-run`]
  [{`--out-link` | `-o`} *outlink*]

# 消歧

本手册页描述的是命令 `nix-build`，它与 `nix
build` 不同。关于后者的文档，请运行 `nix build --help` 或查看 `man
nix3-build`。

# 描述

`nix-build` 命令构建 *paths* 中 Nix
表达式所描述的 derivation（派生）。如果构建成功，它会在当前目录中放置一个指向结果的符号链接。该符号链接名为 `result`。如果
存在多个 Nix 表达式，或者 Nix 表达式求值结果为
多个 derivation，则会创建多个按顺序编号的符号链接（`result`、`result-2`，依此类推）。

如果未指定 *paths*，那么 `nix-build` 会使用
当前目录中的 `default.nix`（如果存在）。

如果 *paths* 的某个元素以 `http://` 或 `https://` 开头，它会被
解释为一个 tarball 的 URL，该 tarball 将被下载并解压
到临时位置。tarball 必须包含一个单一的顶层
目录，其中至少要有一个名为 `default.nix` 的文件。

`nix-build` 本质上是
[`nix-instantiate`](./nix-instantiate.md)（用于将高层 Nix
表达式转换为低层 [store derivation]）和 [`nix-store
--realise`](@docroot@/command-ref/nix-store/realise.md)（用于构建该 store
derivation）的封装。

[store derivation]: @docroot@/glossary.md#gloss-store-derivation

> **警告**
>
> 构建结果会自动注册为
> Nix 垃圾回收器的根。当 `result` 符号链接被删除或重命名时，这个根会自动消失。因此不要重命名该符号链接。

# 选项

此处未列出的所有选项都会传递给
[`nix-store --realise`](./nix-store/realise.md)，
但 `--arg` 和 `--attr` / `-A` 除外，它们会传递给 [`nix-instantiate`](./nix-instantiate.md)。

- <span id="opt-no-out-link">[`--no-out-link`](#opt-no-out-link)<span>

  不要创建指向输出路径的符号链接。请注意，这样一来
  输出就不会成为垃圾回收器的根，因此
  可能被 `nix-store --gc` 删除。

- <span id="opt-dry-run">[`--dry-run`](#opt-dry-run)</span>

  显示将被构建或下载的存储路径。

- <span id="opt-out-link">[`--out-link`](#opt-out-link)</span> / `-o` *outlink*

  将创建的指向输出路径的符号链接从 `result` 改名为
  *outlink*。

{{#include ./status-build-failure.md}}

{{#include ./opt-common.md}}

{{#include ./env-common.md}}

# 示例

```console
$ nix-build '<nixpkgs>' --attr firefox
store derivation is /nix/store/qybprl8sz2lc...-firefox-1.5.0.7.drv
/nix/store/d18hyl92g30l...-firefox-1.5.0.7

$ ls -l result
lrwxrwxrwx  ...  result -> /nix/store/d18hyl92g30l...-firefox-1.5.0.7

$ ls ./result/bin/
firefox  firefox-config
```

如果 derivation 有多个输出，`nix-build` 会构建默认的
（第一个）输出。你也可以构建全部输出：

```console
$ nix-build '<nixpkgs>' --attr openssl.all
```

这将为每个输出创建一个名为 `result-outputname` 的符号链接。
如果输出名为 `out`，则省略后缀。因此如果 `openssl` 有
输出 `out`、`bin` 和 `man`，`nix-build` 会创建符号链接
`result`、`result-bin` 和 `result-man`。也可以构建一个
特定的输出：

```console
$ nix-build '<nixpkgs>' --attr openssl.man
```

这会创建符号链接 `result-man`。

构建命令行上给出的 Nix 表达式：

```console
$ nix-build --expr 'with import <nixpkgs> { }; runCommand "foo" { } "echo bar > $out"'
$ cat ./result
bar
```

从 Nixpkgs master 分支的最新版本构建 GNU Hello 软件包：

```console
$ nix-build https://github.com/NixOS/nixpkgs/archive/master.tar.gz --attr hello
```
