# Name

`nix-store --gc` - 运行垃圾回收

# 概要

`nix-store` `--gc` [`--print-roots` | `--print-live` | `--print-dead`] [`--max-freed` *bytes*]

# 描述

在不带额外标志的情况下，`--gc` 操作会对 Nix store 执行一次垃圾回收。也就是说，所有无法通过文件系统引用从一组"root"（GC root）到达的 Nix store 路径都会被删除。

可以指定以下子操作：

- `--print-roots`

  此操作在标准输出上打印垃圾回收器使用的 root 集合。

- `--print-live`

  此操作在标准输出上打印"活跃"（live）存储路径集合，即所有从 root 可达的存储路径。活跃路径永远不会被删除，否则会破坏一致性——那样就可能安装出引用 store 中已不存在内容的应用程序。

- `--print-dead`

  此操作在标准输出上打印"死"（dead）存储路径集合，即与活跃路径集合相反的集合：store 中任何（相对于 root 而言）不活跃的路径都是死的。

默认情况下，所有不可达的路径都会被删除。以下选项控制删除什么以及按什么顺序删除：

- `--max-freed` *bytes*

  持续删除路径，直到至少删除了 *bytes* 字节为止。参数 *bytes* 后面可以跟乘法后缀 `K`、`M`、`G` 或 `T`，分别表示 KiB、MiB、GiB 或 TiB 单位。

垃圾回收器的行为还受 Nix 配置文件中 `keep-outputs` 和 `keep-derivations` 设置的影响。

默认情况下，垃圾回收器在结束（或被中断）时会打印释放的总字节数。

{{#include ./opt-common.md}}

{{#include ../opt-common.md}}

{{#include ../env-common.md}}

# 示例

要删除所有不可达的路径，只需执行：

```console
$ nix-store --gc
deleting `/nix/store/kq82idx6g0nyzsp2s14gfsc38npai7lf-cairo-1.0.4.tar.gz.drv'
...
8825586 bytes freed (8.42 MiB)
```

要删除至少 100 MiB 的不可达路径：

```console
$ nix-store --gc --max-freed $((100 * 1024 * 1024))
```
