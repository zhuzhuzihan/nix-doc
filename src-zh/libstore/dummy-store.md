R"(

**Store URL 格式**: `dummy://`

此 Store 类型表示一个位于内存中的 Store。
可以读取和写入 Store 对象，但仅在 Store 处于打开状态时有效。
一旦 Store 关闭，所有数据都会被丢弃。

当不存在实际的 Nix Store 但你仍想使用 Nix 求值器时，它非常有用，例如：

```console
# nix eval --store dummy:// --expr '1 + 2'
```

)"
