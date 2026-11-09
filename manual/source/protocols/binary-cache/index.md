# 二进制缓存

二进制缓存格式是一种设计用于通过 HTTP 暴露 store 的接口。

一个二进制缓存由以下部分组成：

- 根目录下的一个 [`nix-cache-info`](./nix-cache-info.md) 文件，包含远端侧配置。
- 对于每个[存储对象](@docroot@/store/store-object.md)：
  - 一个 [`.narinfo`](./narinfo.md) 文件，包含该对象的[元数据](@docroot@/store/store-object.md#metadata)以及指向对应压缩 NAR 的（通常为相对的）URL。
  - 一个可能经过压缩的 [Nix Archive](@docroot@/store/file-system-object/content-address.md#serial-nix-archive)，包含该存储对象的文件系统数据。
- 对于[构建追踪](@docroot@/store/build-trace.md)中的每个条目，在 `build-trace-v2/<drvBaseName>/<outputName>.doi` 处有一个 JSON 文件：
  - 路径编码了[键](@docroot@/protocols/json/build-trace-entry.md#key)
  - 内容则是[值](@docroot@/protocols/json/build-trace-entry.md#value)。

以下[存储类型](@docroot@/store/types/index.md)使用二进制缓存格式：

- [HTTP 二进制缓存存储](@docroot@/store/types/http-binary-cache-store.md) —— 通过 HTTP(S) 提供服务
- [本地二进制缓存存储](@docroot@/store/types/local-binary-cache-store.md) —— 存储在文件系统上
- [S3 二进制缓存存储](@docroot@/store/types/s3-binary-cache-store.md) —— 存储在 AWS S3 存储桶中
