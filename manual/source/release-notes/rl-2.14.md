# Release 2.14 (2023-02-28)

* 新函数 `builtins.readFileType` 可用。它类似于 `builtins.readDir`，但作用于单个文件或目录。

* 在 Flakes 中，flake 的 `.outPath` 属性现在始终指向包含 `flake.nix` 的目录。此前当 `flake.nix` 位于例如某个 Git 仓库的子目录中时并非如此。
  位于子目录中的 flake 的源码根目录仍然可以通过 `.sourceInfo.outPath` 获取。

* 在使用结构化属性的 derivation（派生）中，你现在可以使用 `unsafeDiscardReferences` 来禁用对某个给定输出的运行时依赖扫描：
  ```nix
  __structuredAttrs = true;
  unsafeDiscardReferences.out = true;
  ```
  例如，在生成自带嵌入式 Nix store 的自包含文件系统镜像时这很有用：在该镜像内部发现的哈希指向的是嵌入式 store，而不是宿主的 Nix store。

  这需要启用 `discard-references` 实验性特性。
