# Name

`nix.conf` - Nix 配置文件

# 描述

Nix 支持多种配置设置，它们从配置文件读取，或作为命令行标志传入。

## 配置文件

默认情况下，Nix 从以下各个位置读取设置。设置逐层叠加应用，因此后面的设置会覆盖先前的条目。

1. 配置目录中的系统级配置文件 `nix.conf`。

   配置目录默认为 `${sysconfdir}/nix`（即大多数 Unix 系统上的 `/etc/nix`），Windows 上则为 `%PROGRAMDATA%\nix\conf`，可通过 [`NIX_CONF_DIR`](./env-common.md#env-NIX_CONF_DIR) 覆盖。

   在此文件中加载的值不会转发给 Nix daemon（守护进程）。客户端假定 daemon 已经加载了它们。

1. 如果设置了 [`NIX_USER_CONF_FILES`](./env-common.md#env-NIX_USER_CONF_FILES)，则列表中的每个路径会按相反顺序加载。列表分隔符在 Unix 上为 `:`，在 Windows 上为 `;`。

   否则，它会在以下位置查找 `nix.conf`：

   - [用户配置目录](./env-common.md#user-conf-dir)
   - 在 Unix 上，另外还会查找 [`XDG_CONFIG_DIRS`](./env-common.md#env-XDG_CONFIG_DIRS) 中每个目录下的 `nix/nix.conf`

1. 如果设置了 [`NIX_CONFIG`](./env-common.md#env-NIX_CONFIG)，其内容会被视为一个配置文件的内容。特别是，各设置以换行符分隔，与配置文件中一样。

### 文件格式

配置文件由 `name = value` 对组成，每行一个。注释以 `#` 字符开头。

示例：

```
keep-outputs = true       # 开发者友好
keep-derivations = true   # 同上
```

可以使用 `include <path>` 这样的行包含其他文件，其中 `<path>` 相对于当前配置文件解析。文件缺失是一个错误，除非改用 `!include`。

一个配置设置通常会覆盖之前的任何值。但对于接受条目列表的设置，可以在设置名称前加 `extra-` 前缀来*追加*到之前的值。

例如：

```
substituters = a b
extra-substituters = c d
```

将 `substituters` 设置定义为 `a b c d`。

未知的选项名不是错误，只会伴随一条警告被忽略。

## 命令行标志

配置选项可以在命令行上设置，覆盖[配置文件](#configuration-file)中设置的值：

- 每个配置设置都有对应的命令行标志（例如 `--max-jobs 16`）。布尔设置不需要参数，并且可以使用 `no-` 前缀显式禁用（例如 `--keep-failed` 和 `--no-keep-failed`）。

  未知的选项名是无效的标志（除非已经存在同名标志），会以错误形式拒绝。

- 标志 `--option <name> <value>` 的解释方式与设置文件中的 `<name> = <value>` 完全一致。

  未知的选项名会伴随一条警告被忽略。

对于接受条目列表的设置，支持 `extra-` 前缀（例如 `--extra-trusted users alice` 或 `--option extra-trusted-users alice`）。

## 整数设置

整数类型的设置支持后缀 `K`、`M`、`G`
和 `T`。它们会使指定的值分别乘以 2^10、
2^20、2^30 和 2^40。例如，`--min-free 1M` 等价于
`--min-free 1048576`。

# 可用设置
