# Release 2.6 (2022-01-24)

* Nix CLI 现在会向上层目录搜索 `flake.nix`，直到当前 Git 仓库的根目录或文件系统边界，而不再只在当前目录中查找。
* `builtins.fromTOML` 所使用的 TOML 解析器已被替换为[一个更符合规范的解析器](https://github.com/ToruNiina/toml11)。
* 在 `nix repl` 中新增了 `:st`/`:show-trace` 命令，用于设置或切换错误调用栈信息的显示。
* 新增内置函数 `builtins.zipAttrsWith`，功能与 Nixpkgs 的 `lib.zipAttrsWith` 相同，但效率高得多。
* 新增命令 `nix store copy-log`，用于将构建日志从一个 store 复制到另一个 store。
* 可以将 `commit-lockfile-summary` 选项设置为一个非空字符串，以覆盖提交更新后的 lockfile 时使用的提交摘要。它可以与 `flake.nix` 中的 `nixConfig` 属性配合使用，以便更好地遵循仓库的约定。
* `docker run -ti nixos/nix:master` 会将你带入一个包含 `master` 分支最新版本 Nix 的 Docker 容器。
