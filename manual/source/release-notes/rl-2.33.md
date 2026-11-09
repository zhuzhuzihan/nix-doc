# Release 2.33.0 (2025-12-09)

## 新特性

- 新命令 `nix registry resolve` [#14595](https://github.com/NixOS/nix/pull/14595)

  该命令查询 Flakes registry 中的输入名称，并返回其解析到的 flakeref。

  例如查询 Nixpkgs：

  ```
  $ nix registry resolve nixpkgs
  github:NixOS/nixpkgs/nixpkgs-unstable
  ```

  自 [Determinate Nix 3.14.0](https://github.com/DeterminateSystems/nix-src/pull/273) 上游合并而来。

- `nix flake clone` 支持所有输入类型 [#14581](https://github.com/NixOS/nix/pull/14581)

  `nix flake clone` 现已支持任意输入类型。尤其值得一提的是，这使得克隆 tarball 类型的 Flakes 成为可能，例如 FlakeHub 上的 Flakes。

  自 [Determinate Nix 3.12.0](https://github.com/DeterminateSystems/nix-src/pull/229) 上游合并而来。

## 性能改进

- Git fetcher 使用多线程计算 `revCount` [#14462](https://github.com/NixOS/nix/pull/14462)

  当使用具有较长历史的 Git 仓库时，计算 `revCount` 属性可能耗时很长。Nix 现在使用多线程计算 `revCount`，速度大幅提升（例如对 Nixpkgs 从 9.1 秒缩短到 3.7 秒）。

  请注意，如果你不需要 `revCount`，可以通过设置 Flakes 输入属性 `shallow = true` 完全禁用它。

  自 [Determinate Nix 3.12.2](https://github.com/DeterminateSystems/nix-src/pull/245) 上游合并而来。

- `builtins.stringLength` 现在以常数时间运行 [#14442](https://github.com/NixOS/nix/pull/14442)

  字符串的内部表示已被替换为带长度前缀的 Pascal 风格字符串。此前 Nix 将字符串存储为以 NUL 结尾的字节数组，计算长度时需要进行线性扫描。

- 向 `http://` 和 `https://` 二进制缓存存储的上传现在以常数内存运行 [#14390](https://github.com/NixOS/nix/pull/14390)

  Nix 过去会将整个压缩后的 NAR 内容缓冲在内存中，现在改为以流式方式读取。

- Channel URL 迁移到 channels.nixos.org 子域名 [#14517](https://github.com/NixOS/nix/issues/14517) [#14518](https://github.com/NixOS/nix/pull/14518)

  Nix 中所有的 Channel URL 已从 `https://nixos.org/channels/` 更新为 `https://channels.nixos.org/`。该子域名具备 IPv6 支持和改进的 CDN 分发，可靠性更好。旧域名根路径（`nixos.org/channels/`）目前会重定向到新位置，但未来可能会被弃用。

- 修复 `download buffer is full; consider increasing the 'download-buffer-size' setting` 警告 [#11728](https://github.com/NixOS/nix/issues/11728) [#14614](https://github.com/NixOS/nix/pull/14614)

  导致 [#11728](https://github.com/NixOS/nix/issues/11728) 的根本问题已通过使用 [libcurl 写暂停功能](https://curl.se/libcurl/c/curl_easy_pause.html)来控制背压而得到解决，适用于向较慢的目标（如基于 git 的 tarball 缓存）解包的场景。`download-buffer-size` 的默认值现为 1 MiB，并且由于根本原因已经修复，不再建议增大该值。

  这有望改善快速网络连接下的下载性能，因为此前单个缓慢的下载消费者会阻塞线程，导致其他传输无法推进。

  非常感谢 [Lix 项目](https://lix.systems/)，其[实现](https://git.lix.systems/lix-project/lix/commit/4ae6fb5a8f0d456b8d2ba2aaca3712b4e49057fc)为本变更提供了灵感，并协助排查了 libcurl [与暂停相关的问题](https://github.com/curl/curl/issues/19334)。

- 显著提升 tarball 解包性能 [#14689](https://github.com/NixOS/nix/pull/14689) [#14696](https://github.com/NixOS/nix/pull/14696) [#10683](https://github.com/NixOS/nix/issues/10683) [#11098](https://github.com/NixOS/nix/issues/11098)

  Nix 使用由 libgit2 支持的内容寻址缓存来对通过 `fetchTarball` 以及 `github`、`tarball` Flakes 输入获取的文件进行去重。其使用方式已得到显著优化，以减少执行的 I/O 操作数量。对于一个典型的 nixpkgs 源码 tarball，在 Linux 上系统调用次数减少了 200 倍。结合 libcurl 暂停功能，这缓解了 tarball 缓存带来的性能回退。

- 已经有效的 derivation（派生）不再被复制到 store [#14219](https://github.com/NixOS/nix/pull/14219)

  在使用 Nix daemon（守护进程）时，这会带来一定的提速。

- `nix nar ls` 和 `nix nar cat` 速度显著提升，且不再将整个 NAR 缓冲在内存中 [#14273](https://github.com/NixOS/nix/pull/14273) [#14732](https://github.com/NixOS/nix/pull/14732)

## S3 改进

- 通过 HTTP 改进 S3 二进制缓存支持 [#11748](https://github.com/NixOS/nix/issues/11748) [#12403](https://github.com/NixOS/nix/issues/12403) [#12671](https://github.com/NixOS/nix/issues/12671) [#13084](https://github.com/NixOS/nix/issues/13084) [#13752](https://github.com/NixOS/nix/pull/13752) [#13823](https://github.com/NixOS/nix/pull/13823) [#14026](https://github.com/NixOS/nix/pull/14026) [#14120](https://github.com/NixOS/nix/pull/14120) [#14131](https://github.com/NixOS/nix/pull/14131) [#14135](https://github.com/NixOS/nix/pull/14135) [#14144](https://github.com/NixOS/nix/pull/14144) [#14170](https://github.com/NixOS/nix/pull/14170) [#14190](https://github.com/NixOS/nix/pull/14190) [#14198](https://github.com/NixOS/nix/pull/14198) [#14206](https://github.com/NixOS/nix/pull/14206) [#14209](https://github.com/NixOS/nix/pull/14209) [#14222](https://github.com/NixOS/nix/pull/14222) [#14223](https://github.com/NixOS/nix/pull/14223) [#14330](https://github.com/NixOS/nix/pull/14330) [#14333](https://github.com/NixOS/nix/pull/14333) [#14335](https://github.com/NixOS/nix/pull/14335) [#14336](https://github.com/NixOS/nix/pull/14336) [#14337](https://github.com/NixOS/nix/pull/14337) [#14350](https://github.com/NixOS/nix/pull/14350) [#14356](https://github.com/NixOS/nix/pull/14356) [#14357](https://github.com/NixOS/nix/pull/14357) [#14374](https://github.com/NixOS/nix/pull/14374) [#14375](https://github.com/NixOS/nix/pull/14375) [#14376](https://github.com/NixOS/nix/pull/14376) [#14377](https://github.com/NixOS/nix/pull/14377) [#14391](https://github.com/NixOS/nix/pull/14391) [#14393](https://github.com/NixOS/nix/pull/14393) [#14420](https://github.com/NixOS/nix/pull/14420) [#14421](https://github.com/NixOS/nix/pull/14421)

  S3 二进制缓存操作现在通过 HTTP 进行，利用 `libcurl` 原生的 AWS SigV4 认证，而不是 AWS C++ SDK，带来了显著的改进：

  - **内存占用降低**：消除了导致大文件段错误的内存缓冲问题
  - **上传可靠性修复**：解决了 AWS SDK 的分块错误（`InvalidChunkSizeError`）
  - **依赖更轻量**：使用轻量的 `aws-crt-cpp` 而非完整的 `aws-cpp-sdk`，降低构建复杂度

  新实现要求 curl >= 7.75.0，并使用 `aws-crt-cpp` 进行凭据管理。

  所有现有的 S3 URL 格式和参数均继续受支持，但用于配置分段上传（multipart upload）的 store 设置发生了变化：

  - **`multipart-upload`**（默认值：`false`）：为大型文件启用分段上传。启用后，超过分段阈值的文件将被分成多个部分上传。

  - **`multipart-threshold`**（默认值：`100 MiB`）：使用分段上传的最小文件大小。小于该值的文件将使用常规 PUT 请求。仅在 `multipart-upload` 启用时生效。

  - **`multipart-chunk-size`**（默认值：`5 MiB`）：分段上传中每个部分的大小。必须至少为 5 MiB（AWS S3 的要求）。较大的分块大小会减少请求数量，但会占用更多内存。

  - **`buffer-size`**：已被 `multipart-chunk-size` 取代，现在是它的别名。

  请注意，这一变更还意味着即使 Nix 在构建时未包含 `aws-crt-cpp`，现在也支持 S3 二进制缓存存储，但仅限于无需认证的公开存储桶（public bucket）。

- S3 URL 现在通过 `versionId` 参数支持对象版本控制 [#13955](https://github.com/NixOS/nix/issues/13955) [#14274](https://github.com/NixOS/nix/pull/14274)

  S3 URL 现在支持 `versionId` 查询参数，用于从启用了版本控制的 S3 存储桶中获取特定版本的对象。这允许固定到确切的对象版本，以保证可复现性并防止意外变更：

  ```
  s3://bucket/key?region=us-east-1&versionId=abc123def456
  ```

- S3 二进制缓存存储现在支持存储类配置 [#7015](https://github.com/NixOS/nix/issues/7015) [#14464](https://github.com/NixOS/nix/pull/14464)

  S3 二进制缓存存储现在支持通过 `storage-class` 参数为上传的对象配置存储类。这使得用户可以根据访问模式选择合适的存储层级来优化成本。

  用法示例：

  ```bash
  # Use Glacier storage for long-term archival
  nix copy --to 's3://my-bucket?storage-class=GLACIER' /nix/store/...

  # Use Intelligent Tiering for automatic cost optimization
  nix copy --to 's3://my-bucket?storage-class=INTELLIGENT_TIERING' /nix/store/...
  ```

  存储类同时适用于常规上传和分段上传。未指定时，对象将使用存储桶的默认存储类。

  可用的存储类及其特性请参阅 [S3 存储类文档](https://docs.aws.amazon.com/AmazonS3/latest/userguide/storage-class-intro.html)。


## 存储路径信息 JSON 格式变更

`nix path-info --json` 输出的 JSON 格式已更新为一个结构更完善的新版本。

为保持兼容性，`nix path-info --json` 现在需要一个 `--json-format` 选项来指定输出格式版本。
使用不带 `--json-format` 的 `--json` 已被弃用，并将在未来的版本中变为错误。
目前它会默认使用版本 1 并给出警告，以便更平滑地迁移。

### 版本 1（`--json-format 1`）

这是为了向后兼容而保留的旧版格式：

- 基于字符串的哈希值（例如 `"narHash": "sha256:FePFYIlM..."`）
- 基于字符串的内容地址（例如 `"ca": "fixed:r:sha256:1abc..."`）
- 映射键和引用使用完整的存储路径（例如 `"/nix/store/abc...-foo"`）
- 现在在顶层包含 `"storeDir"` 字段

### 版本 2（`--json-format 2`）

新的结构化格式遵循[数据建模指南](@docroot@/development/data-modeling.md)，包含以下变更：

- **带顶层元数据的嵌套结构**：

  输出现在被包裹在一个包含 `version`、`storeDir` 和 `info` 字段的对象中：

  ```json
  {
    "version": 2,
    "storeDir": "/nix/store",
    "info": { ... }
  }
  ```

  从[存储路径基础名称](@docroot@/store/store-path.md#base-name)到存储对象信息的映射嵌套在 `info` 字段之下。

- **使用[存储路径基础名称](@docroot@/store/store-path.md#base-name)而非完整路径**：

  映射键和引用使用存储路径基础名称（例如 `"abc...-foo"`），而不是完整的绝对存储路径。
  结合 `storeDir` 即可重建完整路径。

- **结构化的 `ca` 字段**：

  内容地址现在是一个结构化的 JSON 对象，而不是字符串：

  - 旧：`"ca": "fixed:r:sha256:1abc..."`
  - 新：`"ca": {"method": "nar", "hash": "sha256-ungWv48Bz+pBQUDeXa4iI7ADYaOWF3qctBD/YfIAFa0="}`
  - 对于输入寻址（input-addressed）的存储对象，其值仍为 `null`

  `hash` 字段与其他哈希一样使用 [SRI](https://developer.mozilla.org/en-US/docs/Web/Security/Subresource_Integrity) 格式。

此外，两种格式都新增了以下字段：

  - **`version` 字段**：

    所有存储路径信息 JSON 现在都包含 `"version": <1|2>`。`version` 用于追踪破坏性变更；向输出的 JSON 中添加字段不属于破坏性变更。

  - **`storeDir` 字段**：

    顶层的 `"storeDir"` 字段包含 store 目录路径（例如 `"/nix/store"`）。

## derivation JSON 格式变更

derivation JSON 格式已从版本 3 更新到版本 4：

- **带顶层元数据的嵌套结构**：

  `nix derivation show` 的输出现在被包裹在一个包含 `version` 和 `derivations` 字段的对象中：

  ```json
  {
    "version": 4,
    "derivations": { ... }
  }
  ```

  从 derivation 路径到 derivation 信息的映射嵌套在 `derivations` 字段之下。

  这与 `nix path-info --json --json-format 2` 所使用的结构一致，同样使该命令符合 JSON 指南的要求。

- **重构后的输入（inputs）**：

  输入现在嵌套在一个 `inputs` 对象之下：

  - 旧：`"inputSrcs": [...], "inputDrvs": {...}`
  - 新：`"inputs": {"srcs": [...], "drvs": {...}}`

- **一致的内容地址**：

  固定内容寻址（fixed content-addressed）输出现在使用结构化的 JSON 格式。
  该格式与存储路径信息中的 `ca` 字段（新版本之后）相同。

读取时*不*接受版本 3 及更早的格式。

**受影响的命令**：`nix derivation`，即其 `show` 和 `add` 子命令。

## 杂项变更

- Git fetcher：恢复进度指示 [#14487](https://github.com/NixOS/nix/pull/14487)

  过去在克隆大型仓库时，Nix 会让人感觉"卡住"了。Nix 现在会在获取（fetch）时显示 Git 原生的进度指示。

  自 [Determinate Nix 3.13.0](https://github.com/DeterminateSystems/nix-src/pull/250) 上游合并而来。

- 中断 REPL 命令可以多次生效 [#13481](https://github.com/NixOS/nix/issues/13481)

  此前，每个 REPL 会话中该操作只能生效一次；后续尝试会被忽略。
  此问题现已修复，因此 `:b` 或 `:p` 等 REPL 命令可以稳定地被取消。
  这是对 [Lix 项目](https://gerrit.lix.systems/c/lix/+/1097)中相应变更的 cherry-pick。

- NAR 解包代码已重写，在可用时改用基于 dirfd 的 `openat` 和 `openat2` 系统调用 [#14597](https://github.com/NixOS/nix/pull/14597)

- 动态大小单位渲染 [#14423](https://github.com/NixOS/nix/pull/14423) [#14364](https://github.com/NixOS/nix/pull/14364)

  各种命令和进度条现在使用动态确定的大小单位，而不是始终使用 `MiB`。例如，进度条现在报告的下载状态如下所示：

  ```
  [1/196/197 copied (773.7 MiB/2.1 GiB), 172.4/421.5 MiB DL]
  ```

  而不是：

  ```
  [1/196/197 copied (773.7/2147.3 MiB), 172.4/421.5 MiB DL]
  ```

## Contributors（贡献者）

本次发布离不开以下 33 位贡献者：

- Adam Dinwoodie [**(@me-and)**](https://github.com/me-and)
- jonhermansen [**(@jonhermansen)**](https://github.com/jonhermansen)
- Arnout Engelen [**(@raboof)**](https://github.com/raboof)
- Jean-François Roche [**(@jfroche)**](https://github.com/jfroche)
- tomberek [**(@tomberek)**](https://github.com/tomberek)
- Eelco Dolstra [**(@edolstra)**](https://github.com/edolstra)
- Marcel [**(@MarcelCoding)**](https://github.com/MarcelCoding)
- David McFarland [**(@corngood)**](https://github.com/corngood)
- Soumyadip Sarkar [**(@neuralsorcerer)**](https://github.com/neuralsorcerer)
- Cole Helbling [**(@cole-h)**](https://github.com/cole-h)
- John Ericson [**(@Ericson2314)**](https://github.com/Ericson2314)
- Tristan Ross [**(@RossComputerGuy)**](https://github.com/RossComputerGuy)
- Alex Auvolat [**(@Alexis211)**](https://github.com/Alexis211)
- edef [**(@edef1c)**](https://github.com/edef1c)
- Sergei Zimmerman [**(@xokdvium)**](https://github.com/xokdvium)
- Vinayak Goyal [**(@vinayakankugoyal)**](https://github.com/vinayakankugoyal)
- Graham Dennis [**(@GrahamDennis)**](https://github.com/GrahamDennis)
- Aspen Smith [**(@glittershark)**](https://github.com/glittershark)
- Jens Petersen [**(@juhp)**](https://github.com/juhp)
- Bernardo Meurer [**(@lovesegfault)**](https://github.com/lovesegfault)
- Peter Bynum [**(@pkpbynum)**](https://github.com/pkpbynum)
- Jörg Thalheim [**(@Mic92)**](https://github.com/Mic92)
- Alex Decious [**(@adeci)**](https://github.com/adeci)
- Matthieu Coudron [**(@teto)**](https://github.com/teto)
- Domen Kožar [**(@domenkozar)**](https://github.com/domenkozar)
- Taeer Bar-Yam [**(@Radvendii)**](https://github.com/Radvendii)
- Seth Flynn [**(@getchoo)**](https://github.com/getchoo)
- Robert Hensing [**(@roberth)**](https://github.com/roberth)
- Vladimir Panteleev [**(@CyberShadow)**](https://github.com/CyberShadow)
- bryango [**(@bryango)**](https://github.com/bryango)
- Henry [**(@cootshk)**](https://github.com/cootshk)
- Martin Joerg [**(@mjoerg)**](https://github.com/mjoerg)
- Farid Zakaria [**(@fzakaria)**](https://github.com/fzakaria)
