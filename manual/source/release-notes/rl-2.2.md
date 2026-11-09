# Release 2.2 (2019-01-11)

这主要是一个缺陷修复版本，同时包含以下变更：

  - 在使用结构化属性（structured attributes）的 derivation（派生）中（即把 `__structuredAttrs` 属性设为 `true`，使全部属性以 JSON 格式传给 builder），现在可以为每个输出单独指定闭包检查，例如：
    
        outputChecks."out" = {
          # 'out' 的闭包不得超过 256 MiB。
          maxClosureSize = 256 * 1024 * 1024;
        
          # 它不得引用 C 编译器或 'dev' 输出。
          disallowedRequisites = [ stdenv.cc "dev" ];
        };
        
        outputChecks."dev" = {
          # 'dev' 输出不得超过 128 KiB。
          maxSize = 128 * 1024;
        };

  - derivation 属性 `requiredSystemFeatures` 现在对本地构建同样生效，而不只是用于把构建路由到远程 builder。机器支持的特性可通过配置项 `system-features` 指定。
    
    默认情况下，若 `/dev/kvm` 存在，`system-features` 会包含 `kvm`。为保持兼容，它还包含 `nixos-test`、`benchmark` 和 `big-parallel` 这些伪特性（pseudo-feature），Nixpkgs 用它们把构建路由到特定的 Hydra 构建机。

  - Linux 上沙箱构建现在默认启用。

  - 新命令 `nix doctor` 用于显示 Nix 安装中的潜在问题。

  - 内置函数 `fetchGit` 现在采用新的缓存方案：把不同的远程仓库放进各自独立的本地仓库，而不是共用一个仓库。这会占用更多磁盘空间，但速度更快。

  - 内置函数 `dirOf` 现在可以处理相对路径。

  - Nix 现在支持 [SRI 哈希](https://www.w3.org/TR/SRI/)，允许在单一字符串中同时指定哈希算法与哈希值。例如，可以写：
    
        import <nix/fetchurl.nix> {
          url = https://nixos.org/releases/nix/nix-2.1.3/nix-2.1.3.tar.xz;
          hash = "sha256-XSLa0FjVyADWWhFfkZ2iKTjFDda6mMXjoYMXLRSYQKQ=";
        };
    
    来替代
    
        import <nix/fetchurl.nix> {
          url = https://nixos.org/releases/nix/nix-2.1.3/nix-2.1.3.tar.xz;
          sha256 = "5d22dad058d5c800d65a115f919da22938c50dd6ba98c5e3a183172d149840a4";
        };
    
    在固定输出 derivation 中，若 `outputHash` 已指明哈希，`outputHashAlgo` 属性不再是必填项。
    
    `nix hash-file` 与 `nix hash-path` 现在默认以 SRI 格式输出哈希，并且默认使用 SHA-256 而非 SHA-512，因为 Nixpkgs 中大多数场景使用的都是 SHA-256。

  - 整数在所有平台上均为 64 位。

  - 求值器现在以 JSON 格式输出性能分析统计（通过环境变量 `NIX_SHOW_STATS` 和 `NIX_COUNT_CALLS` 启用）。

  - `nix-store --query` 中的 `--xml` 选项已被移除，取而代之的是新增的 `--graphml` 选项，可以以 GraphML 格式输出依赖图。

  - 所有 `nix-*` 命令现在都是指向 `nix` 的符号链接，节省了一些磁盘空间。

  - `nix repl` 现在使用 `libeditline` 或 `libreadline`。
