# Name

`nix-copy-closure` - 通过 SSH 向远程机器复制或从远程机器复制 store objects

# 概要

`nix-copy-closure`
  [`--to` | `--from` ]
  [`--gzip`]
  [`--include-outputs`]
  [`--use-substitutes` | `-s`]
  [`-v`]
  [_user_@]_machine_[:_port_] _paths_

# 描述

给定一台机器上的 _paths_，`nix-copy-closure` 会计算这些路径的 [closure（闭包）](@docroot@/glossary.md#gloss-closure)（即它们在 Nix store 中的全部依赖），并通过 SSH 将该闭包中的 [store objects](@docroot@/glossary.md#gloss-store-object) 复制到另一台机器。
它不会复制另一台机器上已经存在的 store objects。

> **注意**
>
> 虽然本地机器使用的 Nix store 可以在命令行上通过 [`--store`](@docroot@/command-ref/conf-file.md#conf-store) 选项指定，但远程机器上要访问的 Nix store 只能在该远程机器上[静态配置](@docroot@/command-ref/conf-file.md#configuration-file)。

由于 `nix-copy-closure` 会调用 `ssh`，你可能需要向远程机器进行身份验证。实际上，你可能会被要求进行 _两次_ 身份验证，因为 `nix-copy-closure` 当前会连接远程机器两次：第一次获取目标机器上缺失的路径集合，第二次发送这些路径的转储。使用公钥身份验证时，可以用 `ssh-agent` 避免输入口令。

# 选项

- `--to`

  将 _paths_ 的闭包从本地机器可访问的 Nix store 复制到远程 _machine_ 的 Nix store。
  这是默认行为。

- `--from`

  将 _paths_ 的闭包从远程 _machine_ 的 Nix store 复制到本地机器指定的 Nix store。

- `--gzip`

  启用 SSH 连接的压缩。

- `--include-outputs`

  同时复制闭包中包含的 [store derivation] 的输出。

  [store derivation]: @docroot@/glossary.md#gloss-store-derivation

- `--use-substitutes` / `-s`

  尝试从 [substitute（替代）源](@docroot@/command-ref/conf-file.md#conf-substituters) 下载目标上缺失的 store objects。
  目标上无法被替代的 store objects 仍会从源正常复制。
  例如，当源机器与目标机器之间的连接很慢，而目标机器与 `cache.nixos.org`（默认的二进制缓存服务器）之间的连接很快时，这就很有用。

{{#include ./opt-common.md}}

# 环境变量

- `NIX_SSHOPTS`

  在命令行上传递给 `ssh` 的附加选项。

{{#include ./env-common.md}}

# 示例

> **示例**
>
> 将 GNU Hello 及其全部依赖复制到一台远程机器：
>
> ```shell-session
> $ storePath="$(nix-build '<nixpkgs>' -I nixpkgs=channel:nixpkgs-unstable -A hello --no-out-link)"
> $ nix-copy-closure --to alice@itchy.example.org "$storePath"
> copying 5 paths...
> copying path '/nix/store/h6q8sqsqfbd3252f9gixqn3z282wds7m-xgcc-13.2.0-libgcc' to 'ssh://alice@itchy.example.org'...
> copying path '/nix/store/imnwvn96lw355giswsk36hx105j4wnpj-libunistring-1.1' to 'ssh://alice@itchy.example.org'...
> copying path '/nix/store/85301indj7scg34spnfczkz72jgv8wa9-libidn2-2.3.7' to 'ssh://alice@itchy.example.org'...
> copying path '/nix/store/ypwfsaljwhzw9iffiysxmxnhjj8v7np0-glibc-2.39-31' to 'ssh://alice@itchy.example.org'...
> copying path '/nix/store/0dklv59zppdsqdvgf0qdvjgzcs5wbwxa-hello-2.12.1' to 'ssh://alice@itchy.example.org'...
> ```

> **示例**
>
> 使用已知的存储路径从远程机器复制 GNU Hello，并运行它：
>
> ```shell-session
> $ storePath="$(nix-instantiate --eval --raw '<nixpkgs>' -I nixpkgs=channel:nixpkgs-unstable -A hello.outPath)"
> $ nix-copy-closure --from alice@itchy.example.org "$storePath"
> $ "$storePath"/bin/hello
> Hello, world!
> ```
