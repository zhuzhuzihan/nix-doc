# Name

`nix-shell` - 基于 Nix 表达式启动一个交互式 shell

# 概要

`nix-shell`
  [`--arg` *name* *value*]
  [`--argstr` *name* *value*]
  [{`--attr` | `-A`} *attrPath*]
  [`--command` *cmd*]
  [`--run` *cmd*]
  [`--exclude` *regexp*]
  [`--pure`]
  [`--keep` *name*]
  {{`--packages` | `-p`} {*packages* | *expressions*} … | [*path*]}

# 消歧

本手册页描述的是命令 `nix-shell`，它与 `nix
shell` 不同。关于后者的文档，请运行 `nix shell --help` 或查看 `man
nix3-env-shell`。

# 描述

命令 `nix-shell` 会构建指定的
derivation（派生）的依赖，但不构建该 derivation 本身。然后它会启动一个
交互式 shell，其中 derivation *path* 定义的所有环境变量都已被设置为其对应的值，并且
脚本 `$stdenv/setup` 已被 source。这对于重现
derivation 的开发环境很有用。

如果未给出 *path*，`nix-shell` 默认使用 `shell.nix`（如果它
存在），否则使用 `default.nix`。

如果 *path* 以 `http://` 或 `https://` 开头，它会被解释为
一个 tarball 的 URL，该 tarball 将被下载并解压到临时
位置。tarball 必须包含一个单一的顶层目录，
其中至少要有一个名为 `default.nix` 的文件。

如果 derivation 定义了变量 `shellHook`，它会在
`$stdenv/setup` 被 source 之后运行。由于常规 Nix 构建不会执行
这个 hook，它允许你执行 `nix-shell` 特有的
初始化操作。例如，derivation 属性

```nix
shellHook =
  ''
    echo "Hello shell"
    export SOME_API_TOKEN="$(cat ~/.config/some-app/api-token)"
  '';
```

会使 `nix-shell` 打印 `Hello shell` 并将 `SOME_API_TOKEN`
环境变量设置为一个用户配置的值。

# 选项

此处未列出的所有选项都会传递给 `nix-store
--realise`，但 `--arg` 和 `--attr` / `-A` 除外，它们会传递给
`nix-instantiate`。

- `--command` *cmd*

  在 derivation 的环境中，运行 shell 命令 *cmd*。
  此命令在交互式 shell 中执行。（使用 `--run`
  可改用非交互式 shell。）不过，对 `exit` 的调用会被
  隐式添加到命令中，因此 shell 会在
  运行完命令后退出。要避免这一点，请在末尾添加 `return`；
  例如 `--command "echo Hello; return"` 会打印 `Hello`，然后
  让你留在交互式 shell 中。这对于执行
  任何额外的初始化很有用。

- `--run` *cmd*

  类似于 `--command`，但它在非交互式
  shell 中执行命令。这意味着（除其他外）如果你在
  命令运行期间按 Ctrl-C，shell 会退出。

- `--exclude` *regexp*

  不构建任何存储路径匹配正则
  表达式 *regexp* 的依赖。此选项可以多次指定。

- `--pure`

  如果指定此标志，环境会在交互式 shell 启动之前被
  几乎完全清空，因此你会得到一个
  更接近于“真实”Nix 构建的环境。少数几个变量，特别是 `HOME`、`USER` 和 `DISPLAY`，
  会被保留。请注意，用于运行命令的 shell 来自
  [`NIX_BUILD_SHELL`](#env-NIX_BUILD_SHELL) / `NIX_PATH` 中的 `<nixpkgs>`，因此
  不受 `--pure` 影响。

- `--packages` / `-p` *packages*…

  建立一个包含指定软件包的环境。
  命令行参数被解释为 Nix Packages 集合中的属性名。因此，`nix-shell --packages libjpeg openjdk`
  会启动一个包含属性名
  `libjpeg` 和 `openjdk` 所表示软件包的 shell。

- `-i` *interpreter*

  要由 `nix-shell` 调用的链式脚本解释器。仅
  适用于 `#!` 脚本（见下文描述）。

- `--keep` *name*

  当启动 `--pure` shell 时，保留列出的环境变量。

{{#include ./opt-common.md}}

# 环境变量

- <span id="env-NIX_BUILD_SHELL">[`NIX_BUILD_SHELL`](#env-NIX_BUILD_SHELL)</span>

  用于启动交互式环境的 shell。
  默认为 `<nixpkgs>` 中 `bashInteractive` 的 `bash`，如果找不到，则回退到 `PATH` 中的 `bash`。

  > **注意**
  >
  > 用这种方式获得的 shell 不一定与 *path* 中请求的任何 shell 相同。

  <!-- -->

  > **Example
  >
  >  尽管使用了 `--pure`，以下调用不会产生完全可重现的 shell 环境：
  >
  > ```nix
  > #!/usr/bin/env -S nix-shell --pure
  > let
  >   pkgs = import (fetchTarball "https://github.com/NixOS/nixpkgs/archive/854fdc68881791812eddd33b2fed94b954979a8e.tar.gz") {};
  > in
  > pkgs.mkShell {
  >   buildInputs = pkgs.bashInteractive;
  > }
  > ```

{{#include ./env-common.md}}

# 示例

构建软件包 Pan 的依赖，并启动一个
用于构建它的交互式 shell：

```console
$ nix-shell '<nixpkgs>' --attr pan
[nix-shell]$ eval ${unpackPhase:-unpackPhase}
[nix-shell]$ cd $sourceRoot
[nix-shell]$ eval ${patchPhase:-patchPhase}
[nix-shell]$ eval ${configurePhase:-configurePhase}
[nix-shell]$ eval ${buildPhase:-buildPhase}
[nix-shell]$ ./pan/gui/pan
```

我们在这里使用 `eval ${configurePhase:-configurePhase}` 这种形式的原因是：那些覆盖这些 phase 的软件包是通过在同名环境变量中导出覆盖后的值来实现的。
这里 bash 被告知：如果 'configurePhase' 作为变量存在，就求值其内容，否则求值 configurePhase 函数。

先清空环境，并对交互式 shell 做一些额外的自动
初始化：

```console
$ nix-shell '<nixpkgs>' --attr pan --pure \
    --command 'export NIX_DEBUG=1; export NIX_CORES=8; return'
```

Nix 表达式也可以使用 `-E` 和
`-p` 标志在命令行上给出。例如，以下命令会启动一个包含
软件包 `sqlite` 和 `libX11` 的 shell：

```console
$ nix-shell --expr 'with import <nixpkgs> { }; runCommand "dummy" { buildInputs = [ sqlite xorg.libX11 ]; } ""'
```

一种更简短的写法是：

```console
$ nix-shell --packages sqlite xorg.libX11
[nix-shell]$ echo $NIX_LDFLAGS
… -L/nix/store/j1zg5v…-sqlite-3.8.0.2/lib -L/nix/store/0gmcz9…-libX11-1.6.1/lib …
```

请注意，`-p` 接受多个完整的、在上面所示的 `buildInputs = [ ... ]` 中有效的 Nix 表达式，而不仅仅是软件包名称。因此
下面这也是合法的：

```console
$ nix-shell --packages sqlite 'git.override { withManual = false; }'
```

`-p` 标志在 Nix 搜索路径中查找 Nixpkgs。你可以通过传递 `-I` 或设置 `NIX_PATH` 来覆盖它。例如，以下命令
给你一个包含来自 Nixpkgs 特定版本的
Pan 软件包的 shell：

```console
$ nix-shell --packages pan -I nixpkgs=https://github.com/NixOS/nixpkgs/archive/8a3eea054838b55aca962c3fbde9c83c102b8bf2.tar.gz

[nix-shell:~]$ pan --version
Pan 0.139
```

# 用作 `#!` 解释器

你可以将 `nix-shell` 用作脚本解释器，使以任意语言编写的脚本能够通过 Nix 获取自己的依赖。做法是在脚本开头加上以下行：

```bash
#! /usr/bin/env nix-shell
#! nix-shell -i real-interpreter --packages packages
```

其中 *real-interpreter* 是在 `nix-shell` 获取依赖并初始化环境之后将由它调用的“真正的”脚本解释器，而 *packages* 是这些依赖在 Nixpkgs 中的属性名。

以 `#! nix-shell` 开头的行指定 `nix-shell` 选项（见
上文）。注意，你不能写 `#! /usr/bin/env nix-shell -i ...`，
因为许多操作系统在 `#!` 行中只允许一个参数。

例如，下面是一个依赖 Python 和
`prettytable` 软件包的 Python 脚本：

```python
#! /usr/bin/env nix-shell
#! nix-shell -i python3 --packages python3 python3Packages.prettytable

import prettytable

# Print a simple table.
t = prettytable.PrettyTable(["N", "N^2"])
for n in range(1, 10): t.add_row([n, n * n])
print(t)
```

类似地，下面是一个 Perl 脚本，它声明自己需要 Perl 以及
`HTML::TokeParser::Simple`、`LWP` 和
`LWP::Protocol::Https` 软件包：

```perl
#! /usr/bin/env nix-shell
#! nix-shell -i perl 
#! nix-shell --packages perl 
#! nix-shell --packages perlPackages.HTMLTokeParserSimple 
#! nix-shell --packages perlPackages.LWP
#! nix-shell --packages perlPackages.LWPProtocolHttps

use HTML::TokeParser::Simple;

# Fetch nixos.org and print all hrefs.
my $p = HTML::TokeParser::Simple->new(url => 'https://nixos.org/');

while (my $token = $p->get_tag("a")) {
    my $href = $token->get_attr("href");
    print "$href\n" if $href;
}
```

有时你需要传入一个简单的 Nix 表达式来自定义像 Terraform 这样的软件包：

```bash
#! /usr/bin/env nix-shell
#! nix-shell -i bash --packages 'terraform.withPlugins (plugins: [ plugins.openstack ])'

terraform apply
```

> **注意**
>
> 在 nix-shell shebang 中传入简单 Nix 表达式时，必须使用单引号或双引号（`'`、`"`）。

最后，利用多个 nix-shell shebang 的合并功能，下面这个
Haskell 脚本使用 Nixpkgs/NixOS 的特定分支（20.03 稳定
分支）：

```haskell
#! /usr/bin/env nix-shell
#! nix-shell -i runghc --packages 'haskellPackages.ghcWithPackages (ps: [ps.download-curl ps.tagsoup])'
#! nix-shell -I nixpkgs=https://github.com/NixOS/nixpkgs/archive/nixos-20.03.tar.gz

import Network.Curl.Download
import Text.HTML.TagSoup
import Data.Either
import Data.ByteString.Char8 (unpack)

-- Fetch nixos.org and print all hrefs.
main = do
  resp <- openURI "https://nixos.org/"
  let tags = filter (isTagOpenName "a") $ parseTags $ unpack $ fromRight undefined resp
  let tags' = map (fromAttrib "href") tags
  mapM_ putStrLn $ filter (/= "") tags'
```

如果你想更精确，可以指定 Nixpkgs 的特定版本：

    #! nix-shell -I nixpkgs=https://github.com/NixOS/nixpkgs/archive/0672315759b3e15e2121365f067c1c8c56bb4722.tar.gz

上面的示例都使用 `-p` 从 Nixpkgs 获取依赖。你也可以
使用 Nix 表达式来构建自己的依赖。例如，Python 示例也可以写成：

```python
#! /usr/bin/env nix-shell
#! nix-shell deps.nix -i python
```

其中与 `#!` 脚本同目录下的文件 `deps.nix` 包含：

```nix
with import <nixpkgs> {};

runCommand "dummy" { buildInputs = [ python3 python3Packages.prettytable ]; } ""
```

脚本的文件名会作为第一个参数传递给由 `-i` 标志指定的解释器。

除了向操作系统发出指令的非常第一行之外，其余的 `#! nix-shell` 行不需要位于文件开头。
这使得在 `#` 不表示注释开始的语言（例如 ECMAScript、Erlang 或 PHP）中，可以把它们包裹在块注释里。
