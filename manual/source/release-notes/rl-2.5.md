# Release 2.5 (2021-12-13)

* 垃圾回收器不再阻塞新的构建，因此 `waiting for the big garbage collector lock...` 这条消息已成为历史。

* 二进制缓存类 store 现在有了 `compression-level` 设置项。

* `nix develop` 新增 `--unpack` 标志，用于运行 `unpackPhase`。

* 列表现在可以使用 `<` 运算符按字典序比较。

* 新增内置函数：`builtins.groupBy`，功能与 Nixpkgs 的 `lib.groupBy` 相同，但速度更快。

* `nix repl` 现在有了 `:log` 命令。
