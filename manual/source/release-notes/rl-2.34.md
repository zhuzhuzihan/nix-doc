# Release 2.34.0 (2026-02-27)

## Highlights（亮点）

- Rust 版 nix-installer 进入 beta

  基于重写的 Rust 版 Nix 安装器现已进入 beta 阶段。
  我们非常期待大家帮忙测试！

  要试用新安装器，请运行：
  ```
  curl -sSfL https://artifacts.nixos.org/nix-installer | sh -s -- install
  ```

  即使你已经存在一个基于脚本的 Nix 安装，该安装器也可以不加任何调整直接运行。

  这个新安装器还支持卸载你的 Nix 安装；运行：
  ```
  /nix/nix-installer uninstall
  ```

  这会移除你的整个 Nix 安装（即使你是在已有的基于脚本的安装之上安装的）。

  该安装器是 Determinate Systems 的 [Determinate Nix Installer](https://github.com/DeterminateSystems/nix-installer) 的修改版本。
  感谢 Determinate Systems 在该安装器上投入的所有心血。

  安装器源码位于 <https://github.com/NixOS/nix-installer>。
  任何问题请在该仓库中报告。

  对于 CI 使用场景，可以在 <https://github.com/NixOS/nix-installer-action> 找到使用该安装器安装 Nix 的 GitHub Action。

- `no-url-literals` 实验性特性稳定化，以及新的诊断基础设施，引入 `lint-url-literals`、`lint-short-path-literals` 和 `lint-absolute-path-literals` 设置 [#8738](https://github.com/NixOS/nix/issues/8738) [#10048](https://github.com/NixOS/nix/issues/10048) [#10281](https://github.com/NixOS/nix/issues/10281) [#15326](https://github.com/NixOS/nix/pull/15326)

  实验性特性 `no-url-literals` 已被稳定化，现在由 `lint-url-literals` 选项控制。
  同时新增了一套诊断基础设施，用于对不推荐使用的语言特性进行 lint 检查。

  ### 新的 lint 基础设施

  #### [`lint-url-literals`](@docroot@/command-ref/conf-file.md#conf-lint-url-literals)

  `no-url-literals` 实验性特性已被稳定化，并替换为新的 [`lint-url-literals`](@docroot@/command-ref/conf-file.md#conf-lint-url-literals) 设置。

  要从该实验性特性迁移，请将：
  ```
  experimental-features = no-url-literals
  ```
  替换为：
  ```
  lint-url-literals = fatal
  ```

  #### [`lint-short-path-literals`](@docroot@/command-ref/conf-file.md#conf-lint-short-path-literals)

  布尔设置 [`warn-short-path-literals`](@docroot@/command-ref/conf-file.md#conf-warn-short-path-literals) 已被弃用，替换为 [`lint-short-path-literals`](@docroot@/command-ref/conf-file.md#conf-lint-short-path-literals)。

  要迁移，请将：
  ```
  warn-short-path-literals = true
  ```
  替换为：
  ```
  lint-short-path-literals = warn
  ```

  #### [`lint-absolute-path-literals`](@docroot@/command-ref/conf-file.md#conf-lint-absolute-path-literals)

  新增了 [`lint-absolute-path-literals`](@docroot@/command-ref/conf-file.md#conf-lint-absolute-path-literals) 设置，用于控制对绝对路径字面量（以 `/` 开头的路径）和家目录路径字面量（以 `~/` 开头的路径）的处理方式。

  #### 设置取值

  这三个设置均接受三种取值：
  - `ignore`：允许使用该特性且不产生任何诊断信息（默认值）
  - `warn`：使用该特性时发出警告
  - `fatal`：将使用该特性视为解析错误

  默认值在未来的版本中可能会变化。

- 改进了解析器错误信息 [#15092](https://github.com/NixOS/nix/pull/15092)

  解析器错误信息现在使用可读的字符串来表示 token，而不是内部名称。例如，格式错误的表达式 `a ++ ++ b` 现在产生如下错误：
  ```
  error: syntax error, unexpected '++'
       at «string»:1:6:
            1| a ++ ++ b
             |      ^
  ```

  而不再是：
  ```
  error: syntax error, unexpected CONCAT
       at «string»:1:6:
            1| a ++ ++ b
             |      ^
  ```

## 新特性

- `nix repl` 现在支持 `inherit` 和一行多个绑定 [#15082](https://github.com/NixOS/nix/pull/15082)

  `nix repl` 现在支持 `inherit` 语句以及一行写多个绑定：

  ```
  nix-repl> a = { x = 1; y = 2; }
  nix-repl> inherit (a) x y
  nix-repl> x + y
  3

  nix-repl> p = 1; q = 2;
  nix-repl> p + q
  3

  nix-repl> foo.bar.baz = 1;
  nix-repl> foo.bar
  { baz = 1; }
  ```

- 新命令 `nix store roots-daemon` 用于提供 GC roots 服务 [#15143](https://github.com/NixOS/nix/pull/15143)

  新命令 [`nix store roots-daemon`](@docroot@/command-ref/new-cli/nix3-store-roots-daemon.md) 运行一个 daemon（守护进程），通过 Unix domain socket 对外提供垃圾回收器 roots 服务。
  它使得垃圾回收器可以在主 Nix daemon 没有 `CAP_SYS_PTRACE` 能力、因而无法扫描 `/proc` 的情况下发现运行时 roots。

  可以通过 [`use-roots-daemon`](@docroot@/store/types/local-store.md#store-local-store-use-roots-daemon) store 设置将垃圾回收器配置为使用该 daemon。

  该特性需要启用 [`local-overlay-store` 实验性特性](@docroot@/development/experimental-features.md#xp-feature-local-overlay-store)。

- `libexec` 中新增命令 `nix-nswrapper` [#15183](https://github.com/NixOS/nix/pull/15183)

  新命令 `libexec/nix-nswrapper` 用于在 Linux 上以非特权用户命名空间运行 Nix daemon。要使用该命令，必须在 `/etc/subuid` 和 `/etc/subgid` 中分配构建用户 UID 和 GID。

  它可以用于以完整沙箱方式运行 Nix daemon，而无需以 root 身份执行。Nixpkgs 已通过新的 `nix.daemonUser` 和 `nix.daemonGroup` 设置提供了支持。

- 本地 store 新增设置 `ignore-gc-delete-failure` [#15054](https://github.com/NixOS/nix/pull/15054)

  新增了本地 store 设置 [`ignore-gc-delete-failure`](@docroot@/store/types/local-store.md#store-local-store-ignore-gc-delete-failure)。
  启用后，垃圾回收在无法删除存储路径时会记录警告而不是失败。
  这对以非特权用户运行 Nix（可能对 store 中的部分路径没有写权限）的场景很有用。

  该设置为实验性，需要启用 [`local-overlay-store`](@docroot@/development/experimental-features.md#xp-feature-local-overlay-store) 实验性特性。

- 新设置 `narinfo-cache-meta-ttl` [#15287](https://github.com/NixOS/nix/pull/15287)

  新设置 `narinfo-cache-meta-ttl` 控制二进制缓存元数据（即 `/nix-cache-info`）在本地缓存的时长（以秒为单位）。此前该值被硬编码为 7 天，这仍是默认值。因此，你现在可以使用 `nix store info --refresh` 来检查某个二进制缓存是否仍然有效。

- 支持使用 mTLS（客户端证书）认证的 HTTPS 二进制缓存 [#13002](https://github.com/NixOS/nix/issues/13002) [#13030](https://github.com/NixOS/nix/pull/13030)

  在 substituter URL 中增加了对 `tls-certificate` 和 `tls-private-key` 选项的支持。

  示例：

  ```
  https://substituter.invalid?tls-certificate=/path/to/cert.pem&tls-private-key=/path/to/key.pem
  ```

  配置这些选项后，Nix 将使用该证书/私钥对向服务器进行认证。

- `nix store gc --dry-run` 和 `nix-collect-garbage --dry-run` 现在会报告将被释放的路径数量 [#15229](https://github.com/NixOS/nix/pull/15229) [#5704](https://github.com/NixOS/nix/issues/5704)

## 性能改进

- 解包 tarball 到 `~/.cache/nix/tarball-cache-v2` 现在是多线程的 [#12087](https://github.com/NixOS/nix/pull/12087)

  `builtins.fetchTarball` 和基于 tarball 的 Flakes 输入（例如 `github:NixOS/nixpkgs`、`https://channels.nixos.org/nixos-25.11/nixexprs.tar.xz`）的内容寻址缓存现在会并发地将 git blob（文件）写入 `tarball-cache-v2` 仓库，这显著缩短了 tarball 解包的挂钟时间（在我们的测试中，`https://channels.nixos.org/nixos-25.11/nixexprs.tar.xz` 的解包速度提升至约 1.8 倍）。

  目前，Nix 尚未对 `~/.cache/nix/tarball-cache-v2` 仓库执行任何维护，这将在未来的版本中解决。希望回收 tarball 缓存占用磁盘空间的用户可以运行：

  ```
  rm -rf ~/.cache/nix/tarball-cache # Historical tarball-cache, not used by Nix >= 2.33
  cd ~/.cache/nix/tarball-cache-v2 && git multi-pack-index write && git multi-pack-index repack && git multi-pack-index expire
  ```

- `nix nar ls` 及其他 NAR 列举操作得到进一步优化 [#15163](https://github.com/NixOS/nix/pull/15163)

- 求值器热路径优化 [#15270](https://github.com/NixOS/nix/pull/15270) [#15271](https://github.com/NixOS/nix/pull/15271)

## C API 变更

- 新增 store API 方法 [#14766](https://github.com/NixOS/nix/pull/14766) [#14768](https://github.com/NixOS/nix/pull/14768)

  C API 现在包含以下额外的方法：

  - `nix_store_query_path_from_hash_part()` - 根据存储路径的 hash 部分获取完整存储路径
  - `nix_store_copy_path()` - 在两个 store 之间复制单个存储路径，支持修复模式以及配置签名检查

- 从你自己的 primop 返回的错误默认不再被视为可恢复 [#13930](https://github.com/NixOS/nix/pull/13930) [#15286](https://github.com/NixOS/nix/pull/15286)

  Nix 2.34 默认会在触发错误的 thunk 中记住该错误。

  之前以下事件序列是可以工作的：

  1. 有一个 thunk 调用了一个通过 C API 定义的 primop
  2. 该 primop 返回错误
  3. 再次强制求值该 thunk
  4. 该 primop 返回一个值
  5. 该 thunk 求值成功

  **解决办法**

  依赖此行为的 C API 使用方必须修改其可恢复错误调用：

  ```diff
  -nix_set_err_msg(context, NIX_ERR_*, msg);
  +nix_set_err_msg(context, NIX_ERR_RECOVERABLE, msg);
  ```

## 修复

- 避免使用 `ssh-ng://` store 复制存储路径时断开 ssh 连接 [#14998](https://github.com/NixOS/nix/pull/14998) [#6950](https://github.com/NixOS/nix/issues/6950)

  由于 Nix 处理 Boost.Coroutine2 挂起与恢复时存在一个 bug，从 `ssh-ng://` store 复制时每复制一个路径都会断开 SSH 连接。该问题已修复，通过避免多次 SSH/Nix Worker Protocol 握手提升了性能。

- S3 二进制缓存现在默认使用 virtual-hosted-style 寻址 [#15208](https://github.com/NixOS/nix/issues/15208) [#15216](https://github.com/NixOS/nix/pull/15216)

  连接标准 AWS S3 端点时，S3 二进制缓存现在使用
  virtual-hosted-style URL（`https://bucket.s3.region.amazonaws.com/key`）
  而不是 path-style URL（`https://s3.region.amazonaws.com/bucket/key`）。
  这启用了 HTTP/2 多路复用，并修复了高并发工作负载下的 TCP 连接
  耗尽问题（TIME_WAIT socket 堆积）。

  新的 `addressing-style` store 选项控制该行为：

  - `auto`（默认值）：标准 AWS 端点使用 virtual-hosted-style，自定义端点使用
    path-style。
  - `path`：强制使用 path-style 寻址（已被 AWS 弃用）。
  - `virtual`：强制使用 virtual-hosted-style 寻址（桶名不得包含点号）。

  包含点号的桶名（例如 `my.bucket.name`）在 `auto` 模式下会自动回退到
  path-style 寻址，因为带点号的名称会创建多级子域名，破坏 TLS 通配符
  证书校验。

  为向后兼容而使用 path-style 的示例：

  ```
  s3://my-bucket/key?region=us-east-1&addressing-style=path
  ```

  此外，所有 HTTP 连接现在都启用了 TCP keep-alive，防止空闲连接被中间
  网络设备（NAT、防火墙、负载均衡器）静默断开。

- `nix-prefetch-url --unpack` 现在会正确检查空压缩包 [#15242](https://github.com/NixOS/nix/pull/15242)

  之前的版本未能检查空压缩包，在解包空压缩包时会因 `nullptr` 解引用而崩溃。
  该问题现已修复。

- 防止在使用构建用户的本地 store 中构建时，Nix 被 `SIGKILL` 杀死后产生失控进程 [#15193](https://github.com/NixOS/nix/pull/15193)

  以 root 运行时，Nix 不通过 daemon 执行构建，而是由自己作为 fork 出的构建进程的父进程。之前的 Nix 版本未能在 `setuid` 调用之间保留 `PR_SET_PDEATHSIG` 父进程死亡信号。这可能导致构建进程被重新挂载到其他父进程并在后台继续运行。该问题已修复。

- 修复在 `--log-format internal-json` 期间中断时的崩溃 [#15335](https://github.com/NixOS/nix/pull/15335)

  在 `--log-format internal-json`（[nix-output-monitor](https://github.com/maralorn/nix-output-monitor) 使用）期间按下 Ctrl-C 不再导致虚假的 "Nix crashed. This is a bug." 报告。

- 修复 `file://` 和 `local://` store URI 中的百分号编码问题 [#15280](https://github.com/NixOS/nix/pull/15280)

  路径中含有 `+` 等特殊字符的 store URI（例如 `file:///tmp/a+b`）不再错误地创建百分号编码的目录（例如 `/tmp/a%2Bb`）。

- 修复 `nix repl` 中 Tab 补全时的崩溃 [#15255](https://github.com/NixOS/nix/pull/15255)

- 修复 macOS 上的 "Too many open files" 问题 [#15205](https://github.com/NixOS/nix/pull/15205)

  Nix 现在会在启动时将打开文件软限制提升到硬限制，修复了 macOS 上默认软限制较低导致的 "Too many open files" 错误。

- 当 `inputs.nixpkgs` 设置了 `flake = false` 时，`nix develop` 不再失败 [#15175](https://github.com/NixOS/nix/pull/15175)

- `builtins.flakeRefToString` 不再报 "attribute is a thunk" 错误 [#15160](https://github.com/NixOS/nix/pull/15160)

- 修复 daemon 中 `QueryPathInfo` 对无效路径抛出异常的问题 [#15134](https://github.com/NixOS/nix/pull/15134)

- `nix-store --generate-binary-cache-key` 现在会对密钥文件执行 fsync 以防止损坏 [#15107](https://github.com/NixOS/nix/pull/15107)

- 修复 `nix.conf` 中的 `build-hook` 设置被忽略的问题 [#15083](https://github.com/NixOS/nix/pull/15083)

- 修复因依赖失败而取消构建时的空错误信息 [#14972](https://github.com/NixOS/nix/pull/14972)

  当某个构建失败且未使用 `--keep-going` 时，其他进行中的构建会被取消。之前，这些被取消的构建会被错误地报告为失败且错误信息为空。这影响了 `buildPathsWithResults` 的调用方，例如 `nix flake check`。

## 杂项

- Content-Encoding 解压缩现在由 libcurl 处理 [#14324](https://github.com/NixOS/nix/issues/14324) [#15336](https://github.com/NixOS/nix/pull/15336)

  对带有 `Content-Encoding` 头的 HTTP 下载的透明解压缩现在使用 libcurl。这增加了对之前已声明但不支持的 `deflate` 编码以及已弃用的 `x-gzip` 别名的支持。
  之前已声明的非标准 `xz`、`bzip2` 编码不再受支持，因为它们在现实中并不常见，合规的服务器也不应发送它们。

  `br`、`zstd`、`gzip` 继续受支持。发行版打包应确保 `libcurl` 依赖链接了支持这些编码所需的库。构建系统现在默认要求 libcurl >= 8.17.0，据所知该版本没有[暂停与解压缩](https://github.com/curl/curl/issues/16280)相关的问题。

- 静态构建现在支持 S3 特性（`libstore:s3-aws-auth` meson 选项）[#15076](https://github.com/NixOS/nix/pull/15076)

- 改进了与 derivation（派生）相关的错误信息 [#15349](https://github.com/NixOS/nix/pull/15349)

  存储路径上下文现在以面向用户的 `hash^out` 格式渲染，而不是内部使用的 `!out!hash` 格式。
  修复了 `nix-env` 中一条误导性的错误信息，它错误地将问题归咎于内容寻址的 derivation。

- 改进了空 derivation 文件的错误信息 [#15298](https://github.com/NixOS/nix/pull/15298)

  解析空的 `.drv` 文件（例如由于非正常关机导致的 store 损坏）现在会产生一条清晰的错误信息，而不是晦涩的 `expected string 'D'`。

- tarball 的相对 `file:` 路径现在会被拒绝并给出清晰的错误 [#14983](https://github.com/NixOS/nix/pull/14983)

- Windows 移植持续取得进展，包括构建修复、CI 改进和平台抽象。

- Nix docker 镜像现在作为发布流程的一部分被上传到 [GHCR](https://github.com/NixOS/nix/pkgs/container/nix)

  历史上，只有 `amd64` docker 镜像的预发布构建被上传到 ghcr.io，且 `latest` 标签指向 `master` 分支上最后构建的镜像。此问题已修复；今后，<https://github.com/NixOS/nix/pkgs/container/nix> 将包含与 <https://hub.docker.com/r/nixos/nix/> 相同的镜像，这些镜像由 [Hydra](https://hydra.nixos.org/project/nix) 为 [arm64](https://hydra.nixos.org/job/nix/maintenance-2.34/dockerImage.aarch64-linux) 和 [amd64](https://hydra.nixos.org/job/nix/maintenance-2.34/dockerImage.x86_64-linux) 构建。预发布版本不再被推送到 registry。

## Contributors（贡献者）

本版本得益于以下 43 位贡献者：

- Taeer Bar-Yam [**(@Radvendii)**](https://github.com/Radvendii)
- Sergei Zimmerman [**(@xokdvium)**](https://github.com/xokdvium)
- Jörg Thalheim [**(@Mic92)**](https://github.com/Mic92)
- Graham Dennis [**(@GrahamDennis)**](https://github.com/GrahamDennis)
- Damien Diederen [**(@ztzg)**](https://github.com/ztzg)
- koberbe-jh [**(@koberbe-jh)**](https://github.com/koberbe-jh)
- Robert Hensing [**(@roberth)**](https://github.com/roberth)
- Bouke van der Bijl [**(@bouk)**](https://github.com/bouk)
- Lisanna Dettwyler [**(@lisanna-dettwyler)**](https://github.com/lisanna-dettwyler)
- kiara [**(@KiaraGrouwstra)**](https://github.com/KiaraGrouwstra)
- Side Effect [**(@YawKar)**](https://github.com/YawKar)
- dram [**(@dramforever)**](https://github.com/dramforever)
- tomf [**(@tomfitzhenry)**](https://github.com/tomfitzhenry)
- Kamil Monicz [**(@Zaczero)**](https://github.com/Zaczero)
- Cosima Neidahl [**(@OPNA2608)**](https://github.com/OPNA2608)
- Siddhant Kumar [**(@siddhantk232)**](https://github.com/siddhantk232)
- Jens Petersen [**(@juhp)**](https://github.com/juhp)
- Johannes Kirschbauer [**(@hsjobeki)**](https://github.com/hsjobeki)
- tomberek [**(@tomberek)**](https://github.com/tomberek)
- Eelco Dolstra [**(@edolstra)**](https://github.com/edolstra)
- Artemis Tosini [**(@artemist)**](https://github.com/artemist)
- David McFarland [**(@corngood)**](https://github.com/corngood)
- Tucker Shea [**(@NoRePercussions)**](https://github.com/NoRePercussions)
- Connor Baker [**(@ConnorBaker)**](https://github.com/ConnorBaker)
- Cole Helbling [**(@cole-h)**](https://github.com/cole-h)
- Eveeifyeve [**(@Eveeifyeve)**](https://github.com/Eveeifyeve)
- John Ericson [**(@Ericson2314)**](https://github.com/Ericson2314)
- Graham Christensen [**(@grahamc)**](https://github.com/grahamc)
- Ilja [**(@iljah)**](https://github.com/iljah)
- Pol Dellaiera [**(@drupol)**](https://github.com/drupol)
- steelman [**(@steelman)**](https://github.com/steelman)
- Brian McKenna [**(@puffnfresh)**](https://github.com/puffnfresh)
- JustAGuyTryingHisBest [**(@JustAGuyTryingHisBest)**](https://github.com/JustAGuyTryingHisBest)
- zowoq [**(@zowoq)**](https://github.com/zowoq)
- Agustín Covarrubias [**(@agucova)**](https://github.com/agucova)
- Sergei Trofimovich [**(@trofi)**](https://github.com/trofi)
- Bernardo Meurer [**(@lovesegfault)**](https://github.com/lovesegfault)
- Peter Bynum [**(@pkpbynum)**](https://github.com/pkpbynum)
- Amaan Qureshi [**(@amaanq)**](https://github.com/amaanq)
- Michael Hoang [**(@Enzime)**](https://github.com/Enzime)
- Michael Daniels [**(@mdaniels5757)**](https://github.com/mdaniels5757)
- Matthew Kenigsberg [**(@mkenigs)**](https://github.com/mkenigs)
- Shea Levy [**(@shlevy)**](https://github.com/shlevy)
