# 环境变量

要使用 Nix，需要设置一些环境变量。特别是，`PATH` 应包含 `prefix/bin` 和 `~/.nix-profile/bin` 目录。前一个目录包含 Nix 工具本身，而 `~/.nix-profile` 是指向当前*用户环境*（一个自动生成的、由指向已安装软件包的符号链接组成的软件包）的符号链接。设置所需环境变量最简单的方式，是在你的 `~/.profile`（或类似文件）中包含文件 `prefix/etc/profile.d/nix.sh`，如下所示：

```bash
source prefix/etc/profile.d/nix.sh
```

# `NIX_SSL_CERT_FILE`

如果你需要指定自定义证书包，以应对进行 HTTPS 拦截的中间人（man in the middle）代理，就必须在环境变量 `NIX_SSL_CERT_FILE` 中指定证书包的路径。

如果不手动指定 `NIX_SSL_CERT_FILE`，Nix 会安装并使用它自己的证书包。

设置该环境变量并安装 Nix：

```console
$ export NIX_SSL_CERT_FILE=/etc/ssl/my-certificate-bundle.crt
$ curl -L https://nixos.org/nix/install | sh
```

在 shell profile 和 rc 文件（例如 `/etc/bashrc`、`/etc/zshrc`）中，添加以下行：

```bash
export NIX_SSL_CERT_FILE=/etc/ssl/my-certificate-bundle.crt
```

> **注意**
>
> 你不得先添加 export 再执行安装，因为 Nix 安装器会检测到已存在的 Nix 配置并中止。

如果你使用 Nix daemon（守护进程），还应将以下内容添加到 `/etc/nix/nix.conf`：

```
ssl-cert-file = /etc/ssl/my-certificate-bundle.crt
```

## 代理环境变量

Nix 安装器对以下与代理相关的环境变量有特殊处理：`http_proxy`、`https_proxy`、`ftp_proxy`、`all_proxy`、`no_proxy`、`HTTP_PROXY`、`HTTPS_PROXY`、`FTP_PROXY`、`ALL_PROXY`、`NO_PROXY`。

如果在运行 Nix 安装器时设置了其中任何一个变量，安装器将在 `/etc/systemd/system/nix-daemon.service.d/override.conf` 创建一个 override 文件，使 `nix-daemon` 使用这些变量。
