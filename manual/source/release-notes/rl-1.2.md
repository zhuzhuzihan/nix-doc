# Release 1.2 (2012-12-06)

本版本包含以下改进和变更：

  - Nix 引入了新的二进制替代器（binary substituter）机制：*二进制缓存*。二进制缓存中存放着预构建好的 Nix 软件包二进制文件。每当 Nix 需要构建一个缺失的 Nix store 路径时，它会检查一组二进制缓存，看其中是否有该路径的预构建二进制文件。配置项 `binary-caches` 是一个二进制缓存 URL 的列表。例如，执行
    
        $ nix-env -i thunderbird --option binary-caches http://cache.nixos.org
    
    将安装 Thunderbird 及其依赖，并使用 <http://cache.nixos.org> 中可用的预构建二进制文件。与旧的基于 "manifest" 的获取预构建二进制文件的方法相比，其主要优势在于你无需担心 manifest 是否与所安装的 Nix 表达式保持同步；也就是说，不再需要运行 `nix-pull` 来更新 manifest。它的可扩展性也更好，因为不再需要每次都重新下载一个巨大的 manifest 文件。
    
    Nix channel 可以提供一个二进制缓存 URL，只要你订阅该 channel，它就会被自动使用。如果你使用 Nixpkgs 或 NixOS channel（<http://nixos.org/channels>），你会自动获得缓存 <http://cache.nixos.org>。
    
    二进制缓存通过 `nix-push` 创建。有关二进制缓存的运行方式和格式的详细信息，请参阅 `nix-push` 的 manpage。更多细节见[这篇 nix-dev 帖子](https://nixos.org/nix-dev/2012-September/009826.html)。

  - 多输出支持现在应当可用了。derivation（派生）可以通过如下声明来表明它要产生多个存储路径：
    
        outputs = [ "lib" "headers" "doc" ];
    
    这会使 Nix 把每个输出的目标存储路径通过环境变量 `lib`、`headers` 和 `doc` 传给构建器。其他软件包可以通过 `pkg.output` 的形式引用某个特定输出，例如：
    
        buildInputs = [ pkg.lib pkg.headers ];
    
    如果你用 `nix-env` 安装一个具有多个输出的软件包，每个输出路径都会以符号链接的形式链接到用户环境中。

  - 连字符（dash）现在是标识符和属性名中的合法字符。

  - 新的操作 `nix-store --repair-path` 允许通过重新下载来修复损坏或缺失的存储路径。`nix-store --verify --check-contents --repair` 会扫描并修复 Nix store 中的所有路径。类似地，`nix-env`、`nix-build`、`nix-instantiate` 和 `nix-store --realise` 都有一个 `--repair` 标志，通过重新构建或重新下载来检测并修复坏的路径。

  - Nix 不再对 Nix store 中的文件设置不可变位（immutable bit）。取而代之的是，在 Linux 上防止 Nix store 被意外修改的推荐做法是把它挂载为只读的 bind mount，如下所示：
    
        $ mount --bind /nix/store /nix/store
        $ mount -o remount,ro,bind /nix/store
    
    Nix 会在需要时自动把 `/nix/store` 变为可写（使用私有的 mount namespace），以允许进行修改。

  - store 优化（把 store 中相同的文件替换为硬链接）现在可以在每次向 store 添加路径时自动执行。将配置选项 `auto-optimise-store` 设为 `true` 即可启用（默认关闭）。

  - 除了 `bzip2` 之外，Nix 现在还支持对 NAR 使用 `xz` 压缩。它在典型归档上的压缩率约高出 30%，解压速度约快一倍。

  - 提供了基本的 Nix 表达式求值性能分析功能：将环境变量 `NIX_COUNT_CALLS` 设为 `1` 会使 Nix 打印每个 primop 或函数被执行的次数。

  - 新增 primop：`concatLists`、`elem`、`elemAt` 和 `filter`。

  - 命令 `nix-copy-closure` 新增标志 `--use-substitutes`（`-s`），可通过 substitute 机制下载目标机器上缺失的路径。

  - 命令 `nix-worker` 已更名为 `nix-daemon`。对以"slave"模式运行 Nix worker 的支持已被移除。

  - 所有 Nix 命令的 `--help` 标志现在会调用 `man`。

  - chroot 构建现在在 systemd 机器上受支持。

本版本包含 Eelco Dolstra、Florian Friesdorf、Mats Erik Andersson 和 Shea Levy 的贡献。
