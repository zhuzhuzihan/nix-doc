# 通过 HTTP 提供 Nix store 服务

你可以轻松地通过 HTTP 共享一台机器上的 Nix store。这样其他机器就可以从该机器获取存储路径（store path），从而加快安装速度。它使用的正是 Nix 通常用来从 <https://cache.nixos.org> 获取预构建二进制产物的*二进制缓存*（binary cache）机制。

通过 HTTP 处理二进制缓存请求的守护进程 `nix-serve` 并不属于 Nix 发行版的一部分，但你可以从 Nixpkgs 安装它：

```console
$ nix-env --install --attr nixpkgs.nix-serve
```

然后就可以启动服务器，让它在你喜欢的任意端口上监听 HTTP 连接：

```console
$ nix-serve -p 8080
```

要检查它是否正常工作，可以在客户端尝试获取 [`nix-cache-info`](@docroot@/protocols/binary-cache/nix-cache-info.md) 文件：

```console
$ curl http://avalon:8080/nix-cache-info
StoreDir: /nix/store
WantMassQuery: 1
Priority: 30
```

在向二进制缓存写入时（例如使用 [`nix copy`](@docroot@/command-ref/new-cli/nix3-copy.md)），如果 [`nix-cache-info`](@docroot@/protocols/binary-cache/nix-cache-info.md) 不存在，Nix 会自动创建它。

在客户端，你可以通过 `--substituters` 告诉 Nix 使用你的二进制缓存，例如：

```console
$ nix-env --install --attr nixpkgs.firefox --substituters http://avalon:8080/
```

选项 `substituters` 告诉 Nix 在使用默认缓存（如 <https://cache.nixos.org>）之外，同时使用这个二进制缓存。因此，对于 Firefox 闭包（closure）中的任何路径，Nix 会先检查该路径在服务器 `avalon` 或其他二进制缓存上是否可用；如果没有，则会退回到从源码构建。

你也可以通过在 `nix.conf` 配置文件中添加如下一行，让 Nix 始终使用你的二进制缓存：

    substituters = http://avalon:8080/ https://cache.nixos.org/
