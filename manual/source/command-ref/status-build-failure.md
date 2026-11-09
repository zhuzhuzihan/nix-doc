# 构建失败的特殊退出码

当请求的构建失败时，会使用 1xx 状态码。当前使用的状态码如下：

- `100` 通用构建失败

  构建器进程以非零退出码返回。

- `101` 构建超时

  构建未能在指定的 `timeout` 时间内完成，因而被中止。

- `102` 哈希不匹配

  构建输出被拒绝，因为它与 [derivation（派生）的 `outputHash` 属性](@docroot@/language/advanced-attributes.md)不匹配。

- `104` 不确定（Not deterministic）

  构建在 check 模式下成功，但产生的输出不是二进制可重现的。

使用 `--keep-going` 标志时可能同时发生多个失败。在这种情况下，1xx 状态码会通过
[按位或](https://en.wikipedia.org/wiki/Bitwise_operation#OR)组合起来。

```
0b1100100
     ^^^^
     |||`- timeout
     ||`-- output hash mismatch
     |`--- build failure
     `---- not deterministic
```
