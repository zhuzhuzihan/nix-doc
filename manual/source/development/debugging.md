# 调试 Nix

本节介绍如何在启用调试符号的情况下构建和调试 Nix。

此外，关于在单元测试或功能测试上下文中调试 Nix 的进一步说明，请参见[测试 Nix](./testing.md)。

## 带调试符号构建 Nix

在开发 shell 中，`mesonBuildType` 会自动设置为 `debugoptimized`。这会带调试符号构建 Nix，而这些符号对于高效调试至关重要。

也可以不进行优化构建以加快构建速度：

```console
[nix-shell]$ NIX_HARDENING_ENABLE=$(printLines $NIX_HARDENING_ENABLE | grep -v fortify)
[nix-shell]$ export mesonBuildType=debug
```

（第一行是必需的，因为 `fortify` 加固至少需要一些优化。）

## 带消毒器（sanitizer）构建 Nix

Nix 可以使用 LLVM 或 GCC 以
[Address](https://clang.llvm.org/docs/AddressSanitizer.html) 和
[UB](https://clang.llvm.org/docs/UndefinedBehaviorSanitizer.html) 消毒器构建。这在调试内存损坏问题时很有用。

```console
[nix-shell]$ export mesonBuildType=debugoptimized
[nix-shell]$ appendToVar mesonFlags "-Dlibexpr:gc=disabled" # Disable Boehm
[nix-shell]$ appendToVar mesonFlags "-Db_sanitize=address,undefined"
```

## 调试 Nix 二进制文件

在开发 shell 中获取你偏好的调试器：

```console
[nix-shell]$ nix-shell -p gdb
```

在 macOS 上，使用 `lldb`：

```console
[nix-shell]$ nix-shell -p lldb
```

### 启动调试器

要调试 Nix 二进制文件，运行：

```console
[nix-shell]$ gdb --args ../outputs/out/bin/nix
```

在 macOS 上，使用 `lldb`：

```console
[nix-shell]$ lldb -- ../outputs/out/bin/nix
```

### 使用调试器

在调试器内部，你可以设置断点、运行程序并检查变量。

```gdb
(gdb) break main
(gdb) run <arguments>
```

全面的用法说明请参阅 [GDB 文档](https://www.gnu.org/software/gdb/documentation/)。

在 macOS 上，使用 `lldb`：

```lldb
(lldb) breakpoint set --name main
(lldb) process launch -- <arguments>
```

全面的用法说明请参阅 [LLDB 教程](https://lldb.llvm.org/use/tutorial.html)。
