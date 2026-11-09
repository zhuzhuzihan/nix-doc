# 使用 `post-build-hook`

# 实现上的注意事项

这里我们使用 post-build hook 向二进制缓存上传内容。这是一个简单且可用的示例，但并不适用于所有使用场景。

post-build hook 程序在每次构建执行完毕后运行，并且会阻塞构建循环。如果 hook 程序失败，构建循环会退出。

具体来说，当互联网连接缓慢或不稳定时，这种实现会让 Nix 变慢甚至无法使用。

更高级的实现可以把存储路径（store path）传递给一个用户提供的守护进程或队列，从而在构建循环之外处理这些存储路径。

# 前提条件

本教程假设你已经将一个 [S3 兼容的二进制缓存](@docroot@/command-ref/new-cli/nix3-help-stores.md#s3-binary-cache-store)配置为 [substituter](../command-ref/conf-file.md#conf-substituters)，并且 `root` 用户的默认 AWS profile 可以上传到该存储桶（bucket）。

# 设置签名密钥

使用 `nix-store --generate-binary-cache-key` 创建我们的公钥和私钥签名密钥。我们将用私钥对路径进行签名，并分发公钥用于验证路径的真实性。

```console
# nix-store --generate-binary-cache-key example-nix-cache-1 /etc/nix/key.private /etc/nix/key.public
# cat /etc/nix/key.public
example-nix-cache-1:1/cKDz3QCCOmwcztD2eV6Coggp6rqc9DGjWv7C0G+rM=
```

然后在任何将要访问该缓存的机器上更新 [`nix.conf`](../command-ref/conf-file.md)。将缓存 URL 添加到 [`substituters`](../command-ref/conf-file.md#conf-substituters)，并将公钥添加到 [`trusted-public-keys`](../command-ref/conf-file.md#conf-trusted-public-keys)：

    substituters = https://cache.nixos.org/ s3://example-nix-cache
    trusted-public-keys = cache.nixos.org-1:6NCHdD59X431o0gWypbMrAURkbJ16ZPMQFGspcDShjY= example-nix-cache-1:1/cKDz3QCCOmwcztD2eV6Coggp6rqc9DGjWv7C0G+rM=

为该缓存执行构建的机器必须使用私钥对 derivation（派生）进行签名。在这些机器上，将密钥文件的路径添加到它们 [`nix.conf`](../command-ref/conf-file.md) 的 [`secret-key-files`](../command-ref/conf-file.md#conf-secret-key-files) 字段中：

    secret-key-files = /etc/nix/key.private

我们会在稍后的步骤中重启 Nix 守护进程。

# 实现构建 hook

将以下脚本写入 `/etc/nix/upload-to-cache.sh`：

```bash
#!/bin/sh

set -eu
set -f # disable globbing
export IFS=' '

echo "Uploading paths" $OUT_PATHS
exec nix copy --to "s3://example-nix-cache" $OUT_PATHS
```

> **注意**
>
> `$OUT_PATHS` 变量是一个以空格分隔的 Nix store 路径列表。在本例中，我们预期并希望 shell 执行词分割（word splitting），使每个输出路径成为 `nix
> store sign` 的一个独立参数。Nix 保证这些路径不会包含任何空格，但存储路径可能包含 glob 字符。`set -f` 用于在 shell 中禁用 glob 展开。
> 如果你还想上传 `.drv` 文件，脚本同样定义了 `$DRV_PATH` 变量，其用法与 `$OUT_PATHS` 相同。

然后确保 hook 程序对 `root` 用户可执行：

```console
# chmod +x /etc/nix/upload-to-cache.sh
```

# 更新 Nix 配置

编辑 `/etc/nix/nix.conf` 来运行我们的 hook，在文件末尾添加以下配置片段：

    post-build-hook = /etc/nix/upload-to-cache.sh

然后重启 `nix-daemon`。

# 测试

构建任意一个 derivation，例如：

```console
$ nix-build --expr '(import <nixpkgs> {}).writeText "example" (builtins.toString builtins.currentTime)'
this derivation will be built:
  /nix/store/s4pnfbkalzy5qz57qs6yybna8wylkig6-example.drv
building '/nix/store/s4pnfbkalzy5qz57qs6yybna8wylkig6-example.drv'...
running post-build-hook '/home/grahamc/projects/github.com/NixOS/nix/post-hook.sh'...
post-build-hook: Signing paths /nix/store/ibcyipq5gf91838ldx40mjsp0b8w9n18-example
post-build-hook: Uploading paths /nix/store/ibcyipq5gf91838ldx40mjsp0b8w9n18-example
/nix/store/ibcyipq5gf91838ldx40mjsp0b8w9n18-example
```

然后从 store 中删除该路径，并尝试从二进制缓存获取（substitute）它：

```console
$ rm ./result
$ nix-store --delete /nix/store/ibcyipq5gf91838ldx40mjsp0b8w9n18-example
```

现在，从缓存把该路径复制回来：

```console
$ nix-store --realise /nix/store/ibcyipq5gf91838ldx40mjsp0b8w9n18-example
copying path '/nix/store/m8bmqwrch6l3h8s0k3d673xpmipcdpsa-example from 's3://example-nix-cache'...
warning: you did not specify '--add-root'; the result might be removed by the garbage collector
/nix/store/m8bmqwrch6l3h8s0k3d673xpmipcdpsa-example
```

# 结论

现在我们拥有了一个配置好的 Nix 安装，它会自动对每次本地构建进行签名并上传到远程二进制缓存。

在将此配置部署到生产环境之前，请务必考虑[实现上的注意事项](#implementation-caveats)。
