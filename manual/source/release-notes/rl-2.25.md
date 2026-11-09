# Release 2.25.0 (2024-11-07)

- 新增用于覆盖 XDG 位置的环境变量 [#11351](https://github.com/NixOS/nix/pull/11351)

  新增了以下环境变量：

  - `NIX_CACHE_HOME`
  - `NIX_CONFIG_HOME`
  - `NIX_DATA_HOME`
  - `NIX_STATE_HOME`

  其中每个变量若已定义，都将优先于对应的 [XDG 环境变量](@docroot@/command-ref/env-common.md#xdg-base-directories)。
  这提供了对 Nix 查找文件位置的更细粒度控制。它允许构建一个仅使用特定目录中文件、且不干扰用户环境的独立 Nix 环境。

- 将 Nix 语言中的整数溢出定义为错误 [#10968](https://github.com/NixOS/nix/issues/10968) [#11188](https://github.com/NixOS/nix/pull/11188)

  此前，Nix 语言中的整数溢出会触发 C++ 层面的有符号溢出，表现为溢出时回绕。现在的表现如下：

  ```
  $ nix eval --expr '9223372036854775807 + 1'
  error: integer overflow in adding 9223372036854775807 + 1
  ```

  还修复了一些其他溢出问题：
  - `builtins.fromJSON` 解析大于有符号 64 位整数可表示最大值的值时将产生错误。
  - Flakes 中的 `nixConfig` 将不再接受配置选项的负值。

- 当把 `libnixstore` 作为库使用时，`build-hook` 设置不再有有用的默认值 [#11178](https://github.com/NixOS/nix/pull/11178)

  *这是一个晦涩的问题，只影响在 Nix 可执行文件之外使用 `libnixstore` 库的场景。它与常用于向缓存推送内容的 `post-build-hook` 设置无关。*

  作为[将构建系统改写](https://github.com/NixOS/nix/issues/2503)为使用 [Meson](https://mesonbuild.com/) 的持续工作的一部分，我们也在转为单独打包各个 Nix 组件（并在各自的 derivation（派生）中构建它们）。
  这意味着在构建 `libnixstore` 时，我们并不知道 Nix 二进制文件会被安装到哪里 —— `libnixstore` 完全不了解 Nix 二进制文件这类下游使用者。

  这对远程构建有一处轻微的不利影响 —— 由 [`build-hook`](@docroot@/command-ref/conf-file.md#conf-build-hook) 设置指定的 `build-remote` 可执行文件将不再从（假定的）安装位置获取，而是会在 `PATH` 上查找。
  这意味着其他链接了 `libnixstore`、希望使用远程构建的应用程序，必须安排 `nix` 命令位于 PATH 上（或手动覆盖 `build-hook`），才能使其正常工作。

  长期来看，我们不认为这会成为一个缺点，因为我们计划[彻底移除 `build-remote` 与 build hook 设置](https://github.com/NixOS/nix/issues/1221)。
  当我们想要连接远程构建器时，根本无需再多一层中间的远程过程调用。
  build hook 协议原则上确实支持自定义的远程构建方式，但这同样可以通过为 ssh 或 daemon/ssh-ng 协议提供自定义服务来实现，或者使用自定义的[存储类型](@docroot@/store/types/index.md)（即 `Store` 子类）。 <!-- we normally don't mention classes, but consider that this release note is about a library use case -->

  Perl 绑定也不再暴露 `getBinDir`，因为这些绑定所封装的底层 C++ 库如上所述不再知晓已安装二进制文件的位置。

- 更正确地包装文件系统异常 [#11378](https://github.com/NixOS/nix/pull/11378)

  随着在多处切换到 `std::filesystem`，Nix 开始在很多地方抛出 `std::filesystem::filesystem_error` 而不是自己的异常。
  因此，Nix 在（例如）列出不存在的目录时不再生成错误跟踪，这也可能导致 Nix REPL 内部崩溃。

  本版本会正确捕获这类异常，并将其包装为 Nix 自己的异常类型。

  作者：[**@Mic92**](https://github.com/Mic92)

- 添加设置 `fsync-store-paths` [#1218](https://github.com/NixOS/nix/issues/1218) [#7126](https://github.com/NixOS/nix/pull/7126)

  Nix 现在有了设置 `fsync-store-paths`，它确保新的存储路径在 Nix 数据库中被注册为“有效”之前，已持久化写入磁盘。这可以在系统崩溃或断电时防止 Nix store 损坏。该设置默认为 `false`。

  作者：[**@squalus**](https://github.com/squalus)

- 移除传递给 `nix fmt` 格式化器的默认参数 [#11438](https://github.com/NixOS/nix/pull/11438)

  当不带参数调用 `nix fmt` 时，底层格式化器不再接收默认参数 `.`。

  此变更很有必要，因为格式化器此前无法区分用户是想用 `nix fmt .` 格式化当前目录，还是想执行通用的
  `nix fmt`。

  默认行为现在由格式化器自身负责，这使得 `treefmt` 等工具可以格式化整个代码树，而不局限于
  当前目录及其子目录。

  作者：[**@zimbatm**](https://github.com/zimbatm)

- `<nix/fetchurl.nix>` 启用 TLS 验证 [#11585](https://github.com/NixOS/nix/pull/11585)

  此前 `<nix/fetchurl.nix>` 不做 TLS 验证。这是因为过去的 Nix 沙箱无法访问 TLS 证书，而且 Nix 反正会检查被抓取文件的哈希。然而，这可能把来自 `netrc` 和 URL 的认证数据暴露给中间人攻击者。此外，Nix 现在在某些情况下（例如使用非纯 derivation 时）*不会*检查哈希。因此我们现已启用 TLS 验证。这意味着，如果你从没有有效证书的 HTTPS 服务器抓取文件，`<nix/fetchurl.nix>` 的下载将会失败。

  `<nix/fetchurl.nix>` 也被称为内建 derivation 构建器 `builtin:fetchurl`。它不应与求值期函数 `builtins.fetchurl` 混淆，后者不受此问题影响。


## 贡献者

本发布版本得益于以下 58 位贡献者：

- 1444 [**(@0x5a4)**](https://github.com/0x5a4)
- Adrian Hesketh [**(@a-h)**](https://github.com/a-h)
- Aleksana [**(@Aleksanaa)**](https://github.com/Aleksanaa)
- Alyssa Ross [**(@alyssais)**](https://github.com/alyssais)
- Andrew Marshall [**(@amarshall)**](https://github.com/amarshall)
- Artemis Tosini [**(@artemist)**](https://github.com/artemist)
- Artturin [**(@Artturin)**](https://github.com/Artturin)
- Bjørn Forsman [**(@bjornfor)**](https://github.com/bjornfor)
- Brian McGee [**(@brianmcgee)**](https://github.com/brianmcgee)
- Brian McKenna [**(@puffnfresh)**](https://github.com/puffnfresh)
- Bryan Honof [**(@bryanhonof)**](https://github.com/bryanhonof)
- Cole Helbling [**(@cole-h)**](https://github.com/cole-h)
- Eelco Dolstra [**(@edolstra)**](https://github.com/edolstra)
- Eman Resu [**(@llakala)**](https://github.com/llakala)
- Emery Hemingway [**(@ehmry)**](https://github.com/ehmry)
- Emil Petersen [**(@leetemil)**](https://github.com/leetemil)
- Emily [**(@emilazy)**](https://github.com/emilazy)
- Geoffrey Thomas [**(@geofft)**](https://github.com/geofft)
- Gerg-L [**(@Gerg-L)**](https://github.com/Gerg-L)
- Ivan Tkachev
- Jacek Galowicz [**(@tfc)**](https://github.com/tfc)
- Jan Hrcek [**(@jhrcek)**](https://github.com/jhrcek)
- Jason Yundt [**(@Jayman2000)**](https://github.com/Jayman2000)
- Jeremy Kerfs [**(@jkerfs)**](https://github.com/jkerfs)
- Jeremy Kolb [**(@kjeremy)**](https://github.com/kjeremy)
- John Ericson [**(@Ericson2314)**](https://github.com/Ericson2314)
- Jonas Chevalier [**(@zimbatm)**](https://github.com/zimbatm)
- Jordan Justen [**(@jljusten)**](https://github.com/jljusten)
- Josh Heinrichs [**(@joshheinrichs-shopify)**](https://github.com/joshheinrichs-shopify)
- Jörg Thalheim [**(@Mic92)**](https://github.com/Mic92)
- Kevin Cox [**(@kevincox)**](https://github.com/kevincox)
- Michael Gallagher [**(@mjgallag)**](https://github.com/mjgallag)
- Michael [**(@michaelvanstraten)**](https://github.com/michaelvanstraten)
- Nikodem Rabuliński [**(@nrabulinski)**](https://github.com/nrabulinski)
- Noam Yorav-Raphael [**(@noamraph)**](https://github.com/noamraph)
- Onni Hakala [**(@onnimonni)**](https://github.com/onnimonni)
- Parker Hoyes [**(@parkerhoyes)**](https://github.com/parkerhoyes)
- Philipp Otterbein
- Pol Dellaiera [**(@drupol)**](https://github.com/drupol)
- Robert Hensing [**(@roberth)**](https://github.com/roberth)
- Ryan Hendrickson [**(@rhendric)**](https://github.com/rhendric)
- Sandro [**(@SuperSandro2000)**](https://github.com/SuperSandro2000)
- Seggy Umboh [**(@secobarbital)**](https://github.com/secobarbital)
- Sergei Zimmerman [**(@xokdvium)**](https://github.com/xokdvium)
- Shivaraj B H [**(@shivaraj-bh)**](https://github.com/shivaraj-bh)
- Siddhant Kumar [**(@siddhantk232)**](https://github.com/siddhantk232)
- Tim [**(@Jaculabilis)**](https://github.com/Jaculabilis)
- Tom Bereknyei
- Travis A. Everett [**(@abathur)**](https://github.com/abathur)
- Valentin Gagarin [**(@fricklerhandwerk)**](https://github.com/fricklerhandwerk)
- Vinayak Kaushik [**(@VinayakKaushikDH)**](https://github.com/VinayakKaushikDH)
- Yann Hamdaoui [**(@yannham)**](https://github.com/yannham)
- Yuriy Taraday [**(@YorikSar)**](https://github.com/YorikSar)
- bryango [**(@bryango)**](https://github.com/bryango)
- emhamm [**(@emhamm)**](https://github.com/emhamm)
- jade [**(@lf-)**](https://github.com/lf-)
- kenji [**(@a-kenji)**](https://github.com/a-kenji)
- pennae [**(@pennae)**](https://github.com/pennae)
- puckipedia [**(@puckipedia)**](https://github.com/puckipedia)
- squalus [**(@squalus)**](https://github.com/squalus)
- tomberek [**(@tomberek)**](https://github.com/tomberek)
