# Release 2.32.0 (2025-10-06)

## 不兼容变更

- 移除对早于 Nix 2.0 的 daemon（守护进程）与客户端的支持 [#13951](https://github.com/NixOS/nix/pull/13951)

  daemon worker 协议已不再支持不支持协议版本 18 及以上的 daemon 与客户端。首个支持该版本的 Nix 发布版是 2018 年 2 月发布的 Nix 2.0。

- derivation（派生）JSON 格式现在只使用存储路径的基名（basename） [#13570](https://github.com/NixOS/nix/issues/13570) [#13980](https://github.com/NixOS/nix/pull/13980)

  许多 JSON 框架（例如 C++ 的 nlohmann/json、Rust 的 Serde、Haskell 的 Aeson）的使用经验表明，在 JSON 格式中使用 store 目录会阻碍系统化的 JSON 格式设计，因为它要求序列化器/反序列化器接受一个额外的参数（store 目录）。

  我们最终希望在我们的稳定性承诺允许的范围内，对所有 JSON 格式纠正这一问题。第一步是修改 derivation 的 JSON 格式，因为 `nix derivation` 命令——除了在形式上属于不稳定命令之外——相比其他不稳定命令使用面更窄。

  更多细节请参阅 [derivation 的 JSON 格式](@docroot@/protocols/json/derivation/index.md) 文档。

- C API：`nix_get_attr_name_byidx`、`nix_get_attr_byidx` 改为接受 `nix_value *` 而非 `const nix_value *` [#13987](https://github.com/NixOS/nix/pull/13987)

  为了支持更优化的属性集合并内部表示，这些函数需要一个可变的 `nix_value *`，在访问时可能会被修改。这 *不会* 破坏这些函数的 ABI。

## 新特性

- C API：新增惰性属性与列表元素访问器 [#14030](https://github.com/NixOS/nix/pull/14030)

  C API 现在包含惰性访问器函数，可以在不强制求值的情况下从列表和属性集中取值：

  - `nix_get_list_byidx_lazy()` - 获取列表元素而不强制对其求值
  - `nix_get_attr_byname_lazy()` - 按名称获取属性值而不强制求值
  - `nix_get_attr_byidx_lazy()` - 按索引获取属性而不强制求值

  这些函数在将未求值的子值转发给其他列表、属性集或函数调用时非常有用。它们通过把求值推迟到真正需要时进行，从而更高效地处理 Nix 值。

  此外，所有 `_byidx` 函数的边界检查也得到了改进，在访问前会正确校验索引，避免潜在的越界错误。

  `NIX_ERR_KEY` 错误处理的文档也做了澄清，明确说明了何时返回该错误码。

- HTTP 二进制缓存现在支持对元数据的透明压缩

  HTTP 二进制缓存 store 现在可以在上传前压缩 `.narinfo`、`.ls` 和构建日志文件，从而降低带宽占用和存储需求。压缩通过 `Content-Encoding` 头部透明地应用，兼容的客户端可以自动解压这些文件。

  三个新的配置选项控制此行为：
  - `narinfo-compression`：`.narinfo` 文件的压缩方式
  - `ls-compression`：`.ls` 文件的压缩方式
  - `log-compression`：`log/` 目录中构建日志的压缩方式

  用法示例：
  ```
  nix copy --to 'http://cache.example.com?narinfo-compression=gzip&ls-compression=gzip' /nix/store/...
  nix store copy-log --to 'http://cache.example.com?log-compression=br' /nix/store/...
  ```

- 临时构建目录不再包含 derivation 名称 [#13839](https://github.com/NixOS/nix/pull/13839)

  在构建 derivation 期间创建的临时构建目录，其路径中不再包含 derivation 名称，以避免在 derivation 名称过长时导致构建失败。此变更确保 `/nix/var/nix/builds` 下构建目录的前缀长度可预测。

- 外部 derivation 构建器 [#14145](https://github.com/NixOS/nix/pull/14145)

  这是 Nix 调用来为指定系统类型执行 derivation 的辅助程序，例如通过 QEMU 模拟不同类型的平台。更多信息见 [`external-builders` 设置](../command-ref/conf-file.md#conf-external-builders)。

  这目前是一项实验特性。

## 性能改进

- 优化属性集合并的内存使用 [#13987](https://github.com/NixOS/nix/pull/13987)

  [属性集更新操作](@docroot@/language/operators.md#update) 已被优化，以在第二个操作数较小时减少内存重新分配。

  对 nixpkgs 的典型求值而言，该优化在几乎不影响求值性能的情况下，使总分配内存减少约 20%。

  参见 [eval-attrset-update-layer-rhs-threshold](@docroot@/command-ref/conf-file.md#conf-eval-attrset-update-layer-rhs-threshold)

- 已 substitute 的 flake 输入不再被重复复制到 store [#14041](https://github.com/NixOS/nix/pull/14041)

  从 2.25 开始，Nix 无法为已 substitute 的 flake 输入写入缓存条目，这导致它们在首次求值时被重复复制到 store。为这些输入建立缓存，在某些情况下可使性能几乎翻倍——尤其是在 I/O 受限的机器上，以及使用会抓取大量输入的命令（如 `nix flake [archive|prefetch-inputs]`）时。

- `nix flake check` 现在会跳过可被 substitute 的 derivation [#13574](https://github.com/NixOS/nix/pull/13574)

  此前，`nix flake check` 会对所有 derivation 进行求值并构建/substitute。现在，它会跳过下载那些可以 substitute 的 derivation。在检查结果可能已有缓存的环境中（比如 CI），这可以大幅缩短调用耗时。

- `fetchTarball` 和 `fetchurl` 现在可以正确 substitute (#14138)

  某个时间点起，我们停止了对带有设定 `narHash` 的 `fetchTarball` 和 `fetchurl` 调用进行 substitute，以避免在 `fetchTree` 中错误地 substitute，尽管对旧式的 `fetch{Tarball,url}` 调用进行 substitute 本来是安全的。此修复在安全的前提下恢复了这一行为。
- 开始将 AST 分配迁移到 bump allocator [#14088](https://github.com/NixOS/nix/issues/14088)

  这使 AST 中留下的是更小的不可变结构。到目前为止，这在一项 NixOS 配置求值上节省了约 2% 的内存。
## Contributors（贡献者）

本次发布由以下 32 位贡献者共同完成：

- Farid Zakaria [**(@fzakaria)**](https://github.com/fzakaria)
- dram [**(@dramforever)**](https://github.com/dramforever)
- Ephraim Siegfried [**(@EphraimSiegfried)**](https://github.com/EphraimSiegfried)
- Robert Hensing [**(@roberth)**](https://github.com/roberth)
- Taeer Bar-Yam [**(@Radvendii)**](https://github.com/Radvendii)
- Emily [**(@emilazy)**](https://github.com/emilazy)
- Jens Petersen [**(@juhp)**](https://github.com/juhp)
- Bernardo Meurer [**(@lovesegfault)**](https://github.com/lovesegfault)
- Jörg Thalheim [**(@Mic92)**](https://github.com/Mic92)
- Leandro Emmanuel Reina Kiperman [**(@kip93)**](https://github.com/kip93)
- Marie [**(@NyCodeGHG)**](https://github.com/NyCodeGHG)
- Ethan Evans [**(@ethanavatar)**](https://github.com/ethanavatar)
- Yaroslav Bolyukin [**(@CertainLach)**](https://github.com/CertainLach)
- Matej Urbas [**(@urbas)**](https://github.com/urbas)
- Jami Kettunen [**(@JamiKettunen)**](https://github.com/JamiKettunen)
- Clayton [**(@netadr)**](https://github.com/netadr)
- Grégory Marti [**(@gmarti)**](https://github.com/gmarti)
- Eelco Dolstra [**(@edolstra)**](https://github.com/edolstra)
- rszyma [**(@rszyma)**](https://github.com/rszyma)
- Philip Wilk [**(@philipwilk)**](https://github.com/philipwilk)
- John Ericson [**(@Ericson2314)**](https://github.com/Ericson2314)
- Tom Westerhout [**(@twesterhout)**](https://github.com/twesterhout)
- Tristan Ross [**(@RossComputerGuy)**](https://github.com/RossComputerGuy)
- Sergei Zimmerman [**(@xokdvium)**](https://github.com/xokdvium)
- Jean-François Roche [**(@jfroche)**](https://github.com/jfroche)
- Seth Flynn [**(@getchoo)**](https://github.com/getchoo)
- éclairevoyant [**(@eclairevoyant)**](https://github.com/eclairevoyant)
- Glen Huang [**(@hgl)**](https://github.com/hgl)
- osman - オスマン [**(@osbm)**](https://github.com/osbm)
- David McFarland [**(@corngood)**](https://github.com/corngood)
- Cole Helbling [**(@cole-h)**](https://github.com/cole-h)
- Sinan Mohd [**(@sinanmohd)**](https://github.com/sinanmohd)
- Philipp Otterbein
