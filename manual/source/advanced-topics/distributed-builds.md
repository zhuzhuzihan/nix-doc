# 远程构建

本地 Nix 安装可以把 Nix 构建转发给其他机器，这样多个构建就可以并行执行。

远程构建还允许 Nix 以半透明的方式执行跨平台构建。例如，如果你在一台 `i686-linux` 机器上为 `aarch64-darwin` 执行构建，只要有一台 `aarch64-darwin` 机器可用，Nix 就可以自动把构建转发过去。

## 前提条件

本地机器要把构建转发给远程机器，远程机器必须：

- 已安装 Nix
- 正在运行 SSH 服务器，例如 `sshd`
- 可以通过网络从本地机器通过 SSH 访问
- 在 `/etc/ssh/authorized_keys.d/<username>` 中拥有本地机器的公钥
- 其 SSH 用户名出现在 `nix.conf` 的 `trusted-users` 设置中

## 测试

要测试能否连接到远程 [Nix 实例]（此处为 `mac`），运行：

```console
nix store info --store ssh://username@mac
```

要在远程 store URI 中指定 SSH 身份文件，请添加一个查询参数，例如：

```console
nix store info --store ssh://username@mac?ssh-key=/home/alice/my-key
```

由于构建应当是非交互式的，密钥不应设置密码短语（passphrase）。另外，你也可以提前把身份加载到 `ssh-agent` 或 `gpg-agent` 中。

在多用户安装（默认）中，构建由 Nix 守护进程执行。Nix 守护进程无法通过终端或 `ssh-agent` 提示输入密码短语，因此 SSH 密钥必须没有密码短语。

此外，Nix 守护进程的用户（通常是 root）需要对远程构建机具有 SSH 访问权限。

可以通过运行 `sudo su`，然后验证 SSH 访问（例如运行 `ssh mac`）来确认访问权限。root 用户的 SSH 身份文件通常存放在 `/root/.ssh/`（Linux）或 `/var/root/.ssh`（MacOS）。

如果你遇到错误

```console
bash: nix: command not found
error: cannot connect to 'mac'
```

那么你需要确保非交互式登录 shell 的 `PATH` 中包含 Nix。

[远程构建机列表](@docroot@/command-ref/conf-file.md#conf-builders)可以在命令行或 Nix 配置文件中指定。例如，以下命令让你在一台 Linux 机器上为 `aarch64-darwin` 构建一个 derivation：

```console
uname
```

```console
Linux
```

```console
nix build --impure \
 --expr '(with import <nixpkgs> { system = "aarch64-darwin"; }; runCommand "foo" {} "uname > $out")' \
 --builders 'ssh://mac aarch64-darwin'
```

```console
[1/0/1 built, 0.0 MiB DL] building foo on ssh://mac
```

```console
cat ./result
```

```console
Darwin
```

可以用分号或换行分隔来指定多台构建机，例如：

```console
  --builders 'ssh://mac aarch64-darwin ; ssh://beastie x86_64-freebsd'
```

远程构建机也可以在 [`nix.conf`](@docroot@/command-ref/conf-file.md) 中配置，例如：

    builders = ssh://mac aarch64-darwin ; ssh://beastie x86_64-freebsd

修改 `nix.conf` 之后，需要重启 Nix 守护进程才能使更改生效。

最后，远程构建机还可以在一个单独的配置文件中配置，并通过语法 `@/path/to/file` 在 `builders` 中引入。例如，

    builders = @/etc/nix/machines

会使 `/etc/nix/machines` 中的机器列表被引入。（这是默认行为。）

[Nix 实例]: @docroot@/glossary.md#gloss-nix-instance
