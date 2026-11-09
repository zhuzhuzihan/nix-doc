# Release 1.9 (2015-06-12)

除了常规的缺陷修复之外，本版本还包含以下新特性：

  - 支持签名的二进制缓存。你可以通过在 `nix.conf` 中添加以下内容来启用签名检查：
    
        signed-binary-caches = *
        binary-cache-public-keys = cache.nixos.org-1:6NCHdD59X431o0gWypbMrAURkbJ16ZPMQFGspcDShjY=
    
    这样可以防止 Nix 从缓存下载任何未由 `binary-cache-public-keys` 中所列密钥之一签名的二进制文件。
    
    只有在你构建 Nix 时带上了 `libsodium` 软件包，签名检查才受支持。
    
    注意，虽然 Nix 从 1.7 版起就已提供签名二进制缓存的实验性支持，但本版本以一种不向后兼容的方式更改了签名格式。

  - 自动下载 Nix 表达式 tarball。现在你可以在多处指定一个包含 Nix 表达式的 tarball 的 URL（例如 Nixpkgs），它会被自动下载并解包。例如：
    
      - 在 `nix-env` 中：
            
            $ nix-env -f https://github.com/NixOS/nixpkgs-channels/archive/nixos-14.12.tar.gz -iA firefox
            
        这会从 NixOS 14.12 channel 的最新已测试、已构建的修订版安装 Firefox。
    
      - 在 `nix-build` 和 `nix-shell` 中：
            
            $ nix-build https://github.com/NixOS/nixpkgs/archive/master.tar.gz -A hello
            
        这会从 Nixpkgs master 分支的最新修订版构建 GNU Hello。
    
      - 在 Nix 搜索路径中（通过 `NIX_PATH` 或 `-I` 指定）。例如，要启动一个包含特定版本 Nixpkgs 中 Pan 软件包的 shell：
            
            $ nix-shell -p pan -I nixpkgs=https://github.com/NixOS/nixpkgs-channels/archive/8a3eea054838b55aca962c3fbde9c83c102b8bf2.tar.gz
    
      - 在 NixOS 上的 `nixos-rebuild` 中：
            
            $ nixos-rebuild test -I nixpkgs=https://github.com/NixOS/nixpkgs-channels/archive/nixos-unstable.tar.gz
    
      - 在 Nix 表达式中，通过新的内置函数 `fetchTarball`：
            
            with import (fetchTarball https://github.com/NixOS/nixpkgs-channels/archive/nixos-14.12.tar.gz) {}; …
            
        （在受限模式（restricted mode）下不允许这样做。）

  - `nix-shell` 的改进：
    
      - `nix-shell` 现在有标志 `--run`，用于在 `nix-shell` 环境中执行一条命令，例如 `nix-shell --run make`。它与已有的 `--command` 标志类似，区别在于它使用非交互式 shell（确保按下 Ctrl-C 不会把你丢进子 shell）。
    
      - `nix-shell` 现在可以用作 `#!` 解释器。这让你可以编写能够动态获取自身依赖的脚本。例如，下面是一个 Haskell 脚本，被调用时它会先下载 GHC 及其依赖的 Haskell 软件包：
            
            #! /usr/bin/env nix-shell
            #! nix-shell -i runghc -p haskellPackages.ghc haskellPackages.HTTP
            
            import Network.HTTP
            
            main = do
              resp <- Network.HTTP.simpleHTTP (getRequest "http://nixos.org/")
              body <- getResponseBody resp
              print (take 100 body)
            
        当然，这些依赖会缓存在 Nix store 中，因此该脚本的第二次调用会快得多。

  - chroot 的改进：
    
      - chroot 构建现在在 Mac OS X 上受支持（利用其沙箱机制）。
    
      - 如果启用了 chroot，那么它现在会被用于所有 derivation（派生），包括固定输出 derivation（fixed-output derivation，例如 `fetchurl`）。后者确实有网络访问权限，但不再能访问宿主文件系统。如果你需要旧行为，可以把选项 `build-use-chroot` 设为 `relaxed`。
    
      - 在 Linux 上，如果启用了 chroot，构建会再次在私有的 PID namespace 中执行。（这一功能在 Nix 1.8 中一度丢失。）
    
      - `build-chroot-dirs` 中列出的存储路径现在会自动展开为它们的 closure。例如，如果你想把 `/nix/store/…-bash/bin/sh` 在 chroot 中挂载为 `/bin/sh`，你只需写 `build-chroot-dirs = /bin/sh=/nix/store/…-bash/bin/sh`；不再需要指定 Bash 的依赖。

  - 新的 derivation 属性 `passAsFile` 允许你指定 derivation 属性的内容应通过文件而不是环境变量传递。当你需要传递超出环境变量大小限制的超长字符串时，这很有用。Nixpkgs 的函数 `writeTextFile` 就用到了它。

  - 现在可以在 Nix 文件名中使用 `~` 来指代你的家目录，例如 `import ~/.nixpkgs/config.nix`。

  - Nix 新增选项 `restrict-eval`，用于限制 Nix 求值器可以访问哪些路径。通过向 Nix 传递 `--option restrict-eval true`，一旦尝试访问 Nix 搜索路径之外的任何文件，求值器就会抛出异常。这主要是为 Hydra 设计的，用以确保 Hydra jobset 只引用其声明的输入（从而保证可复现性）。

  - `nix-env` 现在只有在确实发生变化时才会在 `/nix/var/nix/profiles` 中创建新的"generation"符号链接。

  - 环境变量 `NIX_PAGER` 现在可以设置为覆盖 `PAGER`。你可以把它设为 `cat`，仅对 Nix 命令禁用分页。

  - 失败的 `<...>` 查找现在会显示位置信息。

  - 改进了对 Boehm GC 的使用：我们禁用了内部指针扫描，这应当能减少"`Repeated allocation of very large block`"警告及相关的内存滞留。

本版本包含 aszlig、Benjamin Staffin、Charles Strahan、Christian Theune、Daniel Hahler、Danylo Hlynskyi Daniel Peebles、Dan Peebles、Domen Kožar、Eelco Dolstra、Harald van Dijk、Hoang Xuan Phu、Jaka Hudoklin、Jeff Ramnani、j-keck、Linquize、Luca Bruno、Michael Merickel、Oliver Dunkl、Rob Vermaas、Rok Garbas、Shea Levy、Tobias Geerinckx-Rice 和 William A. Kennington III 的贡献。
