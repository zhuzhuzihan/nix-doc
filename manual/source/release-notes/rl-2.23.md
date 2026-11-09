# Release 2.23.0 (2024-06-03)

- 新内建函数：`builtins.warn` [#306026](https://github.com/NixOS/nix/issues/306026) [#10592](https://github.com/NixOS/nix/pull/10592)

  `builtins.warn` 的行为类似于 `builtins.trace "warning: ${msg}"`，具有准确的日志级别，并由选项
  [`debugger-on-trace`](@docroot@/command-ref/conf-file.md#conf-debugger-on-trace)、
  [`debugger-on-warn`](@docroot@/command-ref/conf-file.md#conf-debugger-on-warn) 和
  [`abort-on-warn`](@docroot@/command-ref/conf-file.md#conf-abort-on-warn) 控制。

- 使 `nix build --keep-going` 与 `nix-build --keep-going` 保持一致

  这意味着，例如当多个 fixed-output derivation（派生）构建失败时，会显示所有哈希不匹配的信息。

- 修改 `nix derivation {add,show}` 的 JSON 格式 [#9866](https://github.com/NixOS/nix/issues/9866) [#10722](https://github.com/NixOS/nix/pull/10722)

  derivation 的 JSON 格式经过小幅修订，以更好地符合我们的[数据建模指南](@docroot@/development/data-modeling.md)。
  特别地，内容寻址（content-addressed）derivation 输出的哈希算法和内容寻址方法现在被拆分为 `hashAlgo` 和 `method` 两个字段，而不是原先一个使用晦涩的 `:` 分隔格式的字段。

  目前该 JSON 格式仅被实验性的 `nix derivation` 系列命令使用。
  由于 JSON 格式即使经过这些变更仍未完全符合规范，预计未来还会有进一步的修订。

- 对命令行中任意位置的未知设置发出警告 [#10701](https://github.com/NixOS/nix/pull/10701)

  所有 `nix` 命令现在在命令行任意位置指定了未知选项时，都会正确发出警告。

  之前：

  ```console
  $ nix-instantiate --option foobar baz --expr '{}'
  warning: unknown setting 'foobar'
  $ nix-instantiate '{}' --option foobar baz --expr
  $ nix eval --expr '{}' --option foobar baz
  { }
  ```

  之后：

  ```console
  $ nix-instantiate --option foobar baz --expr '{}'
  warning: unknown setting 'foobar'
  $ nix-instantiate '{}' --option foobar baz --expr
  warning: unknown setting 'foobar'
  $ nix eval --expr '{}' --option foobar baz
  warning: unknown setting 'foobar'
  { }
  ```

- `nix env shell` 是新的 `nix shell`，`nix shell` 仍作为可用的别名保留 [#10504](https://github.com/NixOS/nix/issues/10504) [#10807](https://github.com/NixOS/nix/pull/10807)

  这是为 CLI 子命令带来更多结构化组织的努力的一部分。

  `nix env` 将专注于进程环境。
  未来的命令可能包括 `nix env run` 和 `nix env print-env`。

  它也在一定程度上类似于[计划中的](https://github.com/NixOS/nix/issues/10504) `nix dev shell`（即当前的 `nix develop`）：后者关注的不是环境变量，而是运行一个开发 shell，这是一个更强大的命令，但也需要更多的准备工作。

- 期望得到 derivation 的 Flakes 操作现在会打印出错的值及其类型 [#10778](https://github.com/NixOS/nix/pull/10778)

  在 `flake output attribute 'nixosConfigurations.yuki.config' is not a derivation or path` 这类错误中，消息现在会包含出错的值及其类型。

  之前：

  ```
  error: flake output attribute 'nixosConfigurations.yuki.config' is not a derivation or path
  ````

  之后：

  ```
  error: expected flake output attribute 'nixosConfigurations.yuki.config' to be a derivation or path but found a set: { appstream = «thunk»; assertions = «thunk»; boot = { bcache = «thunk»; binfmt = «thunk»; binfmtMiscRegistrations = «thunk»; blacklistedKernelModules = «thunk»; bootMount = «thunk»; bootspec = «thunk»; cleanTmpDir = «thunk»; consoleLogLevel = «thunk»; «43 attributes elided» }; «48 attributes elided» }
  ```

- `fetchTree` 现在默认浅克隆（shallow clone）Git 仓库 [#10028](https://github.com/NixOS/nix/pull/10028)

  `builtins.fetchTree` 现在默认对 Git 仓库进行浅克隆，这在许多情况下能显著减少网络流量和磁盘占用。

  此前，默认行为是完整克隆特定标签或分支（例如 `ref`）的完整历史，然后才提取某一个特定修订的文件。

  从现在起，`ref` 和 `allRefs` 参数将被忽略，除非通过设置 `shallow = false` 禁用浅克隆。

  `builtins.fetchGit` 的默认行为保持不变。在这里，浅克隆必须通过传入 `shallow = true` 手动启用。

- Store object 信息 JSON 格式现在使用 `null` 而不是省略字段 [#9995](https://github.com/NixOS/nix/pull/9995)

  [store object 信息 JSON 格式](@docroot@/protocols/json/store-object-info.md)（例如用于 `nix path-info`）不再通过省略字段来表示信息缺失，而是以 `null` 值包含这些字段。
  例如，`"ca": null` 用于表示某个 store object 不是内容寻址的，而不是完全省略 `ca` 字段。
  这使得这类记录更具自描述性，也更容易被程序化消费。

  今后我们将遵循这一设计原则；
  贡献者部分中的[数据建模指南](@docroot@/development/data-modeling.md)也已相应更新。

- 大路径警告 [#10661](https://github.com/NixOS/nix/pull/10661)

  当对 Nix 表达式求值导致一个大路径被复制到 Nix store 时，Nix 现在可以发出警告。该警告的阈值可以通过 [the `warn-large-path-threshold`
  setting](@docroot@/command-ref/conf-file.md#conf-warn-large-path-threshold) 配置，
  例如 `--warn-large-path-threshold 100M` 会对大于 100 MiB 的路径发出警告。
