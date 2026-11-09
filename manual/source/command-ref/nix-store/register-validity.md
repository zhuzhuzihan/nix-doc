# Name

`nix-store --register-validity` - 将 store 对象注册为有效

# 概要

`nix-store` `--register-validity` [`--reregister`] [`--hash-given`]

# 描述

`--register-validity` 操作从标准输入读取 [store 对象][store object] 的序列化[元数据]，并将这些 store 对象注册为[本地 Nix store][local store] 中的[有效路径][validity]。
与构建期间的[传统的（构建后）输出处理](@docroot@/store/building.md#traditional-post-build-processing)一样，此命令用于这样的情况：待注册 store 对象的[文件系统对象]已经存在于本地 store 中，但数据库尚不知道它们的元数据。
运行此命令可以让数据库与文件系统保持同步，使它们成为名副其实的 store 对象。

输入由一系列记录组成，每个 store 对象一条记录。
每条记录的格式如下：

```
path
nar-hash    (only with --hash-given)
nar-size    (only with --hash-given)
deriver
number-of-references
reference-1
...
reference-n
```

这里，*path* 是要注册的 store 对象的[存储路径]。
*nar-hash* 是该路径的 [NAR][Nix Archive] 序列化结果的 base-16 SHA-256 哈希，*nar-size* 是 NAR 的字节大小。
这两行仅在指定 `--hash-given` 时存在；否则必须省略，Nix 会改为从 store 对象计算 NAR 哈希和大小。
*deriver* 是该路径的 [deriver]（即产生此路径的 derivation）的[存储路径]，如果未知则为空行。
*number-of-references* 指定后面跟有多少条[引用]路径，它们列在其后的各行中。

输入通常由其他 Nix 操作生成，例如 [`exportReferencesGraph`](@docroot@/language/advanced-attributes.md#adv-attr-exportReferencesGraph)。
只接受这种文本格式；`exportReferencesGraph` 在使用[结构化属性](@docroot@/language/advanced-attributes.md#adv-attr-structuredAttrs)时生成的 JSON 形式不被接受。
由于为 builder 生成的文件不包含哈希，因此必须在不带 `--hash-given` 的情况下使用。
调用者有责任提供完整的[闭包]。

这是一个面向内部使用的低级操作。
它的主要用途是在正在填充 Nix store 的镜像或 chroot 中注册系统的闭包，例如在构建 NixOS 安装镜像时。

# 选项

- `--reregister`

  即使 store 对象已在 store 中被标记为有效，也仍然注册它们。
  不带此标志时，已经有效的 store 对象会被跳过。

- `--hash-given`

  期望输入中包含 NAR 哈希和大小（如上所述），而不是从 store 对象计算它们。

{{#include ./opt-common.md}}

{{#include ../opt-common.md}}

{{#include ../env-common.md}}

[file system objects]: @docroot@/store/file-system-object.md
[local store]: @docroot@/store/types/local-store.md
[metadata]: @docroot@/store/store-object.md#metadata
[store object]: @docroot@/store/store-object.md
[store path]: @docroot@/store/store-path.md
[validity]: @docroot@/glossary.md#gloss-validity
[Nix Archive]: @docroot@/store/file-system-object/content-address.md#serial-nix-archive
[reference]: @docroot@/glossary.md#gloss-reference
[closure]: @docroot@/glossary.md#gloss-closure
[deriver]: @docroot@/glossary.md#gloss-deriver
