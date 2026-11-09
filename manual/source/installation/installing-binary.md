# 安装二进制发行版

> **更新到 macOS 15 Sequoia**
>
> 如果你最近更新到了 macOS 15 Sequoia，并且在运行 Nix 命令时遇到
> ```console
> error: the user '_nixbld1' in the group 'nixbld' does not exist
> ```
> 错误，请参阅 GitHub issue [NixOS/nix#10892](https://github.com/NixOS/nix/issues/10892)，了解在不重新安装的情况下修复安装的方法。

要安装最新版本的 Nix，请运行以下命令：

```console
$ curl -L https://nixos.org/nix/install | sh
```

该命令会为你的平台执行默认类型的安装：

- [多用户安装](#multi-user-installation)：
  - 带 systemd 且无 SELinux 的 Linux
  - macOS
- [单用户安装](#single-user-installation)：
  - 无 systemd 的 Linux
  - 带 SELinux 的 Linux

如果多用户安装支持你的平台，并且你可以通过 `sudo` 进行身份验证，我们推荐使用多用户安装。

安装器可以通过多种命令行参数和环境变量进行配置。
要查看可用的命令行选项：

```console
$ curl -L https://nixos.org/nix/install | sh -s -- --help
```

要了解它会执行哪些操作以及如何进一步定制，请[下载并编辑第二阶段安装脚本](#installing-from-a-binary-tarball)。

# 从 URL 安装指定版本的 Nix

自 1.11.16 起的所有 Nix 版本都有对应的特定版本安装 URL，可在 [releases.nixos.org](https://releases.nixos.org/?prefix=nix/) 找到。
每个版本的目录中包含相应的 SHA-256 哈希值。

所有安装脚本的调用方式都相同：

```console
$ export VERSION=2.19.2 
$ curl -L https://releases.nixos.org/nix/nix-$VERSION/install | sh
```

# 多用户安装

多用户 Nix 安装会为 Nix daemon（守护进程）创建系统用户和系统服务。

支持的系统：

- 运行 systemd 且禁用了 SELinux 的 Linux
- macOS

要明确指示安装器在你的系统上执行多用户安装：

```console
$ bash <(curl -L https://nixos.org/nix/install) --daemon
```

你可以在常用的用户账户或 `root` 下运行此命令。
脚本会按需调用 `sudo`。

# 单用户安装

要在你的系统上明确选择单用户安装：

```console
$ bash <(curl -L https://nixos.org/nix/install) --no-daemon
```

在单用户安装中，`/nix` 由执行安装的用户所有。
如果 `/nix` 尚不存在，脚本会调用 `sudo` 来创建它。
如果你没有 `sudo`，请以 `root` 身份手动创建 `/nix`：

```console
$ su root
# mkdir /nix
# chown alice /nix
```

# 从二进制 tarball 安装

你也可以下载一个包含 Nix 及其所有依赖的二进制 tarball：
- 选择一个[版本](https://releases.nixos.org/?prefix=nix/)和[系统类型](../development/building.md#platforms)
- 下载并解压 tarball
- 运行安装器

> **示例**
>
> ```console
> $ pushd $(mktemp -d)
> $ export VERSION=2.19.2
> $ export SYSTEM=x86_64-linux
> $ curl -LO https://releases.nixos.org/nix/nix-$VERSION/nix-$VERSION-$SYSTEM.tar.xz
> $ tar xfj nix-$VERSION-$SYSTEM.tar.xz
> $ cd nix-$VERSION-$SYSTEM
> $ ./install
> $ popd
> ```

安装器可以通过文件 `install-multi-user` 中声明的环境变量进行定制。

## Linux 发行版的原生软件包

Nix 社区以部分 Linux 发行版的原生打包格式维护了安装器(https://nix-community.github.io/nix-installers/)。

# macOS 安装

<!-- anchors to catch existing links -->
[]{#sect-macos-installation-change-store-prefix}[]{#sect-macos-installation-encrypted-volume}[]{#sect-macos-installation-symlink}[]{#sect-macos-installation-recommended-notes}

我们相信已经彻底解决了如何完美支持现代 macOS 上的只读根文件系统的问题。新安装会自动完成这项处理。

本节此前详细介绍了相关情况、选项和权衡取舍，但现在只概述安装器所做的工作。运行安装器并不需要了解这些内容，不过如果你遇到问题，它们可能有所帮助：

- 为你的 Nix store 创建一个新的 APFS 卷
- 更新 `/etc/synthetic.conf`，指示 macOS 创建一个"合成的"空根目录用于挂载该卷
- 在 `/etc/fstab` 中为该卷指定挂载选项
  - `rw`：读写
  - `noauto`：阻止系统自动挂载该卷（这样下文提到的 LaunchDaemon 可以控制挂载，并避免掩盖该挂载服务的问题）。
  - `nobrowse`：防止 Nix Store 卷出现在你的桌面上；同时也让 Spotlight 不再消耗资源为该卷建立索引
  <!-- TODO:
  - `suid`: 是否遵循 setuid？显然不应该？……

    目前我不想假装自己对 suid/owners 的理解超出现有水平。
    曾有一些关于文件所有权和权限问题的模糊报告，尤其是在云/虚拟机/无头（headless）环境中。
    我个人的猜测是，这与这些环境缺少一个会被委派给 macOS 上初始/管理员账户的 token 有关。
    更多细节参见 scripts/create-darwin-volume.sh。

    无论如何，截至 2021 年 12 月 4 日，suid、owners 以及调用 diskutil enableOwnership
    的某种组合似乎已经让新的报告不再出现。但我还不敢庆祝，因为我们尚未真正命名并
    归档该行为、理解我们修复的是什么，也没有验证这 3 个组成部分都是必需的。
  -->
- 如果你启用了 FileVault
    - 生成一个加密密码
    - 将其存入你的系统钥匙串（Keychain）
    - 使用它加密该卷
- 创建一个系统 LaunchDaemon，在启动过程中尽早挂载该卷，以避免在加载或恢复任何需要访问你的 Nix store 的程序时出现问题
