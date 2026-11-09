# Release 0.12 (2008-11-20)

  - Nix 不再使用 Berkeley DB 存储 Nix store 元数据。新存储方案的主要优点是：它在可靠的 NFS 实现上能正常工作（从而使 Nix store 可以在多台机器之间共享）；Nix 进程崩溃后无需恢复；只读操作不需要写权限；某些操作不会再耗尽 Berkeley DB 锁。
    
    如果你希望 Nix 自动将旧的 Nix store 转换为新 schema，仍然需要在编译 Nix 时带上 Berkeley DB 支持。如果不需要此功能，你可以使用 `configure` 选项 `--disable-old-db-compat` 构建 Nix。
    
    在自动转换到新 schema 之后，你可以删除旧的 Berkeley DB 文件：
    
        $ cd /nix/var/nix/db
        $ rm __db* log.* derivers references referrers reserved validpaths DB_CONFIG
    
    新的元数据存储在目录 `/nix/var/nix/db/info` 和 `/nix/var/nix/db/referrer` 中。虽然元数据以人类可读的纯文本文件存储，但它们并不打算供人手工编辑，因为 Nix 对格式相当严格。
    
    新的存储 schema 是否比 Berkeley DB 环境占用更少的磁盘空间视情况而定，主要取决于你文件系统的簇大小。在 1 KiB 簇（这似乎是如今 `ext3` 的默认值）下，它通常占用的空间要少得多。

  - 新增一个 substituter，可直接从文件系统中某处挂载的其他（远程）Nix store 复制路径。例如，你可以通过 NFS 或 `sshfs` 挂载某个已包含所需软件包的远程 Nix store 来加速安装。环境变量 `NIX_OTHER_STORES` 指定远程 Nix 目录的位置，例如 `/mnt/remote-fs/nix`。

  - 新增 `nix-store` 操作 `--dump-db` 和 `--load-db`，用于转储和重新载入 Nix 数据库。

  - 垃圾回收器新增了若干选项，允许只删除部分垃圾。选项 `--max-freed N` 告诉回收器在至少删除 *N* 字节后停止。选项 `--max-links
            N` 告诉它在 `/nix/store` 上的链接数降到 *N* 以下后停止。这对位于有 32000 个子目录限制的文件系统（如 `ext3`）上的超大 Nix store 很有用。选项 `--use-atime` 使存储路径按最后访问时间升序删除，从而允许删除不常使用的内容。选项 `--max-atime time` 为可删除路径的最后访问时间设定上限。例如：
    
    ``` 
        $ nix-store --gc -v --max-atime $(date +%s -d "2 months ago")
    ```
    
    会删除两个月内未被访问的所有内容。

  - 在执行安装或升级等操作时，`nix-env` 现在使用乐观 profile 锁，而不是对 profile 设置排他锁。这允许在同一 profile 上并行执行多个 `nix-env -i / -u
    / -e` 操作。如果 `nix-env` 操作在结束时发现 profile 在此期间被另一个进程修改，它会直接重启。这通常是廉价的，因为构建结果仍然在 Nix store 中。

  - `nix-store -r` 和 `nix-build` 现在支持选项 `--dry-run`。

  - 此前由 `--dry-run` 显示的信息（即哪些 derivation（派生）将被构建、哪些路径将被 substitute）现在总是由 `nix-env`、`nix-store -r` 和 `nix-build` 显示。可 substitute 路径的总下载大小现在也会显示。例如，一次构建会显示类似：

        the following derivations will be built:
          /nix/store/129sbxnk5n466zg6r1qmq1xjv9zymyy7-activate-configuration.sh.drv
          /nix/store/7mzy971rdm8l566ch8hgxaf89x7lr7ik-upstart-jobs.drv
          ...
        the following paths will be downloaded/copied (30.02 MiB):
          /nix/store/4m8pvgy2dcjgppf5b4cj5l6wyshjhalj-samba-3.2.4
          /nix/store/spc1m987vlibchdx369qwa391s738s7l-libunwind-0.98.6
          ...

  - 语言特性：
    
      - 类似 Haskell 的 @-模式。例如，在函数定义中
        
            f = args @ {x, y, z}: ...;
        
        `args` 指代整个参数，它随后会针对属性集模式 `{x, y, z}` 进行进一步的模式匹配。
    
      - "`...`"（省略号）模式。属性集模式现在可以在属性名列表末尾写 `...`，以指定该函数*至少*接受列出的属性，同时忽略额外的属性。例如，
        
            {stdenv, fetchurl, fuse, ...}: ...
        
        定义了一个接受任何至少包含这三个所列属性的属性集的函数。
    
      - 新的 primop：`builtins.parseDrvName`（将 `"nix-0.12pre12876"` 这样的软件包名字符串拆分为名称和版本两部分，例如 `"nix"` 和 `"0.12pre12876"`）、`builtins.compareVersions`（使用与 `nix-env` 相同的算法比较两个版本字符串）、`builtins.length`（高效计算列表长度）、`builtins.mul`（整数乘法）、`builtins.div`（整数除法）。

  - `nix-prefetch-url` 现在支持 `mirror://` URL，前提是环境变量 `NIXPKGS_ALL` 指向一个 Nixpkgs 树。

  - 移除了命令 `nix-pack-closure` 和 `nix-unpack-closure`。你可以用 `nix-store --export
            $(nix-store -qR paths) > closure` 和 `nix-store --import <
            closure` 做到几乎同样的事情，但效率高得多。

  - 大量缺陷修复，包括 `with` 表达式处理中的一个严重性能缺陷。
