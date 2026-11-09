# Release 1.7 (2014-04-11)

除了常规的缺陷修复之外，本版本还包含以下新特性：

  - 反引号插入（antiquotation）现在可以用在带引号的属性名中（例如 `set."${foo}"`）。当属性名只是一次单独的反引号插入时，引号可以省略（例如上面的例子可以写成 `set.${foo}`）。如果 set 声明中的属性名求值为 `null`（例如 `{ ${null} = false; }`），那么该属性不会被加入这个 set。

  - 为密码学签名的二进制缓存提供了实验性支持。详见[该 commit](https://github.com/NixOS/nix/commit/0fdf4da0e979f992db75cc17376e455ddc5a96d8)。

  - 一个实验性的新替代器（substituter）`download-via-ssh`，可通过 SSH 从远程机器获取二进制文件。指定标志 `--option use-ssh-substituter true --option ssh-substituter-hosts user@hostname` 会让 Nix 从指定机器下载二进制文件（如果它有这些文件）。

  - `nix-store -r` 和 `nix-build` 新增标志 `--check`，用于把先前构建过的 derivation（派生）再构建一遍，如果输出不完全相同则打印错误信息。这有助于验证一个 derivation 是否真正具有确定性。例如：
    
        $ nix-build '<nixpkgs>' -A patchelf
        …
        $ nix-build '<nixpkgs>' -A patchelf --check
        …
        error: derivation `/nix/store/1ipvxs…-patchelf-0.6' may not be deterministic:
          hash mismatch in output `/nix/store/4pc1dm…-patchelf-0.6.drv'

  - `nix-instantiate` 的标志 `--eval-only` 和 `--parse-only` 已分别更名为 `--eval` 和 `--parse`。

  - `nix-instantiate`、`nix-build` 和 `nix-shell` 现在都有一个标志 `--expr`（或 `-E`），允许你把要求值的表达式作为命令行参数指定。例如，`nix-instantiate --eval -E '1 + 2'` 会打印 `3`。

  - `nix-shell` 的改进：
    
      - 新增标志 `--packages`（或 `-p`），用于搭建一个包含来自 Nixpkgs 的指定软件包的构建环境。例如，命令
            
            $ nix-shell -p sqlite xorg.libX11 hello
            
        会启动一个包含这些软件包的 shell。
    
      - 它现在默认使用 `shell.nix` 作为表达式，若前者不存在则回退到 `default.nix`。这样在你的项目中放一个 `shell.nix` 来搭建舒适的开发环境就非常方便。
    
      - 如果设置了 derivation 属性 `shellHook`，它会对该属性求值。由于 `stdenv` 通常不执行这个钩子，这让你可以做 `nix-shell` 特有的设置。
    
      - 它会保留用户的时区设置。

  - 在 chroot 中，Nix 现在会搭建一个只包含最小设备集合的 `/dev`（例如 `/dev/null`）。注意，只有当你的 `build-chroot-dirs` 设置中*没有*列出 `/dev` 时它才会这样做；否则，它会把 chroot 外部的 `/dev` bind-mount 进来。
    
    类似地，如果 `build-chroot-dirs` 中没有列出 `/dev/pts`，Nix 会在 chroot 的 `/dev/pts` 上挂载一个私有的 `devpts` 文件系统。

  - 新增内置函数：`builtins.toJSON`，它返回一个值的 JSON 表示。

  - `nix-env -q` 新增标志 `--json`，以 JSON 形式打印已安装或可用的软件包。

  - `nix-env` 现在支持取值更复杂的 meta 属性，例如属性集。

  - `-A` 标志现在允许属性名中包含点号，例如
    
        $ nix-instantiate --eval '<nixos>' -A 'config.systemd.units."nscd.service".text'

  - `nix-store --gc` 的 `--max-freed` 选项现在接受单位后缀。例如，`nix-store --gc --max-freed 1G` 最多会释放 1 GB 的磁盘空间。

  - `nix-collect-garbage` 新增标志 `--delete-older-than` *N*`d`，它会删除所有早于 *N* 天的用户环境代（generation）。同样，`nix-env --delete-generations` 也接受 *N*`d` 形式的时限。

  - Nix 现在会启发式地检测构建失败是否由磁盘空间耗尽导致。如果是，该构建不会被标记为"永久失败"。这对 Hydra 尤其有用，因为它需要区分永久性和暂时性的构建失败。

  - 新增符号 `__curPos`，它会展开为一个包含其文件名以及行号和列号的属性集，例如 `{ file = "foo.nix"; line = 10; column = 5; }`。同时还新增了内置函数 `unsafeGetAttrPos`，它返回某个属性的位置。Nixpkgs 用它在错误信息中提供位置信息，例如
    
        $ nix-build '<nixpkgs>' -A libreoffice --argstr system x86_64-darwin
        error: the package ‘libreoffice-4.0.5.2’ in ‘.../applications/office/libreoffice/default.nix:263’
          is not supported on ‘x86_64-darwin’

  - 垃圾回收器现在与其他 Nix 进程的并发性更好，因为它会更早释放某些锁。

  - 二进制 tarball 安装器得到了改进。现在你可以通过运行以下命令来安装 Nix：
    
        $ bash <(curl -L https://nixos.org/nix/install)

  - 更多求值错误包含位置信息。例如，选择一个不存在的属性会打印类似如下的内容
    
        error: attribute `nixUnstabl' missing, at /etc/nixos/configurations/misc/eelco/mandark.nix:216:15

  - 命令 `nix-setuid-helper` 已被移除。

  - Nix 不再使用 Automake，而是改用非递归的、基于 GNU Make 的构建系统。

  - 所有已安装的库现在都以 `libnix` 为前缀。特别是，这去掉了 `libutil`——它可能与来自其他软件包的同名库发生冲突。

  - Nix 现在要求编译器支持 C++11。

本版本包含 Danny Wilson、Domen Kožar、Eelco Dolstra、Ian-Woo Kim、Ludovic Courtès、Maxim Ivanov、Petr Rockai、Ricardo M. Correia 和 Shea Levy 的贡献。
