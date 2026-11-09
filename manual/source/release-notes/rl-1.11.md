# Release 1.11 (2016-01-19)

这主要是一个缺陷修复版本，同时也包含一些新特性：

  - `nix-prefetch-url` 现在可以下载 Nix 表达式中指定的 URL。例如，
    
        $ nix-prefetch-url -A hello.src
    
    会从当前目录的 Nix 表达式中预取属性 `hello.src` 里 `fetchurl` 调用所指定的文件，并将结果文件的密码学哈希打印到 stdout。它与 `nix-build -A
                    hello.src` 的不同之处在于它不验证哈希，因此在更新 Nix 表达式时很有用。
    
    你也可以预取解包 tarball 的函数的结果，例如 `fetchFromGitHub`。比如：
    
        $ nix-prefetch-url --unpack https://github.com/NixOS/patchelf/archive/0.8.tar.gz
    
    或从 Nix 表达式预取：
    
        $ nix-prefetch-url -A nix-repl.src

  - 内建函数 `<nix/fetchurl.nix>` 现在支持下载并解包 NAR。这使得 Nixpkgs stdenv 引导过程中不再需要多次下载（例如 Linux 上单独的 busybox 二进制文件，或 Darwin 上的 curl/mkdir/sh/bzip2）。现在所有这些文件都可以合并为一个 NAR，并可选地用 `xz` 压缩。

  - Nix 现在对固定输出 derivation（派生）的验证以及在 `builtins.hashString` 中支持 SHA-512 哈希。

  - 新标志 `--option build-repeat
                            N` 会使每次构建执行 *N*+1 次。如果任何一轮的构建输出不同，该构建会被拒绝，输出路径不会被注册为有效。这主要用于验证构建的确定性。（我们已有 `--check` 选项来重复一次先前成功的构建。但使用 `--check` 时，非确定性构建仍会注册进数据库。避免这一点对 Hydra 很有用，可确保非确定性构建最终不会发布到二进制缓存。）

  - 选项 `--check` 和 `--option
                            build-repeat N` 如果检测到同一 derivation 的两次运行之间存在差异，且给定了 `-K`，会将另一次运行的输出置于 `store-path-check` 下提供。这使得使用 `diffoscope` 等工具调查非确定性更容易，例如：
    
        $ nix-build pkgs/stdenv/linux -A stage1.pkgs.zlib --check -K
        error: derivation ‘/nix/store/l54i8wlw2265…-zlib-1.2.8.drv’ may not
        be deterministic: output ‘/nix/store/11a27shh6n2i…-zlib-1.2.8’
        differs from ‘/nix/store/11a27shh6n2i…-zlib-1.2.8-check’
        
        $ diffoscope /nix/store/11a27shh6n2i…-zlib-1.2.8 /nix/store/11a27shh6n2i…-zlib-1.2.8-check
        …
        ├── lib/libz.a
        │   ├── metadata
        │   │ @@ -1,15 +1,15 @@
        │   │ -rw-r--r-- 30001/30000   3096 Jan 12 15:20 2016 adler32.o
        …
        │   │ +rw-r--r-- 30001/30000   3096 Jan 12 15:28 2016 adler32.o
        …

  - 改进了 FreeBSD 支持。

  - `nix-env -qa --xml --meta` 现在会打印许可证信息。

  - 二进制缓存 substituter 将使用的最大并行 TCP 连接数已从 150 降到 25。这应该能避免让某些有缺陷的 NAT 路由器不高兴，同时也提升了性能。

  - 所有包含 "chroot" 的字符串都更名为 "sandbox"。特别是一些 Nix 选项被更名，但旧名称仍作为低优先级别名被接受。

本版本包含来自 Anders Claesson、Anthony Cowley、Bjørn Forsman、Brian McKenna、Danny Wilson、davidak、Eelco Dolstra、Fabian Schmitthenner、FrankHB、Ilya Novoselov、janus、Jim Garrison、John Ericson、Jude Taylor、Ludovic Courtès、Manuel Jacob、Mathnerd314、Pascal Wittmann、Peter Simons、Philip Potter、Preston Bennes、Rommel M. Martinez、Sander van der Burg、Shea Levy、Tim Cuthbertson、Tuomas Tynkkynen、Utku Demir 和 Vladimír Čunát 的贡献。
