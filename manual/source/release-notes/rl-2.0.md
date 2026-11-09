# Release 2.0 (2018-02-22)

本版本做出了以下不兼容的变更：

  - 基于 manifest 的替代器（substituter）机制（`download-using-manifests`）已被[移除](https://github.com/NixOS/nix/commit/867967265b80946dfe1db72d40324b4f9af988ed)。它早在几年前就已被二进制缓存替代器机制取代。因此，以下程序已被移除：

      - `nix-pull`

      - `nix-generate-patches`

      - `bsdiff`

      - `bspatch`

  - "从其他 store 复制"的替代器机制（`copy-from-other-stores` 及 `NIX_OTHER_STORES` 环境变量）已被移除。它主要被 NixOS 安装器用来从安装介质复制可用的路径。替代做法是使用 chroot store 作为替代器（例如 `--substituters /mnt`），或者向 chroot store 中构建（例如 `--store /mnt --substituters /`）。

  - 命令 `nix-push` 已作为消除 Nix 对 Perl 依赖的工作的一部分被移除。你可以改用 `nix copy`，例如 `nix copy --to file:///tmp/my-binary-cache paths…`

  - "嵌套"日志输出特性（`--log-type pretty`）已被移除。相应地，`nix-log2xml` 也被移除了。

  - 基于 OpenSSL 的签名功能已被[移除](https://github.com/NixOS/nix/commit/f435f8247553656774dd1b2c88e9de5d59cab203)。该特性从未得到良好支持。`secret-key-files` 和 `trusted-public-keys` 选项提供了更好的替代方案。

  - 失败构建缓存功能已被[移除](https://github.com/NixOS/nix/commit/8cffec84859cec8b610a2a22ab0c4d462a9351ff)。该特性当初是为支持 Hydra 持续构建系统而引入的，但 Hydra 已不再使用它。

  - `nix-mode.el` 已从 Nix 中移除。它现在是[一个独立的仓库](https://github.com/NixOS/nix-mode)，可以通过 MELPA 软件包仓库安装。

本版本包含以下新特性：

  - 它引入了一个名为 `nix` 的新命令，旨在最终以一个更一致、设计更完善的用户界面取代所有 `nix-*` 命令。它目前为 `nix-store`、`nix-build`、`nix-shell -p`、`nix-env -qa`、`nix-instantiate --eval`、`nix-push` 和 `nix-copy-closure` 所提供的部分（但非全部）功能提供了替代。它具有以下主要特性：

      - 与旧式命令不同，它提供了一致的方式来引用软件包及类软件包参数（例如存储路径）。例如，以下命令都会把 GNU Hello 软件包复制到远程机器：

            nix copy --to ssh://machine nixpkgs.hello

            nix copy --to ssh://machine /nix/store/qbhyj3blxpw2i6pb7c6grc9185nbnpvy-hello-2.10

            nix copy --to ssh://machine '(with import <nixpkgs> {}; hello)'

        相比之下，`nix-copy-closure` 只接受存储路径作为参数。

      - 它是自文档化的：`--help` 会显示所有可用的命令行参数。如果在子命令之后给出 `--help`，它会显示该子命令的示例。`nix --help-config` 显示所有配置选项。

      - 它的输出要简洁得多。默认情况下，它显示一个单行进度指示器，标明还剩多少软件包待构建或下载，以及（如果有正在运行的构建）构建器输出的最近一行。如果构建失败，它会显示构建器输出的最后几行。完整的构建日志可以用 `nix log` 获取。

      - 它[提供](https://github.com/NixOS/nix/commit/b8283773bd64d7da6859ed520ee19867742a03ba)了把所有 `nix.conf` 配置选项作为命令行标志使用的能力。例如，你可以写 `--http-connections 100` 来代替 `--option http-connections 100`。布尔选项可以写成 `--foo` 或 `--no-foo`（例如 `--no-auto-optimise-store`）。

      - 许多子命令都有 `--json` 标志，以 JSON 格式把结果写到标准输出。

    > **警告**
    >
    > 请注意，`nix` 命令仍在开发中，其界面可能发生变化。

    它提供以下高层（"porcelain"）子命令：

      - `nix build` 是 `nix-build` 的替代品。

      - `nix run` 在一个指定软件包可用的环境中执行命令。它（大致上）是 `nix-shell -p` 的替代品。与后者不同，它不在 shell 中执行命令，并且有一个标志（`-c`）用于指定要执行的不带引号的命令行。

        它与 chroot store 结合使用时尤其有用，让没有权限在 `/nix/store` 中安装 Nix 的 Linux 用户也能使用假定 `/nix/store` 存在的二进制替代品（binary substitute）。例如，

            nix run --store ~/my-nix nixpkgs.hello -c hello --greeting 'Hi everybody!'

        会把 GNU Hello 软件包下载（或在没有可用替代品时构建）到 `~/my-nix/nix/store`，然后在一个 mount namespace 中运行 `hello`，在该 namespace 中 `~/my-nix/nix/store` 被挂载到 `/nix/store` 上。

      - `nix search` 取代了 `nix-env -qa`。它在属性名、软件包名或描述中搜索出现的搜索字符串。与 `nix-env -qa` 不同，它有缓存来加速后续的搜索。

      - `nix copy` 在任意 Nix store 之间复制路径，是对 `nix-copy-closure` 和 `nix-push` 的推广。

      - `nix repl` 取代了外部程序 `nix-repl`。它提供了一个用于求值和构建 Nix 表达式的交互式环境。注意，它使用 `linenoise-ng` 而不是 GNU Readline。

      - `nix upgrade-nix` 把 Nix 升级到最新的稳定版本。这要求 Nix 安装在 profile 中。（因此在 NixOS 上，或者当它安装在 Nix store 之外时，该命令无法工作。）

      - `nix verify` 检查存储路径是否未被修改和/或是否"受信任"（见下文）。它取代了 `nix-store --verify` 和 `nix-store --verify-path`。

      - `nix log` 显示软件包或路径的构建日志。如果构建日志在本地不可用，它会尝试从配置的替代器（substituter）获取（例如 [cache.nixos.org](https://cache.nixos.org/)，它现在提供构建日志）。

      - `nix edit` 在你的编辑器中打开某个软件包的源代码。

      - `nix eval` 取代了 `nix-instantiate --eval`。

      - `nix why-depends` 显示为什么一个存储路径的 closure 中包含另一个。这主要用于查找 closure 膨胀的原因。例如，

            nix why-depends nixpkgs.vlc nixpkgs.libdrm.dev

        会显示导致 VLC 软件包的 closure 中包含 `libdrm` 的 "dev" 输出的文件链及文件内容片段——这是一种不理想的情况。

      - `nix path-info` 显示关于存储路径的信息，取代了 `nix-store -q`。一个有用的特性是选项 `--closure-size`（`-S`）。例如，以下命令显示当前 NixOS 系统 closure 中每条路径的 closure 大小，并按大小排序：

            nix path-info -rS /run/current-system | sort -nk2

      - `nix optimise-store` 取代了 `nix-store --optimise`。主要区别在于它有进度指示器。

    还有若干低层（"plumbing"）命令可用：

      - `nix ls-store` 和 `nix ls-nar` 列出存储路径或 NAR 文件的内容。前者主要与远程 store 结合使用，例如

            nix ls-store --store https://cache.nixos.org/ -lR /nix/store/qbhyj3blxpw2i6pb7c6grc9185nbnpvy-hello-2.10

        列出某个二进制缓存中路径的内容。

      - `nix cat-store` 和 `nix cat-nar` 允许从存储路径或 NAR 文件中提取文件。

      - `nix dump-path` 以 NAR 格式把存储路径的内容写到标准输出。它取代了 `nix-store --dump`。

      - `nix show-derivation` 以 JSON 格式显示存储的 derivation（派生）。它是 `pp-aterm` 的替代方案。

      - `nix add-to-store` 取代了 `nix-store --add`。

      - `nix sign-paths` 对存储路径进行签名。

      - `nix copy-sigs` 把签名从一个 store 复制到另一个。

      - `nix show-config` 显示所有配置选项及其当前值。

  - Nix 长期以来用于支持通过 Nix daemon（守护进程）访问 store 的 store 抽象得到了大幅扩展。特别是，替代器（过去是外部程序，例如 `download-from-binary-cache`）现在成了抽象 `Store` 类的子类。这使得许多 Nix 命令可以操作这类 store 类型。例如，`nix path-info` 显示本地 Nix store 中路径的信息，而 `nix path-info --store https://cache.nixos.org/` 显示指定二进制缓存中路径的信息。类似地，`nix-copy-closure`、`nix-push` 和替代（substitution）都是"在不同类型的 Nix store 之间复制路径"这一通用概念的具体实例。

    store 使用类 URI 的语法指定，例如 <https://cache.nixos.org/> 或 <ssh://machine>。支持以下 store 类型：

      - `LocalStore`（URI 为 `local` 或绝对路径）和名不副实的 `RemoteStore`（`daemon`）提供对本地 Nix store 的访问，后者通过 Nix daemon 访问。你可以使用 `auto` 或空字符串来自动选择本地 store 或 daemon store，具体取决于你对 Nix store 是否有写权限。不再需要设置 `NIX_REMOTE` 环境变量来使用 Nix daemon。

        如上所述，`LocalStore` 现在支持 chroot 构建，允许 Nix store 的"物理"位置（例如 `/home/alice/nix/store`）与其"逻辑"位置（通常是 `/nix/store`）不同。这让非 root 用户也能使用 Nix，同时仍能享受来自 [cache.nixos.org](https://cache.nixos.org/) 的预构建二进制文件带来的好处。

      - `BinaryCacheStore` 是所有二进制缓存 store 的抽象超类。它支持以 JSON 格式写入构建日志和 NAR 内容清单。

      - `HttpBinaryCacheStore`（`http://`、`https://`）支持通过 HTTP 或 HTTPS 访问的二进制缓存。如果服务器支持 `PUT` 请求，它还支持通过诸如 `nix copy` 之类的命令上传存储路径。

      - `LocalBinaryCacheStore`（`file://`）支持本地文件系统中的二进制缓存。

      - `S3BinaryCacheStore`（`s3://`）支持存储在 Amazon S3 中的二进制缓存，前提是编译时启用了该支持。

      - `LegacySSHStore`（`ssh://`）用于实现远程构建和 `nix-copy-closure`。

      - `SSHStore`（`ssh-ng://`）通过 `nix-daemon` 所用的同一协议在远程机器上执行任意 Nix 操作。

  - 安全性在多个方面得到了改进：

      - Nix 现在为本地存储路径保存签名。当路径在不同 store 之间复制时（例如从二进制缓存复制到本地 store），签名会随之传播。

        本地构建的路径会使用 `secret-key-files` store 选项指定的密钥自动签名。密钥对（私钥/公钥）可以用 `nix-store --generate-binary-cache-key` 生成。

        此外，本地构建的存储路径会被标记为"最终受信任"（ultimately trusted），但当路径在 store 之间复制时，这个位不会传播。

      - 内容寻址（content-addressable）的存储路径不再需要签名——即使没有签名，非特权用户也可以把它们导入 store。

      - 命令 `nix verify` 检查指定的路径是否受信任，即是否拥有一定数量的受信任签名、是否被最终受信任，或者是内容寻址的。

      - 来自二进制缓存的替代（substitution）[现在](https://github.com/NixOS/nix/commit/ecbc3fedd3d5bdc5a0e1a0a51b29062f2874ac8b)默认要求签名。在 NixOS 上此前已是如此。

      - 在 Linux 沙箱构建中，我们[现在](https://github.com/NixOS/nix/commit/eba840c8a13b465ace90172ff76a0db2899ab11b)使用 `/build` 而不是 `/tmp` 作为临时构建目录。这修复了一个潜在的安全问题：当构建意外地把它的 `TMPDIR` 存到某个安全敏感的位置（例如 RPATH）时。

  - *纯求值模式*。通过 `--pure-eval` 标志，Nix 启用了现有受限求值模式的一个变体，它禁止访问任何可能导致同样的命令行参数产生不同求值结果的东西。这包括 `builtins.getEnv` 之类的内置函数，但更重要的是，除非指定了内容哈希或 commit hash，*所有*文件系统和网络访问都被禁止。例如，只有在指定了 `rev` 属性时才允许调用 `builtins.fetchGit`。

    这一特性的目标是在求值层面实现真正的构建可复现性和可追溯性（包括 NixOS 系统配置）。例如，将来 `nixos-rebuild` 可能以纯模式从某个 Git 仓库中的 Nix 表达式构建配置。该表达式可能通过 `builtins.fetchGit` 获取诸如 Nixpkgs 之类的其他仓库。顶层仓库的 commit hash 便唯一标识了正在运行的系统，并结合该仓库，使系统得以复现或修改。

  - 新增了若干特性以支持二进制可复现性（即帮助确保同一个 derivation 的多次构建产生完全相同的输出）。当 `enforce-determinism` 设为 `false` 时，各轮构建产出不同的输出[不再是](https://github.com/NixOS/nix/commit/8bdf83f936adae6f2c907a6d2541e80d4120f051)致命错误。此外还[提供](https://github.com/NixOS/nix/commit/9a313469a4bdea2d1e8df24d16289dc2a172a169)了一个名为 `diff-hook` 的钩子，让你在各轮构建产出不同输出时运行诸如 `diffoscope` 的工具。

  - 配置远程构建现在容易多了。只要你没有使用 Nix daemon，现在就可以直接在命令行上指定远程构建机器，例如 `--option builders 'ssh://my-mac x86_64-darwin'`。环境变量 `NIX_BUILD_HOOK` 已被移除，也不再需要。环境变量 `NIX_REMOTE_SYSTEMS` 为兼容起见仍受支持，但也可以在 `nix.conf` 中通过设置选项 `builders = @path` 来指定构建机器。

  - 如果固定输出 derivation（fixed-output derivation）产出了哈希不正确的结果，输出路径会被移动到与实际哈希对应的位置并注册为有效。因此，随后用正确哈希构建该固定输出 derivation 就不再必要。

  - `nix-shell` [现在](https://github.com/NixOS/nix/commit/ea59f39326c8e9dc42dfed4bcbf597fbce58797c)会在求值期间和 shell 本身中设置 `IN_NIX_SHELL` 环境变量。它可以用来根据你处于 Nix shell 还是常规构建中执行不同的动作。Nixpkgs 提供了 `lib.inNixShell` 用于在求值期间检查该变量。

  - `NIX_PATH` 现在是惰性的，因此路径中的 URI 只有在求值需要时才会被下载。

  - 现在可以使用 `channel:` 作为 <https://nixos.org/channels//nixexprs.tar.xz> [现为 <https://channels.nixos.org//nixexprs.tar.xz>] 的简写。例如，`nix-build channel:nixos-15.09 -A hello` 会从 `nixos-15.09` channel 构建 GNU Hello 软件包。将来，这可能会改用 Git 来更高效地获取更新。

  - 当给定 `--no-build-output` 时，如果构建失败，将显示构建日志的最后 10 行。

  - 网络功能得到改进：

      - 现已支持 HTTP/2。这使得二进制缓存的查询[高效得多](https://github.com/NixOS/nix/commit/90ad02bf626b885a5dd8967894e2eafc953bdf92)。

      - 我们现在会对许多 HTTP 错误重试下载，使二进制缓存替代器对临时故障更有韧性。

      - HTTP 凭据现在可以通过标准的 `netrc` 机制配置。

      - 如果编译时启用了 S3 支持，在 Nix 允许 URI 的所有地方都[支持](https://github.com/NixOS/nix/commit/9ff9c3f2f80ba4108e9c945bbfda2c64735f987b) <s3://> URI。

      - 现已支持 Brotli 压缩。特别是，[cache.nixos.org](https://cache.nixos.org/) 的构建日志现在使用 Brotli 压缩。

  - `nix-env` [现在](https://github.com/NixOS/nix/commit/b0cb11722626e906a73f10dd9a0c9eea29faf43a)会忽略具有非法 derivation 名称的软件包（尤其是以数字开头或包含点号的名称）。

  - 许多配置选项被重命名，或者是因为原来的名字过于冗长（例如 `build-use-sandbox` 现在就是 `sandbox`），或者是为反映泛化后的行为（例如 `binary-caches` 现在是 `substituters`，因为它允许任意 store URI）。出于兼容性考虑，旧名称仍然受支持。

  - `max-jobs` 选项[现在](https://github.com/NixOS/nix/commit/7251d048fa812d2551b7003bc9f13a8f5d4c95a5)可以设为 `auto`，以使用系统中的 CPU 数量。

  - 哈希[现在](https://github.com/NixOS/nix/commit/c0015e87af70f539f24d2aa2bc224a9d8b84276b)可以用 base-64 格式指定了，此外还支持 base-16 和非标准的 base-32。

  - `nix-shell` 现在使用来自 Nixpkgs 的 `bashInteractive`，而不是恰好出现在调用者 `PATH` 中的 `bash` 命令。这在 macOS 上尤为重要，因为系统提供的 `bash` 严重过时，无法执行 `stdenv` 的 setup 脚本。

  - Nix 现在可以在构建期间可用磁盘空间低于某个阈值时自动触发垃圾回收。这通过 `min-free` 和 `max-free` 选项配置。

  - `nix-store -q --roots` 和 `nix-store --gc --print-roots` 现在会显示临时的和内存中的根（root）。

  - Nix 现在可以通过插件扩展。详见 `plugin-files` 选项的文档。

Nix 语言包含以下新特性：

  - 它支持浮点数。浮点数基于 C++ 的 `float` 类型，并为现有的数值运算符所支持。与 JSON 和 XML 之间的导入导出也可用。

  - derivation 属性现在可以使用 `placeholder` 内置函数引用该 derivation 自身的输出。例如，属性

        configureFlags = "--prefix=${placeholder "out"} --includedir=${placeholder "dev"}";

    会使 `configureFlags` 环境变量包含与 `out` 和 `dev` 输出对应的实际存储路径。

以下内置函数是新增或扩展的：

  - `builtins.fetchGit` 允许在求值时获取 Git 仓库。因此它不同于 Nixpkgs 中的 `fetchgit` 函数——后者在构建时获取，无法在求值期间获取 Nix 表达式。一个典型的用例是从你的配置中导入外部 NixOS 模块，例如

        imports = [ (builtins.fetchGit https://github.com/edolstra/dwarffs + "/module.nix") ];

  - 类似地，`builtins.fetchMercurial` 允许你获取 Mercurial 仓库。

  - `builtins.path` 推广了 `builtins.filterSource` 和路径字面量（例如 `./foo`）。它允许指定一个不同于源路径名的存储路径名（例如 `builtins.path { path = ./foo; name = "bar"; }`），并且也支持过滤掉不需要的文件。

  - `builtins.fetchurl` 和 `builtins.fetchTarball` 现在支持 `sha256` 和 `name` 属性。

  - `builtins.split` 使用 POSIX 扩展正则表达式作为分隔符来切分字符串。

  - `builtins.partition` 依据一个布尔谓词把列表的元素划分为两个列表。

  - `<nix/fetchurl.nix>` 现在使用位于 <http://tarballs.nixos.org/> 的内容寻址 tarball 缓存，就像 Nixpkgs 中的 `fetchurl` 一样。(f2682e6e18a76ecbfb8a12c17e3a0ca15c084197)

  - 在受限求值模式和纯求值模式下，从网络下载的内置函数（例如 `fetchGit`）允许获取选项 `allowed-uris` 中指定的 URI 前缀列表之下的内容。

Nix 构建环境包含以下变更：

  - 布尔值、整数、（嵌套）列表和属性集之类的值[现在](https://github.com/NixOS/nix/commit/6de33a9c675b187437a2e1abbcb290981a89ecb1)可以无损地传递给构建器。如果特殊属性 `__structuredAttrs` 设为 `true`，其他 derivation 属性会以 JSON 格式序列化，并通过构建器临时目录中的文件 `.attrs.json` 提供给构建器。这使得 `passAsFile` 不再必要，因为 JSON 文件不像进程环境变量那样有大小限制。

    [作为对 Bash 构建器的一项便利](https://github.com/NixOS/nix/commit/2d5b1b24bf70a498e4c0b378704cfdb6471cc699)，Nix 会向构建器目录写入一个名为 `.attrs.sh` 的脚本，它会初始化与所有可用 Bash 表示的属性对应的 shell 变量。这包括非嵌套的（关联）数组。例如，属性 `hardening.format = true` 最终会成为 Bash 关联数组元素 `${hardening[format]}`。

  - 构建器[现在](https://github.com/NixOS/nix/commit/88e6bb76de5564b3217be9688677d1c89101b2a3)可以通过向 `NIX_LOG_FD` 指定的文件描述符写入消息来告知自己当前处于哪个构建阶段。当前阶段会显示在 `nix` 的进度指示器中。

  - 在 Linux 沙箱构建中，我们[现在](https://github.com/NixOS/nix/commit/a2d92bb20e82a0957067ede60e91fab256948b41)提供一个默认的 `/bin/sh`（即 BusyBox 的 `ash`）。

  - 在结构化属性模式下，`exportReferencesGraph` 会以 JSON 格式[导出](https://github.com/NixOS/nix/commit/c2b0d8749f7e77afc1c4b3e8dd36b7ee9720af4a)关于 closure 的扩展信息。特别是，它包含路径的大小和哈希。这对 NixOS 镜像构建器尤其有用。

  - 一旦 Nix 在构建器的 stdout 或 stderr 上收到 EOF，构建[现在](https://github.com/NixOS/nix/commit/21948deed99a3295e4d5666e027a6ca42dc00b40)会被立即杀死。这修复了一个允许构建无视超时地把 Nix 无限期挂起的缺陷。

  - `sandbox-paths` 配置选项现在可以通过追加 `?` 来指定可选路径，例如 `/dev/nvidiactl?` 只有在 `/dev/nvidiactl` 存在时才会把它 bind-mount 进来。

  - 在 Linux 上，构建现在在 UID 1000、GID 100 的 user namespace 中执行。

内部做出了若干重大变更：

  - Nix 不再依赖 Perl，所有 Perl 组件都已被用 C++ 重写或移除。原先属于 Nix 的 Perl 绑定已被移至独立的软件包 `nix-perl`。

  - 所有 `Store` 类现在都是线程安全的。`RemoteStore` 支持到 daemon 的多个并发连接。这在诸如 `hydra-queue-runner` 之类的多线程程序中尤其有用。

本版本包含 Adrien Devresse、Alexander Ried、Alex Cruice、Alexey Shmalko、AmineChikhaoui、Andy Wingo、Aneesh Agrawal、Anthony Cowley、Armijn Hemel、aszlig、Ben Gamari、Benjamin Hipple、Benjamin Staffin、Benno Fünfstück、Bjørn Forsman、Brian McKenna、Charles Strahan、Chase Adams、Chris Martin、Christian Theune、Chris Warburton、Daiderd Jordan、Dan Connolly、Daniel Peebles、Dan Peebles、davidak、David McFarland、Dmitry Kalinkin、Domen Kožar、Eelco Dolstra、Emery Hemingway、Eric Litak、Eric Wolf、Fabian Schmitthenner、Frederik Rietdijk、Gabriel Gonzalez、Giorgio Gallo、Graham Christensen、Guillaume Maudoux、Harmen、Iavael、James Broadhead、James Earl Douglas、Janus Troelsen、Jeremy Shaw、Joachim Schiele、Joe Hermaszewski、Joel Moberg、Johannes 'fish' Ziemke、Jörg Thalheim、Jude Taylor、kballou、Keshav Kini、Kjetil Orbekk、Langston Barrett、Linus Heckemann、Ludovic Courtès、Manav Rathi、Marc Scholten、Markus Hauck、Matt Audesse、Matthew Bauer、Matthias Beyer、Matthieu Coudron、N1X、Nathan Zadoks、Neil Mayhew、Nicolas B. Pierron、Niklas Hambüchen、Nikolay Amiantov、Ole Jørgen Brønner、Orivej Desh、Peter Simons、Peter Stuart、Pyry Jahkola、regnat、Renzo Carbonara、Rhys、Robert Vollmert、Scott Olson、Scott R. Parish、Sergei Trofimovich、Shea Levy、Sheena Artrip、Spencer Baugh、Stefan Junker、Susan Potter、Thomas Tuegel、Timothy Allen、Tristan Hume、Tuomas Tynkkynen、tv、Tyson Whitehead、Vladimír Čunát、Will Dietz、wmertens、Wout Mertens、zimbatm 和 Zoran Plesivčak 的贡献。
