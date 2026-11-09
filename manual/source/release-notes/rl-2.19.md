# Release 2.19 (2023-11-17)

- 实验性的 `nix` 命令现在可以作为 [shebang 解释器](@docroot@/command-ref/new-cli/nix.md#shebang-interpreter)使用，
  它会把所有 `#! nix` 行的内容和脚本自身的位置合并进一次调用。

- [URL 形式的 flake reference](@docroot@/command-ref/new-cli/nix3-flake.md#flake-references) 现在支持[百分号编码](https://datatracker.ietf.org/doc/html/rfc3986#section-2.1)的字符。

- [类路径形式的 flake reference](@docroot@/command-ref/new-cli/nix3-flake.md#path-like-syntax) 现在接受任意 unicode 字符（`#` 和 `?` 除外）。

- 实验性特性 `repl-flake` 不再需要，因为其功能现在已成为 `flakes` 实验性特性的一部分。要获得原先的行为，请相应地使用 `--file/--expr` 标志。

- 新的 flake installable 语法 `flakeref#.attrPath`，其中 "." 前缀表示 `attrPath` 从 flake 输出的根开始解释，不搜索诸如 `packages.<SYSTEM>` 或 `legacyPackages.<SYSTEM>` 之类的默认属性前缀。

- Nix 在支持虚拟化的 macOS 系统上把 `apple-virt` 加入默认的 system features。这类似于 Linux 主机上对 `kvm` system feature 的做法。

- 新增内置函数 [`builtins.convertHash`](@docroot@/language/builtins.md#builtins-convertHash)。

- `nix-shell` shebang 行现在支持单引号括起来的参数。

- `builtins.fetchTree` 现在是独立的实验性特性，[`fetch-tree`](@docroot@/development/experimental-features.md#xp-feature-fetch-tree)。
  这使得它可以独立于 [`flakes`](@docroot@/development/experimental-features.md#xp-feature-flakes) 所涵盖的其余内容单独稳定下来。

- 创建和更新 lock 文件的界面经过了彻底改造：

  - [`nix flake lock`](@docroot@/command-ref/new-cli/nix3-flake-lock.md) 现在只创建 lock 文件并添加缺失的输入。
    它*绝不会*更新已有的输入。

  - [`nix flake update`](@docroot@/command-ref/new-cli/nix3-flake-update.md) 做同样的事，但*会*更新输入。
    - 不传参数时会更新当前 flake 的所有输入，与它此前的行为一致。
    - 把输入名作为参数传入时，将确保只更新这些输入。这取代了 `nix flake lock --update-input` 的功能
    - 要操作当前目录之外的 flake，你现在必须传 `--flake path/to/flake`。

  - flake 专属标志 `--recreate-lock-file` 和 `--update-input` 已从所有操作 installable 的命令中移除。
    它们被 `nix flake update` 取代。

- 为 [`builtins.fetchGit`](@docroot@/language/builtins.md#builtins-fetchGit) 增加 commit 签名验证，作为新的 [`verified-fetches` 实验性特性](@docroot@/development/experimental-features.md#xp-feature-verified-fetches)。

- [`nix path-info --json`](@docroot@/command-ref/new-cli/nix3-path-info.md)
  （实验性）现在返回 JSON 映射（map）而不是 JSON 列表。
  每个对象的 `path` 字段改为了外层映射的键，因为它本身是唯一的。
  `valid` 字段也被移除，因为我们直接用 `null` 来表示。

  - 旧形式：

    ```json5
    [
      {
        "path": "/nix/store/fvqsvk65d38p8qqir371ii0hyqxvjcw6-bash-5.2-p15",
        "valid": true,
        // ...
      },
      {
        "path": "/nix/store/wffw7l0alvs3iw94cbgi1gmmbmw99sqb-home-manager-path",
        "valid": false
      }
    ]
    ```

  - 新形式

    ```json5
    {
      "/nix/store/fvqsvk65d38p8qqir371ii0hyqxvjcw6-bash-5.2-p15": {
        // ...
      },
      "/nix/store/wffw7l0alvs3iw94cbgi1gmmbmw99sqb-home-manager-path": null,
    }
    ```

  这样它便与 `nix derivation show` 一致了——后者同样把存储路径映射到信息。

- 当使用[二进制安装器](@docroot@/installation/installing-binary.md)安装 Nix 时，在受支持的 shell（Bash、Zsh、Fish）中，
  [`XDG_DATA_DIRS`](https://specifications.freedesktop.org/basedir-spec/basedir-spec-latest.html#variables) 现在会被填入当前 profile 的 `/share` 子目录的路径。
  这意味着通过 [`nix-env`](@docroot@/command-ref/nix-env.md) 或 [`nix profile`](@docroot@/command-ref/new-cli/nix3-profile.md)
  （实验性）安装的命令补全脚本、`.desktop` 文件及类似产物，可以被任何遵循 [XDG Base Directory Specification](https://specifications.freedesktop.org/basedir-spec/basedir-spec-latest.html) 的程序找到。

- 新增命令 `nix store add`。它取代了现已弃用的 `nix store add-file` 和 `nix store add-path`。

- 新增选项 [`always-allow-substitutes`](@docroot@/command-ref/conf-file.md#conf-always-allow-substitutes)。

  设为 `true` 时，Nix 总会尝试对 derivation（派生）执行替代（substitute），即使它设置了 [`allowSubstitutes`]{#adv-attr-allowSubstitutes} 属性为 `false`。
