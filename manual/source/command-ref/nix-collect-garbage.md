# Name

`nix-collect-garbage` - 删除不可达的 [store objects]

# 概要

`nix-collect-garbage` [`--delete-old`] [`-d`] [`--delete-older-than` *period*] [`--max-freed` *bytes*] [`--dry-run`]

# 描述

命令 `nix-collect-garbage` 在很大程度上是 [`nix-store --gc`](@docroot@/command-ref/nix-store/gc.md) 的别名。也就是说，它会删除 Nix store 中所有不可达的 [store objects] 来清理你的系统。

不过，它额外提供了两个选项，
[`--delete-old`](#opt-delete-old) 和 [`--delete-older-than`](#opt-delete-older-than)，
它们还会删除旧的 [profiles]，从而可能删除更多 [store objects]，因为 profile 也是垃圾回收器的根（garbage collection root）。
这两个选项相当于先对多个 profile 以各种参数运行
[`nix-env --delete-generations`](@docroot@/command-ref/nix-env/delete-generations.md)，
然后再不带任何标志运行 `nix-collect-garbage`（或直接 `nix-store --gc`）。

> **注意**
>
> 删除先前的配置会使回滚到这些配置成为不可能。

这些标志应谨慎使用，因为它们可能删除系统上其他用户使用的 profile 的 generation（世代）。

## 搜索 profile 的位置

`nix-collect-garbage` 无法知晓所有 profile；这类信息并不存在。它只会查看少数几个位置，并对在那里找到的所有 profile 执行操作：

1. 手册 [profiles] 一节中指定的默认 profile 位置。

2. > **注意**
   >
   > 不稳定；可能变更
   >
   > 不要依赖此功能；它只是为迁移目的而存在，将来可能会变更。
   > 这些已弃用的路径仍然是 Nix 的私有实现细节。

   `$NIX_STATE_DIR/profiles` 和 `$NIX_STATE_DIR/profiles/per-user`。

   除了 `$NIX_STATE_DIR/profiles/per-user/root` 和 `$NIX_STATE_DIR/profiles/default` 之外，这些目录已不再被其他命令使用。`nix-collect-garbage` 仍会查看这些目录，以便清理旧版本 Nix 遗留的 profile。

# 选项

这些选项用于在删除不可达 [store objects] 之前删除旧的 [profiles]。

- <span id="opt-delete-old">[`--delete-old`](#opt-delete-old)</span> / `-d`

  删除所有 profile 的旧 generation。

  这相当于对每个找到的 profile 调用 [`nix-env --delete-generations old`](@docroot@/command-ref/nix-env/delete-generations.md#generations-old)。

- <span id="opt-delete-older-than">[`--delete-older-than`](#opt-delete-older-than)</span> *period*

  删除所有早于指定时长的 profile generation（除了当时处于活动状态的 generation）。
  *period* 是一个类似 `30d` 的值，表示 30 天。

  这相当于对每个找到的 profile 调用 [`nix-env --delete-generations <period>`](@docroot@/command-ref/nix-env/delete-generations.md#generations-time)。
  关于 *period* 参数的更多信息，请参见该命令的文档。

- <span id="opt-max-freed">[`--max-freed`](#opt-max-freed)</span> *bytes*

   <!-- duplication from https://github.com/NixOS/nix/blob/442a2623e48357ff72c77bb11cf2cf06d94d2f90/doc/manual/source/command-ref/nix-store/gc.md?plain=1#L39-L44 -->

  持续删除路径，直到至少删除了 *bytes* 字节，
  然后停止。参数 *bytes* 后可以跟乘数后缀
  `K`、`M`、`G` 或 `T`，分别表示 KiB、MiB、GiB
  或 TiB 单位。
  
{{#include ./opt-common.md}}

{{#include ./env-common.md}}

# 示例

要删除 Nix store 中所有未被每个 profile 当前 generation 使用的内容，执行：

```console
$ nix-collect-garbage -d
```

[profiles]: @docroot@/command-ref/files/profiles.md
[store objects]: @docroot@/store/store-object.md
