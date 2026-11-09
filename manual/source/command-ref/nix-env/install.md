# Name

`nix-env --install` - 向用户环境添加软件包

概要

`nix-env` {`--install` | `-i`} *args…*
  [{`--prebuilt-only` | `-b`}]
  [{`--attr` | `-A`}]
  [`--from-expression`] [`-E`]
  [`--from-profile` *path*]
  [`--preserve-installed` | `-P`]
  [`--remove-all` | `-r`]
  [`--priority` *priority*]

# 描述

`--install` 操作会创建一个新的用户环境。
它基于当前激活的 [profile](@docroot@/command-ref/files/profiles.md) 的当前 generation，并向其中添加由 *args* 描述的一组[存储路径]。

[store paths]: @docroot@/store/store-path.md

参数 *args* 可以通过以下多种方式映射到存储路径：

- 默认情况下，*args* 是一组名称，表示[默认 Nix 表达式]中的 derivation（派生）。
  这些 derivation 会被[实例化（realise）]，生成的输出路径会被安装。
  如果当前已安装的 derivation 中存在与要添加的 derivation 同名的项，则会被移除，除非指定了选项 `--preserve-installed`。

  [derivation expression]: @docroot@/glossary.md#gloss-derivation-expression
  [default Nix expression]: @docroot@/command-ref/files/default-nix-expression.md
  [realised]: @docroot@/glossary.md#gloss-realise

  如果有多个与 *args* 中某个名称匹配、且名称相同的 derivation（例如 `gcc-3.3.6` 和 `gcc-4.1.1`），则使用*优先级*最高的 derivation。
  derivation 可以通过声明 `meta.priority` 属性来定义优先级。
  该属性应为数字，值越大表示优先级越低。
  默认优先级为 `5`。

  如果多个匹配的 derivation 具有相同的优先级，则会安装版本最高的那个。

  你可以通过明确指定版本号来强制安装多个同名 derivation。
  例如，`nix-env --install
  gcc-3.3.6 gcc-4.1.1` 会同时安装 GCC 的两个版本（并且很可能会导致用户环境冲突\！）。

- 如果指定了 [`--attr`](#opt-attr) / `-A`，则参数是*属性路径*，用于从[默认 Nix 表达式]中选择属性。
  这比使用 derivation 名称更快，而且没有歧义。
  使用 [`nix-env --query`](./query.md) 查看可用软件包的属性路径：

  ```console
  nix-env --query --available --attr-path
  ```

- 如果给定了 `--from-profile` *path*，则 *args* 是一组名称，表示 profile *path* 中已安装的[存储路径]。
  这是在不同 profile 之间复制用户环境元素的简便方法。

- 如果给定了 `--from-expression`，则 *args* 是 [Nix 语言函数](@docroot@/language/syntax.md#functions)，它们会以[默认 Nix 表达式]作为唯一参数被调用。
  这些函数调用返回的 derivation 会被安装。
  这允许以无歧义的方式指定 derivation，当存在多个同名 derivation 时这是必需的。

- 如果给定了 `--priority` *priority*，则被安装的 derivation 的优先级会被设置为 *priority*。
  这可用于覆盖被安装 derivation 的优先级。
  当 *args* 是[存储路径]（它们不携带任何优先级信息）时，这个选项很有用。

- 如果 *args* 是指向 [store derivation] 的[存储路径]，那么这些 store derivation 会被[实例化（realise）]，生成的输出路径会被安装。

- 如果 *args* 是不指向 store derivation 的[存储路径]，那么它们会被直接[实例化（realise）]并安装。

- 默认情况下，每个 [store derivation] 的所有[输出](@docroot@/language/derivations.md#attr-outputs)都会被安装。
  可以通过在 derivation 上添加 `meta.outputsToInstall` 属性并列出输出名称的子集来改变这一行为。

  示例：

  文件 `example.nix` 定义了一个具有两个输出 `foo` 和 `bar` 的 derivation，每个输出中各包含一个文件。

  ```nix
  # example.nix
  let
    pkgs = import <nixpkgs> {};
    command = ''
      ${pkgs.coreutils}/bin/mkdir -p $foo $bar
      echo foo > $foo/foo-file
      echo bar > $bar/bar-file
    '';
  in
  derivation {
    name = "example";
    builder = "${pkgs.bash}/bin/bash";
    args = [ "-c" command ];
    outputs = [ "foo" "bar" ];
    system = builtins.currentSystem;
  }
  ```

  从该 Nix 表达式安装会使两个输出的文件都出现在当前 profile 中。

  ```console
  $ nix-env --install --file example.nix
  installing 'example'
  $ ls ~/.nix-profile
  foo-file
  bar-file
  manifest.nix
  ```

  在该 derivation 上添加 `meta.outputsToInstall` 将使 `nix-env` 只安装来自指定输出的文件。

  ```nix
  # example-outputs.nix
  import ./example.nix // { meta.outputsToInstall = [ "bar" ]; }
  ```

  ```console
  $ nix-env --install --file example-outputs.nix
  installing 'example'
  $ ls ~/.nix-profile
  bar-file
  manifest.nix
  ```

[store derivation]: @docroot@/glossary.md#gloss-store-derivation

# 选项

- `--prebuilt-only` / `-b`

  只使用已注册了 substitute 的 derivation，即存在可以直接下载的预构建二进制文件，用来替代构建该 derivation。
  因此，不会有任何软件包从源码构建。

- `--preserve-installed` / `-P`

  不移除与被安装 derivation 同名的 derivation。
  通常，在同一 generation 的 profile 中安装同一软件包的两个版本，会因为两个版本之间的文件名冲突而导致构建该 generation 时出错。
  不过，并非所有软件包都是如此。

- `--remove-all` / `-r`

  先移除所有先前安装的软件包。
  这等效于先运行 `nix-env --uninstall '.*'`，区别在于所有操作都发生在单个事务中。

{{#include ./opt-common.md}}

{{#include ../opt-common.md}}

{{#include ./env-common.md}}

{{#include ../env-common.md}}

# 示例

使用当前激活 Nix 表达式中特定的属性路径安装软件包：

```console
$ nix-env --install --attr gcc40mips
installing `gcc-4.0.2'
$ nix-env --install --attr xorg.xorgserver
installing `xorg-server-1.2.0'
```

使用 derivation 名称安装特定版本的 `gcc`：

```console
$ nix-env --install gcc-3.3.2
installing `gcc-3.3.2'
uninstalling `gcc-3.1'
```

推荐使用属性路径来选择软件包，因为它快得多，而且不会出现多个匹配。

注意先前安装的版本被移除了，因为没有指定 `--preserve-installed`。

安装任意版本：

```console
$ nix-env --install gcc
installing `gcc-3.3.2'
```

安装 Nix 表达式 `foo.nix` 中的所有 derivation：

```console
$ nix-env --file ~/foo.nix --install '.*'
```

从另一个 profile 复制符号名为 `gcc` 的存储路径：

```console
$ nix-env --install --from-profile /nix/var/nix/profiles/foo gcc
```

安装特定的 [store derivation]（通常由 `nix-instantiate` 创建）：

```console
$ nix-env --install /nix/store/8la6y31fmm6i4wfmby6avly1wf718xnj-gcc-3.4.3.drv
```

安装特定的输出路径：

```console
$ nix-env --install /nix/store/y3cgx0xj1p4iv9x0pnnmdhr8iyg741vk-gcc-3.4.3
```

从命令行指定的 Nix 表达式安装：

```console
$ nix-env --file ./foo.nix --install --expr \
    'f: (f {system = "i686-linux";}).subversionWithJava'
```

也就是说，该表达式求值为 `(f: (f {system =
"i686-linux";}).subversionWithJava) (import ./foo.nix)`，从而从调用
`./foo.nix` 中定义的函数所返回的属性集中选出 `subversionWithJava` 属性。

dry-run 会告诉你哪些路径将被下载或从源码构建：

```console
$ nix-env --file '<nixpkgs>' --install --attr hello --dry-run
(dry run; not doing anything)
installing ‘hello-2.10’
this path will be fetched (0.04 MiB download, 0.19 MiB unpacked):
  /nix/store/ikwkxz4wwlp2g1428n7dy729cg1d9hin-hello-2.10
  ...
```

从 Nixpkgs/NixOS 14.12 channel 的最新版本安装 Firefox：

```console
$ nix-env --file https://github.com/NixOS/nixpkgs/archive/nixos-14.12.tar.gz --install --attr firefox
```
