# Name

`nix-store --realise` - 构建或获取 store 对象

# 概要

`nix-store` {`--realise` | `-r`} *paths…* [`--dry-run`]

# 描述


*paths* 中的每个路径按如下方式处理：

- 如果路径指向一个 [store derivation]：
  1. 如果它不是[有效]的，则通过 substitute 获取 store derivation 文件本身。
  2. 实化它的[输出路径]：
    - 尝试从 [substituters] 获取 store derivation 的[闭包]中与输出路径相关联的 [store 对象]。
      - 对于[内容寻址 derivation]（实验性功能）：
        通过查询 [Nix 数据库]中的内容寻址实化记录来确定要实化的输出路径。
    - 对于无法通过 substitute 获取的任何存储路径，生成所需的 store 对象：
      1. 实化该 derivation 的所有依赖的全部输出
      2. 运行该 derivation 的 [`builder`](@docroot@/language/derivations.md#attr-builder) 可执行文件
         <!-- TODO: Link to build process page #8888 -->
- 否则，如果路径尚不是有效的：尝试从 [substituters] 获取该路径的[闭包]中相关联的 [store 对象]。

如果没有可用的 substitute 且未给定 store derivation，则实化失败。

[store paths]: @docroot@/store/store-path.md
[valid]: @docroot@/glossary.md#gloss-validity
[store derivation]: @docroot@/glossary.md#gloss-store-derivation
[output paths]: @docroot@/glossary.md#gloss-output-path
[store objects]: @docroot@/store/store-object.md
[closure]: @docroot@/glossary.md#gloss-closure
[substituters]: @docroot@/command-ref/conf-file.md#conf-substituters
[content-addressing derivations]: @docroot@/development/experimental-features.md#xp-feature-ca-derivations
[Nix database]: @docroot@/glossary.md#gloss-nix-database

生成的路径会打印在标准输出上。
对于非 derivation 参数，则打印参数本身。

{{#include ../status-build-failure.md}}

# 选项

- `--dry-run`

  在标准错误上打印将要构建或下载哪些软件包的描述，而不实际执行操作。

- `--ignore-unknown`

  如果某个非 derivation 路径没有 substitute，则静默忽略它。

- `--check`

  此选项允许你检查 derivation 是否是确定性的。它会重新构建指定的 derivation，并检查结果是否与现有输出按位相同，如果不同则打印错误。指定的 derivation 的输出必须已经存在。与 `-K` 一起使用时，如果某个输出路径与上一次构建的相应输出不相同，新的输出路径会保留在
  `/nix/store/name.check.` 中。

{{#include ./opt-common.md}}

{{#include ../opt-common.md}}

{{#include ../env-common.md}}

# 示例

此操作通常用于构建由 [`nix-instantiate`](@docroot@/command-ref/nix-instantiate.md) 生成的 [store derivation]：

```console
$ nix-store --realise $(nix-instantiate ./test.nix)
/nix/store/6gwmy5jcnwdlz6aqqhksz863f1l8xc2w-aterm-2.3.1
```

这基本上就是 [`nix-build`](@docroot@/command-ref/nix-build.md) 所做的事情。

要测试先前构建过的 derivation 是否是确定性的：

```console
$ nix-build '<nixpkgs>' --attr hello --check -K
```

使用 [`nix-store --read-log`](./read-log.md) 查看一次构建的标准错误和标准输出：

```console
$ nix-store --read-log $(nix-instantiate ./test.nix)
```
