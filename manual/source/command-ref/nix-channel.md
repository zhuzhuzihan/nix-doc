# Name

`nix-channel` - 管理 Nix channel

# 概要

`nix-channel` {`--add` url [*name*] | `--remove` *name* | `--list` | `--update` [*names…*] | `--list-generations` | `--rollback` [*generation*] }

# 描述

Channel（通道）是一种引用远程 Nix 表达式并便捷地获取其最新版本的机制。

channel 的组成部分包括：
- <https://channels.nixos.org> 上列出的官方 channel
- 用户专属的[已订阅 channel 列表](#subscribed-channels)
- [已下载的 channel 内容](#channels)
- [Nix 表达式搜索路径](@docroot@/command-ref/conf-file.md#conf-nix-path)，通过 [`-I` 选项](#opt-I)或 [`NIX_PATH` 环境变量](#env-NIX_PATH)设置

> **注意**
>
> 已订阅 channel 的状态独立于依赖它的 Nix 表达式之外。
> 这可能限制可重现性。
>
> 对其他 Nix 表达式的依赖可以显式声明：
> - 在 Nix 表达式中使用 [`fetchurl`](@docroot@/language/builtins.md#builtins-fetchurl)、[`fetchTarball`](@docroot@/language/builtins.md#builtins-fetchTarball) 或 [`fetchGit`](@docroot@/language/builtins.md#builtins-fetchGit)
> - 在命令行调用中使用 [`-I` 选项](@docroot@/command-ref/opt-common.md#opt-I)

该命令具有以下操作：

- `--add` *url* \[*name*\]

  将位于 *url* 的 channel *name* 添加到已订阅 channel 列表中。
  如果省略 *name*，则默认使用 *url* 的最后一个组成部分，并移除 `-stable` 或 `-unstable` 后缀。

  > **注意**
  >
  > `--add` 不会自动执行更新。
  > 请显式使用 `--update`。

  channel URL 必须指向一个包含文件 `nixexprs.tar.gz` 的目录。
  在顶层，该 tarball 必须包含一个带有 `default.nix` 文件的目录，该文件作为 channel 的入口点。

- `--remove` *name*

  从已订阅 channel 列表中移除 channel *name*。

- `--list`

  将所有已订阅 channel 的名称和 URL 打印到标准输出。

- `--update` \[*names*…\]

  下载已订阅 channel 的 Nix 表达式并创建新的 generation。
  如果未指定任何 channel，则更新所有 channel；否则只更新 *names* 中包含的那些。

  > **注意**
  >
  > 下载的 channel 内容会被缓存。
  > 使用 `--tarball-ttl` 或 [`tarball-ttl` 配置选项](@docroot@/command-ref/conf-file.md#conf-tarball-ttl)来更改缓存下载的有效期。

- `--list-generations`

  打印 channel profile 当前所有已存在 generation 的列表。

  工作方式与
  ```
  nix-env --profile /nix/var/nix/profiles/per-user/$USER/channels --list-generations
  ```
  相同。

- `--rollback` \[*generation*\]

  将 channel 回退到上一次调用 `nix-channel --update` 之前的状态。
  你还可以选择指定要恢复的特定 channel *generation* 编号。

{{#include ./opt-common.md}}

{{#include ./env-common.md}}

# 文件

`nix-channel` 操作以下文件。

{{#include ./files/channels.md}}

# 示例

订阅 Nixpkgs channel，并运行来自 GNU Hello 软件包的 `hello`：

```console
$ nix-channel --add https://channels.nixos.org/nixpkgs-unstable
$ nix-channel --list
nixpkgs https://channels.nixos.org/nixpkgs
$ nix-channel --update
$ nix-shell -p hello --run hello
hello
```

使用 `--rollback` 回退 channel 更新：

```console
$ nix-instantiate --eval '<nixpkgs>' --attr lib.version
"22.11pre296212.530a53dcbc9"

$ nix-channel --rollback
switching from generation 483 to 482

$ nix-instantiate --eval '<nixpkgs>' --attr lib.version
"22.11pre281526.d0419badfad"
```

移除一个 channel：

```console
$ nix-channel --remove nixpkgs
$ nix-channel --list
```
