R"(

**Store URL 格式**: `local-overlay`

此 Store 类型是[本地 Store] 的一种变体，旨在利用 Linux 的 [Overlay Filesystem](https://docs.kernel.org/filesystems/overlayfs.html)（简称 OverlayFS）。
正如 OverlayFS 将一个下层文件系统和一个上层文件系统组合在一起、把上层视为对下层的补丁一样，本地 overlay store 将一个下层 store 与一个“准”[本地 Store] 的上层组合在一起。
（之所以说“准”，是因为虽然 OverlayFS 的上层文件系统自身是有效的，但这个准上层 Store 单独来看并不是一个有效的本地 Store，因为其中一些引用会是悬空的。）
要使用此 Store，你首先需要[适当地](#example-filesystem-layout)配置一个 OverlayFS 挂载点，Nix 不会替你完成这一步（不过它会验证挂载点是否配置正确）。

### 本地 overlay store 的概念组成

*这是对分层 Store 各组成部分更抽象/概念性的描述，作为权威参考。
更“实际”的操作说明请参见下一小节中的完整示例。*

本地 overlay store 的组成部分如下：

- **下层 store（Lower store）**：

  > 通过 [`lower-store`](#store-experimental-local-overlay-store-lower-store) 设置指定。

  这是任意一种将 Store 目录作为操作系统原生文件系统一部分的 Store 实现。
  例如，它可以是一个[本地 Store]、[本地 daemon Store]，甚至可以是另一个本地 overlay store。

  本地 overlay store 绝不会以任何方式尝试修改下层 store。
  其他东西可以修改下层 store，但对此有一些限制：
  Nix 要求该 store 只能增长，而不能以其他方式改变。
  例如，可以添加新的 store 对象，但一般不允许删除或修改 store 对象，因为这会使使用这些对象的任何本地 overlay store 发生混乱和损坏。
  （此外，底层的文件系统 overlay 机制可能施加额外的限制，见下文。）

  在作为 overlay store 的一部分被挂载期间，下层 store 不得发生改变。
  为确保这一点，你可能希望以只读方式挂载 Store 目录（此时需要将 [read-only] 参数设为 `true`）。

  - **下层 Store 目录**：

    > 通过 `lower-store.real` 设置指定。

    这是下层 store 使用/暴露的目录。

    如上所述，Nix 要求本地 store 只能增长而不能以其他方式改变。
    Linux 的 OverlayFS 还额外要求该目录完全不可改变。
    也就是说，只要存在使用该 store 作为下层 store 的本地 overlay store，此目录就不得发生任何改变。

  - **下层元数据源**：

    > 不直接指定。
    > 它是 `lower-store` 设置的一个结果，取决于所选下层 store 的类型。

    这是一个抽象概念，即某种读取下层 store 的 [store 对象][store object] 元数据的方式。
    例如，它可以是一个 SQLite 数据库（对于[本地 Store]），或一个套接字连接（对于[本地 daemon Store]）。

    它不必是可写的。
    如上所述，本地 overlay store 绝不会尝试修改其下层 store。
    下层 store 的元数据被视为下层 store 的一部分，正如出现在 Store 目录中的 [file system object][file system object] 一样。

- **准上层 store（Upper almost-store）**：

  > 不直接指定。
  > 而是按如下所述分别指定其各个组成部分。

  它几乎就是一个[本地 Store]，但并不完全是。
  这是因为如果把它单独拿出来（不作为本地 overlay store 的一部分），它本身看起来会是损坏的。
  但作为 overlay 本地 store 的一部分、与其他部分组合在一起时，它是有效的。

  - **上层目录（Upper layer directory）**：

    > 通过 [`upper-layer`](#store-experimental-local-overlay-store-upper-layer) 设置指定。

    其中包含额外的 [store 对象][store object]
    （严格来说，是它们的 [file system object][file system object]），本地 overlay store 将用它们来扩展下层 store。

  - **上层 Store 目录**：

    > 通过 [`real`](#store-experimental-local-overlay-store-real) 设置指定。
    > 它与基础本地 Store 的同名设置相同，也可以通过 [`root`](#store-experimental-local-overlay-store-root) 设置间接指定。

    它包含来自上述两个目录的所有 store 对象。

    下层 Store 目录和上层目录通过 OverlayFS 合并而创建出此目录。
    Nix 自身不会执行这一操作，因为它通常没有这样做的权限，因此由用户负责事先完成此设置。
    不过，Nix 可以选择性地检查 OverlayFS 挂载设置是否与预期一致、是否与 Nix 自身的设置相匹配。

  - **上层 SQLite 数据库**：

    > 不直接指定。
    > 数据库的位置取决于 [`state`](#store-experimental-local-overlay-store-state) 设置。
    > 它始终是 `${state}/db`。

    其中包含所有上层 [store 对象][store object] 的元数据（除其 file system object 之外的一切），以及部分下层 store 对象元数据的副本。
    之所以进行复制，是为了使上层 [store 对象][store object] 的[闭包](@docroot@/glossary.md#gloss-closure) 元数据能完全位于上层之内。
    （这使我们能够使用与[本地 Store] 的 SQLite 数据库相同的 SQL Schema，因为该 schema 中的外键强制要求闭包元数据以这种方式自包含。）

[file system object]: @docroot@/store/file-system-object.md
[store object]: @docroot@/store/store-object.md


### 文件系统布局示例

下面是一个遵循上一节概念的完整使用示例。

假设我们有以下路径：

- `/mnt/example/merged-store/nix/store`

- `/mnt/example/store-a/nix/store`

- `/mnt/example/store-b`

那么可以使用以下 Store URI 来访问位于 `/mnt/example/merged-store` 的 local-overlay store：

```
local-overlay://?root=/mnt/example/merged-store&lower-store=/mnt/example/store-a&upper-layer=/mnt/example/store-b
```

下层 Store 目录位于 `/mnt/example/store-a/nix/store`，而上层位于 `/mnt/example/store-b`。

在访问 overlay store 之前，你需要确保 OverlayFS 挂载已正确设置：

```shell
mount -t overlay overlay \
  -o lowerdir="/mnt/example/store-a/nix/store" \
  -o upperdir="/mnt/example/store-b" \
  -o workdir="/mnt/example/workdir" \
  "/mnt/example/merged-store/nix/store"
```

注意，OverlayFS 要求 `/mnt/example/workdir` 与 `upperdir` 位于同一个卷上。

默认情况下，Nix 会检查挂载点是否已正确设置，若未正确设置则会报错。
如有需要，你可以传入 [`check-mount=false`](#store-experimental-local-overlay-store-check-mount) 来覆盖此行为。

)"
