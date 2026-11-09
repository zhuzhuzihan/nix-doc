# Name

`nix-env` - 操作或查询 Nix 用户环境

# 概要

`nix-env` *operation* [*options*] [*arguments…*]
  [`--option` *name* *value*]
  [`--arg` *name* *value*]
  [`--argstr` *name* *value*]
  [{`--file` | `-f`} *path*]
  [{`--profile` | `-p`} *path*]
  [`--system-filter` *system*]
  [`--dry-run`]

# 描述

命令 `nix-env` 用于操作 Nix 用户环境。用户
环境是某个时间点上可供用户使用的软件包的集合。换句话说，它们是
Nix store 中可用程序的一个合成视图。可能存在许多用户
环境：不同用户可以拥有不同的环境，而且
单个用户也可以在不同的环境之间切换。

`nix-env` 恰好接受一个 *operation* 标志，用于指示
要执行的子命令。可用的操作如下：

- [`--install`](./nix-env/install.md)
- [`--upgrade`](./nix-env/upgrade.md)
- [`--uninstall`](./nix-env/uninstall.md)
- [`--set`](./nix-env/set.md)
- [`--set-flag`](./nix-env/set-flag.md)
- [`--query`](./nix-env/query.md)
- [`--switch-profile`](./nix-env/switch-profile.md)
- [`--list-generations`](./nix-env/list-generations.md)
- [`--delete-generations`](./nix-env/delete-generations.md)
- [`--switch-generation`](./nix-env/switch-generation.md)
- [`--rollback`](./nix-env/rollback.md)

这些页面可以离线查看：

- `man nix-env-<operation>`。

  示例：`man nix-env-install`

- `nix-env --help --<operation>`

  示例：`nix-env --help --install`

# 软件包来源

`nix-env` 可以从多个来源获取软件包：

- derivation（派生）的属性集，来自：
  - [默认 Nix 表达式](@docroot@/command-ref/files/default-nix-expression.md)（默认）
  - 通过 `--file` 指定的 Nix 文件
  - 通过 `--from-profile` 指定的 [profile](@docroot@/command-ref/files/profiles.md)
  - 通过 `--from-expression` 指定的、以默认表达式为参数的函数形式的 Nix 表达式
- [存储路径](@docroot@/store/store-path.md)

# 选择器

若干操作，例如 [`nix-env --query`](./nix-env/query.md) 和 [`nix-env --install`](./nix-env/install.md)，接受一个 *arguments* 列表来指定要操作的软件包。

软件包根据[符号化 derivation 名称](@docroot@/language/derivations.md#attr-name)的 `name` 部分和 `version` 部分来识别：

- `name`：直到第一个后面*没有*跟字母的连字符（`-`）之前（不含该连字符）的所有内容。
- `version`：其余部分，不包括作为分隔符的连字符。

> **示例**
>
> `nix-env` 将符号化 derivation 名称 `apache-httpd-2.0.48` 解析为：
>
> ```json
> {
>   "name": "apache-httpd",
>   "version": "2.0.48"
> }
> ```

> **示例**
>
> `nix-env` 将符号化 derivation 名称 `firefox.*` 解析为：
>
> ```json
> {
>   "name": "firefox.*",
>   "version": ""
> }
> ```

`nix-env` 的 *arguments* 的 `name` 部分被视为扩展正则表达式，并与软件包来源中 derivation 名称的 `name` 部分进行匹配。
匹配区分大小写。
正则表达式后面可以可选地跟一个连字符（`-`）和一个版本号；如果省略，则软件包的任何版本都会匹配。
关于正则表达式的详细信息，请参见 [**regex**(7)](https://linux.die.net/man/7/regex)。

> **示例**
>
> 使用 `nix-env` 查找软件包名称的常见模式：
>
> - `firefox`
>
>   匹配软件包名称 `firefox` 的任意版本。
>
> - `firefox-32.0`
>
>   匹配软件包名称 `firefox` 和版本 `32.0`。
>
> - `gtk\\+`
>
>   匹配软件包名称 `gtk+`。
>   必须用反斜杠（`\`）转义 `+` 字符，以防止它被解释为量词，而反斜杠又必须再用一个反斜杠转义，以确保 shell 将其传递下去。
>
> - `.\*`
>
>   匹配任意软件包名称。
>   这是大多数命令的默认值。
>
> - `'.*zip.*'`
>
>   匹配任何包含字符串 `zip` 的软件包名称。
>   注意其中的点：`'*zip*'` 不起作用，因为在正则表达式中，字符 `*` 被解释为量词。
>
> - `'.*(firefox|chromium).*'`
>
>   匹配任何包含字符串 `firefox` 或 `chromium` 的软件包名称。

# 文件

`nix-env` 操作以下文件。

{{#include ./files/default-nix-expression.md}}

{{#include ./files/profiles.md}}
