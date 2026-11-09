## 存储对象（Store Object）

Nix store 是一组*存储对象*以及它们之间的*引用（references）*的集合。
一个存储对象由以下部分组成：

  - 一个作为数据的[文件系统对象](./file-system-object.md)

  - 一组作为对存储对象引用的[存储路径](./store-path.md)

### 引用（References）

存储对象既可以引用其他存储对象，也可以引用自身。
从存储对象到自身的引用称为*自引用（self-references）*。

存储对象及其引用构成一个有向图，其中存储对象是顶点，引用是边。
特别地，与某个引用对应的边，是从包含该引用的存储对象指向该存储路径（即此引用）所指向的存储对象。

自引用之外的引用不得形成环。
因此，排除自引用之后的引用图构成一个[有向无环图]。

[directed acyclic graph]: @docroot@/glossary.md#gloss-directed-acyclic-graph

我们可以取引用图的[传递闭包]，其中任意一对存储对象之间存在一条边，当且仅当从第一个对象到第二个对象存在一条由一个或多个引用构成的*路径*。
（单个引用总是构成长度为 1 的路径，但更长的路径可以连接彼此之间没有直接引用的对象。）
一个存储对象的*必需项（requisites）*，是指从给定存储对象的引用出发、经由引用路径可达的所有存储对象。

[transitive closure]: https://en.wikipedia.org/wiki/Transitive_closure

我们也可以取引用图的[转置图]，即反转所有边的方向。
一个存储对象的*引用者（referrers）*，是引用它的那些存储对象。

[transpose graph]: https://en.wikipedia.org/wiki/Transpose_graph

还可以将这两个概念结合起来：取转置后的引用图的传递闭包。
一个存储对象的*引用者闭包（referrers closure）*，是能够经由引用路径到达给定存储对象的所有存储对象。

> **注意**
>
> 必须小心区分存储对象的内在属性与外在属性。
> 我们可以由一个 store 中的存储对象构造出图，但 store 的内容通常并非固定，而可能随时间变化。
>
> - 存储对象的引用——即称为 references 的那组存储路径——是存储对象的一个字段，因此按定义是内在属性。
>   无论该存储对象位于哪个 store，也无论该 store 可能包含或不包含什么，引用都是相同的。
>
> - 存储对象的必需项几乎是内在的——某些存储路径并不精确指向唯一一个存储对象。
>   究竟引用的是哪个存储对象，以及它*自身*的引用又是什么，取决于所讨论的 store。
>   不同的 store 对某个给定存储路径指向什么，可能有不同看法。
>
> - 存储对象的引用者完全是外在的，仅取决于包含该存储对象的 store，而不取决于存储对象本身。
>   引用该存储对象的其他存储对象可能被加入或移出 store。

### 不可变性

存储对象是[不可变的](https://en.wikipedia.org/wiki/Immutable_object)：
一旦创建，它们不会改变，它们引用的任何存储对象也不能被改变。

> **注意**
>
> 支持原子地删除多个存储对象的 store，可以在保持这一性质的同时获得更多灵活性。

### 闭包性质

一个 store 只有在包含某个存储对象所引用的全部存储对象时，才能包含该存储对象。

> **注意**
>
> "闭包性质"并非意在禁止诸如存储对象的[惰性加载](https://en.wikipedia.org/wiki/Lazy_loading)之类的做法。
> 不过，"闭包性质"与不可变性相结合意味着任何此类惰性加载都应当是确定性的。

### 存储对象元数据 {#metadata}

[存储实现](@docroot@/store/types/index.md)目前为存储对象关联了比上述描述更多的信息。
可以说其中一些信息并不属于这里，因为它混淆了关注点。

两个这样的属性是大小：

- [*NAR size*（NAR 大小）]{#nar-size}：
  存储对象的[文件系统对象](./file-system-object.md)序列化为 [Nix Archive](./file-system-object/content-address.md#serial-nix-archive) 后的字节大小。

  这是存储对象自身的内在属性，与任何特定 store 恰好如何存放它无关。
  特别地，它与存储对象在磁盘上占用的空间无关，后者随压缩、去重和文件系统开销而变化。

- [*closure NAR size*（闭包 NAR 大小）]{#closure-nar-size}：
  该存储对象的[闭包]中每个存储对象（包括其自身）的 [*NAR size*](#nar-size) 之和。

  与 *NAR size* 不同，这并不完全是内在属性。
  由于[必需项](#references)如上所述略有歧义，*closure NAR size* 也略有歧义；
  二者都取决于所讨论的 store 以及该 store 中确切的闭包。

  由于这些问题，目前的实现通常是即时计算而不是存储它。

细节请参见 [store object info](@docroot@/protocols/json/store-object-info.md) JSON 格式或 [narinfo](@docroot@/protocols/binary-cache/narinfo.md) 格式。

[closure]: @docroot@/glossary.md#gloss-closure
