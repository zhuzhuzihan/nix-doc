# Release 1.3 (2013-01-04)

这主要是一个修复缺陷的版本。在 Linux 上首次运行该版本时，它会移除 Nix store 中所有不可变位（immutable bit），并提升 Nix store 的 schema 版本。（上一个版本已移除对设置不可变位的支持；本版本会清除残留的不可变位，以使某些操作更高效。）

本版本包含 Eelco Dolstra 和 Stuart Pernsteiner 的贡献。
