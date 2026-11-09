# Release 1.0 (2012-05-11)

自上一个版本以来有大量改进和缺陷修复。以下是最重要的几项：

  - Nix 现在可以选择使用 Boehm 垃圾回收器。这显著降低了 Nix 求值器的内存占用，尤其是在对大型 NixOS 系统配置求值时。可以使用 `--enable-gc` configure 选项启用它。

  - Nix 现在将 SQLite 用作其数据库。这比旧的*ad hoc*格式更快、更灵活。SQLite 还被用来缓存 `/nix/var/nix/manifests` 中的 manifest，带来了显著的提速。

  - Nix 现在有了表达式的搜索路径。搜索路径通过环境变量 `NIX_PATH` 和命令行选项 `-I` 设置。在 Nix 表达式中，尖括号之间的路径用于指定必须在搜索路径中查找的文件。例如，表达式 `<nixpkgs/default.nix>` 会相对于搜索路径中的每个元素查找文件 `nixpkgs/default.nix`。

  - 新命令 `nix-build --run-env` 构建 derivation（派生）的所有依赖，然后在一个包含 derivation 中所有变量的环境中启动 shell。这对在开发中复现某个 derivation 的环境很有用。

  - 新命令 `nix-store --verify-path` 验证存储路径的内容未被改变。

  - 新命令 `nix-store --print-env` 以 shell 可求值的格式打印出 derivation 的环境。

  - 属性名现在可以是任意字符串。例如，你可以写 `{ "foo-1.2" = …; "bla bla" = …; }."bla
                    bla"`。

  - 属性选择现在可以使用 `or` 运算符提供默认值。例如，表达式 `x.y.z or e` 在属性 `x.y.z` 存在时求值为该属性，否则求值为 `e`。

  - `?` 运算符的右侧现在可以是属性路径，例如 `attrs ?
                    a.b.c`。

  - 在 Linux 上，Nix 现在会在支持的文件系统上将 Nix store 中的文件设为不可变。这可以防止 root 用户意外修改 store 中的文件。

  - Nix 对具有多个输出的 derivation 提供了初步支持。这很有用，因为它允许软件包的各个部分被分别部署和垃圾回收。例如，软件包的开发部分（如头文件或静态库）通常不属于某个应用程序的闭包，从而降低磁盘占用并缩短安装时间。

  - Nix store 垃圾回收器更快了，并且持有全局锁的时间更短。

  - 选项 `--timeout`（对应配置项 `build-timeout`）允许你对构建设置一个绝对超时——如果构建运行超过给定的秒数，它会被终止。这对从陷入无限循环却持续产生输出、因而 `--max-silent-time` 不起作用的构建中自动恢复很有用。

  - Nix 的开发已迁移到 GitHub（<https://github.com/NixOS/nix>）。
