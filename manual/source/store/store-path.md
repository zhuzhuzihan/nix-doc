# 存储路径与 store 目录

Nix 的[存储对象]和[文件系统对象]数据模型是极简且抽象的。
但要让软件真正使用存储对象，就需要通过操作系统的文件系统把它们提供出来。

具体做法是把所有存储对象呈现在同一个 *[store 目录][store directory path]*中。
该目录中的每个条目都是一个指向存储对象的 *[store path base name]*。
以这种方式呈现的存储对象随后就可以通过 *[存储路径][store path]*来引用。

[store object]: ./store-object.md
[file system object]: ./file-system-object.md
[store path]: #store-path
[store path base name]: #base-name
[store directory path]: #store-directory-path

## Store Path Base Name {#base-name}

Nix 把对存储对象的引用实现为 *store path base name*（存储路径基名）。

可以把 store path base name 想成一个[不透明的][opaque]、[唯一的标识符][unique identifier]：
获得 store path base name 的唯一途径是添加或构建存储对象。
一个 store path base name 总是恰好引用一个存储对象。

[opaque]: https://en.m.wikipedia.org/wiki/Opaque_data_type
[unique identifier]: https://en.m.wikipedia.org/wiki/Unique_identifier

store path base name 是一个二元组：

- 一个用于标识的 20 字节[摘要]{#digest}
- 一个供人阅读的符号化[名称]{#name}

> **示例**
>
> - Digest（摘要）：`q06x3jll2yfzckz2bzqak089p43ixkkq`
> - Name（名称）：  `firefox-33.1`

store path base name 渲染为字符串时是以下各部分的拼接：

- 以 [Nix32]（[Base32] 的一个变体）渲染的摘要（20 个哈希字节变成 32 个 ASCII 字符）
- 连字符（`-`）
- 名称

> **示例**
>
> ```
> q06x3jll2yfzckz2bzqak089p43ixkkq-firefox-33.1
> |------------------------------| |----------|
>               digest                 name
> ```

[Nix32]: @docroot@/protocols/nix32.md
[Base32]: https://en.wikipedia.org/wiki/Base32

摘要究竟如何计算，取决于被引用存储对象的类型。
存储路径摘要*本应*是不透明的，因此对大多数操作而言，无需了解细节。
话虽如此，本手册仍提供了完整的[存储路径摘要规范](@docroot@/protocols/store-path.md)。

## Store 目录路径（Store Directory Path）

每个 [Nix store] 都有一个 store 目录路径。
这是一个绝对路径、词法上规范化（不含任何 `..`、`.` 或类似内容）的路径，指向存放所有存储对象的目录。

[Nix store]: ./index.md

> **注意**
>
> store 目录默认为 `/nix/store`，但原则上可以是任意路径。

## 存储路径（Store Path）

存储路径是 store 目录路径与一个 [store path base name] 的二元组。
它渲染为文件系统路径时是以下各部分的拼接：

- [Store 目录路径]（通常为 `/nix/store`）
- 路径分隔符（`/`）
- [store path base name]

> **示例**
>
> ```
>   /nix/store/q06x3jll2yfzckz2bzqak089p43ixkkq-firefox-33.1
>   |--------| |------------------------------| |----------|
> store directory            digest                 name
> ```

当我们固定了某个给定的 store，或某个给定的 store 目录路径（所有在用的 store 都共享它）时，存储路径的抽象语法与 store path base name 的抽象语法就重合了：store 目录路径可由上下文得知，因此各存储路径之间只有另外两个字段在变化。

## 在操作系统文件系统中呈现存储对象 {#exposing}

并非每个 store 都能通过文件系统访问。
但如果某个 store 有文件系统表示，以下性质应当成立：

- store 目录路径是规范的：路径的任何前缀（即前 *n* 个路径段构成的路径）都不指向符号链接。
  换言之，可以在不跟随任何符号链接的情况下从 store 目录路径查找到 store 目录。
  （这个条件是独立于上文所述"词法规范性"之外的另一个条件，后者只是路径本身的属性。
  而这个（常规的）"规范性"是关于路径与其所穿越的文件系统 jointly 的属性。）

  > **注意**
  >
  > [`allow-symlinked-store`](@docroot@/command-ref/conf-file.md#conf-allow-symlinked-store) 设置可用于放宽这一要求。

- store 目录路径实际上指向一个目录。

- store 目录为 store 中的每个存储对象，在（渲染后的）[store path base name] 处包含该存储对象的[文件系统对象]。
  store 目录中这些文件的权限和其他元数据处于[在操作系统文件系统中呈现](./file-system-object/os-file-system.md)所述的规范形式。

上述性质意味着以下文件访问操作能够成功。
假设我们有一个按上述规则可在文件系统上访问的 store，且 `q06x3jll2yfzckz2bzqak089p43ixkkq-firefox-33.1` 是该 store 中某个存储对象的 store path base name。

- 假设 store 目录（路径）为 `/foo/bar`。
  那么 `/foo/bar/q06x3jll2yfzckz2bzqak089p43ixkkq-firefox-33.1` 存在，且就是该存储对象的文件系统对象。

- 假设我们不知道该 store 的 store 目录路径是什么，但确实持有一个指向文件系统上 store 目录的能力（capability）`storeDir`。
  （在 Unix 上这是一个"文件描述符"，在 Windows 上是一个"文件句柄"。）
  那么（此处使用 Unix 记法）：
  ```
  openat(storeDir, "q06x3jll2yfzckz2bzqak089p43ixkkq-firefox-33.1", O_NOFOLLOW)
  ```
  将会成功（只要该文件系统对象不是符号链接），且得到的能力将指向该存储对象的文件系统对象。

  （由于 POSIX 的限制，符号链接情况下的行为较难精确规定。）

## 迁移存储对象

完整渲染的存储路径中包含 store 目录路径，意味着完整渲染的存储路径并非仅由被引用的存储对象本身派生，而是还取决于该存储对象所在的 store。
（实际上，当前所有受支持的存储路径摘要计算方式也都依赖 store 目录路径，参见[存储路径摘要规范](@docroot@/protocols/store-path.md)。
所以一般来说，即使只看 store path base name 也是如此。）

因此，考虑某个给定存储对象属于哪个 store 十分重要：
存储对象中的文件可以包含存储路径，而进程可能会读取这些路径。
只有当存储路径不跨越 store 边界时，Nix 才能保证引用完整性。

只有在以下情况下，才能把存储对象复制到另一个 store：

- 源 store 与目标 store 的目录相匹配

  或者

- 所论存储对象没有引用，即不包含任何存储路径

存储对象无法复制到 store 目录不同的 store。
相反，它必须连同其全部依赖一起重新构建。
一般来说，仅仅替换文件内容中的 store 目录字符串是不够的，因为这可能使内部偏移或校验和失效，导致可执行文件无法使用。
