# 升级 Nix

> **注意**
>
> 这些升级说明适用于按照[本手册中的安装说明](./index.md)安装 Nix 的情况。

检查将安装哪个 Nix 版本，例如来自[发布 channel](http://channels.nixos.org/) 之一的 `nixpkgs-unstable`：

```console
$ nix-shell -p nix -I nixpkgs=channel:nixpkgs-unstable --run "nix --version"
nix (Nix) 2.18.1
```

> **警告**
>
> 使用较新版本的 Nix 写入[本地 store](@docroot@/store/types/local-store.md)，例如用 [`nix-build`](@docroot@/command-ref/nix-build.md) 或 [`nix-store --realise`](@docroot@/command-ref/nix-store/realise.md) 构建 derivation（派生），可能会更改数据库 schema！
> 因此，回退到较旧版本的 Nix 可能需要先清除 store 数据库才能使用。

## Linux 多用户

```console
$ sudo su
# nix-env --install --file '<nixpkgs>' --attr nix cacert -I nixpkgs=channel:nixpkgs-unstable
# systemctl daemon-reload
# systemctl restart nix-daemon
```

## macOS 多用户

```console
$ sudo nix-env --install --file '<nixpkgs>' --attr nix cacert -I nixpkgs=channel:nixpkgs-unstable
$ sudo launchctl remove org.nixos.nix-daemon
$ sudo launchctl load /Library/LaunchDaemons/org.nixos.nix-daemon.plist
```

## 单用户（所有平台）

```console
$ nix-env --install --file '<nixpkgs>' --attr nix cacert -I nixpkgs=channel:nixpkgs-unstable
```
