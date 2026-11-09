# 运算符

| 名称                                   | 语法                                       | 结合性        | 优先级     |
|----------------------------------------|--------------------------------------------|---------------|------------|
| [属性选择]                  | *attrset* `.` *attrpath* \[ `or` *expr* \] | 无            | 1          |
| [函数应用]                 | *func* *expr*                              | 左            | 2          |
| [算术取反][arithmetic]      | `-` *number*                               | 无            | 3          |
| [属性判断]                        | *expr* `?` *attrpath*                      | 无            | 4          |
| 列表拼接                     | *list* `++` *list*                         | 右            | 5          |
| [乘法][arithmetic]           | *number* `*` *number*                      | 左            | 6          |
| [除法][arithmetic]                 | *number* `/` *number*                      | 左            | 6          |
| [减法][arithmetic]              | *number* `-` *number*                      | 左            | 7          |
| [加法][arithmetic]                 | *number* `+` *number*                      | 左            | 7          |
| [字符串拼接]                 | *string* `+` *string*                      | 左            | 7          |
| [路径拼接]                   | *path* `+` *path*                          | 左            | 7          |
| [路径与字符串拼接]        | *path* `+` *string*                        | 左            | 7          |
| [字符串与路径拼接]        | *string* `+` *path*                        | 左            | 7          |
| 逻辑非（`NOT`）               | `!` *bool*                                 | 无            | 8          |
| [更新]                               | *attrset* `//` *attrset*                   | 右            | 9          |
| [小于][Comparison]                | *expr* `<` *expr*                          | 无            | 10         |
| [小于等于][Comparison]    | *expr* `<=` *expr*                         | 无            | 10         |
| [大于][Comparison]             | *expr* `>` *expr*                          | 无            | 10         |
| [大于等于][Comparison] | *expr* `>=` *expr*                         | 无            | 10         |
| [相等]                             | *expr* `==` *expr*                         | 无            | 11         |
| 不等                             | *expr* `!=` *expr*                         | 无            | 11         |
| [逻辑与] (`AND`)          | *bool* `&&` *bool*                         | 左            | [12](#precedence-and-disjunctive-normal-form)         |
| [逻辑或] (`OR`)           | *bool* <code>\|\|</code> *bool*            | 左            | [13](#precedence-and-disjunctive-normal-form)         |
| [逻辑蕴含]                  | *bool* `->` *bool*                         | 右            | 14         |
| [管道运算符] (experimental)         | *expr* `\|>` *func*                        | 左            | 15         |
| [管道运算符] (experimental)         | *func* `<\|` *expr*                        | 右            | 15         |

[string]: ./types.md#type-string
[path]: ./types.md#type-path
[number]: ./types.md#type-float
[list]: ./types.md#type-list
[attribute set]: ./types.md#type-attrs

<!-- TODO(@rhendric, #10970): ^ rationalize number -> int/float -->

## 属性选择

> **语法**
>
> *attrset* `.` *attrpath* \[ `or` *expr* \]

从[属性集][attribute set] *attrset* 中选择由属性路径 *attrpath* 所表示的属性。
如果该属性不存在，则返回 `or` 之后的 *expr*（如果提供了的话），否则中止求值。

[属性选择]: #attribute-selection

## 函数应用

> **语法**
>
> *func* *expr*

将可调用值 *func* 应用到参数 *expr* 上。注意这里没有任何可见的运算符符号。
可调用值可以是以下之一：
- [用户自定义函数][function]
- [内建][builtins]函数
- 带有 [`__functor` 属性](./syntax.md#attr-__functor)的属性集

> **警告**
>
> [列表][list]的元素同样以空白分隔，这意味着列表元素中的函数调用必须用圆括号括起来。

## 属性判断

> **语法**
>
> *expr* `?` *attrpath*

检测 *expr* 是否是一个包含 *[attrpath]* 所表示属性的[属性集][attribute set]。
如果 *attrpath* 包含多个组成部分，且其中任何组成部分（除最后一个外）不对应 *expr* 中的一个属性集，则结果为 false。
结果是一个[布尔值][Boolean]。

参见：[`builtins.hasAttr`](@docroot@/language/builtins.md#builtins-hasAttr)

[attrpath]: ./syntax.md#attrpath-literal

[Boolean]: ./types.md#type-bool

[属性判断]: #has-attribute

在求值 *attrset* 和 *attrpath* 之后，计算复杂度为 O(log(*n*))，其中 *n* 是 *attrset* 中属性的数量。

## 算术运算

数字会保留其类型，除非与其他数值类型混合运算：
纯整数运算总是返回整数，而任何涉及至少一个浮点数的运算都会返回浮点数。

以下数值运算在求值时会抛出求值错误：
- 除以零
- 整数溢出，即任何运算结果超出 [Nix 语言整数](./syntax.md#number-literal)可表示范围的情况

另见 [比较运算][Comparison]与[相等][Equality]。

`+` 运算符被重载，也可用于字符串和路径。

[arithmetic]: #arithmetic

## 字符串拼接

> **语法**
>
> *string* `+` *string*

拼接两个[字符串][string]，并合并它们的[字符串上下文](./string-context.md)。

[字符串拼接]: #string-concatenation

## 路径拼接

> **语法**
>
> *path* `+` *path*

拼接两个[路径][path]。
结果是一个路径。

[路径拼接]: #path-concatenation

## 路径与字符串拼接

> **语法**
>
> *path* + *string*

将 *[path]* 与 *[string]* 拼接。
结果是一个路径。

> **注意**
>
> 该字符串的[字符串上下文](./string-context.md)中不得引用任何[存储路径]。

[路径与字符串拼接]: #path-and-string-concatenation

## 字符串与路径拼接

> **语法**
>
> *string* + *path*

将 *[string]* 与 *[path]* 拼接。
结果是一个字符串。

> **重要**
>
> *path* 处的文件或目录必须存在，并且会被复制到 [store（存储库）][store]。
> 该路径在结果中以对应的[存储路径]形式出现。

[store path]: @docroot@/store/store-path.md
[store]: @docroot@/glossary.md#gloss-store

[字符串与路径拼接]: #string-and-path-concatenation

## 更新

> **语法**
>
> *attrset1* // *attrset2*

用 *attrset2* 中的名字和值更新[属性集][attribute set] *attrset1*。

返回的属性集将包含 *attrset1* 和 *attrset2* 中的所有属性。
如果某个属性名在两者中都存在，则取后者中的属性值。

该运算符对 *attrset1* 和 *attrset2* 都是[严格的](@docroot@/language/evaluation.md#strictness)。
这意味着两个参数都会被求值到[弱首范式](@docroot@/language/evaluation.md#values)，即属性集本身会被求值，但它们的属性值不会被求值。

[更新]: #update

## 比较运算

比较的规则是：

- 对[数字][number]进行算术比较
- 对[字符串][string]和[路径][path]进行字典序比较
- 对[列表][list]逐项进行字典序比较：
  两个列表中相同索引处的元素按其类型进行比较，若相等则跳过。

所有比较运算符都基于 `<` 实现，并且以下等价关系成立：

| 比较         | 实现                  |
|--------------|-----------------------|
| *a* `<=` *b* | `! (` *b* `<` *a* `)` |
| *a* `>`  *b* |       *b* `<` *a*     |
| *a* `>=` *b* | `! (` *a* `<` *b* `)` |

[Comparison]: #comparison

## 相等

- [属性集][attribute set]先按属性名比较，再逐项比较，直到发现差异为止。
- [列表][list]先按长度比较，再逐项比较，直到发现差异为止。
- 对两个不同的[函数][function]进行比较返回 `false`，但相同的函数可能受[值同一性优化](#value-identity-optimization)影响。
- 数字之间类型兼容，参见[算术运算][arithmetic]符。
- 浮点数只在有限的精度范围内区分彼此。

`==` 运算符对两个参数都是[严格的](@docroot@/language/evaluation.md#strictness)；在比较复合类型（[属性集][attribute set]和[列表][list]）时，对其包含的值是部分严格的：这些值会被求值，直到发现差异为止。 <!-- this is woefully underspecified, affecting which expressions evaluate correctly; not just "ordering" or error messages. -->

### 值同一性优化

Nix 通过指针相等性来执行嵌套值的相等比较，或者更抽象地说，通过 _同一性_（identity）。
理想情况下，Nix 语义并不会为创建的值赋予唯一的同一性，但相等比较是这条规则的一个例外。
这样做有争议的好处是效率更高，并且能够比较循环结构，例如 `let x = { x = x; }; in x == x` 的求值结果为 `true`。
然而，其后果是，当比较发生在列表或属性集中时，一个函数会与它自身相等，这与简单直接的比较方式相矛盾。

[function]: ./syntax.md#functions

[Equality]: #equality

## 逻辑与

> **语法**
>
> *bool1* `&&` *bool2*

逻辑与。等价于 `if` *bool1* `then` *bool2* `else false`。

该运算符对 *bool1* 是[严格的](@docroot@/language/evaluation.md#strictness)，但只有在 *bool1* 为 `true` 时才会求值 *bool2*。

> **示例**
>
> ```nix
> true && false
> => false
>
> false && throw "never evaluated"
> => false
> ```

[逻辑与]: #logical-conjunction

## 逻辑或

> **语法**
>
> *bool1* `||` *bool2*

逻辑或。等价于 `if` *bool1* `then true` `else` *bool2*。

该运算符对 *bool1* 是[严格的](@docroot@/language/evaluation.md#strictness)，但只有在 *bool1* 为 `false` 时才会求值 *bool2*。

> **示例**
>
> ```nix
> true || false
> => true
>
> true || throw "never evaluated"
> => true
> ```

[逻辑或]: #logical-disjunction

### 优先级与析取范式

`&&` 和 `||` 的优先级与析取范式相一致。
在没有括号的情况下，一个表达式描述了多个「允许的情形」（由 `||` 连接），其中每个情形由多个同时成立的条件组成（由 `&&` 连接）。

例如，`A || B && C || D && E` 会被解析为 `A || (B && C) || (D && E)`，描述了三种允许的情形：A 成立，或者 B 与 C 同时成立，或者 D 与 E 同时成立。

## 逻辑蕴含

> **语法**
>
> *bool1* `->` *bool2*

逻辑蕴含。等价于 `!`*bool1* `||` *bool2*（或 `if` *bool1* `then` *bool2* `else true`）。

该运算符对 *bool1* 是[严格的](@docroot@/language/evaluation.md#strictness)，但只有在 *bool1* 为 `true` 时才会求值 *bool2*。

> **示例**
>
> ```nix
> true -> false
> => false
>
> false -> throw "never evaluated"
> => true
> ```

[逻辑蕴含]: #logical-implication

## 管道运算符

- *a* `|>` *b* 等价于 *b* *a*
- *a* `<|` *b* 等价于 *a* *b*

> **示例**
>
> ```
> nix-repl> 1 |> builtins.add 2 |> builtins.mul 3
> 9
>
> nix-repl> builtins.add 1 <| builtins.mul 2 <| 3
> 7
> ```

> **警告**
>
> 该语法属于一项
> [实验性特性](@docroot@/development/experimental-features.md)，
> 在未来的版本中可能会发生变化。
>
> 要使用该语法，请确保
> [`pipe-operators` 实验性特性](@docroot@/development/experimental-features.md#xp-feature-pipe-operators)
> 已启用。
> 例如，在 [`nix.conf`](@docroot@/command-ref/conf-file.md) 中加入以下内容：
>
> ```
> extra-experimental-features = pipe-operators
> ```

[管道运算符]: #pipe-operators
[builtins]: ./builtins.md
[函数应用]: #function-application
