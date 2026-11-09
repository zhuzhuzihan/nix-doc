# Name

`nix-env --upgrade` - 升级用户环境中的软件包

概要

`nix-env` {`--upgrade` | `-u`} *args*
  [`--lt` | `--leq` | `--eq` | `--always`]
  [{`--prebuilt-only` | `-b`}]
  [{`--attr` | `-A`}]
  [`--from-expression`] [`-E`]
  [`--from-profile` *path*]
  [`--preserve-installed` | `-P`]

# 描述

upgrade 操作基于当前激活 profile 的当前 generation 创建一个新的用户环境，其中所有在 *args* 所描述的路径集合中存在更新版本的存储路径都会被替换。
没有更新版本的路径保持不变；这不是错误。
如果 *args* 中的某个元素没有匹配到任何已安装的 derivation（派生），也不是错误。

关于 *args* 如何映射到一组存储路径的说明，参见
[`--install`](./install.md)。
如果 *args* 描述了多个具有相同符号名称的存储路径，则只安装版本最高的那个。

# 标志

- `--lt`

  只升级到更新的版本。
  这是默认行为。

- `--leq`

  除了升级到更新的版本之外，还"升级"到具有相同版本的 derivation。
  版本并不是 derivation 的唯一标识，因此可能存在许多版本相同的 derivation。
  此标志可用于在已安装和可用的 derivation 之间强制"同步"。

- `--eq`

  *只*"升级"到具有相同版本的 derivation。
  这看起来没什么用，但实际上很有用，例如当 Nixpkgs 发布了新版本，而你希望用基于更新依赖项构建的同版本软件包替换已安装的应用程序（以减少系统中漂浮的依赖项数量）。

- `--always`

  除了升级到更新的版本之外，还"升级"到具有相同或更低版本的 derivation。
  也就是说，derivation 实际上可能会被降级，取决于当前激活 Nix 表达式中有什么可用。

- `--prebuilt-only` / `-b`

  只使用已注册了 substitute 的 derivation，即存在可以直接下载的预构建二进制文件，用来替代构建该 derivation。
  因此，不会有任何软件包从源码构建。

- `--preserve-installed` / `-P`

  不移除与被安装 derivation 同名的 derivation。
  通常，在同一 generation 的 profile 中安装同一软件包的两个版本，会因为两个版本之间的文件名冲突而导致构建该 generation 时出错。
  不过，并非所有软件包都是如此。

{{#include ./opt-common.md}}

{{#include ../opt-common.md}}

{{#include ./env-common.md}}

{{#include ../env-common.md}}

# 示例

```console
$ nix-env --upgrade --attr nixpkgs.gcc
upgrading `gcc-3.3.1' to `gcc-3.4'
```

当没有可用的更新时，什么都不会发生：

```console
$ nix-env --upgrade --attr nixpkgs.pan
```

尽可能推荐使用 `-A`，因为它更快且没有歧义，但也可以通过匹配 derivation 名称升级到特定版本：

```console
$ nix-env --upgrade gcc-3.3.2 --always
upgrading `gcc-3.4' to `gcc-3.3.2'
```

尝试升级所有内容
（根据 derivation 名称中不含版本号的部分匹配软件包）：

```console
$ nix-env --upgrade
upgrading `hello-2.1.2' to `hello-2.1.3'
upgrading `mozilla-1.2' to `mozilla-1.4'
```

# 版本

upgrade 操作通过查看 derivation `y` 和 `x` 各自的 `name` 属性来判断 `y` 是否是 `x` 的升级。
名称（例如 `gcc-3.3.1`）被拆分为两部分：软件包名
（`gcc`）和版本（`3.3.1`）。
版本部分从第一个后面不紧跟字母的连字符之后开始。
如果 `y` 与 `x` 的软件包名匹配，且 `y` 的版本高于 `x` 的版本，则 `y` 被视为 `x` 的升级。

版本比较的方式是将其拆分为由数字和字母组成的连续组件。
例如，`3.3.1pre5` 被拆分为 `[3, 3, 1,
"pre", 5]`。
然后按字典序（从左到右）比较这些列表。
对应的组件 `a` 和 `b` 按如下方式比较。
如果两者都是数字，则使用整数比较。
如果 `a` 是空字符串而 `b` 是数字，则 `a` 被视为小于 `b`。
特殊的字符串组件 `pre`（表示 *pre-release*，即预发布版）被视为小于其他组件。
字符串组件被视为小于数字组件。
否则，按字典序比较它们（即使用区分大小写的字符串比较）。

以下示例说明了这一点：

    1.0 < 2.3
    2.1 < 2.3
    2.3 = 2.3
    2.5 > 2.3
    3.1 > 2.3
    2.3.1 > 2.3
    2.3.1 > 2.3a
    2.3pre1 < 2.3
    2.3pre3 < 2.3pre12
    2.3a < 2.3c
    2.3pre1 < 2.3c
    2.3pre1 < 2.3q
