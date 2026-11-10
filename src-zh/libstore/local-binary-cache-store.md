R"(

**Store URL 格式**: `file://`*path*

此 Store 允许读取和写入存储在本地文件系统 *path* 中的[二进制缓存](@docroot@/protocols/binary-cache/index.md)。如果 *path* 不存在，将会被创建。

例如，下面的命令会将 `nixpkgs#hello` 构建或下载到本地 Store，然后将其复制到
`/tmp/binary-cache` 中的二进制缓存：

```
# nix copy --to file:///tmp/binary-cache nixpkgs#hello
```

)"
