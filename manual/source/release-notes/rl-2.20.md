# Release 2.20.0 (2024-01-29)

- 选项 `allowed-uris` 现在可以匹配 URI 中不带斜杠的完整协议（scheme） [#9547](https://github.com/NixOS/nix/pull/9547)

  如果在 `allowed-uris` 选项中指定了类似 `github:` 这样的协议，则所有以 `github:` 开头的 URI 都会被允许。
  此前该行为仅对 URI 使用 `://` 语法的协议有效。

- 通过 daemon（守护进程）构建时包含 cgroup 统计信息 [#9598](https://github.com/NixOS/nix/pull/9598)

  当连接双方使用的都是 Nix 2.20 或更新版本时，Nix 在通过 Nix daemon 构建以及使用 `ssh-ng` 进行远程构建时，现在也会报告 cgroup 统计信息。

- `nix search` 不再允许空的搜索正则表达式 [#9481](https://github.com/NixOS/nix/pull/9481)

  [`nix search`](@docroot@/command-ref/new-cli/nix3-search.md) 现在要求必须传入搜索正则表达式。要显示所有软件包，请使用 `^`。

- 新增 `eval-system` 设置 [#4093](https://github.com/NixOS/nix/pull/4093)

  新增 `eval-system` 选项。
  与 `system` 不同，它只覆盖 `builtins.currentSystem` 的值。
  这比覆盖 `system` 更有用，因为你可以在支持目标系统的远程构建机上构建这些 derivation（派生）。
  相比之下，`system` 还会影响调度，这会导致 Nix 即使在本地构建毫无意义的情况下，也在本地构建这些 derivation。

  `eval-system` 仅在其值非空时生效。
  如果为空（默认值），则和以前一样使用 `system`，因此不会造成任何破坏。

- Import-from-derivation 现在在构建用的 store 中构建 derivation [#9661](https://github.com/NixOS/nix/pull/9661)

  使用 `--eval-store` 时，从 derivation 进行 `import` 现在会使该 derivation 在构建用的 store 中构建，即 `store` Nix 选项指定的 store。

  由于生成的 Nix 表达式必须复制回求值（evaluation）用的 store 才能被导入，这要求求值 store 信任构建 store 的签名。

- Mounted SSH Store [#7890](https://github.com/NixOS/nix/issues/7890) [#7912](https://github.com/NixOS/nix/pull/7912)

  引入了 store [`mounted-ssh-ng://`](@docroot@/command-ref/new-cli/nix3-help-stores.md)。
  该 store 允许完全访问远程机器上的 Nix store，并额外要求该 store 被挂载到本地文件系统中。

- 将 `nix show-config` 重命名为 `nix config show` [#7672](https://github.com/NixOS/nix/issues/7672) [#9477](https://github.com/NixOS/nix/pull/9477)

  `nix show-config` 被重命名为 `nix config show`，`nix doctor` 被重命名为 `nix config check`，以便与命令行界面的其他部分保持一致。

- 新增命令 `nix hash convert` [#9452](https://github.com/NixOS/nix/pull/9452)

  它取代了旧的 `nix hash to-*` 命令，旧命令仍然可用，但会发出弃用警告。请按如下方式转换：

  - `nix hash to-base16 $hash1 $hash2`：改用 `nix hash convert --to base16 $hash1 $hash2`。
  - `nix hash to-base32 $hash1 $hash2`：改用 `nix hash convert --to nix32 $hash1 $hash2`。
  - `nix hash to-base64 $hash1 $hash2`：改用 `nix hash convert --to base64 $hash1 $hash2`。
  - `nix hash to-sri $hash1 $hash2`：: 改用 `nix hash convert --to sri $hash1 $hash2`，甚至可以直接使用 `nix hash convert $hash1 $hash2`。

- 将哈希格式 `base32` 重命名为 `nix32` [#9452](https://github.com/NixOS/nix/pull/9452)

  哈希格式 `base32` 被重命名为 `nix32`，因为它使用了一套 Nix 特有的 [Base32](https://en.wikipedia.org/wiki/Base32) 字符集。

- `nix profile` 现在允许通过人类可读的名称引用元素 [#8678](https://github.com/NixOS/nix/pull/8678)

  [`nix profile`](@docroot@/command-ref/new-cli/nix3-profile.md) 在运行 [`list`](@docroot@/command-ref/new-cli/nix3-profile-list.md)、[`remove`](@docroot@/command-ref/new-cli/nix3-profile-remove.md) 或 [`upgrade`](@docroot@/command-ref/new-cli/nix3-profile-upgrade.md) 时，现在使用名称而非索引来指代已安装的软件包。Profile 元素名称在软件包安装时生成，并在该软件包被移除之前保持不变。

  **警告**：用于记录 profile 内容的 `manifest.nix` 文件已经变更。当你修改 profile 时，Nix 会自动将 profile 升级到新版本。此后，旧版本的 Nix 将无法再使用该 profile。

- 为 `nix store add` 添加 `--hash-algo` 标志 [#9809](https://github.com/NixOS/nix/pull/9809)

  补齐了旧 CLI 中已有而新 CLI 缺失的功能，同时这也符合我们为 `nix hash convert` 和 `nix hash path` 提供类似标志的计划。

- 强制转换（coercion）错误会包含出错的值

  `error: cannot coerce a <TYPE> to a string` 消息现在会包含导致该错误的值。

  之前：

  ```
  error: cannot coerce a set to a string
  ```

  之后：

  ```
  error: cannot coerce a set to a string: { aesSupport = «thunk»;
    avx2Support = «thunk»; avx512Support = «thunk»; avxSupport = «thunk»;
    canExecute = «thunk»; config = «thunk»; darwinArch = «thunk»; darwinMinVersion
    = «thunk»; darwinMinVersionVariable = «thunk»; darwinPlatform = «thunk»; «84
    attributes elided»}
  ```

- 类型错误会包含出错的值

  在 `value is an integer while a list was expected` 这类错误中，消息现在会包含出错的值。

  之前：

  ```
  error: value is a set while a string was expected
  ```

  之后：

  ```
  error: expected a string but found a set: { ghc810 = «thunk»;
    ghc8102Binary = «thunk»; ghc8107 = «thunk»; ghc8107Binary = «thunk»;
    ghc865Binary = «thunk»; ghc90 = «thunk»; ghc902 = «thunk»; ghc92 = «thunk»;
    ghc924Binary = «thunk»; ghc925 = «thunk»;  «17 attributes elided»}
  ```

- 错误信息中的源代码位置打印更加一致 [#561](https://github.com/NixOS/nix/issues/561) [#9555](https://github.com/NixOS/nix/pull/9555)

  错误信息现在会更一致地包含源代码位置信息。对于以下代码：

  ```nix
  let
    attr = {foo = "bar";};
    key = {};
  in
    attr.${key}
  ```

  此前，Nix 在尝试对它求值时会显示这条毫无帮助的消息：

  ```
  error:
         … while evaluating an attribute name

         error: value is a set while a string was expected
  ```

  现在，错误信息会显示问题值出现的位置：

  ```
  error:
         … while evaluating an attribute name

           at bad.nix:4:11:

              3|   key = {};
              4| in attr.${key}
               |           ^
              5|

         error: expected a string but found a set
  ```

- 修复了部分栈溢出段错误 [#9616](https://github.com/NixOS/nix/issues/9616) [#9617](https://github.com/NixOS/nix/pull/9617)

  现在限制了嵌套函数调用的数量，以检测并报告无限的函数调用递归。默认最大调用深度为 10,000，可以通过 [the `max-call-depth`
  option](@docroot@/command-ref/conf-file.md#conf-max-call-depth) 进行设置。

  它取代了原来的 `stack overflow (possible infinite recursion)` 消息。

- `with` 表达式的错误报告得到改进 [#9658](https://github.com/NixOS/nix/pull/9658)

  使用非 attrset 值来解析变量的 `with` 表达式现在会以正确的位置报告，例如：

  ```
  nix-repl> with 1; a
  error:
         … while evaluating the first subexpression of a with expression
           at «string»:1:1:
              1| with 1; a
               | ^

         error: expected a set but found an integer
  ```

- 函数打印时包含更多细节 [#7145](https://github.com/NixOS/nix/issues/7145) [#9606](https://github.com/NixOS/nix/pull/9606)

  `nix repl`、`nix eval`、`builtins.trace` 以及大多数其他打印值的地方，现在会包含函数名称和源代码位置信息：

  ```
  $ nix repl nixpkgs
  nix-repl> builtins.map
  «primop map»

  nix-repl> builtins.map lib.id
  «partially applied primop map»

  nix-repl> builtins.trace lib.id "my-value"
  trace: «lambda id @ /nix/store/kgr5lnaiiv08wb7k324yv1i1npjmrvjc-source/lib/trivial.nix:26:5»
  "my-value"
  ```

- 当 `flake.lock` 文件被 `.gitignore` 忽略时，在 Git 仓库中运行 `nix develop` 等 Flakes 操作不再失败
  [#8854](https://github.com/NixOS/nix/issues/8854)
  [#9324](https://github.com/NixOS/nix/pull/9324)

- Nix 命令现在会正确响应 Ctrl-C
  [#7145](https://github.com/NixOS/nix/issues/7145)
  [#6995](https://github.com/NixOS/nix/pull/6995)
  [#9687](https://github.com/NixOS/nix/pull/9687)

  此前，如果在执行各种操作（包括 `nix develop`、`nix flake
  update` 等）时按下 Ctrl-C，许多 Nix 命令会无限期挂起。经过对 Nix 信号处理程序的若干修复，现在 Nix 命令在按下 Ctrl-C 后会快速退出。

- `nix copy` 到 `ssh-ng` store 现在需要 `--substitute-on-destination`（即 `-s`）才能在远程 store 上用 substitute 代替复制路径。
  该行为与其他类型远程 store 的 `nix copy` 行为保持一致。
  此前该行为由 `builders-use-substitutes` 设置控制，而 `--substitute-on-destination` 会被忽略。
