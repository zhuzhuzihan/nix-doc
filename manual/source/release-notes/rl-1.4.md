# Release 1.4 (2013-02-26)

本版本修复了多用户模式下的一个安全缺陷。此前 derivation（派生）可以通过对 Nix store 之外的文件创建硬链接，将这些文件的权限模式改为 444（只读但对所有人可读）（[详情](https://github.com/NixOS/nix/commit/5526a282b5b44e9296e61e07d7d2626a79141ac4)）。

此外还包含以下改进：

  - 新增内置函数：`builtins.hashString`。

  - 构建日志现在存储在 `/nix/var/log/nix/drvs/XX/` 中，其中 *XX* 是 derivation 的前两个字符。这对保留大量构建日志的机器（例如 Hydra 服务器）很有用。

  - 函数 `corepkgs/fetchurl` 现在可以将下载的文件设置为可执行。这将使 Nixpkgs 源码树中的所有 bootstrap 二进制文件得以移除。

  - 语言变更：表达式 `"${./path} ..."` 现在求值为字符串而不是路径。
