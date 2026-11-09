# Release 2.16 (2023-05-31)

* 提升了从二进制缓存下载的速度。
  并行下载数（也称为 substitution 数）已从 [`--max-jobs` 设置](../command-ref/conf-file.md#conf-max-jobs)中分离出来。
  新的设置名为 [`max-substitution-jobs`](../command-ref/conf-file.md#conf-max-substitution-jobs)。
  并行下载数现在默认为 16（此前由于与构建任务耦合，默认值为 1）。

* 函数 [`builtins.replaceStrings`](@docroot@/language/builtins.md#builtins-replaceStrings) 现在对其第二个参数 `to` 的值是惰性的。也就是说，只有当 `from` 中对应的模式在字符串 `s` 中匹配到时，`to` 才会被求值。
