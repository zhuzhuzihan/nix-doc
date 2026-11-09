# 输入寻址 derivation 输出

[input addressing]: #input-addressing

"输入寻址"是指按存储对象*被制造的方式*而非*它是什么*来寻址。
也就是说，输入寻址输出的存储路径不是输出的函数，而是产出它的 derivation 的函数。
即使两个存储路径内容相同，只要它们的产出方式不同，且其中之一是输入寻址的，它们就会有不同的存储路径，从而保证不是同一个存储对象。

## 掩蔽内容寻址的 derivation 输出 {#input-masked-drv}

对输入寻址输出计算输出哈希的朴素做法，是把 derivation 哈希与输出一起做哈希。
这显然具有我们期望的输入寻址输出的唯一性性质，但存在效率问题。
具体来说，每当固定输出 derivation 发生变更时，就需要新的构建，尽管可以证明新 derivation 的输入与原先相比毫无差异。
具体而言，这会导致任何抓取细节（包括镜像列表、证书颁发机构证书等）发生变化时都触发"大规模重建"。

为了解决这个问题，我们以不同的方式计算输出哈希，使某些输出哈希变得相同。
做法是*掩蔽*（masking）：在哈希之前，重写 derivation 中我们不希望看到差异的部分。

有两种掩蔽，它们相互独立：

- *输入掩蔽*把每个输入 derivation 的存储路径替换为一个哈希，该哈希代表那个输入*所产出的东西*，而不是产出它的 derivation。
  这使得产出相同输出的不同固定输出 derivation 输入不再造成影响。

- *输出掩蔽*把 derivation 自身的输出路径置空——在 `outputs` 中，以及以它们命名的环境变量中。
  当我们正在计算的就是那些路径本身时，需要这样做；当 derivation 只是作为某个其他东西的输入的代表而被哈希时，则不希望这样做，因为它已有的路径恰恰是标识它的东西。

只应用第一种掩蔽的 derivation 是*输入掩蔽 derivation*；两种都应用的则是*完全掩蔽 derivation*。

每个非单射函数都会在其定义域上诱导出一个等价关系：把映射到同一值的两个元素视为等价。
但输入掩蔽所诱导的等价关系也可以直接刻画，完全不必提及输入掩蔽。
直觉上这是合理的，因为输入究竟如何被哈希（例如用哪个哈希函数）的细节不应有影响（忽略哈希碰撞之类）——重要的是哪些 derivation 被视为等价。
下文的[语义性质](#semantic-properties)一节将对此进一步展开。

那么，我们如何计算输入寻址 derivation 的输出路径的[哈希部分](@docroot@/store/store-path.md#digest)？
这由下面所示的函数 `hashInputMaskedDerivation` 完成，它执行输入掩蔽本身；其调用者做输出掩蔽。

首先，说一说输入。
`hashInputMaskedDerivation` 只对[输入](@docroot@/store/derivation/index.md#inputs)为一阶形式的 derivation 有定义：
```typescript
type ConstantPath = {
  path: StorePath;
};

type FirstOrderOutputPath = {
  drvPath: StorePath;
  output: OutputName;
};

type FirstOrderDerivingPath = ConstantPath | FirstOrderOutputPath;

type Inputs = Set<FirstOrderDerivingPath>;
```

对下文的算法，我们采用一个把两类（一阶）derived path 划分为两个集合的 derivation，如下：
```typescript
type Derivation = {
  // inputs: Set<FirstOrderDerivingPath>; // replaced
  inputSrcs: Set<ConstantPath>; // new instead
  inputDrvOutputs: Set<FirstOrderOutputPath>; // new instead
  // ...other fields...
};
```

在[当前处于实验状态][xp-feature-dynamic-derivations]的高阶情形下，输出的输出可以作为 [deriving path][deriving-path]、从而作为 derivation 输入；使用这种泛化的 derivation 不是该函数的有效参数。
那些 derivation 必须先（部分地）[解析](@docroot@/store/resolution.md)到足够的程度，直到不再有这样的高阶输入。
然后、且只有然后，才能分配输入地址。

```
function hashInputMaskedDerivation(drv) -> Hash:
    assert(drv.outputs are input-addressed)
    drv′ ← drv with {
        inputDrvOutputs = ⋃(
            assert(drvPath is store path)
            case hashOutputsOrInputMaskedDerivation(readDrv(drvPath)) of
                drvHash : Hash →
                    (drvHash.toBase16(), output)
                outputHashes : Map[String, Hash] →
                    (outputHashes[output].toBase16(), "out")
            | (drvPath, output) ∈ drv.inputDrvOutputs
        )
    }
    return hashSHA256(printDrv(drv′))

function hashOutputsOrInputMaskedDerivation(drv) -> Map[String, Hash] | Hash:
    if drv.outputs are content-addressed:
        return {
            outputName ↦ hashSHA256(
                "fixed:out:" + ca.printMethodAlgo() +
                ":" + ca.hash.toBase16() +
                ":" + ca.makeFixedOutputPath(drv.name, outputName))
            | (outputName ↦ output) ∈ drv.outputs
            , ca = output.contentAddress // or get from build trace if floating
        }
    else: // drv.outputs are input-addressed
        return hashInputMaskedDerivation(drv)
```

### `hashInputMaskedDerivation`

我们用对该元素的 `drvPath` 调用 `hashOutputsOrInputMaskedDerivation` 所得的数据，替换 derivation 的 `inputDrvOutputs` 中的每个元素。
当 `hashOutputsOrInputMaskedDerivation` 返回单个 drv 哈希时（因为所论的输入 derivation 是输入寻址的），我们直接把 `drvPath` 换成那个哈希，并保留相同的输出名。
当 `hashOutputsOrInputMaskedDerivation` 返回按输出的内容地址映射时，我们查找所论的输出，并将其与输出名 `out` 配对。

这一重写就是输入掩蔽。
得到的伪 derivation（`inputDrvs` 中以哈希代替存储路径）随后被打印（为 ["ATerm" 格式](@docroot@/protocols/derivation-aterm.md#input-address-encoding)）并做哈希，这成为输入掩蔽 derivation 的哈希。

在计算输出哈希时，`hashInputMaskedDerivation` 被调用在一个几乎完整的输入寻址 derivation 上，它只缺自己的输入寻址输出路径——也就是说，它已经输出掩蔽，因此是完全掩蔽的。
然后按[完整的存储路径计算](@docroot@/protocols/store-path.md#fingerprint)规范，用该 derivation 哈希为每个输出计算输出路径：它是该规范所要求的被哈希 ATerm 的摘要，属于 `"output:" id` 情形，其中 `id` 是输出名。
存储对象的名称是 derivation 的名称加上 `-` 和输出名——除非输出名为 `out`，此时直接使用 derivation 的名称。

注意，一个 derivation 哈希服务于所有输出；区分它们路径的只有输出名，而且输出名出现了两次：既是 `id`，也是名称的一部分。

随后，这些输出路径可以被代回那个几乎完整的输入寻址 derivation，使其完整。

> **注意**
>
> 当前实现在 `(outputHashes[output].toBase16(), "out")` 情形中可能存在与规范的无意偏差。
> 这不是致命的，因为该偏差只会影响有多个输出的内容寻址 derivation，而这只发生在浮动情形，后者是[实验性的][xp-feature-ca-derivations]。
> 此 bug 修复后，本说明将被移除。

### `hashOutputsOrInputMaskedDerivation`

`hashOutputsOrInputMaskedDerivation` 包含两个主要情形，依据 derivation 的输出将被输入寻址还是内容寻址。

#### 输入寻址输出情形

在输入寻址情形下，它只是调用 `hashInputMaskedDerivation`，并返回那个 derivation 哈希。
这使得 `hashInputMaskedDerivation` 与 `hashOutputsOrInputMaskedDerivation` 相互递归。

> **注意**
>
> 在这种情形下，`hashInputMaskedDerivation` 被调用在一个*完整的*输入寻址 derivation 上，它已经计算出了自己的输出路径：它没有输出掩蔽，因此只是输入掩蔽的，而不是完全掩蔽的。
> 输入掩蔽照样发生。

#### 内容寻址输出情形

如果输出是[内容寻址](./content-address.md)的，它就为每个输出计算一个由该输出的内容地址派生的哈希。

> **注意**
>
> 在[固定](./content-address.md#fixed)内容寻址情形中，输出的内容地址被预先静态指定，所以这总是直接可行。
> （伪代码展示的正是固定情形。）
>
> 在[浮动](./content-address.md#floating)情形中，内容地址没有被预先指定。
> 这就是"浮动时从 [build trace](@docroot@/store/build-trace.md) 获取"这一注释所指的情形。
> 在这种情形下，算法会*卡住*，直到所论的输入被构建、我们知道了所论输出的实际内容为止。
>
> 不过这没有问题，因为把输入地址的分配（请记住，这正是 `hashInputMaskedDerivation` 的最终目的）推迟到所有输入都已知之时，并无不妥。

### 在未知 CA 存储对象的下游推迟输入寻址 {#deferred}

正如前一条说明所说，当一个输入是尚未构建的[浮动内容寻址](./content-address.md#floating)输出时，算法会*卡住*：没有内容地址可以代换它，因此输入掩蔽无法完成，也无法计算输入地址。

derivation 仍会被写入 store，其输出处于*推迟*状态：处于此状态的输出根本没有存储路径，以其命名的环境变量为空。
这没有任何代价，因为 derivation 自身的存储路径是按其序列化字节[内容寻址](@docroot@/store/store-object/content-address.md#method-text)的，而这些字节并不取决于其输出路径是否已知。

推迟的输出并没有使用与输入寻址、内容寻址并列的第三种寻址。
它是输入寻址的；只是还不知道自己的路径。

卡住是会传染的。
就此目的而言，带推迟输出的 derivation 有着自己未知的输出，因此 `hashOutputsOrInputMaskedDerivation` 会转而卡在它上面，任何依赖它的东西也必须推迟。
于是这个条件从引起它的浮动输出向下游传播。

推迟通过构建来化解，而不是通过重新审视同一个 derivation。
一旦出问题的输入被构建，它们的内容地址就已知了，该 derivation 就可以被[解析](@docroot@/store/resolution.md)：其输入被替换为它们实际所表示的普通存储路径。
解析后的 derivation 是一个*不同的* derivation，有自己的存储路径——必然如此，因为它的字节不同。
它不再有会卡住的输入 derivation，因此其输入地址可计算，它才是真正被构建的那个。

> **注意**
>
> 没有任何东西为推迟输出本身设门槛。
> 它们只会在[浮动内容寻址](./content-address.md#floating)输出的下游*出现*。

### 性能

算法中的递归可能低效：
对每条可以到达某个子 derivation 的路径，它都可能调用自身一次，即对一个有 `V` 个 derivation、出度至多 `k` 的 derivation 图，调用次数为 `O(V^k)`。
在实际实现中，使用[备忘](https://en.wikipedia.org/wiki/Memoization)把这一开销降到与遇到的 `inputDrvOutputs` 总数成正比。

### 语义性质 {#semantic-properties}

*参见[本章附录](@docroot@/store/math-notation.md)中关于语法与元变量约定的说明。*

从数学上讲，掩蔽是一个商（quotient），参照商类型或商集：它丢弃的恰恰是我们允许两个 derivation 不同的那些方面。
相应地，`hashInputMaskedDerivation` 把输入寻址 derivation 划分成等价类：该等价类中的每个 derivation 都被映射到同一个 derivation 哈希。
我们可以自底向上地直接刻画这一等价关系。

我们先在引用内容寻址 derivation 输出的一阶输出 deriving path 上定义一个等价关系。两个这样的路径若引用同一存储对象，则等价：

\\[
\\begin{prooftree}
\\AxiomC{$d\_1$ is content-addressing}
\\AxiomC{$d\_2$ is content-addressing}
\\AxiomC{$
  {}^\*(\text{path}(d\_1), o\_1)
  \=
  {}^\*(\text{path}(d\_2), o\_2)
$}
\\TrinaryInfC{$(\text{path}(d\_1), o\_1) \\,\\sim_{\\mathrm{CA}}\\, (d\_2, o\_2)$}
\\end{prooftree}
\\]

其中 \\({}^*(s, o)\\) 表示该输出 deriving path 所引用的存储对象。

我们还需要如下构造，把 \\(X\\) 上的任意等价关系提升为 \\(X\\) 的（有限）集合（简记为 \\(\\mathcal{P}(X)\\)）上的等价关系：

\\[
\\begin{prooftree}
\\AxiomC{$\\forall a \\in A. \\exists b \\in B. a \\,\\sim\_X\\, b$}
\\AxiomC{$\\forall b \\in B. \\exists a \\in A. b \\,\\sim\_X\\, a$}
\\BinaryInfC{$A \\,\\sim_{\\mathcal{P}(X)}\\, B$}
\\end{prooftree}
\\]

现在我们可以在输入寻址 derivation 输出上定义等价关系 \\(\\sim_\\mathrm{IA}\\)。两个输入寻址输出若其 derivation 等价（通过尚未定义的 \\(\\sim_{\\mathrm{IADrv}}\\) 关系）且输出名相同，则等价：

\\[
\\begin{prooftree}
\\AxiomC{$d\_1$ is input-addressing}
\\AxiomC{$d\_2$ is input-addressing}
\\AxiomC{$d\_1 \\,\\sim_{\\mathrm{IADrv}}\\, d\_2$}
\\AxiomC{$o\_1 = o\_2$}
\\QuaternaryInfC{$(\text{path}(d\_1), o\_1) \\,\\sim_{\\mathrm{IA}}\\, (\text{path}(d\_2), o\_2)$}
\\end{prooftree}
\\]

现在我们可以定义 \\(\\sim_{\\mathrm{IADrv}}\\)。
两个输入寻址 derivation 若其内容寻址输入等价、其输入寻址输入也等价、且其余部分相等，则等价：

<!-- cheating a bit with the semantics to get a good layout that fits on the page -->

\\[
\\begin{prooftree}
\\alwaysNoLine
\\AxiomC{$
  \\mathrm{caInputs}(d\_1)
  \\,\\sim_{\\mathcal{P}(\\mathrm{CA})}\\,
  \\mathrm{caInputs}(d\_2)
$}
\\AxiomC{$
  \\mathrm{iaInputs}(d\_1)
  \\,\\sim_{\\mathcal{P}(\\mathrm{IA})}\\,
  \\mathrm{iaInputs}(d\_2)
$}
\\BinaryInfC{$
  d\_1\left[\\mathrm{inputDrvOutputs} := \\{\\}\right]
  \=
  d\_2\left[\\mathrm{inputDrvOutputs} := \\{\\}\right]
$}
\\alwaysSingleLine
\\UnaryInfC{$d\_1 \\,\\sim_{\\mathrm{IADrv}}\\, d\_2$}
\\end{prooftree}
\\]

其中 \\(\\mathrm{caInputs}(d)\\) 返回 \\(d\\) 的内容寻址输入，\\(\\mathrm{iaInputs}(d)\\) 返回输入寻址输入。

> **注意**
>
> 细心的读者可能会注意到，`inputSrcs` 在这些定义中完全没有出现。
> 这意味着把一个输入 derivation 替换为其输出并直接加入 `inputSrcs`，总会得到一个处于不同等价类的 derivation，尽管得到的输入闭包（即构建时挂载进 store 的内容）是相同的。
> [Issue #9259](https://github.com/NixOS/nix/issues/9259) 就是要创建一个更粗的等价关系来解决这个问题。
>
> 来自 [derivation 解析](@docroot@/store/resolution.md)的 \\(\\sim_\mathrm{Drv}\\) 就是这样一个等价关系。
> 它比这一个更粗：任何两个"'hash input-masked derivation'-等价"（\\(\\sim_\mathrm{IADrv}\\)）的 derivation 也是"解析等价"（\\(\\sim_\mathrm{Drv}\\)）的。
> 它还关联那些 `inputDrvOutputs` 被改写为 `inputSrcs` 的 derivation。
>
> 如上所述，内容寻址下游的输入寻址已经预见了这一点。
> 由于内容寻址输入贡献的只是其内容地址、而非产出它的 derivation，仅在*相同*的内容寻址输入如何被产出上有差异的 derivation 已经是 \\(\\sim_\mathrm{IADrv}\\)-等价的。
> 又由于推迟的 derivation 在被输入寻址之前已完全解析，其输入寻址的 `inputDrvOutputs` 也被规范化为 `inputSrcs`——因此仅在*相同的输入寻址*输入如何被产出上有差异的 derivation 也是 \\(\\sim_\mathrm{IADrv}\\)-等价的。
> 这与 \\(\\sim_\mathrm{Drv}\\) 的"按输入是什么、而非按它如何被制造来识别输入"的思路相同。
> 区别在于 \\(\\sim_\mathrm{Drv}\\) 无条件地这样做，而在这里，它对内容寻址输入总是成立，对其余输入只在推迟迫使先解析时才成立。

[deriving-path]: @docroot@/store/derivation/index.md#deriving-path
[xp-feature-dynamic-derivations]: @docroot@/development/experimental-features.md#xp-feature-dynamic-derivations
[xp-feature-ca-derivations]: @docroot@/development/experimental-features.md#xp-feature-ca-derivations
