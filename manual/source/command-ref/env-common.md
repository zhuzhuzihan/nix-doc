# 通用环境变量

大多数 Nix 命令都会解释以下环境变量。

## 配置类环境变量

以下环境变量影响 Nix 加载其配置的方式。
完整细节请参见[配置文件](@docroot@/command-ref/conf-file.md#configuration-file)文档。

- <span id="env-NIX_CONF_DIR">[`NIX_CONF_DIR`](#env-NIX_CONF_DIR)</span>

  覆盖系统配置目录。

- <span id="env-NIX_USER_CONF_FILES">[`NIX_USER_CONF_FILES`](#env-NIX_USER_CONF_FILES)</span>

  覆盖用户配置文件的位置。

- <span id="env-NIX_CONFIG">[`NIX_CONFIG`](#env-NIX_CONFIG)</span>

  以内联方式提供配置设置。

## store 设置类环境变量

- <span id="env-NIX_IGNORE_SYMLINK_STORE">[`NIX_IGNORE_SYMLINK_STORE`](#env-NIX_IGNORE_SYMLINK_STORE)</span>

  通常，Nix store 目录（通常是 `/nix/store`）
  的路径中不允许包含任何符号链接组件。这是为了防止
  “不纯”的构建。构建器有时会通过
  解析所有符号链接组件来“规范化（canonicalise）”路径。因此，在不同机器上
  （`/nix/store` 解析到不同位置）进行的构建可能产生
  不同的结果。这通常不是问题，除非
  构建被部署到 `/nix/store` 解析结果
  不同的机器上。如果你确定不会这样做，你
  可以将 `NIX_IGNORE_SYMLINK_STORE` 设置为 `1`。

  请注意，如果你是为了把 Nix store 放到
  根文件系统之外的另一个文件系统上而对其使用符号链接，在 Linux 上
  更好的做法是使用 `bind` 挂载点，例如：

  ```console
  $ mkdir /nix
  $ mount -o bind /mnt/otherdisk/nix /nix
  ```

  详情请查阅 mount 8 手册页。

- <span id="env-NIX_STORE_DIR">[`NIX_STORE_DIR`](#env-NIX_STORE_DIR)</span>

  覆盖 Nix store 的位置。
  在 Unix 上，默认值为 `/nix/store`，由编译期的 `libstore:store-dir` 构建选项设置。
  在 Windows 上没有编译期设置；默认值为 `%PROGRAMDATA%\nix\store`，运行时通过 [`%PROGRAMDATA%` Known Folder](#known-folders) 确定。

  参见 [Store Types] 一章；每种 store 都有一个 `store` 设置，其默认值指向这里。

- <span id="env-NIX_LOG_DIR">[`NIX_LOG_DIR`](#env-NIX_LOG_DIR)</span>

  覆盖 Nix 日志目录的位置。
  在 Unix 上，默认值为 `/nix/var/log/nix`，由编译期的 `log-dir` 构建选项设置。
  在 Windows 上没有编译期设置；默认值为 `%PROGRAMDATA%\nix\log`，运行时通过 [`%PROGRAMDATA%` Known Folder](#known-folders) 确定。

  [Local Store]、[Local Daemon Store] 和 [Experimental SSH Store with filesystem mounted] 都有覆盖此项的 per-store 设置。

- <span id="env-NIX_STATE_DIR">[`NIX_STATE_DIR`](#env-NIX_STATE_DIR)</span>

  覆盖 Nix 状态目录的位置。
  在 Unix 上，默认值为 `${localstatedir}/nix`，其中 `localstatedir` 是一个编译期构建选项，默认为 `/nix/var`。
  在 Windows 上没有编译期设置；默认值为 `%PROGRAMDATA%\nix\state`，运行时通过 [`%PROGRAMDATA%` Known Folder](#known-folders) 确定。

  [Local Store]、[Local Daemon Store] 和 [Experimental SSH Store with filesystem mounted] 都有覆盖此项的 per-store 设置。

- <span id="env-NIX_DAEMON_SOCKET_PATH">[`NIX_DAEMON_SOCKET_PATH`](#env-NIX_DAEMON_SOCKET_PATH)</span>

  覆盖用于与 Nix daemon（守护进程）通信的 Unix domain socket 的路径。
  默认为状态目录中的 `daemon-socket/socket`（参见 [`NIX_STATE_DIR`](#env-NIX_STATE_DIR)）。

  关于 socket 路径如何解析的细节，请参见 [Local Daemon Store] 文档。

- <span id="env-TMPDIR">[`TMPDIR`](#env-TMPDIR)</span>

  使用指定目录存放临时文件。特别是，
  其中包括临时构建目录；它们可能占用
  相当可观的磁盘空间。默认值为 `/tmp`。

- <span id="env-NIX_REMOTE">[`NIX_REMOTE`](#env-NIX_REMOTE)</span>

  覆盖 [`store`](@docroot@/command-ref/conf-file.md#conf-store) 设置。

[Store Types]: @docroot@/store/types/index.md
[store URL format]: @docroot@/store/types/index.md#store-url-format
[Local Store]: @docroot@/store/types/local-store.md
[Local Daemon Store]: @docroot@/store/types/local-daemon-store.md
[Experimental SSH Store with filesystem mounted]: @docroot@/store/types/experimental-ssh-store-with-filesystem-mounted.md

## Nix 语言求值器设置

- <span id="env-NIX_SHOW_STATS">[`NIX_SHOW_STATS`](#env-NIX_SHOW_STATS)</span>

  如果设置为 `1`，Nix 将打印一些求值统计信息，例如
  分配的值的数量。

- <span id="env-NIX_COUNT_CALLS">[`NIX_COUNT_CALLS`](#env-NIX_COUNT_CALLS)</span>

  如果设置为 `1`，Nix 将打印 Nix 表达式求值期间
  函数被调用的次数。这对于对 Nix
  表达式做性能分析很有用。

- <span id="env-GC_INITIAL_HEAP_SIZE">[`GC_INITIAL_HEAP_SIZE`](#env-GC_INITIAL_HEAP_SIZE)</span>

  如果 Nix 被配置为使用 Boehm 垃圾回收器，这个
  变量以字节为单位设置堆的初始大小。默认值为
  384 MiB。将其设为较小的值可以降低内存占用，但由于垃圾回收的开销，
  会增加运行时间。

- <span id="env-NIX_PATH">[`NIX_PATH`](#env-NIX_PATH)</span>

  以冒号分隔的搜索路径条目列表，用于解析 [lookup paths](@docroot@/language/constructs/lookup-path.md)。

  此环境变量覆盖 [`nix-path` 配置设置](@docroot@/command-ref/conf-file.md#conf-nix-path)的值。

  可以使用 [`-I` 选项](@docroot@/command-ref/opt-common.md#opt-I)扩展。

  > **示例**
  >
  > ```bash
  > $ export NIX_PATH=/home/eelco/Dev:nixos-config=/etc/nixos
  > ```

  如果 `NIX_PATH` 被设置为空字符串，解析搜索路径将总是失败。

  > **示例**
  >
  > ```bash
  > $ NIX_PATH= nix-instantiate --eval '<nixpkgs>'
  > error: file 'nixpkgs' was not found in the Nix search path (add it using $NIX_PATH or -I)
  > ```

## 用户目录

Nix 支持针对每个用户的**配置**、**状态**和**缓存**目录。
以下环境变量覆盖这些目录的位置：

- [用户配置目录]{#user-conf-dir}：[`NIX_CONFIG_HOME`]{#env-NIX_CONFIG_HOME}
- 用户状态目录：[`NIX_STATE_HOME`]{#env-NIX_STATE_HOME}
- 用户缓存目录：[`NIX_CACHE_HOME`]{#env-NIX_CACHE_HOME}

当这些变量未设置时，默认值取决于平台：

- 在 Unix 上，为 [XDG base directories](#xdg-base-directories)：`$XDG_CONFIG_HOME/nix`、`$XDG_STATE_HOME/nix`、`$XDG_CACHE_HOME/nix`
- 在 Windows 上，为 [Windows Known Folders](#known-folders)：`%APPDATA%\nix\config`、`%LOCALAPPDATA%\nix\state`、`%LOCALAPPDATA%\nix\cache`

[`use-xdg-base-directories`]: @docroot@/command-ref/conf-file.md#conf-use-xdg-base-directories

为了向后兼容，旧式 Nix 命令（例如 `nix-env`、`nix-channel`）使用 `$HOME` 中的点文件而非这些目录，除非启用了 [`use-xdg-base-directories`]。
[新式 Nix 命令](@docroot@/command-ref/new-cli/nix.md)（实验性）默认使用正确的目录。

启用 [`use-xdg-base-directories`] 时，配置目录按如下方式解析：

1. `$NIX_CONFIG_HOME`，如果它已定义
2. 否则，使用平台默认值（例如 Unix 上的 `$XDG_CONFIG_HOME/nix`）

状态目录和缓存目录的处理方式相同。

## 其他环境变量

- <span id="env-IN_NIX_SHELL">[`IN_NIX_SHELL`](#env-IN_NIX_SHELL)</span>

  指示当前环境是否由
  `nix-shell` 建立。它可以取值 `pure` 或 `impure`。

## 附录：操作系统特定约定

此信息并非 Nix 特有，但上文引用了它。

### Unix：XDG Base Directories {#xdg-base-directories}

[XDG Base Directory Specification] 定义了 Unix 系统上用户专属配置、状态和缓存文件的标准位置。

[XDG Base Directory Specification]: https://specifications.freedesktop.org/basedir-spec/basedir-spec-latest.html

使用以下环境变量：

- [`XDG_CONFIG_HOME`]{#env-XDG_CONFIG_HOME}（默认 `~/.config`）
- [`XDG_STATE_HOME`]{#env-XDG_STATE_HOME}（默认 `~/.local/state`）
- [`XDG_CACHE_HOME`]{#env-XDG_CACHE_HOME}（默认 `~/.cache`）
- [`XDG_CONFIG_DIRS`]{#env-XDG_CONFIG_DIRS}（默认 `/etc/xdg`）——以冒号分隔的附加配置基础目录列表，在 `XDG_CONFIG_HOME` 之后搜索

### Windows：Known Folders {#known-folders}

在 Windows 上，[Known Folders][windows-known-folders] 为 Windows 上的应用数据提供标准位置。

[windows-known-folders]: https://learn.microsoft.com/en-us/windows/win32/shell/known-folders

相关的文件夹包括：

- [`%APPDATA%`]{#env-APPDATA} —— 每个用户的漫游应用数据
- [`%LOCALAPPDATA%`]{#env-LOCALAPPDATA} —— 每个用户的本地应用数据
- [`%PROGRAMDATA%`]{#env-PROGRAMDATA} —— 系统级应用数据
