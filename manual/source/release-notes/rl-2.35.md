# Release 2.35.0 (2026-06-22)

## Highlights（亮点）

- 源码现在以更惰性的方式复制到 Nix store [#3121](https://github.com/NixOS/nix/issues/3121) [#15711](https://github.com/NixOS/nix/pull/15711) [#15920](https://github.com/NixOS/nix/pull/15920)

  历史上，Flakes 源码树会被急切地抓取到 Nix store 中并从中求值，以确保求值的确定性与封闭性，即使产生的 store 对象并未用作 derivation（派生）输入。这让实现更简单，却使 Flakes 在大型仓库中不可用，并且每次源码树变更都会对 store 执行不必要的写入。

  自 Nix 2.32 起，求值期间读取源码的所有 I/O（`path:` 和 `hg+:` 风格的输入除外）都被导向其原始文件系统位置（对于基于 tarball 的输入，则导向 `~/.cache/nix/tarball-cache-v2` 这个 bare git 仓库）。然而，源码树仍会被抓取到 store 中——主要是为了计算最终的内容寻址存储路径。在多数情况下（例如导入 `nixpkgs` 软件包集合），这并非必要。

  触碰（并对其 NAR 序列化结果做哈希）整个源码树是不可避免的，因为：

  - 对于 Flakes 输入，`narHash` 完整性必须被急切地检查。
  - Flakes 的 `outPath` 属性必须事先可知，并且出于向后兼容，它必须是一个带有[常量字符串上下文](@docroot@/language/string-context.md#string-context-constant)的内容寻址存储路径字符串，代表该 Flakes 源码树。

  即使在向后兼容性要求所施加的约束之内，仍有若干可以实现的改进。为了减少执行的复制次数，Nix 现在会在不复制的情况下先对输入做哈希，假定 `.outPath` 不会出现在 derivation 属性中，因而永远不会真正被抓取到 store。这样做的代价是当假定不成立时需要做更多工作，但在典型用例中减少了工作量。求值器仍会表现得好像复制已经执行过：

  - 从求值器的视角看，Flakes 仍然是从 store 中求值的。
  - `toString ./.` 仍然产生一个不带上下文的内容寻址存储路径字符串。
  - 跨越文件系统中的树与 Nix 视角中的树（其上有"虚拟"覆盖层）的路径解析仍可工作。例如，Flakes 源码树中可以包含指向其对应 store 对象之外的相对符号链接（尽管这种用法不被推荐，并且会使进一步的惰性化改进变得难以实现）。
  - 从 Flakes 的 `outPath` 读取文件仍可工作。例如，以下代码是良构的，且不被视为 [IFD](@docroot@/language/import-from-derivation.md)：

  ```nix
  builtins.readFile ( /. + (builtins.unsafeDiscardStringContext self.outPath) + "/flake.nix" )
  ```

  类似的处理也已应用于 `builtins.fetchTarball`，它不再急切地将路径复制到 store。
  `builtins.storePath` 现在也会在"半惰性"的存储路径上短路，除非必要才执行 substitute。

  预期这一变化会显著减少典型求值所需的磁盘占用，并使抓取和解包 nixpkgs tarball（无论通过 `fetchTree`/Flakes 还是通过 `fetchTarball`）获得约 2 倍的速度提升。

- 支持基于 FreeBSD `libjail` 的沙箱，在安装器中加入 `x86_64-freebsd` [#9968](https://github.com/NixOS/nix/pull/9968) [#13281](https://github.com/NixOS/nix/pull/13281) [#15673](https://github.com/NixOS/nix/pull/15673)

  FreeBSD 版本的 Nix 现在支持通过 FreeBSD jails 进行构建沙箱隔离，并且默认启用。
  传统的安装器脚本中也加入了 FreeBSD 构建。beta 版的 Rust 安装器尚不支持。
  FreeBSD 支持不如 Linux 或 macOS 那样经过充分测试，但完全能够构建软件包并完成在 Linux 上对 Nix 所期待的其他任务。

## 改进

- HTTP/3 (QUIC) 支持 [#15961](https://github.com/NixOS/nix/pull/15961)

  Nix 现在可以通过 HTTP/3 (QUIC) 从二进制缓存和其他 HTTP(S) 来源抓取，由新的 [`http3`](@docroot@/command-ref/conf-file.md#conf-http3) 设置控制（默认禁用）。
  启用后，Nix 会请求 HTTP/3，并且对未通告 QUIC 的服务器透明地回退到 HTTP/2 或 HTTP/1.1。
  该设置仅在链接到以 HTTP/3 支持构建的 `libcurl` 时生效，否则会被忽略，Nix 继续使用 HTTP/2，不会发出警告或错误。

  启用方式：

  ```
  nix.conf: http3 = true
  CLI:      --http3
  ```

  或禁用方式：

  ```
  nix.conf: http3 = false
  CLI:      --no-http3
  ```

- 链接 mimalloc 以加快求值 [#15596](https://github.com/NixOS/nix/pull/15596)

  `nix` 二进制文件现在默认链接 [mimalloc](https://github.com/microsoft/mimalloc)，为所有非 GC 分配替换 glibc 的 malloc。
  这在求值工作负载上带来了 **5–12% 的挂钟时间提升**，范围从 `nix-instantiate hello` 到 `nix-env -qa` 以及完整的 NixOS 配置。
  该分配器可以在构建时通过 `-Dnix:mimalloc=disabled` 禁用。

- Git 抓取器的 `revCount` 属性现在被惰性计算，且在显式指定时原样透传 [#15772](https://github.com/NixOS/nix/pull/15772) [#14596](https://github.com/NixOS/nix/pull/14596)

  传递给 Git 抓取器的 `revCount` 和 `lastModified` 属性在显式指定时不再被急切地校验。

  当未显式指定时，`revCount` 现在也是一个 thunk 值，不再被急切地计算。这会将这项（可能）昂贵的计算推迟到实际需要该值时才进行。

- 可配置的文件传输重试退避，支持 full jitter 与 `Retry-After` [#15023](https://github.com/NixOS/nix/issues/15023) [#15419](https://github.com/NixOS/nix/issues/15419) [#15449](https://github.com/NixOS/nix/pull/15449)

  文件传输重试（下载与上传）现在使用 AWS 风格的 "full jitter" 指数退避，将 HTTP 503 视为限速响应（与 429 相同的更长延迟），
  并遵循 `Retry-After` 响应头。

  重试时机可通过新的 `nix.conf` 设置进行配置：

  - [`filetransfer-retry-delay`](@docroot@/command-ref/conf-file.md#conf-filetransfer-retry-delay)：瞬时错误的基础延迟
  - [`filetransfer-retry-delay-rate-limited`](@docroot@/command-ref/conf-file.md#conf-filetransfer-retry-delay-rate-limited)：429/503 的基础延迟
  - [`filetransfer-retry-max-delay`](@docroot@/command-ref/conf-file.md#conf-filetransfer-retry-max-delay)：每次尝试的延迟上限
  - [`filetransfer-retry-jitter`](@docroot@/command-ref/conf-file.md#conf-filetransfer-retry-jitter)：启用 full jitter

  现有的 `download-attempts` 设置已重命名为 [`filetransfer-retry-attempts`](@docroot@/command-ref/conf-file.md#conf-filetransfer-retry-attempts)，以反映它同样适用于上传。
  旧名称作为别名保留以实现向后兼容。

  每个 substituter 的覆盖配置可以作为 store 引用参数使用（[`retry-delay`](@docroot@/store/types/http-binary-cache-store.md#store-http-binary-cache-store-retry-delay)、[`retry-delay-rate-limited`](@docroot@/store/types/http-binary-cache-store.md#store-http-binary-cache-store-retry-delay-rate-limited)、[`retry-max-delay`](@docroot@/store/types/http-binary-cache-store.md#store-http-binary-cache-store-retry-max-delay)、[`retry-attempts`](@docroot@/store/types/http-binary-cache-store.md#store-http-binary-cache-store-retry-attempts)），例如 `s3://my-cache?retry-attempts=8`。

- 改进 chroot store 的 daemon socket 路径逻辑 [#15190](https://github.com/NixOS/nix/pull/15190)

  默认的 daemon socket 路径现在会在定义了 per-store [`state`](@docroot@/store/types/local-store.md#store-local-store-state) 目录时使用它，而不是总是使用全局的 [`NIX_STATE_DIR`](@docroot@/command-ref/env-common.md#env-NIX_STATE_DIR)。
  这意味着每个[本地 chroot store](@docroot@/store/types/local-store.md#chroot) 都会自动获得自己的 socket 路径。

  示例：

  ```bash
  nix-daemon --store /foo/bar
  ```

  现在会使用位于以下位置的 socket：
  ```
  /foo/bar/nix/var/nix/daemon-socket/socket
  ```
  而不是
  ```
  $NIX_STATE_DIR/daemon-socket/socket
  ```

  希望在旧位置对外提供或连接 chroot store 的用户必须强制指定 socket 位置：

  - 作为服务端（运行 daemon）时，使用新的 [`--socket-path`](@docroot@/command-ref/new-cli/nix3-daemon.md#opt-socket-path) 标志：

    ```bash
    nix daemon --socket-path "$NIX_STATE_DIR/daemon-socket/socket"
    ```

  - 作为客户端连接时，把路径放进 [store URL](@docroot@/store/types/local-daemon-store.md)：

    ```
    unix://$NIX_STATE_DIR/daemon-socket/socket
    ```

- Linux 沙箱：同时屏蔽 `listxattr` 系统调用 [#15743](https://github.com/NixOS/nix/pull/15743)

  Linux 沙箱现在对 `listxattr`、`llistxattr` 和 `flistxattr` 也返回 `ENOTSUP`，与现有的 `getxattr`/`setxattr`/`removexattr` 处理方式保持一致。
  这可以防止宿主的 xattr（例如 `security.selinux`）泄漏进构建，并修复了通过 `listxattr` 探测 xattr 支持的工具（例如 `mkfs.ubifs`）。

- fetchGit 与 type = "git" 的 Flakes 输入支持 SCP 风格 URL [#14852](https://github.com/NixOS/nix/issues/14852) [#14867](https://github.com/NixOS/nix/issues/14867) [#14863](https://github.com/NixOS/nix/pull/14863)

  Nix 现在（再次）识别 [Git URL 的 SCP 风格语法](https://git-scm.com/docs/git-clone#_git_urls)。这部分恢复了
  `fetchGit` 与 Nix 2.3 的兼容性。以下语法重新受到支持：

  ```nix
  builtins.fetchGit "host:/absolute/path/to/repo"
  ```

  Nix 还会原样透传波浪号（用于家目录）：

  ```nix
  builtins.fetchGit "host:~/relative/to/home"
  ```

  加上方括号时也支持 IPv6 地址：

  ```nix
  builtins.fetchGit "user@[::1]:~/relative/to/home"
  ```

  `builtins.fetchTree` 现在也支持该语法：

  ```nix
  builtins.fetchTree { type = "git"; url = "host:/path/to/repo"; }
  ```

- `nix flake check` 现在支持 `--print-out-paths` [#13470](https://github.com/NixOS/nix/issues/13470) [#15476](https://github.com/NixOS/nix/pull/15476) 和 `--out-link` [#13470](https://github.com/NixOS/nix/issues/13470) [#15476](https://github.com/NixOS/nix/pull/15476)，未指定该标志时默认不创建 out link。

- 为 `nix store delete` 新增 `--skip-alive`（以及为兼容 Lix 用户的 `--skip-live` 别名）选项，用于在闭包内回收垃圾 [#7239](https://github.com/NixOS/nix/issues/7239) [#15236](https://github.com/NixOS/nix/pull/15236) [#15727](https://github.com/NixOS/nix/pull/15727)

  `nix store delete --recursive --skip-alive` 可用于在闭包内回收垃圾，此时它只会收集其参数闭包中属于死路径的部分。
  为支持该模式还新增了额外选项 `--also-referrers`，允许同时删除闭包中路径的 referrers。

- `builtins.getFlake` 现在支持 path 值 [#15290](https://github.com/NixOS/nix/pull/15290)

  `builtins.getFlake` 现在接受 path 值，不再仅限于 flakerefs。这提升了相对 Flakes 的可用性，让你可以写 `builtins.getFlake ./subflake`。
  该变化不允许指定尚未进入 store 的路径（不过它们并没有有效的 store 对象，即如果该 Flakes 只是被哈希过——而未被复制到 store——这不会强制触发一次复制）。这一点在未来的版本中可能会改变。

- `nix-profile.fish` 和 `nix-profile-daemon.fish` 现在使用 `$NIX_LINK` 而不是 `$HOME/.nix-profile` 来计算 `NIX_PROFILE` 的值 [#14293](https://github.com/NixOS/nix/pull/14293)

- `nix` 二进制文件现在导出 C 绑定中的符号 [#15696](https://github.com/NixOS/nix/pull/15696)

  这使得基于 C API 编写的 Nix 插件能够动态查找符号，而无需链接对应的 `libnix*c.so` 库。

- 修复了计算出的 Git LFS 端点 URL 以遵循规范 [#15891](https://github.com/NixOS/nix/pull/15891)，并降低了 LFS 抓取的内存占用 [#15912](https://github.com/NixOS/nix/pull/15912)

- 我们现在会校验抓取到的 Git LFS 对象的 OID 与请求一致 [#15845](https://github.com/NixOS/nix/pull/15845)

- Primop 文档现在包含时间复杂度信息 [#14554](https://github.com/NixOS/nix/pull/14554)

- 改进了关于存储路径与 derivation 构建的文档 [#14699](https://github.com/NixOS/nix/pull/14699)

- [build hook](@docroot@/command-ref/conf-file.md#conf-build-hook) 现在以 `SIGTERM` 而不是 `SIGKILL` 终止 [#15105](https://github.com/NixOS/nix/pull/15105)

- 下载/上传日志会去除 URL 的 `userinfo` 组件 [#15715](https://github.com/NixOS/nix/pull/15715)

## 内容寻址 derivation 变更

  实验性的内容寻址（CA）derivation 特性在构建痕迹（以前称为 "realisations"）的标识方式上经历了一次重大变化。
  这改变了 realisations 的二进制缓存端点以及 daemon/nix-serve 协议（由 daemon 协议特性开关控制）。

- realisations 改为以存储路径为键，而不是 hash modulo [#11897](https://github.com/NixOS/nix/issues/11897) [#12464](https://github.com/NixOS/nix/pull/12464)

  之前，构建痕迹条目（realisation）以 derivation 的 hash modulo 为键。简单来说，传递依赖于具有相同 `outPath` 的不同 fixed-output derivation 的 derivation 会共享同一个 realisation。

  现在，构建痕迹条目以常规的 derivation 存储路径（`.drvPath`）加上输出名为键。例如，不再是：

  ```
  sha256:ba7816bf8f01...!out
  ```

  而键现在为：

  ```
  /nix/store/abc...-foo.drv^out
  ```

- 移除了对 "deep" realisations 的支持 [#15289](https://github.com/NixOS/nix/pull/15289)

  之前构建痕迹（"realisations" 的集合）中同时包含未解析（unresolved）和[已解析](@docroot@/store/resolution.md)（resolved）derivation 的条目。
  现在，它只包含已解析 derivation 的条目。
  目前，未解析的 derivation 仍会从这些底层构建痕迹条目中解析出来。
  这样做更慢，但好处是构建痕迹条目变为无状态且自描述的——使得在 store 之间共享 realisations 更加容易。

  该变化 necessitates 对二进制缓存格式的修改：

  - 构建痕迹的目录从 `realisations/` 移动到 `build-trace-v2/`。
  - 文件路径从 `realisations/<hash>!<output>.doi` 变为 `build-trace-v2/<drvName>/<outputName>.doi`。
  - 构建痕迹条目的 JSON 格式现在拆分为 `key` 和 `value` 两个对象：
    ```json
    {
      "key": {
        "drvPath": "abc...-foo.drv",
        "outputName": "out"
      },
      "value": {
        "outPath": "xyz...-foo",
        "signatures": [{ "keyName": "cache.example.com-1", "sig": "..." }]
      }
    }
    ```
    之前，这些是带有字符串 `id` 字段（如 `"sha256:...!out"`）的扁平对象。
  - 已弃用的 `dependentRealisations` 字段被移除。

  本地 SQLite 数据库中存储的构建痕迹条目不再有任何指向 store 对象的外键引用。
  这是因为可能已被删除的已解析 derivation 的构建痕迹条目需要被保留，否则其他未解析 derivation 的输出将实际上被遗忘。
  由于缺乏明确的默认策略，构建痕迹的垃圾回收尚未实现。

- realisations 和 `path-info` 的结构化签名 [#15009](https://github.com/NixOS/nix/pull/15009)

  JSON 格式中的[签名](@docroot@/protocols/json/signature.md)现在表示为带有 `keyName` 和 `sig` 字段的结构化对象，而不是冒号分隔的字符串。
  `nix path-info --json --json-format 3` 为该命令启用新版本。
  出于向后兼容，JSON 解析同时接受旧的字符串格式和新的结构化格式。

  该格式也用于二进制缓存中的构建痕迹条目。

- `nix realisation` 命令已更名为 `nix store build-trace` [#16000](https://github.com/NixOS/nix/pull/16000) [#15948](https://github.com/NixOS/nix/pull/15948)

## 构建性能改进

- 将 post-build-hook 改为异步执行 [#15406](https://github.com/NixOS/nix/issues/15406) [#15451](https://github.com/NixOS/nix/pull/15451)

  [`post-build-hook`](@docroot@/command-ref/conf-file.md#conf-post-build-hook) 现在异步运行，不再阻塞构建事件循环。
  依赖的构建仍要等 hook 结束才会启动，但多个 hook 实例现在会并发启动——上限为 [`max-jobs`](@docroot@/command-ref/conf-file.md#conf-max-jobs) 限制。

- zstd 压缩现在输出多帧结果并使用更少的内存 [#15550](https://github.com/NixOS/nix/pull/15550)

  zstd 压缩的 NAR 现在写为一系列独立的 16 MiB 帧，而不是单个大帧。
  这为未来版本中的并行解压奠定了基础，且无需重新填充缓存，并显著降低了压缩期间的峰值内存占用
  （例如对于 1 GiB 的存储路径，从约 600 MiB 降到约 100 MiB）。

  输出仍是标准 zstd，可被现有的 Nix 二进制文件和 `zstd` CLI 原样解码；压缩比实际上没有变化。

  每帧压缩现在最多使用 4 个工作线程。对于 zstd 这是新的默认值：当 `compression=zstd` 时，[`parallel-compression`](@docroot@/store/types/http-binary-cache-store.md#store-http-binary-cache-store-parallel-compression) store 设置默认为 `true`（对于 `xz` 等其他压缩算法仍为 `false`）。
  设置 `?parallel-compression=false` 可选择退出。

- 二进制缓存上传获得更多并行度 [#15957](https://github.com/NixOS/nix/pull/15957)

  NAR 的上传现在不必等待所有引用上传完毕即可开始。
  此外，NAR 现在按（解压后）NAR 大小降序上传。
  闭包不变性仍通过以拓扑排序的顺序复制 `.narinfo` 来维护。

- derivation 构建调度器的内存占用降低与性能改进 [#15611](https://github.com/NixOS/nix/pull/15611) [#15695](https://github.com/NixOS/nix/pull/15695)

  derivation 构建调度器的内存占用得到改进，以允许更多的状态共享。
  导致构建/substitute 任务调度出现平方复杂度的低效问题已被解决。
  调度资源现在更节约地分配并更早地释放，以降低峰值消耗。

  这些改进使得典型工作负载下 `nix-daemon` 的内存占用降低约 2-8 倍，在更大的 derivation 图中效果更明显，其中不包括 substitute 期间使用的短生命周期分配。

  值得注意的是，当前构建调度器架构在 Linux 上会随着堆的增大而按比例变慢，因为 derivation "builder" 进程是直接从 Nix 进程 `fork` 出来的，这会在 `fork` 期间阻塞 builder 事件循环。因此，`nix-daemon` 更小的堆意味着更快的构建启动。

- 相同输入的并发路径 substitute 与求值期抓取现在只会运行一次 [#15555](https://github.com/NixOS/nix/pull/15555) [#15644](https://github.com/NixOS/nix/pull/15644)

  这避免了多个 Nix 进程并发尝试 substitute/下载同一资源时的冗余工作。

- 二进制缓存中的 `.narinfo` 查询更具并发性

  在二进制缓存中查询存在性与路径元数据的操作现在更加异步。像 `nix path-info` 这样针对大型闭包的操作更快、更高效。
  构建调度器事件循环现在不再阻塞在 `.narinfo` 查询上，这提升了使用 passthru 二进制缓存时的性能。

## 修复

- 修复带自引用的存储路径与其清零等价物之间的哈希碰撞 [#15837](https://github.com/NixOS/nix/issues/15837) [#15931](https://github.com/NixOS/nix/pull/15931)

  在计算带自引用的 NAR 的哈希时，Nix 会将自引用清零，但同时对它们的位置做哈希。
  后者在 Nix 2.17.0 中被意外丢失，这意味着一个带自引用的 NAR 可能与另一个内容完全相同但部分自引用被清零的 NAR 哈希出相同的存储路径。

  本版本恢复了对自引用位置做哈希。
  其结果是，由带自引用的 NAR 得到的内容寻址存储路径将与 Nix 2.17 至 2.34 产生的不同。
  这会影响实验性 `ca-derivations` 特性的用户，以及 `nix store make-content-addressed` 的用户。

- C API：修复传递给 primop 回调的 `EvalState` 指针 [#15300](https://github.com/NixOS/nix/pull/15300) [#15383](https://github.com/NixOS/nix/pull/15383)

  传递给 C API primop 回调的 `EvalState *` 错误地指向内部的 `nix::EvalState`，而不是 C API 包装结构体。
  当回调将该指针与 `nix_alloc_value()` 等 C API 函数一起使用时，会导致段错误。
  同样的问题也影响了外部值的 `printValueAsJSON` 和 `printValueAsXML` 回调。

- GitHub 抓取器现在校验 URL 参数 [#15304](https://github.com/NixOS/nix/issues/15304) [#15331](https://github.com/NixOS/nix/pull/15331)

  `github:` 抓取器现在会校验 URL 参数，如果提供了像 `tag` 这样的无效参数将会报错。

- 修复 keep-outputs 和 keep-derivations 可能干扰删除命令的 bug [#15776](https://github.com/NixOS/nix/pull/15776)

  之前，将 [`keep-derivations`](@docroot@/command-ref/conf-file.md#conf-keep-derivations) 设为 `true` 并尝试删除一个已实现（realised）输出的 derivation 会失败。
  [`keep-outputs`](@docroot@/command-ref/conf-file.md#conf-keep-outputs) 同理，尝试删除一个仍有 derivers 的输出也会失败。
  这些选项不再影响删除命令，文档也相应更新。

- S3 substituter 在 STS WebIdentity 认证时回退到 URL 中的 region [#15594](https://github.com/NixOS/nix/pull/15594)

  通过 STS WebIdentity（EKS IRSA、GitHub Actions OIDC）向 S3 二进制缓存认证时，如果既未设置 `AWS_REGION` 也未设置 `AWS_DEFAULT_REGION`，Nix 现在会使用 S3 URL 中的 `?region=` 参数作为 STS 端点 region 的回退值。
  之前，导出了 `AWS_WEB_IDENTITY_TOKEN_FILE` 和 `AWS_ROLE_ARN` 但未导出 region 的 IRSA 配置会因一条误导性的 "IMDS provider" 错误而失败。

- S3：恢复 STS WebIdentity 与 ECS 容器凭证提供者 [#15507](https://github.com/NixOS/nix/pull/15507)

  Nix 2.33 将 S3 后端的 `aws-sdk-cpp` 凭证链替换为基于 `aws-c-auth` 构建的自定义凭证链。
  该链遗漏了两个提供者，破坏了容器工作负载中的 S3 二进制缓存访问：

  - **STS WebIdentity**（`AWS_WEB_IDENTITY_TOKEN_FILE`、`AWS_ROLE_ARN`、`AWS_ROLE_SESSION_NAME`）——被 EKS IRSA、GitHub Actions OIDC 以及任何 `sts:AssumeRoleWithWebIdentity` 联合认证使用。
  - **ECS 容器元数据**（`AWS_CONTAINER_CREDENTIALS_RELATIVE_URI`、`AWS_CONTAINER_CREDENTIALS_FULL_URI`）——被 ECS 任务和 EKS Pod Identity 使用。

  典型症状是一条误导性的 IMDS 错误（`Valid credentials could not be sourced by the IMDS provider`），因为 IMDS 是在正确的提供者被跳过之后最后尝试的提供者。

  这两个提供者现在都已加入凭证链，顺序与 2.33 之前的行为一致。
  与新旧 AWS SDK 的默认凭证链一样，ECS 与 IMDS 互斥：当设置了容器凭证环境变量时，会跳过 IMDS。

- 来自二进制缓存的 HTTP 401 和 407 响应不再被视为文件缺失 [#15877](https://github.com/NixOS/nix/pull/15877)

  Nix 不再将 `Unauthorized` 和 `Proxy Authentication Required` HTTP 状态码视为文件缺失的标志。之所以曾经如此，是因为 AWS S3 对不可列举桶中的缺失对象返回 403 `Forbidden`。401/407 被意外地包含进来，现在该变通处理被严格限定为 403 响应。

- 修复 Linux 构建沙箱在不支持用户命名空间时 `/etc/group` 中的 `nixbld` gid [#15131](https://github.com/NixOS/nix/pull/15131)

- store 垃圾回收现在更加健壮 [#15992](https://github.com/NixOS/nix/pull/15992) [#15720](https://github.com/NixOS/nix/pull/15720) [#15616](https://github.com/NixOS/nix/pull/15616)

- 修复哈希不匹配的 fixed-output derivation 的死锁 [#15874](https://github.com/NixOS/nix/pull/15874)

- `nix-copy-closure` 不再忽略 `--include-outputs` 标志 [#15896](https://github.com/NixOS/nix/pull/15896)

- 修复 `recursive-nix` 实验性特性

  在本版本之前，实现该特性所用的内部数据结构没有以线程安全的方式使用。
  处理 daemon 连接的线程现在会被及时回收，修复了资源泄漏。

## Contributors（贡献者）

本版本得益于以下 59 位贡献者：

- Michael Wang [**(@zwang20)**](https://github.com/zwang20)
- Amaan Qureshi [**(@amaanq)**](https://github.com/amaanq)
- Sergei Zimmerman [**(@xokdvium)**](https://github.com/xokdvium)
- Reuben Gardos Reid [**(@ReubenJ)**](https://github.com/ReubenJ)
- StepBroBD [**(@stepbrobd)**](https://github.com/stepbrobd)
- dram [**(@dramforever)**](https://github.com/dramforever)
- Tom [**(@thunze)**](https://github.com/thunze)
- Sergei Trofimovich [**(@trofi)**](https://github.com/trofi)
- Robert Hensing [**(@roberth)**](https://github.com/roberth)
- steveoliphant [**(@steveoliphant)**](https://github.com/steveoliphant)
- espes [**(@espes)**](https://github.com/espes)
- Jörg Thalheim [**(@Mic92)**](https://github.com/Mic92)
- Artemis Tosini [**(@artemist)**](https://github.com/artemist)
- sander [**(@sandydoo)**](https://github.com/sandydoo)
- Erik Jensen [**(@rkjnsn)**](https://github.com/rkjnsn)
- Cameron Will [**(@cwill747)**](https://github.com/cwill747)
- Maciej Krüger [**(@mkg20001)**](https://github.com/mkg20001)
- Dror Speiser [**(@drorspei)**](https://github.com/drorspei)
- Eveeifyeve [**(@Eveeifyeve)**](https://github.com/Eveeifyeve)
- Audrey Dutcher [**(@rhelmot)**](https://github.com/rhelmot)
- Lisanna Dettwyler [**(@lisanna-dettwyler)**](https://github.com/lisanna-dettwyler)
- TyIsI [**(@TyIsI)**](https://github.com/TyIsI)
- Adam Kliś [**(@BonusPlay)**](https://github.com/BonusPlay)
- Domen Kožar [**(@domenkozar)**](https://github.com/domenkozar)
- Taeer Bar-Yam [**(@Radvendii)**](https://github.com/Radvendii)
- ryota2357 [**(@ryota2357)**](https://github.com/ryota2357)
- LIN, Jian [**(@jian-lin)**](https://github.com/jian-lin)
- znmz [**(@znmz)**](https://github.com/znmz)
- Felix Stupp [**(@Zocker1999NET)**](https://github.com/Zocker1999NET)
- Johannes Kirschbauer [**(@hsjobeki)**](https://github.com/hsjobeki)
- Antonio Nuno Monteiro [**(@anmonteiro)**](https://github.com/anmonteiro)
- tomberek [**(@tomberek)**](https://github.com/tomberek)
- Eelco Dolstra [**(@edolstra)**](https://github.com/edolstra)
- adisbladis [**(@adisbladis)**](https://github.com/adisbladis)
- Luna Nova [**(@LunNova)**](https://github.com/LunNova)
- Riccardo Mazzarini [**(@noib3)**](https://github.com/noib3)
- Bouke van der Bijl [**(@bouk)**](https://github.com/bouk)
- Dario [**(@dve00)**](https://github.com/dve00)
- Michael Hoang [**(@Enzime)**](https://github.com/Enzime)
- Paul Sbarra [**(@tones111)**](https://github.com/tones111)
- edef [**(@edef1c)**](https://github.com/edef1c)
- Adam Dinwoodie [**(@me-and)**](https://github.com/me-and)
- Brian McKenna [**(@puffnfresh)**](https://github.com/puffnfresh)
- Jeremy Fleischman [**(@jfly)**](https://github.com/jfly)
- John Ericson [**(@Ericson2314)**](https://github.com/Ericson2314)
- Alex Ionescu [**(@aionescu)**](https://github.com/aionescu)
- Tristan Ross [**(@RossComputerGuy)**](https://github.com/RossComputerGuy)
- Bernardo Meurer [**(@lovesegfault)**](https://github.com/lovesegfault)
- Pierre Penninckx [**(@ibizaman)**](https://github.com/ibizaman)
- Leonard Sheng Sheng Lee [**(@sheeeng)**](https://github.com/sheeeng)
- rszyma [**(@rszyma)**](https://github.com/rszyma)
- Ryan Hendrickson [**(@rhendric)**](https://github.com/rhendric)
- Lennart Kolmodin [**(@kolmodin)**](https://github.com/kolmodin)
- zowoq [**(@zowoq)**](https://github.com/zowoq)
- Peter Collingbourne [**(@pcc)**](https://github.com/pcc)
- Simon Žlender [**(@szlend)**](https://github.com/szlend)
- Lily Foster [**(@lilyinstarlight)**](https://github.com/lilyinstarlight)
- randomizedcoder [**(@randomizedcoder)**](https://github.com/randomizedcoder)
- Krish Jaiswal
