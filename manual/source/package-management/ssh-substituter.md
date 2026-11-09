# 通过 SSH 提供 Nix store 服务

你可以告诉 Nix 通过 SSH 自动从远程 Nix store 获取所需的二进制产物。例如，以下命令安装 Firefox，并自动获取 Firefox 闭包（closure）中在服务器 `avalon` 上可用的任何存储路径（store path）：

```console
$ nix-env --install --attr nixpkgs.firefox --substituters ssh://alice@avalon
```

它的工作方式类似于 Nix 通常使用的二进制缓存 substituter，只是用 SSH 代替了 HTTP：当需要某个存储路径 `P` 时，Nix 会先检查它是否在 `avalon` 的 Nix store 中可用。如果没有，则退回到使用二进制缓存 substituter，最后退回到从源码构建。

> **注意**
> 
> SSH substituter 目前不支持以交互方式输入 SSH 密码短语（passphrase）。因此，你应当使用 `ssh-add` 将解密后的私钥加载到 `ssh-agent` 中。

你也可以只复制某个存储路径的闭包，而不将它安装到你的 profile 中，例如：

```console
$ nix-store --realise /nix/store/m85bxg…-firefox-34.0.5 --substituters
ssh://alice@avalon
```

这本质上等同于执行

```console
$ nix-copy-closure --from alice@avalon
/nix/store/m85bxg…-firefox-34.0.5
```

你可以利用 SSH 的*强制命令*（forced command）功能，为 SSH substituter 访问设置一个受限用户账户，使其对本地 Nix store 只有只读访问权限，而不能做其他任何事情。例如，将以下行添加到 `sshd_config` 中来限制用户 `nix-ssh`：

    Match User nix-ssh
      AllowAgentForwarding no
      AllowTcpForwarding no
      PermitTTY no
      PermitTunnel no
      X11Forwarding no
      ForceCommand nix-store --serve
    Match All

在 NixOS 上，通过在 `configuration.nix` 中添加以下内容可以达到同样的效果：

```nix
nix.sshServe.enable = true;
nix.sshServe.keys = [ "ssh-dss AAAAB3NzaC1k... bob@example.org" ];
```

其中后一行列出了允许连接的用户公钥。
