# Name

`nix-env --query` - 显示软件包信息

概要

`nix-env` {`--query` | `-q`} *names…*
  [`--installed` | `--available` | `-a`]
  [{`--status` | `-s`}]
  [{`--attr-path` | `-P`}]
  [`--no-name`]
  [{`--compare-versions` | `-c`}]
  [`--system`]
  [`--drv-path`]
  [`--out-path`]
  [`--description`]
  [`--meta`]
  [`--xml`]
  [`--json`]
  [{`--prebuilt-only` | `-b`}]
  [{`--attr` | `-A`} *attribute-path*]

# 描述

query 操作显示的信息要么关于安装在当前激活 profile 的当前 generation 中的存储路径（`--installed`），要么关于当前激活 Nix 表达式中可供安装的 derivation（派生）（`--available`）。
它只打印符号名称与 *names* 中某一项匹配的 derivation 的信息。

derivation 按 `name` 属性排序。

# 来源选择

以下标志指定查询操作所针对的对象集合。

  - `--installed`

    查询操作针对安装在当前激活 profile 的当前 generation 中的存储路径。
    这是默认值。

  - `--available` / `-a`

    查询操作针对当前激活 Nix 表达式中可用的 derivation。

# 查询项

以下标志指定对选定的 derivation 显示哪些信息。
可以指定多个标志，此时信息按此处给出的顺序显示。
注意，除非指定了 `--no-name`，否则总是显示 derivation 的名称。

  - `--xml`

    以适合其他工具自动处理的 XML 表示形式打印结果。
    根元素名为 `items`，其中每个可用或已安装的 derivation 对应一个 `item` 元素。
    下文讨论的字段都存储在 `item` 元素的属性中。

  - `--json`

    以适合其他工具自动处理的 JSON 表示形式打印结果。

  - `--prebuilt-only` / `-b`

    只显示已注册了 substitute 的 derivation，即存在可以直接下载的预构建二进制文件，用来替代构建该 derivation。
    因此，这会显示所有可能可以快速安装的软件包。

  - `--status` / `-s`

    打印 derivation 的*状态*。
    状态由三个字符组成。
    第一个是 `I` 或 `-`，表示该 derivation 当前是否安装在当前激活 profile 的当前 generation 中。
    对于 `--installed`，按定义这总是成立，但对 `--available` 则不然。
    第二个是 `P` 或 `-`，表示该 derivation 是否存在于系统中。
    这表明安装一个可用的 derivation 是否需要构建。
    第三个是 `S` 或 `-`，表示该 derivation 是否有可用的 substitute。

  - `--attr-path` / `-P`

    打印 derivation 的*属性路径*，可以使用 `--attr` 选项（在 `nix-env --install` 等安装 derivation 的命令中可用）无歧义地选中它。
    此选项只能与 `--available` 一起使用

  - `--no-name`

    不打印每个 derivation 的 `name` 属性。

  - `--compare-versions` / `-c`

    比较已安装版本与可用版本，反之亦然（如果给定了
    `--available`）。
    这有助于快速查看已安装软件包在 Nix 表达式中是否有可用的升级。
    会添加一个具有以下含义的列：

      - `<` *version*

        有更新版本的软件包可用或已安装。

      - `=` *version*

        可用或已安装的软件包版本至多相同。

      - `>` *version*

        只有更旧版本的软件包可用或已安装。

      - `- ?`

        该软件包没有任何版本可用或已安装。

  - `--system`

    打印 derivation 的 `system` 属性。

  - `--drv-path`

    打印指向 [store derivation] 的[存储路径]。

    [store path]: @docroot@/glossary.md#gloss-store-path
    [store derivation]: @docroot@/glossary.md#gloss-derivation

  - `--out-path`

    打印 derivation 的输出路径。

  - `--description`

    打印 derivation 的简短（单行）描述（如果有）。
    描述取自 derivation 的 `meta.description` 属性。

  - `--meta`

    打印 derivation 的所有元属性。
    此选项只能与 `--xml` 或 `--json` 一起使用。

{{#include ./opt-common.md}}

{{#include ../opt-common.md}}

{{#include ./env-common.md}}

{{#include ../env-common.md}}

# 示例

显示已安装的软件包：

```console
$ nix-env --query
bison-1.875c
docbook-xml-4.2
firefox-1.0.4
MPlayer-1.0pre7
ORBit2-2.8.3
…
```

显示可用的软件包：

```console
$ nix-env --query --available
firefox-1.0.7
GConf-2.4.0.1
MPlayer-1.0pre7
ORBit2-2.8.3
…
```

显示可用软件包的状态：

```console
$ nix-env --query --available --status
-P- firefox-1.0.7   (not installed but present)
--S GConf-2.4.0.1   (not present, but there is a substitute for fast installation)
--S MPlayer-1.0pre3 (i.e., this is not the installed MPlayer, even though the version is the same!)
IP- ORBit2-2.8.3    (installed and by definition present)
…
```

显示 Nix 表达式 `foo.nix` 中的可用软件包：

```console
$ nix-env --file ./foo.nix --query --available
foo-1.2.3
```

比较已安装版本与可用版本：

```console
$ nix-env --query --compare-versions
...
acrobat-reader-7.0 - ?      (package is not available at all)
autoconf-2.59      = 2.59   (same version)
firefox-1.0.4      < 1.0.7  (a more recent version is available)
...
```

显示名称中包含 “`zip`” 的所有软件包：

```console
$ nix-env --query --available '.*zip.*'
bzip2-1.0.6
gzip-1.6
zip-3.0
…
```

显示名称中包含 “`firefox`” 或 “`chromium`” 的所有软件包：

```console
$ nix-env --query --available '.*(firefox|chromium).*'
chromium-37.0.2062.94
chromium-beta-38.0.2125.24
firefox-32.0.3
firefox-with-plugins-13.0.1
…
```

显示 Nixpkgs 仓库最新版本中的所有软件包：

```console
$ nix-env --file https://github.com/NixOS/nixpkgs/archive/master.tar.gz --query --available
```
