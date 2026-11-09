# Release 2.24.0 (2024-07-31)

### 显著变更

- 加强用户沙箱

  构建目录现在嵌套在另一个由 daemon（守护进程）用户拥有（且仅该用户可读）的目录之内，从而得到加固，以免受到外部世界的干扰。

  这是一处低严重性的安全修复，[CVE-2024-38531](https://www.cve.org/CVERecord?id=CVE-2024-38531)。

  鸣谢：[**@alois31**](https://github.com/alois31)、[**Linus Heckemann (@lheckemann)**](https://github.com/lheckemann)
  共同作者：[**@edolstra**](https://github.com/edolstra)

- `nix-shell <directory>` 查找 `shell.nix` [#496](https://github.com/NixOS/nix/issues/496) [#2279](https://github.com/NixOS/nix/issues/2279) [#4529](https://github.com/NixOS/nix/issues/4529) [#5431](https://github.com/NixOS/nix/issues/5431) [#11053](https://github.com/NixOS/nix/issues/11053) [#11057](https://github.com/NixOS/nix/pull/11057)

  当 `$x` 解析为一个目录时，`nix-shell $x` 现在会查找 `$x/shell.nix`。

  虽然这可能被视为破坏性变更，但其主要用途是交互式的，因此只是一个次要问题。
  这一调整解决了一个被大量报告的常见问题。

  这同样适用于 `nix-shell` shebang 脚本。考虑以下示例：

  ```shell
  #!/usr/bin/env nix-shell
  #!nix-shell -i bash
  ```

  现在，如果脚本所在目录中存在 `shell.nix`，则加载该文件；否则加载 `default.nix`。

  可以通过将选项 [`nix-shell-always-looks-for-shell-nix`](@docroot@/command-ref/conf-file.md#conf-nix-shell-always-looks-for-shell-nix) 设为 `false` 来选择沿用旧行为。

  作者：[**Robert Hensing (@roberth)**](https://github.com/roberth)

- `nix-repl` 的 `:doc` 显示文档注释 [#3904](https://github.com/NixOS/nix/issues/3904) [#10771](https://github.com/NixOS/nix/issues/10771) [#1652](https://github.com/NixOS/nix/pull/1652) [#9054](https://github.com/NixOS/nix/pull/9054) [#11072](https://github.com/NixOS/nix/pull/11072)

  `nix repl` 有一个 `:doc` 命令，此前只能为内部定义的函数渲染文档。
  该功能现已扩展，可以按照 [RFC 145] 渲染函数的文档注释。

  示例：

  ```
  nix-repl> :doc lib.toFunction
  Function toFunction
      … defined at /home/user/h/nixpkgs/lib/trivial.nix:1072:5

      Turns any non-callable values into constant functions. Returns
      callable values as is.

  Inputs

      v

        : Any value

  Examples

      :::{.example}

  ## lib.trivial.toFunction usage example

        | nix-repl> lib.toFunction 1 2
        | 1
        |
        | nix-repl> lib.toFunction (x: x + 1) 2
        | 3

      :::
  ```

  已知限制：
  - 它不会为“形参”（formals）渲染文档，例如 `{ /** the value to return */ x, ... }: x`。
  - 某些 markdown 扩展尚不支持，如上例所示。

  我们要感谢 [Yingchi Long (@inclyc)](https://github.com/inclyc) 在 [#9054](https://github.com/NixOS/nix/pull/9054) 中为此功能提出了概念验证，同时感谢 [@sternenseemann](https://github.com/sternenseemann) 和 [Johannes Kirschbauer (@hsjobeki)](https://github.com/hsjobeki) 的贡献、提案以及他们在 [RFC 145] 上所做的工作。

  作者：[**Robert Hensing (@roberth)**](https://github.com/roberth)

  [RFC 145]: https://github.com/NixOS/rfcs/pull/145

### 其他变更

- 解决 `cached failure of attribute X` 问题 [#9165](https://github.com/NixOS/nix/issues/9165) [#10513](https://github.com/NixOS/nix/issues/10513) [#10564](https://github.com/NixOS/nix/pull/10564)

  此更改通过在需要向用户展示异常时强制求值原始值，消除了所有 “cached failure of attribute X” 消息。这一增强通过提供底层消息和堆栈跟踪，改进了错误报告。

  作者：[**Eelco Dolstra (@edolstra)**](https://github.com/edolstra)

- 运行 flake 回归测试套件 [#10603](https://github.com/NixOS/nix/pull/10603)

  本次更新引入了一个 GitHub action，用于运行 [flake 回归测试套件](https://github.com/NixOS/flake-regressions)的一个子集，其中包含 259 个 flake 及其预期的求值结果。由于完整测试套件运行时间过长，该 action 目前只运行前 25 个 flake。后续可能会实现一个手动触发的 action 来运行整个测试套件。

  作者：[**Eelco Dolstra (@edolstra)**](https://github.com/edolstra)

- 配置设置支持单位前缀 [#10668](https://github.com/NixOS/nix/pull/10668)

  Nix 的配置设置现在支持单位前缀，使配置更加直观易读。例如，现在可以指定 [`--min-free 1G`](@docroot@/command-ref/conf-file.md#conf-min-free) 将最小可用空间设为 1 GB。

  此增强从 [#7851](https://github.com/NixOS/nix/pull/7851) 中提取而来，对 PR [#10661](https://github.com/NixOS/nix/pull/10661) 同样有用。

  作者：[**Eelco Dolstra (@edolstra)**](https://github.com/edolstra)

- `nix build`：使用 `--keep-going` 显示所有 FOD 错误 [#10734](https://github.com/NixOS/nix/pull/10734)

  [`nix build`](@docroot@/command-ref/new-cli/nix3-build.md) 命令已更新，改进了 [`--keep-going`] 标志的行为。现在，使用 `--keep-going` 时，所有构建失败的 fixed-output derivation（派生）（FOD，固定输出 derivation）的哈希不匹配错误都会被显示出来，与其他构建失败时的行为类似。这一增强确保显示所有相关的构建错误，让用户更容易一次更新多个 derivation，或诊断并修复问题。

  作者：[**Jörg Thalheim (@Mic92)**](https://github.com/Mic92)、[**Maximilian Bosch (@Ma27)**](https://github.com/Ma27)

  [`--keep-going`](@docroot@/command-ref/opt-common.md#opt-keep-going)

- 使用 Meson 构建 [#2503](https://github.com/NixOS/nix/issues/2503) [#10378](https://github.com/NixOS/nix/pull/10378) [#10855](https://github.com/NixOS/nix/pull/10855) [#10904](https://github.com/NixOS/nix/pull/10904) [#10908](https://github.com/NixOS/nix/pull/10908) [#10914](https://github.com/NixOS/nix/pull/10914) [#10933](https://github.com/NixOS/nix/pull/10933) [#10936](https://github.com/NixOS/nix/pull/10936) [#10954](https://github.com/NixOS/nix/pull/10954) [#10955](https://github.com/NixOS/nix/pull/10955) [#10963](https://github.com/NixOS/nix/pull/10963) [#10967](https://github.com/NixOS/nix/pull/10967) [#10973](https://github.com/NixOS/nix/pull/10973) [#11034](https://github.com/NixOS/nix/pull/11034) [#11054](https://github.com/NixOS/nix/pull/11054) [#11055](https://github.com/NixOS/nix/pull/11055) [#11060](https://github.com/NixOS/nix/pull/11060) [#11064](https://github.com/NixOS/nix/pull/11064) [#11155](https://github.com/NixOS/nix/pull/11155)

  这些变更旨在用 Meson 取代 autotools 和 `make` 来构建 Nix 的各个组件。此外，每个库都在各自的 derivation 中构建，并利用 Meson 的 “subprojects” 特性，既允许用一个开发 shell 构建所有库，也支持各自单独构建。与 make 以及单一的整体式基于 Meson 的 derivation 相比，这种方式旨在提升生产力和构建的模块化程度。

  特别感谢所有为 Meson 移植做出贡献的人，尤其是 [**@p01arst0rm**](https://github.com/p01arst0rm) 和 [**@Qyriad**](https://github.com/Qyriad)。

  作者：[**John Ericson (@Ericson2314)**](https://github.com/Ericson2314)、[**Tom Bereknyei**](https://github.com/tomberek)、[**Théophane Hufschmitt (@thufschmitt)**](https://github.com/thufschmitt)、[**Valentin Gagarin (@fricklerhandwerk)**](https://github.com/fricklerhandwerk)、[**Robert Hensing (@roberth)**](https://github.com/roberth)
  共同作者：[**@p01arst0rm**](https://github.com/p01arst0rm)、[**@Qyriad**](https://github.com/Qyriad)

- 求值缓存：修复缓存回归 [#10570](https://github.com/NixOS/nix/issues/10570) [#11086](https://github.com/NixOS/nix/pull/11086)

  此更新修复了求值缓存系统中的两个缺陷：

  1. #10570 引入的回归：求值缓存未在 `nix develop` 中持久化。
  2. Nix 有时会在没有活动事务的情况下尝试提交求值缓存的 SQLite 事务，导致打印出非错误性质的错误信息。

  作者：[**Lexi Mattick (@kognise)**](https://github.com/kognise)

- 引入 `libnixflake` [#9063](https://github.com/NixOS/nix/pull/9063)

  引入了一个新库 `libnixflake`，以便更好地在 Nix 内部分离 Flakes 层。此变更重构了代码库，将 Flakes 特有的功能封装到其独立的库中。

  详细变更请参见该拉取请求中的提交，其中唯一重要的代码修改发生在初始提交里。

  此变更在 [RFC 134](https://github.com/nixos/rfcs/blob/master/rfcs/0134-nix-store-layer.md) 中已被提及，是迈向更加模块化、更易维护的代码库的一步。

  作者：[**John Ericson (@Ericson2314)**](https://github.com/Ericson2314)

- CLI 选项 `--arg-from-file` 与 `--arg-from-stdin` [#9913](https://github.com/NixOS/nix/pull/9913)

- `--debugger` 现在打印源码位置信息，而不是源码位置信息的指针。修改前：

  ```
  nix-repl> :bt
  0: while evaluating the attribute 'python311.pythonForBuild.pkgs'
  0x600001522598
  ```

  修改后：

  ```
  0: while evaluating the attribute 'python311.pythonForBuild.pkgs'
  /nix/store/hg65h51xnp74ikahns9hyf3py5mlbbqq-source/overrides/default.nix:132:27

     131|
     132|       bootstrappingBase = pkgs.${self.python.pythonAttr}.pythonForBuild.pkgs;
       |                           ^
     133|     in
  ```

- 停止内置（vendor）`toml11`

  我们不对其应用任何补丁，而将它内置在源码树中会把用户锁定在缺陷之上（自 2021 年底引入以来它从未更新过）。

  作者：[**Winter (@winterqt)**](https://github.com/winterqt)

- 将哈希格式 `base32` 重命名为 `nix32` [#8678](https://github.com/NixOS/nix/pull/8678)

  哈希格式 `base32` 被重命名为 `nix32`，因为它为 [Base32](https://en.wikipedia.org/wiki/Base32) 使用了一个特殊的 Nix 专属字符集。

  **弃用**：在 `toHashFormat` 中请使用 `nix32` 而不是 `base32`

  对于内建函数 `convertHash`，`toHashFormat` 参数现在接受与 `nix hash convert` 命令的 `--to`/`--from` 参数相同的哈希格式：`"base16"`、`"nix32"`、`"base64"` 和 `"sri"`。原先的 `"base32"` 值仍作为 `"nix32"` 的弃用别名保留。请将代码从：

  ```nix
  builtins.convertHash { inherit hash hashAlgo; toHashFormat = "base32";}
  ```

  改为

  ```nix
  builtins.convertHash { inherit hash hashAlgo; toHashFormat = "nix32";}
  ```

- 添加 `pipe-operators` 实验性特性 [#11131](https://github.com/NixOS/nix/pull/11131)

  这是 [RFC 0148](https://github.com/NixOS/rfcs/pull/148) 的草案实现。

  `pipe-operators` 实验性特性为 Nix 语言添加了 [`<|` 与 `|>` 运算符][pipe operators]。
  *a* `|>` *b* 等价于函数应用 *b* *a*，而
  *a* `<|` *b* 等价于函数应用 *a* *b*。

  例如：

  ```
  nix-repl> 1 |> builtins.add 2 |> builtins.mul 3
  9

  nix-repl> builtins.add 1 <| builtins.mul 2 <| 3
  7
  ```

  `<|` 与 `|>` 分别为右结合和左结合，且优先级低于任何其他运算符。
  这些性质在未来的版本中可能会改变。

  更多示例和设计理由请参见[该 RFC](https://github.com/NixOS/rfcs/pull/148)。

  [pipe operators]: @docroot@/language/operators.md#pipe-operators

- `nix-shell` shebang 使用相对路径 [#4232](https://github.com/NixOS/nix/issues/4232) [#5088](https://github.com/NixOS/nix/pull/5088) [#11058](https://github.com/NixOS/nix/pull/11058)

  <!-- unfortunately no link target for the specific syntax -->
  `nix-shell` shebang 脚本选项中的相对 [path](@docroot@/language/types.md#type-path) 字面量现在相对于[脚本所在位置](@docroot@/glossary.md?highlight=base%20directory#gloss-base-directory)解析。
  此前它们相对于当前工作目录解析。

  例如，考虑 `~/myproject/say-hi` 中的以下脚本：

  ```shell
  #!/usr/bin/env nix-shell
  #!nix-shell --expr 'import ./shell.nix'
  #!nix-shell --arg toolset './greeting-tools.nix'
  #!nix-shell -i bash
  hello
  ```

  旧版本的 `nix-shell` 会相对当前工作目录解析 `shell.nix`，例如本例中的用户主目录：

  ```console
  [hostname:~]$ ./myproject/say-hi
  error:
         … while calling the 'import' builtin
           at «string»:1:2:
              1| (import ./shell.nix)
               |  ^

         error: path '/home/user/shell.nix' does not exist
  ```

  自本版本起，`nix-shell` 相对脚本所在位置解析 `shell.nix`，因此会使用 `~/myproject/shell.nix`。

  ```console
  $ ./myproject/say-hi
  Hello, world!
  ```

  **选择退出**

  这在技术上是一次破坏性变更，因此我们添加了一个选项，使你可以在不依赖 Nix 更新节奏的情况下自行调整。
  可以通过将选项 [`nix-shell-shebang-arguments-relative-to-script`](@docroot@/command-ref/conf-file.md#conf-nix-shell-shebang-arguments-relative-to-script) 设为 `false` 来选择沿用旧行为。
  该选项将在未来的版本中被移除。

  作者：[**Robert Hensing (@roberth)**](https://github.com/roberth)

- 改进对不含单一顶层目录的 tarball 的处理 [#11195](https://github.com/NixOS/nix/pull/11195)

  在之前的 Nix 版本中，tarball 抓取器（由 `builtins.fetchTarball` 使用）会错误地把多个顶层目录合并成一个目录，并静默丢弃不属于目录的顶层文件。现在不再如此。新行为是：*仅当* tarball 由单一目录组成时，才会移除其中文件的顶层路径组件（类似于 `tar` 的 `--strip-components=1`）。

  作者：[**Eelco Dolstra (@edolstra)**](https://github.com/edolstra)

- 添加针对大路径发出警告的设置 [#10778](https://github.com/NixOS/nix/pull/10778)

  现在，当对 Nix 表达式的求值导致一个大路径被复制到 Nix store 时，Nix 可以发出警告。该警告的阈值可通过 `warn-large-path-threshold` 设置进行配置，例如 `--warn-large-path-threshold 100M`。


## 贡献者

本发布版本得益于以下 43 位贡献者：

- Andreas Rammhold [**(@andir)**](https://github.com/andir)
- Andrew Marshall [**(@amarshall)**](https://github.com/amarshall)
- Brian McKenna [**(@puffnfresh)**](https://github.com/puffnfresh)
- Cameron [**(@SkamDart)**](https://github.com/SkamDart)
- Cole Helbling [**(@cole-h)**](https://github.com/cole-h)
- Corbin Simpson [**(@MostAwesomeDude)**](https://github.com/MostAwesomeDude)
- Eelco Dolstra [**(@edolstra)**](https://github.com/edolstra)
- Emily [**(@emilazy)**](https://github.com/emilazy)
- Enno Richter [**(@elohmeier)**](https://github.com/elohmeier)
- Farid Zakaria [**(@fzakaria)**](https://github.com/fzakaria)
- HaeNoe [**(@haenoe)**](https://github.com/haenoe)
- Hamir Mahal [**(@hamirmahal)**](https://github.com/hamirmahal)
- Harmen [**(@alicebob)**](https://github.com/alicebob)
- Ivan Trubach [**(@tie)**](https://github.com/tie)
- Jared Baur [**(@jmbaur)**](https://github.com/jmbaur)
- John Ericson [**(@Ericson2314)**](https://github.com/Ericson2314)
- Jonathan De Troye [**(@detroyejr)**](https://github.com/detroyejr)
- Jörg Thalheim [**(@Mic92)**](https://github.com/Mic92)
- Klemens Nanni [**(@klemensn)**](https://github.com/klemensn)
- Las Safin [**(@L-as)**](https://github.com/L-as)
- Lexi Mattick [**(@kognise)**](https://github.com/kognise)
- Matthew Bauer [**(@matthewbauer)**](https://github.com/matthewbauer)
- Max “Goldstein” Siling [**(@GoldsteinE)**](https://github.com/GoldsteinE)
- Mingye Wang [**(@Artoria2e5)**](https://github.com/Artoria2e5)
- Philip Taron [**(@philiptaron)**](https://github.com/philiptaron)
- Pierre Bourdon [**(@delroth)**](https://github.com/delroth)
- Pino Toscano [**(@pinotree)**](https://github.com/pinotree)
- RTUnreal [**(@RTUnreal)**](https://github.com/RTUnreal)
- Robert Hensing [**(@roberth)**](https://github.com/roberth)
- Romain Neil [**(@romain-neil)**](https://github.com/romain-neil)
- Ryan Hendrickson [**(@rhendric)**](https://github.com/rhendric)
- Sergei Trofimovich [**(@trofi)**](https://github.com/trofi)
- Shogo Takata [**(@pineapplehunter)**](https://github.com/pineapplehunter)
- Siddhant Kumar [**(@siddhantk232)**](https://github.com/siddhantk232)
- Silvan Mosberger [**(@infinisil)**](https://github.com/infinisil)
- Théophane Hufschmitt [**(@thufschmitt)**](https://github.com/thufschmitt)
- Valentin Gagarin [**(@fricklerhandwerk)**](https://github.com/fricklerhandwerk)
- Winter [**(@winterqt)**](https://github.com/winterqt)
- jade [**(@lf-)**](https://github.com/lf-)
- kirillrdy [**(@kirillrdy)**](https://github.com/kirillrdy)
- pennae [**(@pennae)**](https://github.com/pennae)
- poweredbypie [**(@poweredbypie)**](https://github.com/poweredbypie)
- tomberek [**(@tomberek)**](https://github.com/tomberek)
