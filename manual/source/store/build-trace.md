# Build Trace（构建痕迹）

> **警告**
>
> 这一整个概念目前处于
> [**实验性**](@docroot@/development/experimental-features.md#xp-feature-ca-derivations)
> 阶段，可能发生变化。

*build trace*（构建痕迹）是构建的[备忘表（memoization table）](https://en.wikipedia.org/wiki/Memoization)。
它将构建的输入映射到构建的输出。
build trace 中的每个*条目*将一个 [derivation][derivation] 映射到一个由 [output]（输出）名称到[存储对象][store object]的映射。

一般而言，作为键使用的 derivation 应当是已经[*resolved*（已解析）](./resolution.md)的。
为格外清晰起见，键全部为已解析 derivation 的 build trace 也被称为*基础 build trace*。
如果一个 derivation 的所有已解析输入都是内容寻址的，那意味着输入将被完全确定，对执行了哪次构建不再有任何歧义。
（然而以输入寻址的输入仍然有歧义。它们同样应当被锁定，但这被留作未来的工作。）

相应地，要查找一个未解析的 derivation，必须先将其解析为已解析的 derivation。
解析过程本身又涉及查找 build trace 中的条目，因此这是一个相互递归的过程，最终可能要检查许多条目。

除了上文指出的输入寻址路径的问题之外，基础 build trace 显然是*连贯的*——不可能出现不连贯。
也就是说，基础 build trace 各条目所做出的断言彼此独立，任何一个映射都不会使另一个映射失效。

至于这些映射是否*为真*，即是否忠实地记录了实际执行的构建，则是另一回事。
连贯性关注的是 build trace 的多条断言相互一致，而不关注各条断言本身是真是假。

一般而言，除了从头重新执行一次构建之外，没有办法审计一个 build trace 条目。
而且即便如此，结果不同也并不意味着原来的条目是"谎言"，因为被构建的 derivation 可能是非确定性的。
因此，是否信任对方的 build trace，从根本上说是一个主观的策略选择。
build trace 条目通常会被*签名*，以便支持任意的基于公钥的信任策略。

## Derived build traces（派生 build trace） {#derived}

希望对上述机制做备忘的实现还可以保存额外的*派生* build trace 条目，它们确实会映射未解析的 derivation。
但如果这样做，它们*必须*同时保存底层的、以已解析 derivation 为键的基础条目。
首先，这确保了派生条目仅仅是缓存，可以从头重新计算。
其次，这确保了派生 build trace 的连贯性。

与基础 build trace 不同，派生 build trace 是可能出现不连贯的。
关键在于，derivation 的解析只有在固定某个基础 build trace 的前提下才是确定性的。
不固定基础 build trace 的话，它就会继承基础 build trace 本身的主观性。

具体来说，假设有三个 derivation \\(a\\)、\\(b\\) 和 \\(c\\)。
设 \\(a\\) 是已解析的 derivation，而 \\(b\\) 和 \\(c\\) 未解析，且二者都以 \\(a\\) 的某个输出作为输入。
再假设针对 \\(b\\) 和 \\(c\\) 的派生条目是基于 \\(a\\) 的两个不同条目建立的。
（如果 \\(a\\) 是非确定性的，\\(a\\) 与 \\(b\\) 在一个 store 中构建，\\(a\\) 与 \\(c\\) 在另一个 store 中构建，然后第三个 store 从前两个 store 都进行了 substitute（替代），就可能发生这种情况。）

如果信任 \\(b\\) 和 \\(c\\) 的派生 build trace 条目要求同时也信任它们各自底层的 \\(a\\) 条目，那么 \\(a\\) 的两个不同映射就会被发现。
然而，如果 \\(b\\) 和 \\(c\\) 的条目可以各自孤立地组合使用，就没有任何东西能发现它们关于 \\(a\\) 输出的隐含假设中的矛盾。

[derivation]: ./derivation/index.md
[output]: ./derivation/outputs/index.md
[store object]: @docroot@/store/store-object.md
