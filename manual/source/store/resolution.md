# Derivation 解析（Resolution）

*参见[本章附录](@docroot@/store/math-notation.md)中关于语法与元变量约定的说明。*

*解析*（resolve）一个 derivation，是指把它的[输入]替换为表示相同存储对象的最简输入——即普通的存储路径。

只以存储路径作为输入的 derivation 同样被称为 *resolved derivation*（已解析 derivation）。
（无论它们实际上是 derivation 解析的产物，还是一开始就不含非存储路径输入、天然如此，都这样称呼。）

## Derivation 的输入内容等价

[Deriving paths][deriving-path] 有意使同一个[存储对象]可以被多种方式引用。
这是内容寻址的结果，因为不同的 derivation 可以产出相同的输出，而且相同的数据也可以被手动添加进 store。
这甚至也是输入寻址的结果，因为一个输出既可以按 derivation 与输出名引用，也可以直接按其[计算出的](./derivation/outputs/input-address.md)存储路径引用。
由于对 deriving path 的解引用不是单射的，它在 deriving path 上诱导出一个等价关系。

我们把这一等价关系记为 \\(\\sim\\)，其中 \\(p_1 \\sim p_2\\) 表示 deriving path \\(p_1\\) 与 \\(p_2\\) 引用同一个存储对象。

**内容等价（Content Equivalence）**：两个 deriving path 若引用同一存储对象，则等价：

\\[
\\begin{prooftree}
\\AxiomC{${}^*p_1 = {}^*p_2$}
\\UnaryInfC{$p_1 \\,\\sim_\\mathrm{DP}\\, p_2$}
\\end{prooftree}
\\]

其中 \\({}^\*p\\) 表示 deriving path \\(p\\) 所引用的存储对象。

这也在 deriving path 的集合上诱导出一个等价关系：

\\[
\\begin{prooftree}
\\AxiomC{$\\{ {}^*p | p \\in P_1 \\} = \\{ {}^*p | p \\in P_2 \\}$}
\\UnaryInfC{$P_1 \\,\\sim_{\\mathcal{P}(\\mathrm{DP})}\\, P_2$}
\\end{prooftree}
\\]

**输入内容等价（Input Content Equivalence）**：这又进一步在 derivation 上诱导出一个等价关系：若两个 derivation 的输入等价且其余部分相等，则二者等价：

\\[
\\begin{prooftree}
\\AxiomC{$\\mathrm{inputs}(d_1) \\,\\sim_{\\mathcal{P}(\\mathrm{DP})}\\, \\mathrm{inputs}(d_2)$}
\\AxiomC{$
  d\_1\left[\\mathrm{inputs} := \\{\\}\right]
  \=
  d\_2\left[\\mathrm{inputs} := \\{\\}\right]
$}
\\BinaryInfC{$d_1 \\,\\sim_\\mathrm{Drv}\\, d_2$}
\\end{prooftree}
\\]

derivation 解析总是把 derivation 映射到与其输入内容等价的 derivation。

## 解析关系

对 derived path 的解引用——即上文的 \\({}^\*p\\)——此前只是作为一个黑箱引入的。
但实际上它是一个多步骤的过程：在 [build trace] 中查找构建结果，而查找本身就依赖于对查找键的解析。
因此解析是一个递归的多步骤过程，值得形式化地画出来。

我们可以用一个小步二元迁移关系来做到这一点；记之为 \\(\rightsquigarrow\\)。
然后我们可以这样得出解引用后的相等：

\\[
\\begin{prooftree}
\\AxiomC{$p\_1 \\rightsquigarrow^* p$}
\\AxiomC{$p\_2 \\rightsquigarrow^* p$}
\\BinaryInfC{${}^*p\_1 = {}^*p\_2$}
\\end{prooftree}
\\]

也就是说，通过证明两个原始项都（经过 0 步或多步小步规约，故有 \\({}^*\\)）解析到完全相同的项。

带着这一动机，我们现在来形式化一个用于解析的[小步](https://en.wikipedia.org/wiki/Operational_semantics#Small-step_semantics)规约规则系统。

### 形式化规则

### \\(\text{resolved}\\) 一元关系

\\[
\\begin{prooftree}
\\AxiomC{$s \in \text{store-path}$}
\\UnaryInfC{$s$ resolved}
\\end{prooftree}
\\]

\\[
\\begin{prooftree}
\\AxiomC{$\forall i \in \mathrm{inputs}(d). i \text{ resolved}$}
\\UnaryInfC{$d$ resolved}
\\end{prooftree}
\\]

### \\(\rightsquigarrow\\) 二元关系

> **注记**
>
> 实际上，若要完全形式化，我们还需要跟踪我们所选定据以解析的 build trace。
>
> 我们可以把 \\(\rightsquigarrow\\) 做成三元关系来做到这一点，它会把 build trace 一路传递给自己，直到在最后一条规则中真正用上它。
> 但这带来的繁琐多于洞见，所以我们没有费心去写。
>
> 还有其他办法，例如说整个规约规则系统以 build trace 为参数，本质上是把三元关系 \\(\rightsquigarrow\\) 经过[柯里化](https://en.wikipedia.org/wiki/Currying)变成一个从 build trace 到上文所写二元关系的函数。

#### 核心 build trace 查找规则

\\[
\\begin{prooftree}
\\AxiomC{$s \in \text{store-path}$}
\\AxiomC{${}^*s \in \text{derivation}$}
\\AxiomC{${}^*s$ resolved}
\\AxiomC{$\mathrm{build\text{-}trace}[s][o] = t$}
\\QuaternaryInfC{$(s, o) \rightsquigarrow t$}
\\RightLabel{\\scriptsize output path resolution}
\\end{prooftree}
\\]

#### 归纳规则

\\[
\\begin{prooftree}
\\AxiomC{$i \\rightsquigarrow i'$}
\\AxiomC{$i \\in \\mathrm{inputs}(d)$}
\\BinaryInfC{$d \\rightsquigarrow d[i \\mapsto i']$}
\\end{prooftree}
\\]

\\[
\\begin{prooftree}
\\AxiomC{$d \\rightsquigarrow d'$}
\\UnaryInfC{$(\\mathrm{path}(d), o) \\rightsquigarrow (\\mathrm{path}(d'), o)$}
\\end{prooftree}
\\]

\\[
\\begin{prooftree}
\\AxiomC{$p \\rightsquigarrow p'$}
\\UnaryInfC{$(p, o) \\rightsquigarrow (p', o)$}
\\end{prooftree}
\\]

### 性质

与所有表现良好的求值关系一样，部分解析是[*合流的*](https://en.wikipedia.org/wiki/Confluence_(abstract_rewriting))。
此外，若取 \\(\\rightsquigarrow^\*\\) 的对称闭包，就会得到上一节中的那些等价关系。
解析尊重 deriving path 的内容等价和 derivation 的输入内容等价。

> **注记**
>
> 我们选择在上面从零开始显式定义一个 "resolved" 一元关系。
> 但它也可以被定义为 \\(\\rightsquigarrow^\*\\) 关系的范式：
>
> \\[ a \text{ resolved} \Leftrightarrow \forall b. b \rightsquigarrow^* a \Rightarrow b = a\\]
>
> 用散文来说：resolved 的项，是指 \\(\\rightsquigarrow^\*\\) 在左侧把它们与右侧同一项相关联的项；它们是不能再被进一步解析的项。

## 部分解析与完全解析

与求值类似，我们也可以谈论*部分*与*完全*的 derivation 解析。
部分 derivation 解析就是我们上面用 \\(\\rightsquigarrow^\*\\) 实际形式化的东西。
完全解析则是以 resolved 项（deriving path 或 derivation）收尾的解析。
（按上面的注记，它是该关系的一个范式。）

在部分解析下，一个 derivation 会关联到输入相同或更简单的等价 derivation，但并非所有那些输入都会是普通存储路径。
当输入引用一个我们尚未构建的浮动内容寻址输出时，这很有用——我们不知道该 derivation 将使用什么（内容寻址的）存储路径，所以在解析所论的 deriving path 时会"卡住"。
（在上面的形式化中，这发生在 build trace 缺少我们想要查找的键的时候。）

完全解析是一个*函数性的*关系，即左边的值与右边的值唯一地相关联。
然而，它一般而言不是一个*全*关系（在任意 build trace 的假设下）。
这一点将在下一节讨论。

## 终止性

对于静态的 derivation 图，完全解析确实是全的，因为它对所有输入总是终止。
（既是全的又是函数性的关系就是一个函数。）

然而对于[动态][xp-feature-dynamic-derivations]的 derivation 图，情况并非如此——解析不保证终止。
问题不在于重写 deriving path 本身：
把一个输出的 deriving path 规范化为常量 deriving path 的单次重写总是存在，且总是一步完成。
问题在于动态 derivation（即由先前的解析填充进图中的那些）可能比原始 derivation 有更多的传递依赖。

> **示例**
>
> 假设有这个 deriving path
> ```json
> {
>   "drvPath": {
>     "drvPath": "...-foo.drv",
>     "output": "bar.drv"
>   },
>   "output": "baz"
> }
> ```
> 且 derivation `foo` 已经解析。
> 当我们解析这个 deriving path 时，最终会得到类似
> ```json
> {
>   "drvPath": "...-foo-bar.drv",
>   "output": "baz"
> }
> ```
> 的结果。
> 到目前为止这只是一次原子的单步重写，没有终止性问题。
> 但 derivation `foo-bar` 可能有其*自身*的动态 derivation 输入。
> 解析必须先解析那个 derivation，上面的 deriving path 才能最终被规范化为普通的 `...-foo-bar-baz` 存储路径。

需要注意的重要一点是："build trace" 的*键*必须是 resolved 的。
但这些键所映射到的*值*没有这样的约束。
任意的存储对象没有 resolved 与否的概念。
不过，任意的存储对象都可以被读回为一个 derivation（动态 derivation / 嵌套输出 deriving path 的情形实际上正是如此）。
而这些 derivation *未必*是 resolved 的。

正是这些动态的、未 resolved 的 derivation 是非终止性的来源。
同理，它们也是动态 derivation 具有更强表达能力的原因。

[store object]: @docroot@/store/store-object.md
[inputs]: @docroot@/store/derivation/index.md#inputs
[build trace]: @docroot@/store/build-trace.md
[deriving-path]: @docroot@/store/derivation/index.md#deriving-path
[xp-feature-dynamic-derivations]: @docroot@/development/experimental-features.md#xp-feature-dynamic-derivations
