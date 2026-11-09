# `nix-cache-info` 格式

`nix-cache-info` 文件是位于[二进制缓存](@docroot@/protocols/binary-cache/index.md)根目录下的元数据文件（例如 `https://cache.example.com/nix-cache-info`）。

MIME 类型：`text/x-nix-cache-info`

## 格式

基于行的键值格式：

```
Key: value
```

值的首尾空白会被去除。
没有冒号的行会被忽略。
未知的键会被静默忽略。

## 字段

### `StoreDir`

该缓存构建时所面向的 Nix store 目录路径（例如 `/nix/store`）。

如果存在，Nix 会验证其与客户端的存储目录是否匹配：

```
error: binary cache 'https://example.com' is for Nix stores with prefix '/nix/store', not '/home/user/nix/store'
```

### `WantMassQuery`

`1` 或 `0`。设置 [`want-mass-query`](@docroot@/store/types/http-binary-cache-store.md#store-http-binary-cache-store-want-mass-query) 的默认值。

### `Priority`

整数。设置 [`priority`](@docroot@/store/types/http-binary-cache-store.md#store-http-binary-cache-store-priority) 的默认值。

## 示例

```
StoreDir: /nix/store
WantMassQuery: 1
Priority: 30
```

## 缓存行为

Nix 会将 `nix-cache-info` 缓存在[缓存目录](@docroot@/command-ref/env-common.md#env-NIX_CACHE_HOME)中，TTL 为 7 天。

## 另请参阅

- [HTTP 二进制缓存存储](@docroot@/store/types/http-binary-cache-store.md)
- [通过 HTTP 提供 Nix store 服务](@docroot@/package-management/binary-cache-substituter.md)
- [`substituters`](@docroot@/command-ref/conf-file.md#conf-substituters)
