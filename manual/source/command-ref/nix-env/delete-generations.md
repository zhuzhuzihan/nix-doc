# Name

`nix-env --delete-generations` - 删除 profile 的 generation（代）

概要

`nix-env` `--delete-generations` *generations*

# 描述

该操作删除当前 profile 的指定 generation。

*generations* 可以是以下之一：

- <span id="generations-list">[`<number>...`](#generations-list)</span>

  一组 generation 编号，每个编号作为单独的命令行参数。

  按编号精确删除指定的 profile generation。
  禁止删除当前 generation。

- <span id="generations-old">[特殊值 `old`](#generations-old)</span>

  删除除当前 generation 之外的所有 generation。

  > **警告**
  >
  > 该操作会删除比当前 generation 更旧*以及更新*的 generation。
  >
  > 有人可能以为它只会删除比当前更旧的 generation，但这只有在当前 generation 同时也是最新 generation 时才成立。
  > 由于可以回滚到先前的 generation，因此可能存在比当前 generation 更新的 generation。
  > 它们也会被删除。

- <span id="generations-time">[`<number>d`](#generations-time)</span>

  最近 *number* 天

  *示例*：`30d`

  删除创建于 *number* 天前的所有 generation，但保留其中最近的一个。
  这样可以回滚到指定时间段内曾经可用的 generation。

- <span id="generations-count">[`+<number>`](#generations-count)</span>

  截至当前的最后 *number* 个 generation

  *示例*：`+5`

  保留最后 *number* 个 generation，以及所有比当前 generation 更新的 generation。

定期删除旧的 generation 对于使垃圾回收生效非常重要。
这是因为 profile 也是垃圾回收根——从 profile 可达的任何 [store object] 都是"存活"的，不会被删除。

[store object]: @docroot@/store/store-object.md

{{#include ./opt-common.md}}

{{#include ../opt-common.md}}

{{#include ./env-common.md}}

{{#include ../env-common.md}}

# 示例

## 按编号显式删除 generation

```console
$ nix-env --delete-generations 3 4 8
```

删除编号为 3、4、8 的 generation，前提是当前激活的 generation 不是其中任何一个。

## 按数量（generation 个数）保留最近的

```console
$ nix-env --delete-generations +5
```

假设 `30` 是当前 generation，且我们目前拥有编号 `20` 到 `32` 的 generation。

那么该命令会删除 generation `20` 到 `25`（`<= 30 - 5`），
并保留 generation `26` 到 `31`（`> 30 - 5`）。

## 按时间（天数）保留最近的

```console
$ nix-env --delete-generations 30d
```

该命令会删除所有超过 30 天的 generation，但保留 30 天前激活的那个 generation（如果它目前仍然存在）。

## 删除所有更旧的

```console
$ nix-env --profile other_profile --delete-generations old
```
