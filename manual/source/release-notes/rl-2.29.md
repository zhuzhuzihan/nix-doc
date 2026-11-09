# Release 2.29.0 (2025-05-14)

在基于向后移植的特殊版本 Nix 2.28（刻意与 Nixpkgs 25.05 同步发布）之后，发布流程从 2.29 起恢复正常。
因此，本次从 `master` 汇集的工作周数比往常略多一些（因为 2.28 是从 2.27 分支出来的）。
不过这一点被另一个事实抵消了：这些变更大多是缺陷修复，而不是较大的新特性。

- 终端上的 JSON 输出美化 [#12555](https://github.com/NixOS/nix/issues/12555) [#12652](https://github.com/NixOS/nix/pull/12652)

  这让输出更易于阅读。

  脚本基本不受影响，因为对脚本而言，stdout 通常是一个文件或管道而不是终端；这种情况仍沿用旧的单行输出行为。

  即使输出不是终端，也可以传入 `--json --pretty` 来启用美化。
  如果你的脚本为 Nix 的 stdout 创建了伪终端，可以传入 `--no-pretty` 来禁用这一新行为。

- REPL：改进不完整表达式的续行提示符 [#12846](https://github.com/NixOS/nix/pull/12846)

  通过将续行提示符从不可见的空白改为可见的 `" > "`，改进了 REPL 的用户体验，让输入多行表达式时更加清晰。

- REPL 的 `:load-flake` 与 `:reload` 现在可以协同工作 [#8753](https://github.com/NixOS/nix/issues/8753) [#13180](https://github.com/NixOS/nix/pull/13180)

  以前，`:reload` 只会重新加载用 `:load`（或在命令行上）指定的文件。
  现在，它对用 `:load-flake`（或在命令行上）指定的 Flakes 也同样生效。
  这样就能正确重新加载此前加载过的所有内容，无论每一项是普通文件还是 Flakes。

- 增大 HTTP 429 Too Many Requests 的重试延迟 [#13052](https://github.com/NixOS/nix/pull/13052)

  下载 Nix 时，重试延迟以前是 0.25 秒，现在已增加到 1 分钟，以便更好地处理瞬时 CI 故障，尤其是 GitHub 上的故障。

- S3：可选择启用 STSProfileCredentialsProvider [#12646](https://github.com/NixOS/nix/pull/12646)

  为基于 S3 的二进制缓存增加了基于 STS 的身份验证支持，即实现与 `aws sso login` 的无缝集成。

- 缩短 HTTP substituter 的连接超时 [#12876](https://github.com/NixOS/nix/pull/12876)

  以前，Nix 设置 `connect-timeout` 没有上限。现在默认设为 `5s`，为自托管二进制缓存的用户提供了更实用的默认值——这类缓存偶尔会不可用，例如在更新期间。


- C API：用于锁定和加载 Flakes 的函数 [#10435](https://github.com/NixOS/nix/issues/10435) [#12877](https://github.com/NixOS/nix/pull/12877) [#13098](https://github.com/NixOS/nix/pull/13098)

  本次发布在 C API 中新增了处理 Flakes 加载的函数。以前只能借助 `builtins.getFlake` 变通实现。
  C API 的使用者和语言绑定现在可以使用基本的锁定功能。

  这里并未暴露完整的锁定 API，以便实现可以更自由地演进。
  锁定由以下函数控制，它们覆盖了使用 Flakes 的常见场景：
  - `nix_flake_lock_flags_set_mode_check`
  - `nix_flake_lock_flags_set_mode_virtual`
  - `nix_flake_lock_flags_set_mode_write_as_needed`
  - `nix_flake_lock_flags_add_input_override`（它同时启用 `virtual`）

  这项变更还引入了新的 `nix-fetchers-c` 库，它目前唯一的用途是管理内置 fetcher 的（`nix.conf`）设置。

  更多细节请参阅 [C API 文档](@docroot@/c-api.md)。

- 不再复制位于 Nix store 中的 Flakes [#10435](https://github.com/NixOS/nix/issues/10435) [#12877](https://github.com/NixOS/nix/pull/12877) [#13098](https://github.com/NixOS/nix/pull/13098)

  以前，我们会把诸如 `path:/nix/store/*` 之类的条目重复复制回 Nix store。
  在 NixOS 中，这一点在使用固定的系统 Flakes 注册表条目时格外明显，例如运行 `nix run nixpkgs#hello` 的时候。

- 一致地保留来自缓存求值的错误消息 [#12762](https://github.com/NixOS/nix/issues/12762) [#12809](https://github.com/NixOS/nix/pull/12809)

  在某个代码路径中，我们此前返回的不是先前求值缓存的错误，而是抛出因值缺失（由错误导致）而产生的通用错误。
  这些通用错误消息的信息量少得多。
  现在我们会一致地返回原始错误消息。

- 更快的 blake3 哈希 [#12676](https://github.com/NixOS/nix/pull/12676)

  blake3 哈希的实现现在是多线程的，并使用了内存映射 IO。
  基准测试结果见该[拉取请求](https://github.com/NixOS/nix/pull/12676)。

- 修复 S3 二进制缓存的进度条，并使文件传输可中断 [#12877](https://github.com/NixOS/nix/issues/12877) [#13098](https://github.com/NixOS/nix/issues/13098) [#12538](https://github.com/NixOS/nix/pull/12538)

  进度条现在能正确显示 S3 上传/下载的进度。S3 上传现在可以中断了。

- 将 github/gitlab flakeref 的 host 属性纳入 URL 序列化 [#12580](https://github.com/NixOS/nix/pull/12580)

  修复了 `github:` 或 `gitlab:` URL 写入 lockfile 时丢失 `host` 属性、从而产生无效 URL 的问题。

- store URL 中的多重签名支持 [#12976](https://github.com/NixOS/nix/pull/12976)

  在 Nix store URI 中增加了对 `secretKeyFiles` URI 参数的支持，允许以逗号分隔的列表形式指定多个签名密钥文件。
  这使得可以用多个密钥对路径签名。这有助于 [RFC #149](https://github.com/NixOS/rfcs/pull/149) 在 NixOS 基础设施中实现二进制缓存密钥轮换。

  用法示例：

  ```bash
  nix copy --to "file:///tmp/store?secret-keys=/tmp/key1,/tmp/key2" \
    "$(nix build --print-out-paths nixpkgs#hello)"
  ```

- nix flake show 现在会跳过依赖从 derivation（派生）导入的输出 [#4265](https://github.com/NixOS/nix/issues/4265) [#12583](https://github.com/NixOS/nix/pull/12583)

  以前，如果某个 Flakes 的输出在求值时依赖[从 derivation 导入](@docroot@/language/import-from-derivation.md)（import-from-derivation），`nix flake show` 将无法显示该 Flakes 的其余部分。更新后的行为会跳过这类输出，从而让 Flakes 的其余部分得以显示。

- 新增 `nix formatter build` 和 `nix formatter run` 命令 [#13063](https://github.com/NixOS/nix/pull/13063)

  `nix formatter run` 是 `nix fmt` 的别名，并无新意。

  `nix formatter build` 则有点类似于 `nix build`：它会构建、链接并打印格式化器程序的路径：

  ```
  $ nix formatter build
  /nix/store/cb9w44vkhk2x4adfxwgdkkf5gjmm856j-treefmt/bin/treefmt
  ```

  注意，与 `nix build` 不同，它打印的是程序的完整路径，而不仅仅是存储路径（在上面的示例中，存储路径是 `/nix/store/cb9w44vkhk2x4adfxwgdkkf5gjmm856j-treefmt`）。

- 修正针对 xterm 风格分隔符的 OSC 8 转义序列剥离 [#13109](https://github.com/NixOS/nix/pull/13109)

  改进终端转义序列的过滤逻辑，使其能够识别第二种类型的超链接转义序列。
  这尤其避免了 GCC 14 的诊断信息中的一部分被错误地过滤掉。


## 贡献者


本次发布由以下 40 位贡献者共同促成：

- Farid Zakaria [**(@fzakaria)**](https://github.com/fzakaria)
- The Tumultuous Unicorn Of Darkness [**(@TheTumultuousUnicornOfDarkness)**](https://github.com/TheTumultuousUnicornOfDarkness)
- Robert Hensing [**(@roberth)**](https://github.com/roberth)
- Félix [**(@picnoir)**](https://github.com/picnoir)
- Valentin Gagarin [**(@fricklerhandwerk)**](https://github.com/fricklerhandwerk)
- Eelco Dolstra [**(@edolstra)**](https://github.com/edolstra)
- Vincent Breitmoser [**(@Valodim)**](https://github.com/Valodim)
- Brian McKenna [**(@puffnfresh)**](https://github.com/puffnfresh)
- ulucs [**(@ulucs)**](https://github.com/ulucs)
- John Ericson [**(@Ericson2314)**](https://github.com/Ericson2314)
- Andrey Butirsky [**(@bam80)**](https://github.com/bam80)
- Dean De Leo [**(@whatsthecraic)**](https://github.com/whatsthecraic)
- Las Safin [**(@L-as)**](https://github.com/L-as)
- Sergei Zimmerman [**(@xokdvium)**](https://github.com/xokdvium)
- Shahar "Dawn" Or [**(@mightyiam)**](https://github.com/mightyiam)
- Ryan Hendrickson [**(@rhendric)**](https://github.com/rhendric)
- Rodney Lorrimar [**(@rvl)**](https://github.com/rvl)
- Erik Nygren [**(@Kirens)**](https://github.com/Kirens)
- Cole Helbling [**(@cole-h)**](https://github.com/cole-h)
- Martin Fischer [**(@not-my-profile)**](https://github.com/not-my-profile)
- Graham Christensen [**(@grahamc)**](https://github.com/grahamc)
- Vit Gottwald [**(@VitGottwald)**](https://github.com/VitGottwald)
- silvanshade [**(@silvanshade)**](https://github.com/silvanshade)
- Illia Bobyr [**(@ilya-bobyr)**](https://github.com/ilya-bobyr)
- Jeremy Fleischman [**(@jfly)**](https://github.com/jfly)
- Ruby Rose [**(@oldshensheep)**](https://github.com/oldshensheep)
- Sergei Trofimovich [**(@trofi)**](https://github.com/trofi)
- Tim [**(@Jaculabilis)**](https://github.com/Jaculabilis)
- Anthony Wang [**(@anthowan)**](https://github.com/anthowan)
- Jörg Thalheim [**(@Mic92)**](https://github.com/Mic92)
- Sandro [**(@SuperSandro2000)**](https://github.com/SuperSandro2000)
- tomberek [**(@tomberek)**](https://github.com/tomberek)
- Dmitry Bogatov [**(@KAction)**](https://github.com/KAction)
- Sizhe Zhao [**(@Prince213)**](https://github.com/Prince213)
- jade [**(@lf-)**](https://github.com/lf-)
- Pierre-Etienne Meunier [**(@P-E-Meunier)**](https://github.com/P-E-Meunier)
- Alexander Romanov [**(@ajlekcahdp4)**](https://github.com/ajlekcahdp4)
- Domagoj Mišković [**(@allrealmsoflife)**](https://github.com/allrealmsoflife)
- Thomas Miedema [**(@thomie)**](https://github.com/thomie)
- Yannik Sander [**(@ysndr)**](https://github.com/ysndr)
- Philipp Otterbein
- Dmitry Bogatov
