# 内容寻址 derivation 输出

一个输出的内容寻址只取决于该存储对象本身，而不取决于任何外部信息（例如它是如何被制造的、何时被制造的等）。
因此，无论一个存储对象是手动插入 store 的、由某个 derivation 输出的，还是由另一个 derivation 输出的，它都会以相同的方式被内容寻址。

内容寻址输出的输出规格必须包含以下字段：

- *method*：存储对象的数据如何被摘要为一个内容地址

*method* 的可能取值在[存储对象内容寻址一节](@docroot@/store/store-object/content-address.md)中描述。
给定 method、输出的名称（按上文所述由 derivation 名称和输出规格映射计算得出）以及存储对象的数据，输出的存储路径将按该节所述计算。

## 固定输出内容寻址 {#fixed}

在这种情况下，内容地址由 derivation 本身*预先固定*。
换言之，当该 derivation 完成[构建](@docroot@/store/building.md)后，临时输出的内容地址会在把它变成*真正的*存储对象的过程中被计算，计算出的内容地址必须与 derivation 中给定的相符，否则该 derivation 的构建将被判定为失败。

带固定内容地址的输出的输出规格额外包含：

- *hash*，即对存储对象的文件系统对象做摘要所期望得到的哈希。
  该哈希可以采用自由选择的（Nix 所支持的）哈希算法

> **设计说明**
>
> 原则上，输出规格也可以指明存储对象应当拥有的引用，因为引用和文件系统对象同样是内容寻址存储对象本体中对其内容地址有贡献的组成部分。
> 然而目前没有这样做，因为所有固定内容寻址的输出都被要求没有任何引用（包括自引用）。
>
> 同样在原则上，与其用分开的哈希来分别约束引用和文件系统对象数据，也可以用一个同时约束两者的哈希。
> 这可以用最终存储路径的摘要来实现，或者更好的是，用即将成为存储路径摘要、但尚未截断的哈希来实现。
>
> 这里列出这些可能的未来扩展，是为了阐明固定输出内容寻址的核心性质——输出的所有部分都必须用一个或多个哈希以密码学方式固定下来——并把这一性质与当前受支持的存储对象内容寻址方案的细节区分开来。

### 设计动机

预先固定输出的内容地址有什么用处？
抽象地说，答案是经过精心控制的不纯性。
与常规 derivation 不同，产出固定输出的 derivation 的 [builder] 可执行文件可以访问网络。
输出的有保证的内容地址正是为了缓解赋予构建器这些能力所带来的风险；
无论构建器在构建*期间*做什么，它都无法以未预料的方式影响下游构建，因为它传给下游的所有信息都流经那些内容地址已被固定的输出。

[builder]: @docroot@/store/derivation/index.md#builder

具体地说，该功能的用途是从网络抓取固定输入数据，例如源代码。
例如，考虑一族"fetch URL" derivation。
这些 derivation 从给定的 URL 下载文件。
为确保下载的文件未被改动，每个 derivation 还必须指定该文件的密码学哈希。
例如，

```jsonc
{
  "outputs: {
    "out": {
      "method": "nar",
      "hashAlgo": "sha256",
      "hash: "1md7jsfd8pa45z73bz1kszpp01yw6x5ljkjk2hx7wl800any6465",
    },
  },
  "env": {
    "url": "http://ftp.gnu.org/pub/gnu/hello/hello-2.1.1.tar.gz"
    // ...
  },
  // ...
}
```

有时文件的 URL 会变化，
例如服务器重组或不再可用。
在这些情况下，我们必须更新对 `fetchurl` 的调用，例如：

```diff
   "env": {
-    "url": "http://ftp.gnu.org/pub/gnu/hello/hello-2.1.1.tar.gz"
+    "url": "ftp://ftp.nluug.nl/pub/gnu/hello/hello-2.1.1.tar.gz"
     // ...
   },
```

如果 `fetchurl` derivation 的输出是[输入寻址][input addressing]的，那么该 derivation 以及*所有依赖它的 derivation* 的输出路径都会改变。
例如，如果我们修改 Nixpkgs 中 Glibc 源码分发的 URL（在 Linux 上几乎所有其他包都依赖这个包），就需要大规模重新构建。
对于一个我们明知不会在沿依赖图向上传播时产生任何实际影响的变更来说，这很不幸。

而对于内容寻址的输出（固定或浮动），输出的存储路径只取决于 derivation 的名称、数据以及输出规格的 `method`。
为计算输出路径，derivation 的其余部分被忽略。

> **历史说明**
>
> 固定内容寻址无论在今天还是历史上都格外重要，因为它是*唯一*一种已稳定的内容寻址形式。
> 这也是为什么上面的动机部分把它与[输入寻址][input addressing]进行对比。

## （浮动）内容寻址 {#floating}

> **警告**
> 这属于某个[实验性特性](@docroot@/development/experimental-features.md)。
>
> 要使用这种类型的输出寻址，必须启用
> [`ca-derivations`][xp-feature-ca-derivations] 实验性特性。
> 例如，可以在 [nix.conf](@docroot@/command-ref/conf-file.md) 中添加：
>
> ```
> extra-experimental-features = ca-derivations
> ```

启用该实验性特性后，derivation 输出也可以被内容寻址，而*无需*在输出规格中固定输出的内容地址必须是什么。

### 纯性

因为 derivation 输出不是固定的（与[输入寻址][input addressing]一样），[builder] 不会被给予任何不纯能力 [^purity]。

> **配置说明**
>
> 严格来说，沙箱化与去特权化的可行程度随 Nix 的运行环境而异。
> Nix 的配置设置指明要求或启用了何种程度的沙箱。
> 如果 derivation 的构建请求了不被允许的无沙箱，构建将失败。
> 如果配置中指定的沙箱程度超过了给定环境所能达到的程度，构建同样会失败。
>
> （此处的"环境"由 Nix 所运行于其上的操作系统等属性，以及 Nix 被授予的操作系统特定权限构成。
> 由于 macOS、Linux 等常规操作系统的工作方式，讽刺的是，给予构建器*更少*的权限可能反而要求 Nix 以*更多*权限运行。）

话虽如此，产出浮动内容寻址输出的 derivation 可以把其构建器声明为不纯的（就像产出固定输出的 derivation 的构建器那样）。
这目前作为 [`impure-derivations`][xp-feature-impure-derivations] 实验性特性的一部分得到临时支持。

### 兼容性协商

任何产出浮动内容寻址输出的 derivation 都隐式要求 `ca-derivations` [system feature](@docroot@/command-ref/conf-file.md#conf-system-features)。
这可以避免把该 derivation 的构建调度到未启用该实验性特性的机器上。
即使该实验性特性稳定之后，这仍然有用：可以允许使用运行较旧版本 Nix 的远程构建器，或不支持浮动内容寻址的其他实现。

### 确定性

在早前[关于存储对象内容寻址时如何处理自引用的讨论](@docroot@/store/store-object/content-address.html#self-references)中指出，产出存储对象的方法应当是确定性的，与临时存储路径的选择无关。
对于通过手动插入 store 来创建存储对象而产出的存储对象，"生产方法"是一个非正式概念——形式上，Nix 并不知道存储对象来自哪里，而内容寻址正是确保该 derivation *内在*防篡改的关键。
但对于由 derivation 产出的存储对象，"生产方法是相当形式化的"——derivation 的全部意义就在于它是构建的形式化概念。
在这种情况下，我们可以把这个非正式性质提升为形式化性质。

一个*确定性的*内容寻址 derivation 应当产出具有相同内容地址的输出：

1. 每次运行构建器时

  这是因为构建器要么被完全沙箱化，要么构建器会忽略所有泄露进构建沙箱的残余不纯性，它们不影响其行为。

2. 无论选择了怎样的临时输出路径

  对任何有自引用的输出，必须选择临时存储路径。
  临时存储路径的选择可以被视为一种不纯性，因为它是一个任意的选择。

  如果临时输出路径是被确定性选择的，我们就处于第 (1) 条的第一个分支。
  构建器可以基于它以任意方式生成其产出的数据，但这让我们更接近[输入寻址][input addressing]。
  确定性地选择临时路径可以通过消除一种不纯性而被视为"完全沙箱化"，但这并不令人满意

  <!--

  TODO
  (Both these points will be expanded-upon below.)

  -->

  如果临时输出路径是随机选择的，我们就处于第 (1) 条的第二个分支。
  构建器*不得*让这个随机输入影响其产出的最终输出，并且可以执行多次构建并加以比较，以确保情况确实如此。

### 浮动与固定

内容寻址与输入寻址的区别是*机制*层面的，而固定与浮动内容寻址的区别则更多是*策略*层面的。
一个通过其内容地址检查的固定输出，与浮动输出别无二致。
它们只在该检查可能失败这一点上有所不同。

> **设计说明**
>
> 在浮动内容寻址也稳定之后的未来世界里，原则上我们不再需要单独的[固定](#fixed)内容寻址。
> 相反，我们可以始终使用浮动内容寻址，并另行断言某个给定存储对象的精确内容地址值，以将其用作（另一个 derivation 的）输入。
> 这种独立的断言对象尚未实现，其可能的创建在 [issue #11955](https://github.com/NixOS/nix/issues/11955) 中跟踪。
>
> 在当前的 Nix 版本中，未通过哈希检查的固定输出仍会被登记为有效的存储对象，只是不会被登记为产出它的 derivation 的输出。
> 这是一种优化，意味着如果在 derivation 中指定了错误的输出哈希，随后又用正确的输出哈希重建该 derivation，那么 derivation 无需重新构建——避免把可能很大的数据下载两次。
> 这一优化预示了上述设计：
> 如果把输出哈希断言移到 derivation 之外，Nix 不仅可以像今天一样登记那个输出的存储对象，还可以额外记录该 derivation 确实成功下载了一些数据。
例如，对上面的"fetch URL"示例，做这样的记录就相当于记录了在下载时刻给定 URL 上可用的数据。
> 只有当 Nix 随后尝试用那个（细化我们的示例）下载的源代码构建某些东西时，Nix 才会被迫检查输出哈希断言，从而阻止它例如构建被攻陷的恶意软件。
>
> 总结一下，Nix 会
>
> 1. 成功下载数据
> 2. 把数据插入 store
> 3. 将下载的数据与下载它的 derivation 关联（大概配合某种过期策略）
>
> 但只在断言通过时，才在依赖该断言的后续 derivation 中使用下载的存储对象。
>
> 这里列出这个可能的未来扩展，是为了说明上述区别：

[input addressing]: ./input-address.md
[xp-feature-ca-derivations]: @docroot@/development/experimental-features.md#xp-feature-ca-derivations
[xp-feature-git-hashing]: @docroot@/development/experimental-features.md#xp-feature-git-hashing
[xp-feature-impure-derivations]: @docroot@/development/experimental-features.md#xp-feature-impure-derivations
