# Release 0.14 (2010-02-04)

本版本包含以下改进：

  - 垃圾回收器现在开始删除垃圾的速度比以前快得多。它不再确定 store 中所有路径的活跃性，而是按需进行。

  - 新增一个操作 `nix-store --query
                    --roots`，用于显示直接或间接指向给定存储路径的垃圾回收器根。

  - 移除了将基于 Berkeley DB 的 Nix 数据库转换为新 schema 的支持。

  - 移除了垃圾回收器选项 `--use-atime` 和 `--max-atime`。它们在实际中用处不大。

  - 在 Windows 上，Nix 现在要求 Cygwin 1.7.x。

  - 若干缺陷修复。
