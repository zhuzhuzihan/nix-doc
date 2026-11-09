# Release 2.28.0 (2025-04-02)

这是一个非典型的发布版本；无论从哪个角度看，它基本上都只是 2.27 的延续，而不是一个新特性版本。

我们最初的目标是让 2.27 成为 NixOS 25.05 中 Nixpkgs 的默认版本，但链接到 Nix 的下游项目需要在 C++ 头文件中做出某些*破坏接口*的变更。这类变更不适合放在补丁版本中做，因此我们直接从 2.27（而不是 `master`）分出了 2.28 分支。

本次发布完成了 [RFC 132](https://github.com/NixOS/rfcs/blob/master/rfcs/0132-meson-builds-nix.md) 所规划的将构建系统切换到 meson 的基础设施改造工作。

## 重大变更

- 重构了不稳定的 C++ API
  [#12836](https://github.com/NixOS/nix/pull/12836)
  [#12798](https://github.com/NixOS/nix/pull/12798)
  [#12773](https://github.com/NixOS/nix/pull/12773)

  现在 C++ 接口比以往更符合通用惯例：

  - 所有头文件都应带上 `nix/` 前缀来包含，例如 `#include "nix/....hh"`（Nix 自身的头文件现在就是这样）或 `#include <nix/....hh>`（下游项目可以选择这种方式）。
    同样，pkg-config 文件使用 `-I${includedir}`，而不再是 `-I${includedir}/nix` 之类的形式。

    以前不带 `nix/` 前缀的包含有时能正常工作，是因为 C 预处理器处理 `#include` 时会检查当前文件所在目录（而不仅仅是查找路径），但这种方式并不可靠。

  - 所有配置头文件都由需要它们的（常规）头文件显式包含。
    不再需要通过 `-include` 强制包含额外的文件。

  - 公开安装的配置头文件不再包含与 API 无关的实现细节。
    原先放在其中的绝大多数定义已被移到新的头文件中，这些头文件不会被安装，仅在 Nix 自身编译时使用。
    保留下来的宏定义都被重命名，加上 `NIX_` 前缀。

  - 头文件所属的 Nix 组件名
    （如 `util`、`store`、`expr`、`flake` 等）
    现在成为头文件路径的一部分，位于 `nix` 之后、头文件名之前
    （如果该路径本身已在某个目录中，则位于路径其余部分之前）。

  下面是一个人为构造的 diff，一次性展示了上述几项变更：

  ```diff
  @@ @@
  -#include "derived-path.hh"
  +#include "nix/store/derived-path.hh"
  @@ @@
  +// Would include for the variables used before. But when other headers
  +// need these variables. those will include these config themselves.
  +#include "nix/store/config.hh"
  +#include "nix/expr/config.hh"
  @@ @@
  -#include "config.hh"
  +// Additionally renamed to distinguish from components' config headers.
  +#include "nix/util/configuration.hh"
  @@ @@
  -#if HAVE_ACL_SUPPORT
  +#if NIX_SUPPORT_ACL
  @@ @@
  -#if HAVE_BOEHMGC
  +#if NIX_USE_BOEHMGC
  @@ @@
   #endif
   #endif
  @@ @@
  -const char *s = "hi from " SYSTEM;
  +const char *s = "hi from " NIX_LOCAL_SYSTEM;
  ```

- 移除 C API 函数 `nix_flake_init_global` [#5638](https://github.com/NixOS/nix/issues/5638) [#12759](https://github.com/NixOS/nix/pull/12759)

  为了提升代码库的模块化程度，我们移除了一处全局状态的使用，也就是 `nix_flake_init_global` 函数。

  作为替代，请使用 `nix_flake_settings_add_to_eval_state_builder`。例如：

  ```diff
  -    nix_flake_init_global(ctx, settings);
  -    HANDLE_ERROR(ctx);
  -
       nix_eval_state_builder * builder = nix_eval_state_builder_new(ctx, store);
       HANDLE_ERROR(ctx);

  +    nix_flake_settings_add_to_eval_state_builder(ctx, settings, builder);
  +    HANDLE_ERROR(ctx);
  ```

  虽然这项变更没有前者那么关键，但我们认为趁此机会一并完成这个 API 变更是有好处的。
  另请注意，我们尽量保持 C API 的兼容性，但之所以决定破坏这个函数，是因为它还很年轻、大概率尚未被广泛使用。这为我们腾出时间，去推进 C API 其余部分的重要进展。

## 贡献者

这次早于惯例的发布由以下 16 位贡献者共同促成：

- Farid Zakaria [**(@fzakaria)**](https://github.com/fzakaria)
- Jörg Thalheim [**(@Mic92)**](https://github.com/Mic92)
- Eelco Dolstra [**(@edolstra)**](https://github.com/edolstra)
- Graham Christensen [**(@grahamc)**](https://github.com/grahamc)
- Thomas Miedema [**(@thomie)**](https://github.com/thomie)
- Brian McKenna [**(@puffnfresh)**](https://github.com/puffnfresh)
- Sergei Trofimovich [**(@trofi)**](https://github.com/trofi)
- Dmitry Bogatov [**(@KAction)**](https://github.com/KAction)
- Erik Nygren [**(@Kirens)**](https://github.com/Kirens)
- John Ericson [**(@Ericson2314)**](https://github.com/Ericson2314)
- Sergei Zimmerman [**(@xokdvium)**](https://github.com/xokdvium)
- Ruby Rose [**(@oldshensheep)**](https://github.com/oldshensheep)
- Robert Hensing [**(@roberth)**](https://github.com/roberth)
- jade [**(@lf-)**](https://github.com/lf-)
- Félix [**(@picnoir)**](https://github.com/picnoir)
- Valentin Gagarin [**(@fricklerhandwerk)**](https://github.com/fricklerhandwerk)
- Dmitry Bogatov
