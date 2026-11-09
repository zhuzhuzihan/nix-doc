# Release 2.30.0 (2025-07-07)

## 破坏性变更与弃用

- [`build-dir`] 不再默认为 `$TMPDIR`

  临时构建目录的创建位置不再默认为 `TMPDIR` 或 `/tmp`，以避免构建器将自己的目录设为全局可访问。这一行为允许逃逸出构建沙箱，而且即使没有被恶意利用，也可能造成构建的不纯净。现在我们默认使用 `NIX_STATE_DIR` 中的 `builds`（在默认配置下即 `/nix/var/nix/builds`）。

- 弃用通过 `__json` 属性手动构造结构化属性（structured attrs）的做法 [#13220](https://github.com/NixOS/nix/pull/13220)

  在 Nix 语言中，使用 [结构化属性（structured attrs）] 创建 derivation（派生）的正确方式是配合 [`builtins.derivation`] 使用 `__structuredAttrs = true`。
  然而，利用结构化属性的实现方式，此前也可以通过将 `__json` 环境变量设为一个序列化的 JSON 字符串来创建它们。
  这种取巧的替代做法现在已被弃用，并且在未来的 Nix 版本中可能会被禁止。

  [结构化属性（structured attrs）]: @docroot@/language/advanced-attributes.md#adv-attr-structuredAttrs
  [`builtins.derivation`]: @docroot@/language/builtins.html#builtins-derivation

- 将 `nix profile install` 更名为 [`nix profile add`] [#13224](https://github.com/NixOS/nix/pull/13224)

  命令 `nix profile install` 已更名为 [`nix profile add`]（前者仍作为别名可用）。这是因为动词 "add" 与动词 "remove"（即 `nix profile remove`）是一对更贴切的反义词。此外，Nix 也没有与"安装"（install）通常相关联的 install hook 或通用行为。

## 性能改进

本次发布包含多项性能改进，尤其是：

- 将 value 的大小从 24 字节缩减到 16 字节 [#13407](https://github.com/NixOS/nix/pull/13407)

  这显著减少了求值所占用的内存（最大堆大小约减少 20%，总字节数约减少 17%）。

## 新特性

- 新增[栈采样求值分析器（stack sampling evaluation profiler）] [#13220](https://github.com/NixOS/nix/pull/13220)

  Nix 求值器现在支持通过 [`--eval-profiler flamegraph`] 设置进行[栈采样求值分析](@docroot@/advanced-topics/eval-profiler.md)。
  它将折叠后的调用栈信息输出到 [`--eval-profile-file`]（默认为 `nix.profile`）所指定的文件中，其格式可被 `flamegraph.pl` 及 [speedscope](https://speedscope.app/) 等兼容工具直接使用。
  采样频率可通过 [`--eval-profiler-frequency`] 配置（默认为 99 Hz）。

  与现有的 [`--trace-function-calls`] 不同，该分析器在可获得函数名时会包含被调用函数的名称。

- [`nix repl`] 会打印加载了哪些变量 [#11406](https://github.com/NixOS/nix/pull/11406)

  它现在不再打印 `Added <n> variables`，而是打印前 10 个被加入全局作用域的变量。

- `nix flake archive`：新增 [`--no-check-sigs`] 选项 [#13277](https://github.com/NixOS/nix/pull/13277)

  在使用 [`nix flake archive`] 且目标为远程 store 时，这个选项很有用。

- 通过 [`trace-import-from-derivation`] 选项为 IFD 发出警告 [#13279](https://github.com/NixOS/nix/pull/13279)

  虽然我们有 [`allow-import-from-derivation`] 设置来禁止 import-from-derivation（IFD），但有时用户希望在 CI 流程中观察 IFD 的发生，以便逐步淘汰这一惯用法。新增的 `trace-import-from-derivation` 设置在启用时会向控制台记录一条简单的警告。

- `json-log-path` 设置 [#13003](https://github.com/NixOS/nix/pull/13003)

  新增设置 [`json-log-path`]，它会将所有 Nix 日志消息（JSON 格式）的一份副本发送到某个文件或 Unix 域套接字。

- 非 Flakes 输入现在包含 `sourceInfo` 属性 [#13164](https://github.com/NixOS/nix/issues/13164) [#13170](https://github.com/NixOS/nix/pull/13170)

  Flakes 一直有一个 `sourceInfo` 属性，用于描述该 Flakes 的来源。
  `sourceInfo.outPath` 通常与该 Flakes 的 `outPath` 相同。但当 Flakes 位于其来源的某个子目录中时，两者可能不同。

  非 Flakes 输入（即设置了 [`flake = false`] 的输入）也可能位于一个更大的来源内的某个路径上。
  这通常发生在把相对路径输入定义在与父级 Flakes 相同的来源中时，例如 `inputs.foo.url = ./some-file.nix`。
  这类相对输入现在会继承其父级的 `sourceInfo`。

  这也意味着现在可以对非 Flakes 输入使用 `?dir=subdir`。

  这是建立在 2.26 中改进相对路径支持的工作（[#10089](https://github.com/NixOS/nix/pull/10089)）之上的，
  并修复了 2.28 中引入的关于嵌套相对路径输入的回归（[#13164](https://github.com/NixOS/nix/issues/13164)）。

## 杂项变更

- [`builtins.sort`] 改用 PeekSort [#12623](https://github.com/NixOS/nix/pull/12623)

  以前它使用 libstdc++ 的 `std::stable_sort()`。然而，当用户提供的比较函数不是一个严格的弱序时，该实现并不可靠。

- 回退"不完整闭包"混合下载与构建特性 [#77](https://github.com/NixOS/nix/issues/77) [#12628](https://github.com/NixOS/nix/issues/12628) [#13176](https://github.com/NixOS/nix/pull/13176)

  自 Nix 1.3（2013 年的[提交 `299141e`]）以来，当远程替代器（substituter）包含"不完整闭包"（拥有某些 store 对象，但没有它们所引用的 store 对象）时，Nix 一直尝试将上游的新鲜构建与下游的 substitute（替代下载）混合进行。
  该特性现已被移除。

  在最坏的情况下，移除该特性可能导致下游进行更多构建，但不应该造成彻底失败，因为对于我们不透明、不知如何构建的 store 对象，如果我们决定不进行替代下载，这种情况并不会发生。
  不过在实践中，我们认为额外构建增多的可能性也不大。
  远程 store 以任意方式缺失依赖（例如损坏）的情形似乎并不常见。

  相反，当远程 store 未能实现[闭包性质](@docroot@/store/store-object.md#closure-property)时，这通常是远程 store 一方的*有意*选择，因为它希望充当另一个 store（例如 `https://cache.nixos.org`）之上的"覆盖层"（overlay）store。
  在这种情况下遇到"不完整闭包"时，正确的做法不是像该特性所实现的那样进行某种"拼接式构建"（franken-building），而是确保两个替代器（substituter）都在设置中被启用。

  （将来，我们应当让远程 store 更容易向客户端表明这一点，以便在真正遇到缺失的依赖之前，就能发现那些在一般情况下行不通的设置。）

## 贡献者

本次发布由以下 32 位贡献者共同促成：

- Cole Helbling [**(@cole-h)**](https://github.com/cole-h)
- Eelco Dolstra [**(@edolstra)**](https://github.com/edolstra)
- Egor Konovalov [**(@egorkonovalov)**](https://github.com/egorkonovalov)
- Farid Zakaria [**(@fzakaria)**](https://github.com/fzakaria)
- Graham Christensen [**(@grahamc)**](https://github.com/grahamc)
- gustavderdrache [**(@gustavderdrache)**](https://github.com/gustavderdrache)
- Gwenn Le Bihan [**(@gwennlbh)**](https://github.com/gwennlbh)
- h0nIg [**(@h0nIg)**](https://github.com/h0nIg)
- Jade Masker [**(@donottellmetonottellyou)**](https://github.com/donottellmetonottellyou)
- jayeshv [**(@jayeshv)**](https://github.com/jayeshv)
- Jeremy Fleischman [**(@jfly)**](https://github.com/jfly)
- John Ericson [**(@Ericson2314)**](https://github.com/Ericson2314)
- Jonas Chevalier [**(@zimbatm)**](https://github.com/zimbatm)
- Jörg Thalheim [**(@Mic92)**](https://github.com/Mic92)
- kstrafe [**(@kstrafe)**](https://github.com/kstrafe)
- Luc Perkins [**(@lucperkins)**](https://github.com/lucperkins)
- Matt Sturgeon [**(@MattSturgeon)**](https://github.com/MattSturgeon)
- Nikita Krasnov [**(@synalice)**](https://github.com/synalice)
- Peder Bergebakken Sundt [**(@pbsds)**](https://github.com/pbsds)
- pennae [**(@pennae)**](https://github.com/pennae)
- Philipp Otterbein
- Pol Dellaiera [**(@drupol)**](https://github.com/drupol)
- PopeRigby [**(@poperigby)**](https://github.com/poperigby)
- Raito Bezarius
- Robert Hensing [**(@roberth)**](https://github.com/roberth)
- Samuli Thomasson [**(@SimSaladin)**](https://github.com/SimSaladin)
- Sergei Zimmerman [**(@xokdvium)**](https://github.com/xokdvium)
- Seth Flynn [**(@getchoo)**](https://github.com/getchoo)
- Stefan Boca [**(@stefanboca)**](https://github.com/stefanboca)
- tomberek [**(@tomberek)**](https://github.com/tomberek)
- Tristan Ross [**(@RossComputerGuy)**](https://github.com/RossComputerGuy)
- Valentin Gagarin [**(@fricklerhandwerk)**](https://github.com/fricklerhandwerk)
- Vladimír Čunát [**(@vcunat)**](https://github.com/vcunat)
- Wolfgang Walther [**(@wolfgangwalther)**](https://github.com/wolfgangwalther)

<!-- markdown links -->
[栈采样求值分析器（stack sampling evaluation profiler）]: @docroot@/advanced-topics/eval-profiler.md
[`--eval-profiler`]: @docroot@/command-ref/conf-file.md#conf-eval-profiler
[`--eval-profiler flamegraph`]: @docroot@/command-ref/conf-file.md#conf-eval-profiler
[`--trace-function-calls`]: @docroot@/command-ref/conf-file.md#conf-trace-function-calls
[`--eval-profile-file`]: @docroot@/command-ref/conf-file.md#conf-eval-profile-file
[`--eval-profiler-frequency`]: @docroot@/command-ref/conf-file.md#conf-eval-profiler-frequency
[`build-dir`]: @docroot@/command-ref/conf-file.md#conf-build-dir
[`nix profile add`]: @docroot@/command-ref/new-cli/nix3-profile-add.md
[`nix repl`]: @docroot@/command-ref/new-cli/nix3-repl.md
[`nix flake archive`]: @docroot@/command-ref/new-cli/nix3-flake-archive.md
[`json-log-path`]: @docroot@/command-ref/conf-file.md#conf-json-log-path
[`trace-import-from-derivation`]: @docroot@/command-ref/conf-file.md#conf-trace-import-from-derivation
[`allow-import-from-derivation`]: @docroot@/command-ref/conf-file.md#conf-allow-import-from-derivation
[`builtins.sort`]: @docroot@/language/builtins.md#builtins-sort
[`flake = false`]: @docroot@/command-ref/new-cli/nix3-flake.md?highlight=false#flake-inputs
[`--no-check-sigs`]: @docroot@/command-ref/new-cli/nix3-flake-archive.md#opt-no-check-sigs
[提交 `299141e`]: https://github.com/NixOS/nix/commit/299141ecbd08bae17013226dbeae71e842b4fdd7
