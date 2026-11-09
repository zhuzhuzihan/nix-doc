# Release 2.17 (2023-07-24)

* [`nix-channel`](../command-ref/nix-channel.md) 现在支持 `--list-generations` 子命令。

* 函数 [`builtins.fetchClosure`](../language/builtins.md#builtins-fetchClosure) 现在可以在[纯求值模式](../command-ref/conf-file.md#conf-pure-eval)下获取 input-addressed 路径，因为它们并非非纯（impure）。

* Nix 现在允许非特权用户/[`allowed-users`](../command-ref/conf-file.md#conf-allowed-users) 对路径签名。
  此前，只有 [`trusted-users`](../command-ref/conf-file.md#conf-trusted-users) 中的用户可以对路径签名。

* 解析器现在会正确合并嵌套的动态属性。例如：

  ```nix
  {
    nested = {
      foo = 1;
    };
    nested = {
      ${"ba" + "r"} = 2;
    };
  }
  ```

  这过去会静默丢弃 `nested.bar`，但现在的行为符合预期，求值结果为：

  ```nix
  { nested = { bar = 2; foo = 1; }; }
  ```

  注意，合并像例子中 `nested` 这样的属性集的多个*完整声明*这一特性，其价值值得怀疑。
  它允许写出非常难以阅读的表达式，例如同一个属性的两处声明之间隔了很多行代码的情况。
  这一行为已存在很久，因此出于向后兼容而受支持，但不应依赖它。

  作为替代，请考虑使用*嵌套属性路径*（nested attribute path）语法：

  ```nix
  {
    nested.foo = 1;
    nested.${"ba" + "r"} = 2;
  }
  ```

* Tarball flake 现在可以重定向到一个会被记录在 lock 文件中的"不可变"（immutable）URL。这允许在 flake 中使用诸如 `https://example.org/hello/latest.tar.gz` 的"可变"（mutable）tarball URL。详情参见 [tarball fetcher](../protocols/tarball-fetcher.md)。
