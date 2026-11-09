# Name

`nix-env --set-flag` - 修改已安装软件包的 meta 属性

概要

`nix-env` `--set-flag` *name* *value* *drvnames*

# 描述

`--set-flag` 操作允许修改已安装软件包的 meta 属性。
有几个属性可以有效地修改，因为它们会影响 `nix-env` 或用户环境构建脚本的行为：

- `priority` 可以修改以解决文件名冲突。
  用户环境构建脚本使用 derivation（派生）的 `meta.priority` 属性来解决软件包之间的文件名冲突。
  优先级值越小表示优先级越高。
  例如，Nixpkgs 中的 GCC wrapper 软件包和 Binutils 软件包都包含文件
  `bin/ld`，因此以前如果同时安装两者就会产生冲突。
  而现在，GCC wrapper 声明的优先级高于 Binutils，因此前者的 `bin/ld` 会被符号链接到用户环境中。

- `keep` 可以设置为 `true`，以防止该软件包被升级或替换。
  当你想保留软件包的旧版本时，这很有用。

- `active` 可以设置为 `false` 来"禁用"该软件包。
  也就是说，不会为该软件包的文件生成符号链接，但它仍然是 profile 的一部分（因此不会被垃圾回收）。
  可以重新设置为 `true` 来重新启用该软件包。

{{#include ./opt-common.md}}

{{#include ../opt-common.md}}

{{#include ../env-common.md}}

# 示例

防止当前安装的 Firefox 被升级：

```console
$ nix-env --set-flag keep true firefox
```

此后，`nix-env --upgrade ` 会忽略 Firefox。

禁用当前安装的 Firefox，然后安装一个新的 Firefox，同时旧版本仍然是 profile 的一部分：

```console
$ nix-env --query
firefox-2.0.0.9 (the current one)

$ nix-env --preserve-installed --install firefox-2.0.0.11
installing `firefox-2.0.0.11'
building path(s) `/nix/store/myy0y59q3ig70dgq37jqwg1j0rsapzsl-user-environment'
collision between `/nix/store/...-firefox-2.0.0.11/bin/firefox'
  and `/nix/store/...-firefox-2.0.0.9/bin/firefox'.
(i.e., can’t have two active at the same time)

$ nix-env --set-flag active false firefox
setting flag on `firefox-2.0.0.9'

$ nix-env --preserve-installed --install firefox-2.0.0.11
installing `firefox-2.0.0.11'

$ nix-env --query
firefox-2.0.0.11 (the enabled one)
firefox-2.0.0.9 (the disabled one)
```

让来自 `binutils` 的文件优先于来自 `gcc` 的文件：

```console
$ nix-env --set-flag priority 5 binutils
$ nix-env --set-flag priority 10 gcc
```
