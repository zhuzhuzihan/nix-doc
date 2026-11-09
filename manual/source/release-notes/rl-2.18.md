# Release 2.18 (2023-09-20)

- 新增两个内置函数：
  [`builtins.parseFlakeRef`](@docroot@/language/builtins.md#builtins-parseFlakeRef)
  和
  [`builtins.flakeRefToString`](@docroot@/language/builtins.md#builtins-flakeRefToString)。
  这两个函数可用于在以属性集和 URL 两种形式编码的 flake reference 之间相互转换。

- [`builtins.toJSON`](@docroot@/language/builtins.md#builtins-parseFlakeRef) 现在会为它发现求值错误所在的路径打印 [--show-trace](@docroot@/command-ref/conf-file.html#conf-show-trace) 条目。

- 关于 [`nix derivation add`](@docroot@/command-ref/new-cli/nix3-derivation-add.md) 输入格式不合法的错误信息现在更清晰、更详细。

- `discard-references` 特性已经稳定。
  这意味着
  [unsafeDiscardReferences](@docroot@/language/advanced-attributes.md#adv-attr-unsafeDiscardReferences)
  属性不再由实验性标志守护，可以自由使用。

- 作为存储路径的 derived path，其 JSON 输出现在是一个字符串，而不是带单个 `path` 字段的对象。
  这只影响 `nix-build --json` "构建"非 derivation 之物（例如获取的源码）的情况——那本就是一个空操作。

- 新增内置函数 [`outputOf`](@docroot@/language/builtins.md#builtins-outputOf)。
  它是 [`dynamic-derivations`](@docroot@/development/experimental-features.md#xp-feature-dynamic-derivations) 实验性特性的一部分。

- 深度大于 2 的 flake follow 路径现在能被正确处理，避免了"follows a non-existent input"错误。

- [`nix-store --query`](@docroot@/command-ref/nix-store/query.md) 新增一种查询类型：`--valid-derivers`。它返回本地 store 中所有*可以*用来构建所传参数输出的 `.drv` 文件。与之相对，`--deriver` 返回的是*实际*用于构建所传参数输出的那一个 `.drv` 文件。如果该输出是从二进制缓存替代（substitute）而来的，这个 `.drv` 文件可能只存在于那个二进制缓存上而不在本地。
