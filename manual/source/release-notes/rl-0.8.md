# Release 0.8 (2005-04-11)

注意：Nix 0.8 的哈希方案发生了变化（详见下文）。因此，为 Nix 0.7 及以下版本构建的 `nix-pull` manifest 和 channel 将不再可用。不过 Nix 表达式语言没有变化，所以你仍然可以从源码构建。此外，现有的用户环境可以继续工作。Nix 0.8 在首次运行时会自动升级先前安装的数据库 schema。

如果你看到错误消息

    you have an old-style manifest `/nix/var/nix/manifests/[...]'; please
    delete it

你应当删除先前下载的 manifest：

    $ rm /nix/var/nix/manifests/*

如果 `nix-channel` 给出错误消息

    manifest `http://catamaran.labs.cs.uu.nl/dist/nix/channels/[channel]/MANIFEST'
    is too old (i.e., for Nix <= 0.7)

那么你应当退订有问题的 channel（`nix-channel
--remove
URL`；去掉 `/MANIFEST`），然后订阅同一个 URL，并将 `channels` 替换为 `channels-v3`（例如 <http://catamaran.labs.cs.uu.nl/dist/nix/channels-v3/nixpkgs-unstable>）。

Nix 0.8 有以下改进：

  - 存储路径中使用的密码学哈希现在为 160 位，但以 base-32 编码，因此仍然只有 32 个字符长（例如 `/nix/store/csw87wag8bqlqk7ipllbwypb14xainap-atk-1.9.0`）。（这实际上是对 SHA-256 哈希的 160 位截断。）

  - 对基本 store 语义的大清理和简化。"closure store 表达式"的概念已不复存在（"successors" 的概念也随之消失）；存储路径的文件系统引用现在直接存储在数据库中。

    例如，给定任意存储路径，你可以查询其闭包：

        $ nix-store -qR $(which firefox)
        ... lots of paths ...

    此外，Nix 现在会为每个存储路径记住构建它的 derivation（即 "deriver"）：

        $ nix-store -qR $(which firefox)
        /nix/store/4b0jx7vq80l9aqcnkszxhymsf1ffa5jd-firefox-1.0.1.drv

    因此，要查看构建时依赖，你可以执行

        $ nix-store -qR $(nix-store -qd $(which firefox))

    或者以更友好的格式：

        $ nix-store -q --tree $(nix-store -qd $(which firefox))

    文件系统引用也会以反向存储。例如，你可以查询直接或间接使用某个 Glibc 的所有路径：

        $ nix-store -q --referrers-closure \
            /nix/store/1a6mdrjz4wn7b9sfmcw5ggbk1mi281mh-glibc-2.3.4

  - 固定输出 derivation（派生）的概念已被形式化。此前，Nixpkgs 中的 `fetchurl` 等函数使用一种 hack（即显式指定一个存储路径哈希）来防止诸如文件 URL 的变更沿着依赖图向上传播、导致所有内容重新构建。现在可以通过指定 `outputHash` 和 `outputHashAlgo` 属性干净地做到这一点。Nix 自身会检查输出的内容是否具有指定的哈希。（这对维护某些不变量很重要，它们是未来关于安全共享 store 工作的必要条件。）

  - 一键安装 :-) 现在可以通过 Web 直接安装 Nixpkgs 中的任何顶层组件——例如参见 <http://catamaran.labs.cs.uu.nl/dist/nixpkgs-0.8/>。你所要做的只是将 `/nix/bin/nix-install-package` 与 MIME 类型 `application/nix-package`（或扩展名 `.nixpkg`）关联起来，点击软件包链接就会导致它连同所有相应依赖一起被安装。如果你只想安装某个特定应用程序，这比订阅 channel 更简单。

  - `nix-store -r
            PATHS` 现在会并行构建所有 derivation PATHS。此前它是顺序执行的（尽管会利用子 derivation 之间可能的并行性）。这对构建农场很有好处。

  - `nix-channel` 新增操作 `--list` 和 `--remove`。

  - 将组件安装到用户环境的新方式：

      - 从另一个用户环境复制：

            $ nix-env -i --from-profile .../other-profile firefox

      - 直接安装一个 store 中的 derivation（完全绕过 Nix 表达式语言）：

            $ nix-env -i /nix/store/z58v41v21xd3...-aterm-2.3.1.drv

        （这被用于实现 `nix-install-package`，因此它不受 Nix 表达式语言演变的影响。）

      - 直接安装一个已构建好的存储路径：

            $ nix-env -i /nix/store/hsyj5pbn0d9i...-aterm-2.3.1

      - 安装以命令行参数形式指定的 Nix 表达式的结果：

            $ nix-env -f .../i686-linux.nix -i -E 'x: x.firefoxWrapper'

        与普通安装模式的区别在于 `-E` 不使用 derivation 的 `name` 属性。因此，这可用于对多个同名 derivation 进行消歧。

  - 构建成功后，存储路径内容的哈希现在会存入数据库。这让你可以检查存储路径是否被篡改：`nix-store
            --verify --check-contents`。

  - 实现了并发垃圾回收器。现在运行垃圾回收器始终是安全的，即使其他 Nix 操作正在同时进行。

    但是，如果你直接使用 `nix-instantiate` 和 `nix-store
                    --realise` 来构建内容，仍可能出现 GC 竞态。为防止竞态，请使用这些命令的 `--add-root` 标志。

  - 垃圾回收器现在终于按正确的顺序（即在"references"关系下拓扑排序的顺序）删除路径，从而使得中断回收器是安全的，不会冒着 store 违反闭包不变量的风险。

  - 同样，substitute 机制现在也按正确的顺序下载文件，从而始终维持闭包不变量。

  - `nix-build` 的结果现在被注册为垃圾回收器的根。如果 `./result` 链接被删除，GC 根会自动消失。

  - 垃圾回收器的行为可以通过在 `/nix/etc/nix/nix.conf` 中设置选项来全局改变。

      - `gc-keep-derivations` 指定在搜索活跃路径时是否应跟随 deriver 链接。

      - `gc-keep-outputs` 指定在搜索活跃路径时是否应跟随 derivation 的输出。

      - `env-keep-derivations` 指定用户环境在添加时是否应存储 derivation 的路径（从而保持这些 derivation 活跃）。

  - 新的 `nix-env` 查询标志 `--drv-path` 和 `--out-path`。

  - `fetchurl` 除 MD5 外还允许 SHA-1 和 SHA-256。只需指定属性 `sha1` 或 `sha256` 而不是 `md5`。

  - 手册更新。
