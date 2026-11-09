# `.narinfo` 格式

`.narinfo` 文件以[二进制缓存](@docroot@/protocols/binary-cache/index.md)格式包含[存储对象的元数据](@docroot@/store/store-object.md#metadata)。
它是一种简单的面向行的格式，每行是一个 `Key: Value`（键: 值）对。
某些键（例如 `Sig`）可能出现多次。

文件名为 `<hash>.narinfo`，其中 `<hash>` 是该存储对象的[存储路径](@docroot@/store/store-path.md)的[哈希部分](@docroot@/store/store-path.md#digest)。

这些字段与 [store object info](@docroot@/protocols/json/store-object-info.md) JSON 格式中记录的字段相对应：

| `.narinfo` 字段 | JSON 字段 | 差异 |
|---|---|---|
| `StorePath` | [`path`](@docroot@/protocols/json/store-object-info.md#oneOf_i2_path) | 完整的[存储路径](@docroot@/store/store-path.md)而非[存储路径基本名称](@docroot@/store/store-path.md#base-name) |
| `URL` | [`url`](@docroot@/protocols/json/store-object-info.md#oneOf_i2_url) | |
| `Compression` | [`compression`](@docroot@/protocols/json/store-object-info.md#oneOf_i2_compression) | 若省略则默认为 `bzip2` |
| `FileHash` | [`downloadHash`](@docroot@/protocols/json/store-object-info.md#oneOf_i2_downloadHash) | 字符串编码的哈希而非结构化形式 |
| `FileSize` | [`downloadSize`](@docroot@/protocols/json/store-object-info.md#oneOf_i2_downloadSize) | |
| `NarHash` | [`narHash`](@docroot@/protocols/json/store-object-info.md#oneOf_i2_narHash) | 字符串编码的哈希而非结构化形式 |
| `NarSize` | [`narSize`](@docroot@/protocols/json/store-object-info.md#oneOf_i2_narSize) | |
| `References` | [`references`](@docroot@/protocols/json/store-object-info.md#oneOf_i2_references) | 以空格分隔的[存储路径基本名称](@docroot@/store/store-path.md#base-name)列表而非 JSON 数组 |
| `Deriver` | [`deriver`](@docroot@/protocols/json/store-object-info.md#oneOf_i2_deriver) | [存储路径基本名称](@docroot@/store/store-path.md#base-name)；以 `unknown-deriver` 代替 `null` |
| `Sig` | [`signatures`](@docroot@/protocols/json/store-object-info.md#oneOf_i2_signatures) | 可出现多次而非使用数组 |
| `CA` | [`ca`](@docroot@/protocols/json/store-object-info.md#oneOf_i2_ca) | 字符串编码的[内容地址](@docroot@/store/store-object/content-address.md)而非结构化形式 |

## 示例

<!-- TODO make this include a test file instead of being manually written once we have one -->

```
StorePath: /nix/store/n5wkd9frr45pa74if5gpz9j7mifg27fh-foo
URL: nar/1w1fff338fvdw53sqgamddn1b2xgds473pv6y13gizdbqjv4i5p3.nar.xz?sha256=1w1fff338fvdw53sqgamddn1b2xgds473pv6y13gizdbqjv4i5p3
Compression: xz
FileHash: sha256:09ymwqf5i9q7d4dm7x4pjjcqqj0qrcp5lnznbh42gfsci5hcbqqm
FileSize: 4029176
NarHash: sha256:09ymwqf5i9q7d4dm7x4pjjcqqj0qrcp5lnznbh42gfsci5hcbqqm
NarSize: 34878
References: g1w7hy3qg1w7hy3qg1w7hy3qg1w7hy3q-bar n5wkd9frr45pa74if5gpz9j7mifg27fh-foo
Deriver: g1w7hy3qg1w7hy3qg1w7hy3qg1w7hy3q-bar.drv
Sig: asdf:AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA==
Sig: qwer:AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA==
CA: fixed:r:sha256:1lr187v6dck1rjh2j6svpikcfz53wyl3qrlcbb405zlh13x0khhh
```
