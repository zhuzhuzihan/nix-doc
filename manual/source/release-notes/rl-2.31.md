# Release 2.31.0 (2025-08-21)

- `build-cores = 0` 现在会自动检测 CPU 核心数 [#13402](https://github.com/NixOS/nix/pull/13402)

  当 `build-cores` 设置为 `0` 时，Nix 现在会自动检测可用的 CPU 核心数，并通过 `NIX_BUILD_CORES` 传递该值，而不是直接传递 `0`。这与未设置 `build-cores` 时的行为一致。这避免了构建器不得不自行检测核心数。

- 修复 Git LFS SSH 问题 [#13337](https://github.com/NixOS/nix/issues/13337) [#13743](https://github.com/NixOS/nix/pull/13743)

  修复了 Git LFS 与 SSH 相关的一些遗留问题。

  * 新增对 `NIX_SSHOPTS` 的支持。
  * 正确使用从 URL 中解析出的端口。
  * 在 API 未暴露在 443 端口时，更好地利用 `git-lfs-authenticate` 的响应来确定 API 端点。

- 在 store URI 中支持 `user@address:port` 语法 [#7044](https://github.com/NixOS/nix/issues/7044) [#3425](https://github.com/NixOS/nix/pull/3425)

  现在可以按照 [RFC3986](https://datatracker.ietf.org/doc/html/rfc3986) 直接在 store URL 中指定 SSH store 所使用的端口。此前指定自定义端口的唯一方式是通过 `ssh_config` 或 `NIX_SSHOPTS` 环境变量，因为 Nix 此前错误地将端口号连同主机名一起传给了 SSH 可执行文件。

  此变更影响在 CLI 中通过 `--store` 及类似标志传递的 [store 引用](@docroot@/store/types/index.md#store-url-format)，以及[远程构建器](@docroot@/command-ref/conf-file.md#conf-builders)的配置。例如，以下 store URI 现在均可正常工作：

  - `ssh://127.0.0.1:2222`
  - `ssh://[b573:6a48:e224:840b:6007:6275:f8f7:ebf3]:22`
  - `ssh-ng://[b573:6a48:e224:840b:6007:6275:f8f7:ebf3]:22`

- 按照 RFC6874 表示 IPv6 RFC4007 ZoneId 字面量 [#13445](https://github.com/NixOS/nix/pull/13445)

  自 [#4646](https://github.com/NixOS/nix/pull/4646) 以来，Nix 的早期版本接受 URI 中的 [IPv6 作用域地址](https://datatracker.ietf.org/doc/html/rfc4007)（如 [store 引用](@docroot@/store/types/index.md#store-url-format)）以字面百分号字符表示的文本形式：`[fe80::1%18]`。这是有歧义的，因为百分号字面量 `%` 被 [RFC3986](https://datatracker.ietf.org/doc/html/rfc3986) 保留用于指示百分号编码。Nix 现在要求将百分号 `%` 符号百分号编码为 `%25`。这实现了 [RFC6874](https://datatracker.ietf.org/doc/html/rfc6874)，它定义了 URI 中区域标识符（zone identifier）的表示方式。上面示例中的地址现在必须写成 `[fe80::1%2518]`。

- 为 SQLite 缓存数据库启用 WAL 模式 [#13800](https://github.com/NixOS/nix/pull/13800)

  此前，Nix 对缓存使用 SQLite 的 "truncate" 模式。然而，当另一个进程正在更新缓存时，这可能导致某个 Nix 进程被阻塞。这对 flake 求值缓存来说尤其是个问题，因为它使用长时间运行的事务。因此，操作同一 flake 的并发 Nix 命令可能被阻塞任意长的时间。WAL 模式避免了这个问题。

  此变更要求更新 SQLite 缓存的版本。例如，`eval-cache-v5.sqlite` 现在变为 `eval-cache-v6.sqlite`。

- 在 bdwgc 中启用并行标记 [#13708](https://github.com/NixOS/nix/pull/13708)

  此前标记（marking）只由单个线程完成，当堆变大时耗时很长。启用并行标记大幅加速了求值，例如（在 Ryzen 9 5900X 12 核上）：

  * `nix search nixpkgs` 从 24.3 秒降到 18.9 秒。
  * 对 `NixOS/nix/2.21.2` flake 回归测试的求值从 86.1 秒降到 71.2 秒。

- 新命令 `nix flake prefetch-inputs` [#13565](https://github.com/NixOS/nix/pull/13565)

  该命令并行抓取一个 flake 的所有输入。这比常规 flake 求值期间串行的按需抓取快得多。缺点是它可能会抓取一些通常不会用到的输入。

- 新增 `warn-short-path-literals` 设置 [#13489](https://github.com/NixOS/nix/pull/13489)

  启用该设置后，当 Nix 遇到不以 `.` 或 `/` 开头的相对路径字面量时会发出警告，例如建议将 `foo/bar` 改写为 `./foo/bar`。

- 更新锁文件时尊重输入自身的锁文件 [#13437](https://github.com/NixOS/nix/pull/13437)

  例如，如果一个 flake 对 `a` 和 `a/b` 都持有锁，而我们修改了 `a` 的 flakeref，此前 Nix 会抓取 `b` 的最新版本，而不是使用 `a` 中对 `b` 的锁。

- 实现使用 SHA-256 的 Git 哈希支持 [#13543](https://github.com/NixOS/nix/pull/13543)

  [Git 哈希](@docroot@/development/experimental-features.md#xp-feature-git-hashing) store 对象的实验性支持现在不仅支持 SHA-1，也支持 SHA-256，与上游 Git 保持一致。

## Contributors（贡献者）

本次发布由以下 34 位贡献者共同完成：

- John Soo [**(@jsoo1)**](https://github.com/jsoo1)
- Alan Urmancheev [**(@alurm)**](https://github.com/alurm)
- Manse [**(@PedroManse)**](https://github.com/PedroManse)
- Pol Dellaiera [**(@drupol)**](https://github.com/drupol)
- DavHau [**(@DavHau)**](https://github.com/DavHau)
- Leandro Emmanuel Reina Kiperman [**(@kip93)**](https://github.com/kip93)
- h0nIg [**(@h0nIg)**](https://github.com/h0nIg)
- Philip Taron [**(@philiptaron)**](https://github.com/philiptaron)
- Eelco Dolstra [**(@edolstra)**](https://github.com/edolstra)
- Connor Baker [**(@ConnorBaker)**](https://github.com/ConnorBaker)
- kenji [**(@a-kenji)**](https://github.com/a-kenji)
- Oleksandr Knyshuk [**(@k1gen)**](https://github.com/k1gen)
- Maciej Krüger [**(@mkg20001)**](https://github.com/mkg20001)
- Justin Bailey [**(@jgbailey-well)**](https://github.com/jgbailey-well)
- Emily [**(@emilazy)**](https://github.com/emilazy)
- Volker Diels-Grabsch [**(@vog)**](https://github.com/vog)
- gustavderdrache [**(@gustavderdrache)**](https://github.com/gustavderdrache)
- Elliot Cameron [**(@de11n)**](https://github.com/de11n)
- Alexander V. Nikolaev [**(@avnik)**](https://github.com/avnik)
- tomberek [**(@tomberek)**](https://github.com/tomberek)
- Matthew Kenigsberg [**(@mkenigs)**](https://github.com/mkenigs)
- Sergei Zimmerman [**(@xokdvium)**](https://github.com/xokdvium)
- Cosima Neidahl [**(@OPNA2608)**](https://github.com/OPNA2608)
- John Ericson [**(@Ericson2314)**](https://github.com/Ericson2314)
- m4dc4p [**(@m4dc4p)**](https://github.com/m4dc4p)
- Graham Christensen [**(@grahamc)**](https://github.com/grahamc)
- Jason Yundt [**(@Jayman2000)**](https://github.com/Jayman2000)
- Jens Petersen [**(@juhp)**](https://github.com/juhp)
- the-sun-will-rise-tomorrow [**(@the-sun-will-rise-tomorrow)**](https://github.com/the-sun-will-rise-tomorrow)
- Farid Zakaria [**(@fzakaria)**](https://github.com/fzakaria)
- AGawas [**(@aln730)**](https://github.com/aln730)
- Robert Hensing [**(@roberth)**](https://github.com/roberth)
- Dmitry Bogatov [**(@KAction)**](https://github.com/KAction)
- Jörg Thalheim [**(@Mic92)**](https://github.com/Mic92)
- Philipp Otterbein
