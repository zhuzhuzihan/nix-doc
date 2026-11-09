# Nix Store（Nix 存储）

*Nix store*（Nix 存储）是一种用于存放不可变文件系统数据（例如软件包）的抽象，这些数据可以依赖于其他同类数据。

具体而言（尽管其中用到了本章其余部分才定义的概念），一个 store 由以下部分组成：

- 一组[存储对象][store object]，即不可变的文件系统数据。

  也可以将其看作一个从[存储路径][store path]到存储对象的映射。

- 一组 [derivation（派生）][derivation]，即构建存储对象的指令。

  也可以将其看作一个从[存储路径][store path]到 derivation 的映射。
  由于 derivation 的存储路径总是以 `.drv` 结尾，而其他存储对象的存储路径从不如此，这两个映射还可以合并为一个。
  derivation 本身也可以被编码为存储对象。

- 一个 [build trace]（构建痕迹），记录了哪些 derivation 已被构建以及它们产出了什么。

  > **警告**
  >
  > build trace 这一概念目前处于
  > [**实验性**](@docroot@/development/experimental-features.md#xp-feature-ca-derivations)
  > 阶段，可能发生变化。

存在[多种类型的 Nix store][store type]，它们具有不同的能力，例如[本地文件系统][local store]（`/nix/store`）上的默认 store，或[二进制缓存][binary cache]。

[store object]: ./store-object.md
[store path]: ./store-path.md
[derivation]: ./derivation/index.md
[build trace]: ./build-trace.md

[store type]: ./types/index.md
[local store]: ./types/local-store.md
[binary cache]: ./types/http-binary-cache-store.md
