# 构建 Nix

本节提供一些关于如何着手开发 Nix 的说明。
要从 GitHub 获取最新版本的 Nix：

> **注意**
>
> 在 Windows 上检出该仓库时，请确保在克隆之前已启用 git 设置 `core.symlinks`，因为仓库中包含符号链接。

```console
$ git clone https://github.com/NixOS/nix.git
$ cd nix
```

> **注意**
>
> 以下说明假设你本地已安装某个版本的 Nix，以便用它来搭建开发环境。
> 如果尚未安装，请按照[安装说明](../installation/index.md)操作。


要构建所有依赖并启动一个已设置好所有环境变量（以便能找到这些依赖）的 shell：

```console
$ nix-shell
```

要获取其他[受支持编译环境](#compilation-environments)之一的 shell：

```console
$ nix-shell --attr devShells.x86_64-linux.native-clangStdenv
```

> **注意**
>
> 你可以使用 `native-ccacheStdenv` 来大幅缩短重新构建的时间。
> 默认情况下，[ccache](https://ccache.dev) 将产物保存在 `~/.cache/ccache/` 中。

要在该 shell 中构建 Nix 本身：

```console
[nix-shell]$ out="$(pwd)/outputs/out" dev=$out debug=$out mesonFlags+=" --prefix=${out}"
[nix-shell]$ dontAddPrefix=1 configurePhase
[nix-shell]$ buildPhase
```

要测试它：

```console
[nix-shell]$ checkPhase
```

要将它安装到 `$(pwd)/outputs`：

```console
[nix-shell]$ installPhase
[nix-shell]$ ./outputs/out/bin/nix --version
nix (Nix) 2.12
```

要为当前操作系统和 CPU 架构构建 Nix 的 release 版本：

```console
$ nix-build
```

你也可以为[受支持的平台](#platforms)之一构建 Nix。

## 使用 flakes 构建 Nix

本节假设你使用启用了 [`flakes`] 和 [`nix-command`] 实验性特性的 Nix。

[`flakes`]: @docroot@/development/experimental-features.md#xp-feature-flakes
[`nix-command`]: @docroot@/development/experimental-features.md#xp-feature-nix-command

要构建所有依赖并启动一个已设置好所有环境变量（以便能找到这些依赖）的 shell：

```console
$ nix develop
```

该 shell 还会将 `./outputs/bin/nix` 添加到你的 `$PATH`，这样你可以在构建完成后立即运行 `nix`。

要获取其他[受支持编译环境](#compilation-environments)之一的 shell：

```console
$ nix develop .#native-clangStdenv
```

> **注意**
>
> 使用 `ccacheStdenv` 来大幅缩短重新构建的时间。
> 默认情况下，[ccache](https://ccache.dev) 将产物保存在 `~/.cache/ccache/` 中。

要在该 shell 中构建 Nix 本身：

```console
[nix-shell]$ configurePhase
[nix-shell]$ buildPhase
```

要测试它：

```console
[nix-shell]$ checkPhase
```

要将它安装到 `$(pwd)/outputs`：

```console
[nix-shell]$ installPhase
[nix-shell]$ nix --version
nix (Nix) 2.12
```

关于运行和过滤测试的更多信息，请参见
[`testing.md`](./testing.md)。

要为当前操作系统和 CPU 架构构建 Nix 的 release 版本：

```console
$ nix build
```

你也可以为[受支持的平台](#platforms)之一构建 Nix。

## 平台

Nix 可以在多种平台上构建，如 [`flake.nix`] 中所指定：

[`flake.nix`]: https://github.com/nixos/nix/blob/master/flake.nix

- `x86_64-linux`
- `i686-linux`
- `aarch64-linux`
- `aarch64-darwin`
- `armv6l-linux`
- `armv7l-linux`
- `powerpc64-linux` (ELFv1 ABI)
- `powerpc64le-linux`
- `riscv64-linux`

要为不同于当前平台的平台构建 Nix，你需要有一种方式让当前的 Nix 安装为该平台构建代码。常见方案包括[远程构建机器]和[二进制格式模拟]（仅在 NixOS 上受支持）。

[remote builders]: @docroot@/language/derivations.md#attr-builder
[binary format emulation]: https://nixos.org/manual/nixos/stable/options.html#opt-boot.binfmt.emulatedSystems

在具备这样的环境之后，执行构建只需要选择相应的属性即可。
例如，要为 `aarch64-linux` 编译：

```console
$ nix-build --attr packages.aarch64-linux.default
```

或者，对于启用了 [`flakes`] 和 [`nix-command`] 实验性特性的 Nix：

```console
$ nix build .#packages.aarch64-linux.default
```

交叉编译构建可用于：
- `armv6l-linux`
- `armv7l-linux`
- `powerpc64-linux` (ELFv1 ABI)
- `powerpc64le-linux`
- `riscv64-linux`
在 `flake.nix` 的 `crossSystems` 中添加更多[系统类型](#system-type)，即可在不受支持的平台上引导构建 Nix。

### 同时为多个平台构建

在同一个源码树上执行多个交叉构建和原生构建是很有用的，例如确保对一个平台的更好支持不会破坏另一个平台的构建。好在 Meson 让这一点变得非常简单——它将所有构建产物限制在构建目录中，只需在多个构建目录之间共享同一个源码目录，每个目录各自包含面向不同平台的 Nix 构建。

具体做法如下：

1. 告诉 Nixpkgs 的基础设施我们希望 Meson 把构建目录放在哪里

   ```bash
   mesonBuildDir=build-my-variant-name
   ```

1. 像往常一样配置

   ```bash
   configurePhase
   ```

3. 像往常一样构建

   ```bash
   buildPhase
   ```

## 系统类型

Nix 使用如下格式的字符串来标识它所运行的*系统类型*或*平台*：

```
<cpu>-<os>[-<abi>]
```

它在 Nix 针对给定系统编译时被设定，其依据是 Meson 的 [`host_machine` 信息](https://mesonbuild.com/Reference-manual_builtin_host_machine.html)的输出。

由于历史原因和向后兼容性，一些 CPU 和 OS 标识符会按如下方式转换：

| `host_machine.cpu_family()` | `host_machine.endian()` | Nix                 |
|-----------------------------|-------------------------|---------------------|
| `x86`                       |                         | `i686`              |
| `arm`                       |                         | `host_machine.cpu()`|
| `ppc`                       | `little`                | `powerpcle`         |
| `ppc64`                     | `little`                | `powerpc64le`       |
| `ppc`                       | `big`                   | `powerpc`           |
| `ppc64`                     | `big`                   | `powerpc64`         |
| `mips`                      | `little`                | `mipsel`            |
| `mips64`                    | `little`                | `mips64el`          |
| `mips`                      | `big`                   | `mips`              |
| `mips64`                    | `big`                   | `mips64`            |


在本地开发中使用 Meson 交叉编译 Nix 时，需要通过 `--cross-file` 选项指定一个[交叉文件](https://mesonbuild.com/Cross-compilation.html)。交叉文件定义目标架构和工具链。而使用 Nix 本身交叉编译 Nix 时，Nixpkgs 会替你处理好这些。

在 nix flake 中，我们还提供了一些交叉编译目标：

```
nix build .#nix-everything-riscv64-unknown-linux-gnu
nix build .#nix-everything-armv7l-unknown-linux-gnueabihf
nix build .#nix-everything-armv7l-unknown-linux-gnueabihf
nix build .#nix-everything-x86_64-unknown-freebsd
nix build .#nix-everything-x86_64-w64-mingw32
```

## 编译环境

Nix 可以使用多种环境编译：

- `stdenv`：默认；
- `gccStdenv`：强制使用 `gcc` 编译器；
- `clangStdenv`：强制使用 `clang` 编译器；
- `ccacheStdenv`：启用 [ccache]，这是一种用于加速编译的编译器缓存。

要使用其中某种环境构建，对于支持 flake 的 Nix，可以使用

```console
$ nix build .#nix-cli-ccacheStdenv
```

对于经典 Nix，可以使用

```console
$ nix-build --attr nix-cli-ccacheStdenv
```

你可以用其他任何受支持的环境替换 `nix-cli-ccacheStdenv`。

## 编辑器集成

`clangd` LSP 服务器默认安装在基于 `clang` 的 `devShell` 中。
参见[受支持的编译环境](#compilation-environments)，以及[使用 flakes](#building-nix-with-flakes) 或[经典 Nix](#building-nix) 设置 shell 的说明。

要在编辑器中使用 LSP，你需要一个 `compile_commands.json` 文件来告诉 `clangd` 我们是如何编译代码的。
Meson 的 configure 始终会在构建目录内生成该文件。

将你的编辑器配置为使用 `.#native-clangStdenv` shell 中的 `clangd`。
你可以在开发 shell 中运行它，或者使用 [nix-direnv](https://github.com/nix-community/nix-direnv) 和[相应的编辑器插件](https://github.com/direnv/direnv/wiki#editor-integration)来实现。

> **注意**
>
> 对于某些编辑器（例如 Visual Studio Code），你可能需要安装一个[专用扩展](https://open-vsx.org/extension/llvm-vs-code-extensions/vscode-clangd)，编辑器才能与 `clangd` 交互。
> 其他一些编辑器（例如 Emacs、Vim）需要插件才能支持 LSP 服务器（例如 Emacs 的 [lsp-mode](https://github.com/emacs-lsp/lsp-mode) 和 vim 的 [vim-lsp](https://github.com/prabirshrestha/vim-lsp)）。
> 各编辑器的具体配置往往见仁见智，因此我们在此不做更详细的介绍。

## 格式化与 pre-commit 钩子

你可以通过以下命令一次性运行格式化工具：

```console
./maintainers/format.sh
```

### Pre-commit 钩子

如果你希望在每次提交前都运行格式化工具，请安装钩子：

```
pre-commit-hooks-install
```

这会通过 [cachix/git-hooks.nix](https://github.com/cachix/git-hooks.nix) 安装 [pre-commit](https://pre-commit.com)。

提交时请留意控制台输出。
如果提交失败，请运行 `git add --patch` 采纳建议*并再次提交*。

要刷新 pre-commit 钩子的配置文件，请执行以下操作：
1. 退出开发 shell，然后通过运行 `nix develop` 重新进入。
2. 如果你也使用了 pre-commit 钩子，请再次运行 `pre-commit-hooks-install`。

### VSCode

将以下 json 插入你的 `.vscode/settings.json` 文件来配置 `nixfmt`。
它会被 _Format Document_ 命令、`"editor.formatOnSave"` 等功能采用。

```json
{
  "nix.formatterPath": "nixfmt",
  "nix.serverSettings": {
    "nixd": {
      "formatting": {
        "command": [
          "nixfmt"
        ],
      },
    },
    "nil": {
      "formatting": {
        "command": [
          "nixfmt"
        ],
      },
    },
  },
}
```
