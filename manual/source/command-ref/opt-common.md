<!-- Some of the options documented here are hardcopied from
     src/libcmd/common-eval-args.cc
-->

# 通用选项

大多数 Nix 命令接受以下命令行选项：

- <span id="opt-help">[`--help`](#opt-help)</span>

  打印命令语法摘要并退出。

- <span id="opt-version">[`--version`](#opt-version)</span>

  将 Nix 版本号打印到标准输出并退出。

  关于机器可读的输出（包括 Nix 所链接
  库的版本），请参见 [`nix version`](@docroot@/command-ref/new-cli/nix3-version.md) 命令。

- <span id="opt-verbose">[`--verbose`](#opt-verbose)</span> / `-v`

  提高打印到标准错误的诊断消息的详细程度。
  对于每个 Nix 操作，打印到标准输出的信息是有明确定义的；
  任何诊断信息都打印到标准错误，绝不会打印到标准输出。

  此选项可以重复指定。
  目前存在以下详细程度级别：

  - `0` “Errors only”（仅错误）

    只打印解释 Nix 调用为何失败的消息。

  - `1` “Informational”（信息性）

    打印关于 Nix 正在做什么的*有用*消息。
    这是默认级别。

  - `2` “Talkative”

    打印更多的信息性消息。

  - `3` “Chatty”

    打印更多的信息性消息。

  - `4` “Debug”

    打印调试信息。

  - `5` “Vomit”

    打印海量的调试信息。

- <span id="opt-quiet">[`--quiet`](#opt-quiet)</span>

  降低打印到标准错误的诊断消息的详细程度。
  它是 `-v` / `--verbose` 的反向选项。

  此选项可以重复指定。
  参见上一条详细程度级别列表。

- <span id="opt-log-format">[`--log-format`](#opt-log-format)</span> *format*

  此选项可用于更改日志格式的输出，*format* 为以下之一：

  - `raw`

    这是原始格式，如同 nix-build 输出的那样。

  - `internal-json`

    以结构化方式输出日志。

    > **警告**
    >
    > 虽然 schema 本身相对稳定，但错误消息
    > 的格式（即 `msg` 字段）在各个
    > 版本之间可能发生变化。

  - `bar`

    在构建期间只显示进度条。

  - `bar-with-logs`

    显示原始日志，进度条位于底部。

- <span id="opt-no-build-output">[`--no-build-output`](#opt-no-build-output)</span> / `-Q`

  默认情况下，构建器写到标准输出和标准错误的内容会被转发到 Nix 命令的标准错误。
  此选项抑制这种行为。
  请注意，构建器的标准输出和标准错误始终会写入 `prefix/nix/var/log/nix` 中的一个日志文件。

- <span id="opt-max-jobs">[`--max-jobs`](#opt-max-jobs)</span> / `-j` *number*

  将 Nix 并行执行的构建任务的最大数量设置为指定数值。
  指定 `auto` 可使用系统中的 CPU 数量。
  默认值由 `max-jobs` 配置设置指定，而它本身默认为 `1`。
  在 SMP 系统上或为了利用 I/O 延迟时，更大的值很有用。

  将其设为 `0` 禁止在本地机器上构建，当你希望构建只在远程构建器上发生时很有用。

- <span id="opt-cores">[`--cores`](#opt-cores)</span>

  在调用构建器时设置 `NIX_BUILD_CORES` 环境变量的值。
  构建器可自行决定使用该变量来控制最大并行度。
  例如，在 Nixpkgs 中，如果 derivation 属性 `enableParallelBuilding` 被设置为 `true`，构建器会将 `-jN` 标志传给 GNU Make。
  它默认为 `cores` 配置设置的值（如果设置了），否则为 `1`。
  值 `0` 表示构建器应使用系统中所有可用的 CPU 核心。

- <span id="opt-max-silent-time">[`--max-silent-time`](#opt-max-silent-time)</span>

  设置构建器在标准输出或标准错误上不产生任何数据的最长秒数。
  默认值由 `max-silent-time` 配置设置指定。
  `0` 表示没有超时。

- <span id="opt-timeout">[`--timeout`](#opt-timeout)</span>

  设置构建器可以运行的最长秒数。
  默认值由 `timeout` 配置设置指定。
  `0` 表示没有超时。

- <span id="opt-keep-going">[`--keep-going`](#opt-keep-going)</span> / `-k`

  在构建失败时尽可能地继续进行。
  也就是说，如果某个 derivation 的某个输入构建失败，Nix 仍会构建其他输入，但不构建该 derivation 本身。
  没有此选项时，任何构建失败都会使 Nix 停止（substitute 的构建除外），可能杀死正在进行中的构建（在并行或分布式构建的情况下）。

- <span id="opt-keep-failed">[`--keep-failed`](#opt-keep-failed)</span> / `-K`

  指定在构建失败的情况下，构建所在的临时目录（通常位于 `/tmp`）不应被删除。
  构建目录的路径会作为信息性消息打印出来。

- <span id="opt-fallback">[`--fallback`](#opt-fallback)</span>

  每当 Nix 尝试构建一个其每个输出路径都已知有 substitute（替代）的 derivation，但通过这些 substitute 实现输出路径失败时，回退为直接构建该 derivation。

  这种做法最有用的最常见场景是：我们注册了 substitute 以便从某个（例如）网络仓库执行二进制分发。
  如果该仓库不可用，derivation 的实现（realisation）就会失败。
  指定此选项后，Nix 将改为构建该 derivation。
  这样，从二进制安装就回退为从源码安装。
  此选项不是默认行为，因为 substitute 获取过程中的瞬时故障一般不应导致完整的源码构建（以及相关的资源消耗）。

- <span id="opt-readonly-mode">[`--readonly-mode`](#opt-readonly-mode)</span>

  使用此选项时，不会尝试打开 Nix 数据库。
  大多数 Nix 操作确实需要访问数据库，因此这些操作会失败。

- <span id="opt-arg">[`--arg`](#opt-arg)</span> *name* *value*

  此选项被 `nix-env`、`nix-instantiate`、`nix-shell` 和 `nix-build` 接受。
  在对 Nix 表达式求值时，求值器会自动尝试调用它遇到的函数。
  它可以自动调用每个参数都有[默认值](@docroot@/language/syntax.md#functions)的函数（例如 `{ argName ?  defaultValue }: ...`）。

  使用 `--arg`，你还可以调用带有无默认值参数的函数（或覆盖默认值）。
  也就是说，如果求值器遇到一个带有名为 *name* 的参数的函数，它会以值 *value* 调用它。

  例如，Nixpkgs 中的顶层 `default.nix` 实际上是一个函数：

  ```nix
  { # The system (e.g., `i686-linux') for which to build the packages.
    system ? builtins.currentSystem
    ...
  }: ...
  ```

  因此，如果你调用这个 Nix 表达式（例如执行 `nix-env --install --attr pkgname` 时），该函数会被自动调用，`system` 参数取值 [`builtins.currentSystem`](@docroot@/language/builtins.md)。
  你可以使用 `--arg` 覆盖它，例如 `nix-env --install --attr pkgname --arg system \"i686-freebsd\"`。
  （注意，由于参数是 Nix 字符串字面量，你必须转义引号。）

- <span id="opt-arg-from-file">[`--arg-from-file`](#opt-arg-from-file)</span> *name* *path*

  将文件 *path* 的内容作为参数 *name* 传递给 Nix 函数。

- <span id="opt-arg-from-stdin">[`--arg-from-stdin`](#opt-arg-from-stdin)</span> *name*

  将标准输入的内容作为参数 *name* 传递给 Nix 函数。

- <span id="opt-argstr">[`--argstr`](#opt-argstr)</span> *name* *value*

  此选项类似于 `--arg`，只是值不是一个 Nix 表达式而是一个字符串。
  因此你可以用 `--argstr system i686-linux` 代替 `--arg system \"i686-linux\"`（外层引号是为了让 shell 满意）。

- <span id="opt-attr">[`--attr`](#opt-attr)</span> / `-A` *attrPath*

  从被求值的顶层 Nix 表达式中选择一个属性。
  （仅限 `nix-env`、`nix-instantiate`、`nix-build` 和 `nix-shell`。）
  *属性路径* *attrPath* 是一个以点分隔的属性名序列。
  例如，给定顶层 Nix 表达式 *e*，属性路径 `xorg.xorgserver` 会导致使用表达式 `e.xorg.xorgserver`。
  具体示例请参见 [`nix-env --install`](@docroot@/command-ref/nix-env/install.md)。

  除了属性名，你还可以指定数组索引。
  例如，属性路径 `foo.3.bar` 选择顶层表达式
  的 `foo` 属性中数组第四个元素的 `bar`
  属性。

- <span id="opt-eval-store">[`--eval-store`](#opt-eval-store)</span> *store-url*

  用于求值的[指向 Nix store 的 URL](@docroot@/store/types/index.md#store-url-format)，即存放 derivation（`.drv` 文件）及其引用的输入的位置。

- <span id="opt-expr">[`--expr`](#opt-expr)</span> / `-E`

  将命令行参数解释为要解析和求值的 Nix 表达式列表，而不是 Nix 表达式的文件名列表。
  （仅限 `nix-instantiate`、`nix-build` 和 `nix-shell`。）

  对于 `nix-shell`，此选项通常用于给你一个可以在其中构建表达式所返回软件包的 shell。
  如果你想要一个包含*已构建*软件包、可直接使用的 shell，请将表达式传给 `nix-shell --packages ` 这一便捷标志。

- <span id="opt-I">[`-I` / `--include`](#opt-I)</span> *path*

  向用于解析 [lookup paths](@docroot@/language/constructs/lookup-path.md) 的搜索路径列表添加一个条目。
  此选项可以多次给出。

  通过 `-I` 添加的路径优先于 [`nix-path` 配置设置](@docroot@/command-ref/conf-file.md#conf-nix-path)和 [`NIX_PATH` 环境变量](@docroot@/command-ref/env-common.md#env-NIX_PATH)。

- <span id="opt-impure">[`--impure`](#opt-impure)</span>

  允许访问可变路径和仓库。

- <span id="opt-option">[`--option`](#opt-option)</span> *name* *value*

  将 Nix 配置选项 *name* 设置为 *value*。
  这会覆盖 Nix 配置文件中的设置（见 nix.conf5）。

- <span id="opt-repair">[`--repair`](#opt-repair)</span>

  通过重新下载或重新构建来修复损坏或缺失的存储路径。
  请注意这很慢，因为它需要计算构建闭包中每个路径内容的密码学哈希。
  另请注意 `nix-store --repair-path` 下的警告。

> **注意**
>
> 关于用命令行标志覆盖配置设置，请参见 [`man nix.conf`](@docroot@/command-ref/conf-file.md#command-line-flags)。
