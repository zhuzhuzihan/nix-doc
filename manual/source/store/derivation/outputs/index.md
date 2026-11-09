# Derivation 输出与 derivation 的类型

正如 [derivation 主页面](../index.md#store-derivation)所述，
derivation 产出[存储对象](@docroot@/store/store-object.md)，它们被称为该 derivation 的*输出*。
的确，derivation 的全部意义就在于产出这些输出，并在每次运行 derivation 时可靠且可复现地产出它们。

derivation 的组成部分之一是它的*输出规格*，它指明 derivation 运行时所产出输出的某些信息。
输出规格是一个映射，从名称到单个输出的规格。

## 输出名称 {#outputs}

输出名称可以是任何同时是有效[存储路径名称](@docroot@/store/store-path.md#name)的字符串。
映射到每个输出规格的名称实际上并不是输出的名称。
在一般情况下，输出存储对象的名称是 `derivationName + "-" + outputSpecName`，而非关于它的其他任何元数据。
不过，名为 "out" 的输出规格所描述的输出存储对象，其名称就是 derivation 的名称本身。

> **示例**
>
> 一个 derivation 名为 `hello`，有两个输出：`out` 和 `dev`：
>
> - 该 derivation 的路径将是：`/nix/store/<hash>-hello.drv`。
>
> - `out` 的存储路径将是：`/nix/store/<hash>-hello`。
>
> - `dev` 的存储路径将是：`/nix/store/<hash>-hello-dev`。

输出就是 derivation 有义务产出的那些[存储对象](@docroot@/store/store-object.md)。

> **注意**
>
> 这里的正式术语与如今 Nix 社区的日常用语有些出入。
> 在随意场合，"output" 既可以指实际的输出存储对象，也可以指名义上的输出规格，视上下文而定。
>
> 例如 "hello 的 `dev` 输出"指的是存储路径 `/nix/store/<hash>-hello-dev` 所指的存储对象。
> 人们通常不会把它称为 "`hello-dev` 输出"，尽管 `hello-dev` 才是该存储对象的实际名称。

## 输出寻址的类型

输出规格所包含的主要信息是 derivation 输出的寻址方式。
特别地，该规格决定：

- 输出是[内容寻址](./content-address.md)还是[输入寻址](./input-address.md)

- 如果是内容寻址的，采用何种内容寻址方式

- 如果是内容寻址的，[其内容地址是什么](./content-address.md#fixed)（从而其[存储路径]是什么）

## 输出检查 {#output-checks}

除上述输出规格之外，derivation 还可以对其输出强制额外的*检查*：
即为了使构建被视为成功，产出的存储对象必须满足的性质。
检查可以按输出分别指定，也可以对 derivation 的所有输出统一指定一次。

### 引用检查

主要的检查约束一个输出的[引用][reference]。
这些检查沿两个维度变化，共有 4 种可能的检查：

- 检查是作用于输出的*直接*引用，还是作用于其经由*传递*引用构成的整个[闭包]（[必需项][requisite]）。

- 检查是*允许*一组引用（每个引用都必须是该集合的成员，但并非每个成员都需要被引用），还是*禁止*一组引用（任何引用都不得是该集合的成员）。

四种检查分别是：

- [*allowed references*（允许的引用）]{#allowed-references}：
  一个可选集合；输出的引用必须是它的子集。
  集合缺省时跳过该检查，即允许任何引用。

  例如，空集合强制输出完全没有运行时依赖。

  > **用法提示**
  >
  > NixOS 用它来检查生成的文件（例如用于引导 Linux 的初始内存盘）不会意外依赖 Nix store 中的其他路径。

- [*allowed requisites*（允许的必需项）]{#allowed-requisites}：
  与 *allowed references* 类似，但作用于输出的整个闭包：
  每个传递依赖都必须是该集合的成员。

- [*disallowed references*（禁止的引用）]{#disallowed-references}：
  一个集合，其任何成员都不得是输出的直接引用。
  （这个检查无需可选：禁止空集等同于跳过检查。）

- [*disallowed requisites*（禁止的必需项）]{#disallowed-requisites}：
  与 *disallowed references* 类似，但作用于输出的整个闭包：
  该集合的任何成员不得出现在输出的传递依赖中的任何位置。

存储对象的引用总是存储路径。
然而，如果这些集合的每个元素都必须是存储路径，那么要约束输出对*同一 derivation 的其他输出*的引用将很难甚至不可能，因为一般来说输出的存储路径在 derivation 构建之前是未知的。
为此，这些集合的元素也可以是被检查 derivation 的一个*输出名称*，代表该输出的存储路径，无论它最终是什么。
例如，可以通过把输出自己的名称放进它的 *allowed references*，允许输出引用自身。

### 大小检查

- [*max size*（最大大小）]{#max-size}：
  输出的存储对象的 [NAR size][nar size] 不得超过给定的字节数。

- [*max closure size*（最大闭包大小）]{#max-closure-size}：
  输出的存储对象的 [closure NAR size][closure nar size] 不得超过给定的字节数。

### 自引用处理

- [*ignore self references*（忽略自引用）]{#ignore-self-refs}：
  输出对自身的引用是否豁免于上述引用检查。

## 引用扫描 {#reference-scanning}

除输出检查之外，还有一个按输出配置的设置。
它*不是*检查——对产出的存储对象不作任何校验——但它以同样的按输出方式配置，因此在这里记述：

- [*unsafe discard references*（不安全地丢弃引用）]{#unsafe-discard-references}：
  完全禁用[扫描输出的运行时引用](../../building.md#scanning-for-references)。
  之后该输出将被登记为没有任何引用，无论其内容如何。

  例如，在生成带有自身内嵌 Nix store 的自包含文件系统镜像时，这很有用：
  此类镜像内部找到的哈希指向的是内嵌的 store，而不是宿主的 Nix store。

  顾名思义，这是不安全的：丢弃运行时实际需要的引用会使闭包不完整，因此把输出复制到别处将不会带上其依赖。

[closure]: @docroot@/glossary.md#gloss-closure
[nar size]: @docroot@/store/store-object.md#nar-size
[closure nar size]: @docroot@/store/store-object.md#closure-nar-size
[reference]: @docroot@/glossary.md#gloss-reference
[requisite]: @docroot@/store/store-object.md#references

## Derivation 的类型

关于各类型 derivation 输出寻址的小节最终都讨论了 derivation 除输出之外的其他属性，例如纯性、调度、确定性等。
这并非巧合；因为 derivation 的类型实际上与其输出的类型一一对应：

- 产出 *xyz-addressed* 输出的 derivation 是一个 *xyz-addressing* derivation。

这方面的规则相当简洁：

- 所有输出必须是同一类型／使用同一寻址方式

  - derivation 必须至少有一个输出

  - 此外，如果输出是固定内容寻址的，则必须恰好有一个输出，其规格映射自名称 `out`。
    （按照上文所述的规则，名称 `out` 是特殊的。
    只有一个输出且把它的规格称为 `out`，意味着这个单一输出实际上是匿名的；存储路径只有 derivation 的名称。）

    （这是一个任意的限制，本可以取消。）

- 输出要么是*固定的*（fixed），要么是*浮动的*（floating），表明存储路径在构建之前是否已知。

  - 固定内容寻址时是固定的。

    > *固定内容寻址*的 derivation 也被称为*固定输出 derivation*（fixed-output derivation），因为它是当前唯一实现的固定输出寻址形式

  - 浮动内容寻址或输入寻址时是浮动的。

  > 因此，历史上在 Nix 未启用任何实验性特性时，*所有*输出都是固定的。

- derivation 可以是*纯的*或*不纯的*，表明 [builder](../index.md#builder) 对外部世界的读访问权限。

  - 输入寻址 derivation *必须*是纯的。

    > 如果它是不纯的，就会有大麻烦，因为输入寻址 derivation 总是产出具有相同路径的输出。


  - 内容寻址 derivation 可以是纯的或不纯的

   - 如果它是不纯的，可以是固定的（典型情况），或者在启用了额外的 [`impure-derivations`][xp-feature-impure-derivations] 实验性特性时是浮动的。

   - 如果它是纯的，则必须是浮动的。

   - 纯的、固定内容寻址的 derivation 不受支持

     > 这种第四种组合没有用处。
     > 输出存储路径被固定的唯一目的，就是支持 derivation 可以是不纯的。

[xp-feature-ca-derivations]: @docroot@/development/experimental-features.md#xp-feature-ca-derivations
[xp-feature-git-hashing]: @docroot@/development/experimental-features.md#xp-feature-git-hashing
[xp-feature-impure-derivations]: @docroot@/development/experimental-features.md#xp-feature-impure-derivations
