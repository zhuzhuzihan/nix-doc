# Name

`nix-store --query` - 显示存储路径的信息

# 概要

`nix-store` {`--query` | `-q`}
  {`--outputs` | `--requisites` | `-R` | `--references` | `--referrers` |
  `--referrers-closure` | `--deriver` | `-d` | `--valid-derivers` |
  `--graph` | `--tree` | `--binding` *name* | `-b` *name* | `--hash` |
  `--size` | `--roots`}
  [`--use-output`] [`-u`] [`--force-realise`] [`-f`]
  *paths…*

# 描述

`--query` 操作显示有关存储路径的各种信息。各查询项在下面描述。最多只能指定一个查询。默认查询为 `--outputs`。

*paths* 路径也可以是来自 Nix store 之外、指向 Nix store 的符号链接。在这种情况下，查询将作用于符号链接的目标。

# 通用查询选项

- `--use-output` / `-u`

  对于查询参数中每个是 [store derivation] 的参数，改为对该 derivation 的输出路径应用查询。

- `--force-realise` / `-f`

  先对每个查询参数进行实化（realise）（参见 [`nix-store --realise`](./realise.md)）。

[store derivation]: @docroot@/glossary.md#gloss-store-derivation

# 查询

- `--outputs`

  打印 store derivation *paths* 的[输出路径]。这些是构建该 derivation 时会产生的路径。

  [output paths]: @docroot@/glossary.md#gloss-output-path

- `--references`

  打印存储路径 *paths* 的[引用]集合，即它们的直接依赖。（要获取*所有*依赖，请使用 `--requisites`。）

  [references]: @docroot@/glossary.md#gloss-reference

- `--requisites` / `-R`

  打印存储路径 *paths* 的[*requisites* 集合][requisite]（更常见的叫法是[闭包]）。

  [requisite]: @docroot@/glossary.md#gloss-requisite
  [closure]: @docroot@/glossary.md#gloss-closure

  此查询有一个选项：

    - `--include-outputs`
      同时包含 [store derivation] 现有的输出路径及其闭包。

  此查询可用于实现各种类型的部署。*源码部署*（source deployment）通过分发一个 store derivation 的闭包实现。*二进制部署*（binary deployment）通过分发一个输出路径的闭包实现。*缓存部署*（cache deployment，即源码/二进制的组合部署，包含仅构建时依赖的二进制文件）通过分发一个 store derivation 的闭包并指定选项 `--include-outputs` 实现。

- `--referrers`

  打印存储路径 *paths* 的[*referrer* 集合][referrer]，即当前 Nix store 中引用了 *paths* 之一的存储路径。注意，与 references 不同，referrer 集合不是恒定的；随着存储路径被添加或删除，它可能会发生变化。

  [referrer]: @docroot@/glossary.md#gloss-referrer

- `--referrers-closure`

  打印存储路径集合 *paths* 在 [referrer 关系][referrer]下的闭包；也就是说，所有直接或间接引用 *paths* 之一的存储路径。这些是当前 Nix store 中依赖于 *paths* 的全部路径。

  [referrer]: @docroot@/glossary.md#gloss-referrer

- `--deriver` / `-d`

  打印用于构建存储路径 *paths* 的 [deriver]。如果该路径没有 deriver（例如它是一个源文件），或者 deriver 未知（例如在仅二进制部署的情况下），则打印字符串 `unknown-deriver`。
  返回的 deriver 不保证在本地 store 中存在，例如当 *paths* 是从二进制缓存通过 substitute（替代）获取时。
  请改用 `--valid-derivers` 来获取有效路径。

  [deriver]: @docroot@/glossary.md#gloss-deriver

- `--valid-derivers`

  打印一组 derivation 文件（`.drv`），这些文件在实化时应当产生所述路径。可能什么都不打印，例如对于源码路径或从二进制缓存通过 substitute 获取的路径。

- `--graph`

  以 AT\&T [Graphviz
  软件包](http://www.graphviz.org/)的 `dot` 工具格式打印存储路径 *paths* 的引用图。这可用于可视化依赖图。要获得构建时依赖图，请对 store derivation 应用此查询。要获得运行时依赖图，请对输出路径应用此查询。

- `--tree`

  以嵌套 ASCII 树的形式打印存储路径 *paths* 的引用图。引用按闭包大小降序排列；这往往会使树更扁平、更易读。该查询只在首次遇到某个存储路径时才递归进入它；这可以防止图的树形表示爆炸式增长。

- `--graphml`

  以 [GraphML](http://graphml.graphdrawing.org/) 文件格式打印存储路径 *paths* 的引用图。这可用于可视化依赖图。要获得构建时依赖图，请对 [store derivation] 应用此查询。要获得运行时依赖图，请对输出路径应用此查询。

- `--binding` *name* / `-b` *name*

  打印 store derivation *paths* 的属性 *name*（即环境变量）的值。如果某个 derivation 没有指定的属性，则是一个错误。

- `--hash`

  打印存储路径 *paths* 内容的 SHA-256 哈希（即对给定路径执行 `nix-store --dump` 的输出的哈希）。由于哈希存储在 Nix 数据库中，这是一个快速操作。

- `--size`

  打印存储路径 *paths* 内容的字节大小——确切地说，是对给定路径执行 `nix-store --dump` 的输出的大小。注意，存储路径实际占用的磁盘空间可能更高，尤其是在簇（cluster）较大的文件系统上。

- `--roots`

  打印直接或间接指向存储路径 *paths* 的垃圾回收器 root（GC root）。

{{#include ./opt-common.md}}

{{#include ../opt-common.md}}

{{#include ../env-common.md}}

# 示例

打印当前用户环境中 `svn` 程序的闭包（运行时依赖）：

```console
$ nix-store --query --requisites $(which svn)
/nix/store/5mbglq5ldqld8sj57273aljwkfvj22mc-subversion-1.1.4
/nix/store/9lz9yc6zgmc0vlqmn2ipcpkjlmbi51vv-glibc-2.3.4
...
```

打印 `svn` 的构建时依赖：

```console
$ nix-store --query --requisites $(nix-store --query --deriver $(which svn))
/nix/store/y6qa66l9h0pw161crnlk6y16rdrcljx4-grep-2.5.1.tar.bz2.drv
/nix/store/z716h753s97jhnzvfank2srqbljswpgm-gcc-wrapper.sh
/nix/store/f39x0q73rjdyvzm93y9wrkfr6x39lb7f-glibc-2.3.4.drv
... lots of other paths ...
```

与上一个示例的区别在于，我们查询的是 derivation（`-qd`）的闭包，而不是包含 `svn` 的输出路径的闭包。

以树形显示构建时依赖：

```console
$ nix-store --query --tree $(nix-store --query --deriver $(which svn))
/nix/store/7i5082kfb6yjbqdbiwdhhza0am2xvh6c-subversion-1.1.4.drv
+---/nix/store/vxnmkc8l8d2ijjha4xwhkfgx9vvc3q4c-builder.sh
+---/nix/store/rn9776dy82n5qrgz7xbcl1iw4vfkcrkk-bash-3.0.drv
|   +---/nix/store/x9j20hz6bln1crzn55qifk0bbsm8v5ac-bash
|   +---/nix/store/ajnn1mcm45wjvn0rlc22gvx2cwhjnazx-builder.sh
...
```

显示所有与 `svn` 使用同一个 OpenSSL 库的路径：

```console
$ nix-store --query --referrers $(nix-store --query --binding openssl $(nix-store --query --deriver $(which svn)))
/nix/store/23ny9l9wixx21632y2wi4p585qhva1q8-sylpheed-1.0.0
/nix/store/5mbglq5ldqld8sj57273aljwkfvj22mc-subversion-1.1.4
/nix/store/dpmvp969yhdqs7lm2r1a3gng7pyq6vy4-subversion-1.1.3
/nix/store/l51240xqsgg8a7yrbqdx1rfzyv6l26fx-lynx-2.8.5
```

显示所有直接或间接依赖于 `svn` 所使用的 Glibc（C 库）的路径：

```console
$ nix-store --query --referrers-closure $(ldd $(which svn) | grep /libc.so | awk '{print $3}')
/nix/store/034a6h4vpz9kds5r6kzb9lhh81mscw43-libgnomeprintui-2.8.2
/nix/store/15l3yi0d45prm7a82pcrknxdh6nzmxza-gawk-3.1.4
...
```

注意，`ldd` 是一个打印 ELF 可执行文件所使用的动态库的命令。

为当前用户环境的运行时依赖图生成一张图片：

```console
$ nix-store --query --graph ~/.nix-profile | dot -Tps > graph.ps
$ gv graph.ps
```

显示所有指向依赖于 `svn` 的存储路径的垃圾回收器 root：

```console
$ nix-store --query --roots $(which svn)
/nix/var/nix/profiles/default-81-link
/nix/var/nix/profiles/default-82-link
/home/eelco/.local/state/nix/profiles/profile-97-link
```
