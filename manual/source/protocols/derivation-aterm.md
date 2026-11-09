# derivation「ATerm」文件格式

出于历史原因，[store derivation][store derivation] 以「带注解项」（ATerm, Annotated Term）格式存储在磁盘上
（[指南](https://homepages.cwi.nl/~daybuild/daily-books/technology/aterm-guide/aterm-guide.html)，
[论文](https://doi.org/10.1002/(SICI)1097-024X(200003)30:3%3C259::AID-SPE298%3E3.0.CO;2-Y)）。

实际只用到 ATerm 的一小部分：下文的构造器、字符串字面量、列表和元组。

## 所使用的 ATerm 格式

derivation（派生）以以下格式之一序列化：

- ```
  Derive(...)
  ```

  用于所有稳定的 derivation。

- ```
  DrvWithVersion(<version-string>, ...)
  ```

  如今在用的 `version-string` 只有为[实验性特性](@docroot@/development/experimental-features.md)准备的那几种：

  - `"xp-dyn-drv"`，用于 [`dynamic-derivations`](@docroot@/development/experimental-features.md#xp-feature-dynamic-derivations) 实验性特性。

## 文法

```ebnf
derivation = "Derive(" fields ")"
            | "DrvWithVersion(" version "," fields ")" ;

fields = outputs "," input-drvs "," input-srcs ","
         platform "," builder "," args "," env ;

outputs    = "[" [ output { "," output } ] "]" ;
output     = "(" output-name "," output-path "," hash-algo "," hash ")" ;

input-drvs = "[" [ input-drv { "," input-drv } ] "]" ;
input-drv  = "(" drv-path "," input-drv-node ")" ;

input-srcs = "[" [ store-path { "," store-path } ] "]" ;

builder    = string ;
args       = "[" [ string { "," string } ] "]" ;

env        = "[" [ env-entry { "," env-entry } ] "]" ;
env-entry  = "(" string "," string ")" ;
```

所有叶子节点都带双引号，但分为两类。

```ebnf
(* may contain escape sequences *)
string      = '"' { char | escape } '"' ;

(* drawn from restricted alphabets, so never escaped *)
verbatim    = '"' { char } '"' ;

(* Not an alternation but a parameter of the grammar: the store
   directory fixes which one holds, for the whole file at once.
   See the note below. *)
store-path  = ? verbatim under a Unix store directory,
                string under a Windows one ? ;

drv-path    = store-path ; (* a store path whose name ends in ".drv" *)
output-path = store-path | '""' ;
output-name = verbatim ;
platform    = verbatim ;
version     = verbatim ;

hash-algo     = '"' [ method-prefix ] algorithm '"' | '""' ;
method-prefix = "r:" | "text:" | "git:" ;      (* flat has none *)
algorithm     = "blake3" | "md5" | "sha1" | "sha256" | "sha512" ;

hash        = '"' hex-digit { hex-digit } '"' | '""' | '"impure"' ;
```

`store-path` 是完整书写的[存储路径](@docroot@/protocols/store-path.md)，包含存储目录本身。

注意，derivation 的*名称*并不出现在文件中的任何地方。
它取自 derivation 的存储路径，因此必须在带外提供；见下文。

> **注意**
>
> `store-path` 是唯一未被文法固定下来的叶子，原因在于存储目录。
> Unix 的存储目录 `/nix/store` 恰好不含任何该格式需要转义的字符，因此路径可以原样书写。
> Windows 的存储目录则不然：`C:\ProgramData\nix\store` 包含反斜杠，必须转义，这使得该叶子成为 `string`：
>
> ```
> "C:\\ProgramData\\nix\\store/ib3sh3pcz10wsmavxvkdbayhqivbghlq-foo"
> ```
>
> 受影响的只有存储目录本身；将其与路径其余部分分隔开的 `/` 无论哪种情形都是正斜杠。
> 其余部分都不受影响：无论使用哪种存储目录，`output-name`、`platform`、`version` 以及两个哈希字段所取自的字母表都不需要转义。
>
> 这是一种模式，而不是对每个存储路径重新做出的选择：在给定文件中二者之一贯穿始终，且其中每个存储路径都按该方式书写。
> 该模式不记录在文件中，也无法从字节中恢复 —— 原样书写的路径同时也是合法的 `string` —— 因此它必须像 derivation 名称一样在带外提供。
> Nix 从它正在读写的 store 取得该模式，默认为其构建时所面向的平台，并据此约束解析器：在 Unix 存储目录下，带有转义字符的存储路径会被*拒绝*，而不会被当作同一路径的另一种写法接受。
> 正是这样保证了编码在两种情形下都是[规范形式](#canonical-form)。

### 字符串

上文中的每个叶子都是一个双引号字符串。
在字符串内，`"` 和 `\` 用反斜杠转义，换行符、回车符和制表符分别写作 `\n`、`\r` 和 `\t`。
这五种是仅有的转义，且这五个字符只会以转义形式书写；见[规范形式](#canonical-form)。

取自受限字母表的字段 —— 输出名称、平台和哈希字段 —— 不可能包含其中任何一个字符，因此原样书写。
存储路径同样原样书写，除非存储目录本身需要转义；见上文的注意事项。

### 输出

输出的类型没有显式标记；它由三个字段中哪些为空来推断。

| `output-path` | `hash-algo` | `hash` | 输出 |
| --- | --- | --- | --- |
| 已设置 | 为空 | 为空 | [输入寻址](@docroot@/store/derivation/outputs/input-address.md) |
| 为空 | 为空 | 为空 | [延迟输入寻址](@docroot@/store/derivation/outputs/input-address.md#deferred) |
| 已设置 | 已设置 | 已设置 | [固定输出内容寻址](@docroot@/store/derivation/outputs/content-address.md#fixed) |
| 为空 | 已设置 | 为空 | [浮动内容寻址](@docroot@/store/derivation/outputs/content-address.md#floating) |
| 为空 | 已设置 | `"impure"` | [非纯][xp-feature-impure-derivations] |

延迟输出并不使用自己的一种寻址方式：它是输入寻址的，但其路径尚不可知，这种情况出现在浮动内容寻址输入的下游。
它没有任何门控。
浮动输出需要 [`ca-derivations`][xp-feature-ca-derivations]，非纯输出需要 [`impure-derivations`][xp-feature-impure-derivations]；固定输出在方法为 `text:` 时还需要 [`dynamic-derivations`][xp-feature-dynamic-derivations]。

`hash-algo` 的 `method-prefix` 即[内容寻址方法](@docroot@/store/store-object/content-address.md)：

| 前缀 | 方法 |
| --- | --- |
| *（无）* | [Flat](@docroot@/store/store-object/content-address.md#method-flat) |
| `r:` | [Nix Archive](@docroot@/store/store-object/content-address.md#method-nix-archive) |
| `text:` | [Text](@docroot@/store/store-object/content-address.md#method-text) |
| `git:` | [Git](@docroot@/store/store-object/content-address.md#method-git) |

`hash` 为小写，且自身不带算法前缀 —— 算法由 `hash-algo` 指明。

对于固定输出 derivation，`output-path` 是冗余的 —— 它是内容地址的函数 —— 但它仍必须与内容地址一致。
否则，含义相同的两个 derivation 会得到不同的编码，进而得到不同的存储路径。

### 输入 derivation

每个条目将一个输入 derivation 的存储路径与其被使用的输出配对：

```ebnf
input-drv-node = output-names ;
output-names   = "[" [ output-name { "," output-name } ] "]" ;
```

在 `DrvWithVersion("xp-dyn-drv", ...)` 形式
—— 它需要 [`dynamic-derivations`][xp-feature-dynamic-derivations] 实验性特性 ——
中，节点可以改为嵌套，以指名某个 derivation 的输出，而该 derivation *本身*又是另一个 derivation 的输出：

```ebnf
input-drv-node = output-names
               | "(" output-names "," "[" [ child { "," child } ] "]" ")" ;
child          = "(" output-name "," input-drv-node ")" ;
```

### 规范形式

这种编码旨在是规范的（canonical）：每个 derivation 恰有一种。
这一点很重要，因为这些字节会被哈希——既用于对 derivation 自身做内容寻址，也用于计算[输入寻址](@docroot@/protocols/store-path.md)的输出路径——因此同一 derivation 的两种写法就会是两个不同的 derivation。

因此：

- 输出、输入 derivation、输入源和环境变量按键的升序出现，且无重复。
  `output-names`（指明使用了输入 derivation 的哪些输出）同样如此。

- 可转义的字符必须转义，且其他任何转义序列都无效。
  这两个方面都重要：字符串中的字面换行字节和 `\q`，各自都是对已有写法之物的第二种写法。

- 取自受限字母表的字段 —— 输出名称和平台 —— 完全不含转义序列，因为那里的转义会是同一值的第二种编码，而非必要的编码。
  存储路径遵循同样的规则，除非存储目录需要转义——此时转义属于必要的那种。

- 存储路径以其规范形式书写，且 `inputDrvs` 条目的键是一个 derivation 路径，以 `.drv` 结尾。

- 闭括号之后没有尾随内容。

已知有一个例外。
使用结构化属性（structured attributes）的 derivation 在其 [`__json` 环境变量](@docroot@/store/derivation/index.md#structured-attrs)中保存的 JSON *不*要求是规范 JSON。
相反，它必须逐字保留，而不是重新序列化。
由于这些字节会被哈希，derivation 恰好采用的任何编码都是其身份的一部分。
重新输出它 —— 即使是等价的 JSON —— 也会改变该 derivation。

> **注意**
>
> 这并不是因为此处不需要规范性，而是因为不存在一个已定论的规范性概念可供要求。
> 「规范 JSON」有多个相互竞争的定义，它们在键排序、数字表示和 Unicode 转义上意见不一。
> 它在技术上也很棘手：
> 例如，若没有浮点数的十六进制字面量，数字表示几乎难以处理。
> 结构化属性已经面世多年，因此任何此类选择还必须顾及已经存在的各种编码。
> 因此，就这个格式而言，我们目前还没有条件从中做出选择。

## 掩码 derivation {#input-address-encoding}

[输入寻址](@docroot@/store/derivation/outputs/input-address.md)的输出路径的计算方式是：先对一个被[掩码](@docroot@/store/derivation/outputs/input-address.md#input-masked-drv)处理过的 derivation 的 ATerm 表示做哈希：其中一部分内容在哈希前被置空，使得仅在被置空内容上不同的 derivation 哈希结果相同。

其编码与上文文法的差异在于两个产生式：

```ebnf
masked-derivation   = "Derive(" fields ")" ;

input-drv           = "(" drv-hash "," output-names ")" ;
drv-hash            = verbatim ;   (* lowercase hexadecimal *)
```

也就是说：

- 没有版本头。
  掩码 derivation 只会在动态 derivation 被解析消解之后构造，因此它从来不需要版本头，`DrvWithVersion(...)` 不会出现。

- `inputDrvs` 的键是哈希而非存储路径，且其节点总是扁平的 `output-names` —— 出于同样的原因，`dynamic-derivations` 版本允许的嵌套形式不会出现。

这些哈希如何得出以及为何如此，参见[输入寻址](@docroot@/store/derivation/outputs/input-address.md#input-masked-drv)；简而言之，它们按输入 derivation 产出什么（而非如何产出）来标识它，使得固定输出输入的获取来源发生变化不会影响下游的任何东西。

像这样把输入 derivation 的路径替换为哈希就是*输入掩码*（input masking），它作用于所有 derivation。

输出是否携带其路径取决于被哈希的对象是什么。
在计算 derivation 自身的输出路径时，输出还会被*输出掩码* —— `output-path` 以及以每个输出命名的环境变量都为空 —— 因为这些路径正是正在计算的内容；其结果为*完全掩码*。
当对一个 derivation 做哈希、让它作为另一个 derivation 的*输入*替身时，这些路径保持原样，结果仅为*输入掩码*。

其结果并不是一个可以被构建、写入 store 或被 `parse` 读回的 derivation：它的输入指名的是哈希而非路径。
它存在的意义只是被哈希。

## 用于编码为存储对象

当 derivation 被编码为[存储对象][store object]时，我们做出以下选择：

- 存储路径的[名称](@docroot@/store/store-path.md#name)是 derivation 名称，末尾加上 `.drv` 后缀

  实际上，上述 ATerm 格式*并不*包含 derivation 的名称，其前提是存储路径也会在带外提供。

- derivation 使用对 derivation 进行内容寻址的 ["Text" 方法]进行内容寻址

目前我们总是使用 ATerm 格式（以及前两个选择）把 derivation 编码为存储对象，
但我们保留将来以不同方式编码新种类 derivation 的选项。

[store derivation]: @docroot@/glossary.md#gloss-store-derivation
[store object]: @docroot@/glossary.md#gloss-store-object
["Text" method]: @docroot@/store/store-object/content-address.md#method-text
[xp-feature-ca-derivations]: @docroot@/development/experimental-features.md#xp-feature-ca-derivations
[xp-feature-dynamic-derivations]: @docroot@/development/experimental-features.md#xp-feature-dynamic-derivations
[xp-feature-impure-derivations]: @docroot@/development/experimental-features.md#xp-feature-impure-derivations
