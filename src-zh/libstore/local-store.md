R"(

**Store URL 格式**: `local`, *root*

此 Store 类型直接访问本地文件系统中的 Nix Store
（即不经由 Nix daemon）。*root* 是一个绝对路径，
会被添加到 Nix Store 目录等其他目录之前。
Store 伪 URL `local` 表示以 `/` 作为根目录的 Store。

## 本地 chroot Store {#chroot}

使用 `/` 以外的 *root* 的本地 Store 被称为*本地 chroot Store*。
对于这类 Store，Store 目录在“逻辑上”仍然是
`/nix/store`，因此存放在其中的程序只能通过 `chroot` 进入 *root*
来构建和执行。Chroot Store 仅在启用了 [`mount namespaces`](https://man7.org/linux/man-pages/man7/mount_namespaces.7.html) 和 [`user namespaces`](https://man7.org/linux/man-pages/man7/user_namespaces.7.html) 的
Linux 上支持构建和运行。

例如，下面使用 `/tmp/root` 作为 chroot 环境
来构建或下载 `nixpkgs#hello`，然后执行它：

```console
# nix run --store /tmp/root nixpkgs#hello
Hello, world!
```

这里，“物理” Store 位置是 `/tmp/root/nix/store`，
而 Nix 的 Store 元数据位于 `/tmp/root/nix/var/nix/db`。

也可以把 Nix Store 的“逻辑”位置从默认的 `/nix/store` 改为其他路径，但并不推荐。
这会导致
`https://cache.nixos.org/` 等默认 substitute 站点不可用，
因此你可能不得不在本地构建所有内容。示例如下：

```console
# nix build --store 'local?store=/tmp/my-nix/store&state=/tmp/my-nix/state&log=/tmp/my-nix/log' nixpkgs#hello
```

)"
