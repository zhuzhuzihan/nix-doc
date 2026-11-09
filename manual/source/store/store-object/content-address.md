# 存储对象的内容寻址

正如[文件系统对象][File System Object]可以[按内容寻址][fso-ca]一样，
[存储对象][Store Object]也可以进行[内容寻址](@docroot@/glossary.md#gloss-content-address)，
除非它们是[输入寻址](@docroot@/glossary.md#gloss-input-addressed-store-object)的。

对存储对象而言，我们产出的内容地址将采取[存储路径]（Store Path）而非普通哈希的形式。
特别地，内容寻址方案会确保存储路径的摘要仅由该存储对象的以下信息计算得出：

- 文件系统对象图（根对象及其子对象，如果有的话）
- 引用（references）
- [store 目录路径](../store-path.md#store-directory-path)
- 名称（name）

而不包含任何其他信息——其他信息都不是该存储对象的内在属性。

相关算法的完整规范请参见[存储路径摘要规范][sp-spec]。

[File System Object]: ../file-system-object.md
[Store Object]: ../store-object.md
[Store Path]: ../store-path.md

## 对存储对象各部分的内容寻址

### 文件系统对象

在当前所有受支持的存储对象内容寻址方法中，总是先对文件系统对象进行[内容寻址][fso-ca]，然后该哈希再被纳入存储对象内容地址的计算。

### 引用

#### 对其他存储对象的引用

在当前所有受支持的存储对象内容寻址方法中，
对其他对象的引用都通过其常规的（字符串编码的）[存储路径][Store Path]来表示。

#### 自引用

然而自引用无法通过其路径来表示，因为我们此刻正在描述的正是如何计算该路径！

> 另一种做法需要找到哈希函数的不动点，即求解形如
> ```
> digest = hash(..... || digest || ....)
> ```
> 的方程，这在计算上是不可行的。
> 据我们所知，这等价于寻找哈希碰撞。

取而代之的是一个"是否有自引用"的布尔值，它最终会影响摘要：
在当前所有受支持的存储对象内容寻址方法中，对文件系统对象数据做哈希时，被摘要数据中出现的存储对象自身存储路径都会被替换为一个[哨兵值](https://en.wikipedia.org/wiki/Sentinel_value)。
随后使用的是这些修改后的输入流的哈希。

在事后校验存储对象的内容地址时，上述过程按字面描述即可工作。
然而，在首次创建存储对象时，如上所述，我们还不知道该存储对象的存储路径。
因此严格来说，我们并不知道在对哈希函数的输入中将把哪个值替换为哨兵值。
实际发生的是：临时存储对象——即我们希望据此创建存储对象的数据——会与一个临时的"草稿"存储路径配对（该路径大概是在数据创建时选定的）。
被替换为哨兵值的是这个临时存储路径，而不是我们还不得而知最终存储路径。

> **设计说明**
>
> 内容寻址存储对象有一个非正式的性质：临时存储路径的选择不应产生影响。
> 换言之，如果一个临时存储对象除临时存储路径的选择之外都以相同方式准备，那么临时数据不必完全相同。
> 但是，在把哨兵值替换掉每个临时存储对象的临时存储路径之后，最终经此规范化的数据*应当*是完全相同的。
>
> 反过来，如果经过该规范化过程后数据仍然不同，我们就会计算出不同的内容地址。
> 准备临时自引用数据的方法就*未能*做到确定性——它把临时存储路径的选择（本应是任意的选择）*泄露*进了最终存储对象。
>
> 这个性质在现阶段是非正式的，因为我们此时只是在描述存储对象，而存储对象没有关于其来源的形式化概念。
> 缺少这一点，我们就无法严格定义"过程确定性不足"意味着什么。
> 当我们讲到 [derivation](@docroot@/store/derivation/index.md) 时，将能够把它变成一个形式化性质——不是关于内容寻址存储对象本身，而是关于*产出*它们的 derivation。

### 名称与 store 目录

这两项以存储路径摘要计算的标准方式影响摘要，并非内容寻址所特有。
进一步细节请查阅[存储路径摘要规范][sp-spec]。

## 内容寻址方法

出于历史原因，我们并不在所有组合中支持所有特性。
当前受支持的每种内容寻址方法都选择单一的文件系统对象哈希方法，并可能对引用施加一些限制。
不过名称和 store 目录不受限制。

### Flat（扁平） { #method-flat }

使用对应的[扁平（Flat）](../file-system-object/content-address.md#serial-flat)文件系统对象内容寻址方法。

不支持引用：无法创建同时使用扁平哈希*和*引用的存储对象。

### Text（文本） { #method-text }

同样使用对应的[扁平（Flat）](../file-system-object/content-address.md#serial-flat)文件系统对象内容寻址方法。

支持对其他存储对象的引用，但不支持自引用。

这是唯一一个与对应文件系统对象方法不同名的存储对象内容寻址方法。
它比较冷僻，主要用于 "drv 文件"
（以["ATerm" 文件格式](@docroot@/protocols/derivation-aterm.md#use-for-encoding-to-store-object)序列化为存储对象的 derivation）。
如有可能，请优先选择其他方法。

### Nix Archive（NAR） { #method-nix-archive }

使用对应的 [Nix Archive](../file-system-object/content-address.md#serial-nix-archive) 文件系统对象内容寻址方法。

只要哈希算法是 SHA-256，就支持引用（包括对其他存储对象的引用和自引用）；否则两者都不支持。

### Git { #method-git }

> **警告**
>
> 该方法属于 [`git-hashing`][xp-feature-git-hashing] 实验性特性。

使用对应的 [Git](../file-system-object/content-address.md#git) 文件系统对象内容寻址方法。

不支持引用。

目前仅支持 SHA-1。
如果[基于 SHA-256 的 Git](https://git-scm.com/docs/hash-function-transition)变得更加普及，将重新审视这一限制。

[fso-ca]: ../file-system-object/content-address.md
[sp-spec]: @docroot@/protocols/store-path.md
[xp-feature-git-hashing]: @docroot@/development/experimental-features.md#xp-feature-git-hashing
