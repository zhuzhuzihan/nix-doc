# Release 1.10 (2015-09-03)

这主要是一个缺陷修复版本，同时也包含一些新特性：

  - 新增了多个内建函数，以减少 Nixpkgs/NixOS 的求值时间和内存消耗：`all`、`any`、`concatStringsSep`、`foldl’`、`genList`、`replaceStrings`、`sort`。

  - 垃圾回收器在磁盘满时更加健壮。

  - Nix 支持一个新的构建 derivation（派生）的 API，它不要求磁盘上存在 `.drv` 文件；只需要 derivation 的内存表示。Hydra 持续构建系统用它来提高远程构建的效率。

  - 函数 `<nix/fetchurl.nix>` 现在使用*内建* builder（也就是说，它无需启动外部进程；下载由 Nix 自身完成）。这确保了 derivation 路径在 Nix 升级时不会改变，并且免除了为支持 chroot 执行而采用的丑陋 hack。

  - `--version -v` 现在会打印一些配置信息，特别是启用了哪些编译期可选特性，以及各个目录的路径。

  - 构建用户的补充组现在被正确设置。

本版本包含来自 Eelco Dolstra、Guillaume Maudoux、Iwan Aucamp、Jaka Hudoklin、Kirill Elagin、Ludovic Courtès、Manolis Ragkousis、Nicolas B. Pierron 和 Shea Levy 的贡献。
