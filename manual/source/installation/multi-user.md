# 多用户模式

为了允许多个用户安全地共享 Nix store，必须确保用户无法运行会以任意方式修改 Nix store 或数据库的构建器（builder），也无法干扰其他用户启动的构建。否则，用户可能在某个软件包中植入木马，从而危及其他用户的账户。

为防止这种情况，Nix store 及其数据库由某个特权用户（通常是 `root`）所有，而构建器则在特殊的用户账户下执行（通常名为 `nixbld1`、`nixbld2` 等）。当非特权用户运行 Nix 命令时，作用于 Nix store 的操作（例如构建）会被转发给一个以 Nix store/数据库所有者身份运行的 *Nix daemon（守护进程）*，由它执行该操作。

> **注意**
> 
> 多用户模式有一个重要限制：只有 root 和 `nix.conf` 中指定的一组受信任用户才能指定任意的二进制缓存。因此，虽然非特权用户可以从任意的 Nix 表达式安装软件包，但他们可能无法获取预构建的二进制文件。

## 设置构建用户

*构建用户*是执行构建时所使用的特殊 UID。它们应当都是*构建用户组* `nixbld` 的成员。该组不应有其他成员，构建用户也不应是任何其他组的成员。在 Linux 上，可以按如下方式创建该组和用户：

```console
$ groupadd -r nixbld
$ for n in $(seq 1 10); do useradd -c "Nix build user $n" \
    -d /var/empty -g nixbld -G nixbld -M -N -r -s "$(which nologin)" \
    nixbld$n; done
```

这将创建 10 个构建用户。并发构建的数量永远不会超过构建用户的数量，因此如果你预期会同时进行大量构建，可能需要增加这一数量。

## 运行 daemon

[Nix daemon](../command-ref/nix-daemon.md) 应按如下方式启动（以 `root` 身份）：

```console
$ nix-daemon
```

你可能希望把这一行放到系统启动脚本中的某个位置。

要让非特权用户使用 daemon，他们应将 [`NIX_REMOTE` 环境变量](../command-ref/env-common.md)设置为 `daemon`。因此，你应在用户的登录脚本中加入类似下面的一行：

```console
export NIX_REMOTE=daemon
```

## 限制访问

要限制哪些用户可以执行 Nix 操作，可以使用目录 `/nix/var/nix/daemon-socket` 的权限。例如，如果想把 Nix 的使用限制在名为 `nix-users` 的组的成员内，执行：

```console
$ chgrp nix-users /nix/var/nix/daemon-socket
$ chmod ug=rwx,o= /nix/var/nix/daemon-socket
```

这样，不在 `nix-users` 组中的用户就无法连接到 Unix 域套接字 `/nix/var/nix/daemon-socket/socket`，因此无法执行 Nix 操作。
