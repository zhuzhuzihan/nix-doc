# 安装

本节介绍如何在首次使用时安装和配置 Nix。

目前在 Linux 和 macOS 上的推荐选项是[多用户模式](#multi-user)。

## 多用户模式

这种安装方式比单用户安装提供更好的共享性、更强的隔离性和更高的安全性。

该选项要求满足以下条件之一：

* 运行 systemd 且禁用了 SELinux 的 Linux
* macOS

> **更新到 macOS 15 Sequoia**
>
> 如果你最近更新到了 macOS 15 Sequoia，并且在运行 Nix 命令时遇到
> ```console
> error: the user '_nixbld1' in the group 'nixbld' does not exist
> ```
> 错误，请参阅 GitHub issue [NixOS/nix#10892](https://github.com/NixOS/nix/issues/10892)，了解在不重新安装的情况下修复安装的方法。

```console
$ curl -L https://nixos.org/nix/install | sh -s -- --daemon
```

## 单用户模式

> Mac 不支持单用户模式。

> `warning: installing Nix as root is not supported by this script!`

这种安装方式的要求比多用户安装更低，但它无法提供同等的共享性、隔离性或安全性。

该选项适用于没有 systemd 的系统。

```console
$ curl -L https://nixos.org/nix/install | sh -s -- --no-daemon
```

## 发行版

Nix 社区为多个发行版维护了安装器。

它们可以在 [`nix-community/nix-installers`](https://github.com/nix-community/nix-installers) 仓库中找到。
