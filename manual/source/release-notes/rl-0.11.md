# Release 0.11 (2007-12-31)

Nix 0.11 相较上一个稳定版本有诸多改进。最重要的改进是安全的多用户支持。它还包含许多易用性增强和语言扩展，其中许多是由基于 Nix 的纯函数式 Linux 发行版 NixOS 催生的。以下是（不完整的）列表：

  - 安全的多用户支持。单个 Nix store 现在可以在多个（可能不受信任的）用户之间共享。这对 NixOS 是一项重要特性，它使非 root 用户也能安装软件。旧的在多用户间共享 store 的 setuid 方法已被移除。设置多用户 store 的详细信息见手册。

  - 新命令 `nix-copy-closure` 为你提供了一种在机器之间交换软件的简便高效方式。它通过 `ssh` 将一组存储路径的闭包中缺失的部分复制到远程机器或从远程机器复制过来。

  - 一种新的字符串字面量：夹在双单引号（`''`）之间的字符串会"智能地"去除缩进。这使得大型字符串（例如 NixOS 中的 shell 脚本或配置文件片段）能够整洁地跟随外围表达式的缩进。它需要的转义也少得多，因为 `''` 在大多数语言中都比 `"` 少见。

  - `nix-env` `--set` 修改 profile 的当前代际，使其恰好包含指定的 derivation（派生）而不包含其他内容。例如，`nix-env -p /nix/var/nix/profiles/browser --set
            firefox` 使名为 `browser` 的 profile 仅包含 Firefox。

  - `nix-env` 现在在 profile 中维护已安装软件包的元信息。元信息是 derivation 的 `meta` 属性的内容，例如 `description` 或 `homepage`。命令 `nix-env -q --xml
            --meta` 显示全部元信息。

  - `nix-env` 现在使用 derivation 的 `meta.priority` 属性来解决软件包之间的文件名冲突。优先级值越低表示优先级越高。例如，Nixpkgs 中的 GCC wrapper 软件包和 Binutils 软件包都有文件 `bin/ld`，因此以前如果你尝试同时安装两者就会产生冲突。而现在，GCC wrapper 声明了比 Binutils 更高的优先级，因此前者的 `bin/ld` 会被符号链接到用户环境中。

  - `nix-env -i / -u`：不再按版本决胜软件包的并列关系，而是按优先级和版本号决胜。也就是说，如果有多个同名软件包，则选择优先级最高的那个；只有在多个软件包优先级相同时才使用版本号。
    
    这使得可以在 Nixpkgs 中将某些特定版本/变体标记为比其他版本或多或少更可取。一个典型例子是某个软件包的 beta 版本（例如 `gcc-4.2.0rc1`），即使它是最高版本也不应被安装，除非被显式选择（例如 `nix-env -i
            gcc-4.2.0rc1`）。

  - `nix-env --set-flag` 允许修改已安装软件包的元属性。有若干属性可以被有效地修改，因为它们会影响 `nix-env` 或用户环境构建脚本的行为：
    
      - 可以修改 `meta.priority` 来解决文件名冲突（见上文）。
    
      - 可以将 `meta.keep` 设为 `true` 以防止软件包被升级或替换。当你想保留某个软件包的旧版本时很有用。
    
      - 可以将 `meta.active` 设为 `false` 来"禁用"该软件包。也就是说，不会生成指向该软件包文件的符号链接，但它仍然是 profile 的一部分（因此不会被垃圾回收）。将其重新设为 `true` 可重新启用该软件包。

  - `nix-env -q` 现在有一个标志 `--prebuilt-only`（`-b`），使 `nix-env` 只显示那些输出已在 Nix store 中或可以被 substitute（即从某处下载）的 derivation。换句话说，它显示可以"快速"安装的软件包，即无需从源码构建。`-b` 标志在 `nix-env -i` 和 `nix-env -u` 中也可用，用于过滤掉没有预构建二进制文件的 derivation。

  - 新选项 `--argstr`（在 `nix-env`、`nix-instantiate` 和 `nix-build` 中）与 `--arg` 类似，只是其值为字符串。例如，`--argstr system
            i686-linux` 等价于 `--arg system
            \"i686-linux\"`（注意 `--argstr` 避免了 shell 参数周围恼人的引号）。

  - `nix-store` 有一个新操作 `--read-log`（`-l`）`paths`，显示给定路径的构建日志。

  - Nix 现在使用 Berkeley DB 4.5。数据库会自动升级，但你要小心，不要使用仍然使用 Berkeley DB 4.4 的旧版本 Nix。

  - 选项 `--max-silent-time`（对应配置项 `build-max-silent-time`）允许你为构建设置超时——如果构建在给定的秒数内没有在 `stdout` 或 `stderr` 上产生输出，它会被终止。这对从陷入无限循环的构建中自动恢复很有用。

  - `nix-channel`：每个订阅的 channel 在为该 channel 生成的顶层表达式中都是自己独立的属性。这允许消歧（例如 `nix-env
            -i -A nixpkgs_unstable.firefox`）。

  - substitutes 表已从数据库中移除。这使得 `nix-pull` 和 `nix-channel --update` 等操作快了很多很多。

  - `nix-pull` 现在支持 bzip2 压缩的 manifest。这加快了 channel 的速度。

  - `nix-prefetch-url` 现在有一种有限形式的缓存。`nix-channel` 用它来防止在 channel 未变化时进行不必要的下载。

  - `nix-prefetch-url` 现在默认计算文件的 SHA-256 哈希而不是 MD5 哈希。在调用 `fetchurl` 时，你应当传递 `sha256` 属性而不是 `md5`。哈希可以传十六进制编码或 base-32 编码。

  - Nix 现在可以在自动生成的"chroot"中执行构建。这可以防止 builder 访问 Nix store 之外的内容，从而有助于保证纯净性。这是一个实验性特性。

  - 新命令 `nix-store
            --optimise` 通过在 store 中查找相同的文件并将它们彼此硬链接来减少 Nix store 的磁盘占用。它通常能把 store 的体积减少约 25-35%。

  - `~/.nix-defexpr` 现在可以是一个目录，此时该目录中的 Nix 表达式会被合并成一个属性集，文件名用作属性名。命令 `nix-env
            --import`（用于设置 `~/.nix-defexpr` 符号链接）已被移除。

  - derivation 可以指定新的特殊属性 `allowedReferences`，以强制 derivation 输出中的引用是所声明路径集合的子集。例如，如果 `allowedReferences` 是空列表，则输出不得有任何引用。NixOS 用它来检查生成的文件（例如用于引导 Linux 的初始 ramdisk）没有任何依赖。

  - 新属性 `exportReferencesGraph` 允许 builder 访问其输入的引用图。NixOS 用它来完成诸如生成包含填充了某些路径闭包的 Nix store 的 ISO-9660 镜像之类的任务。

  - 固定输出 derivation（如 `fetchurl`）可以定义属性 `impureEnvVars`，以允许将外部环境变量传递给 builder。Nixpkgs 用它来支持代理配置等。

  - 若干新的内建函数：`builtins.attrNames`、`builtins.filterSource`、`builtins.isAttrs`、`builtins.isFunction`、`builtins.listToAttrs`、`builtins.stringLength`、`builtins.sub`、`builtins.substring`、`throw`、`builtins.trace`、`builtins.readFile`。
