# 标识符

*标识符（identifier）*是一个 [ASCII](https://en.wikipedia.org/wiki/ASCII) 字符序列，它：
- 以字母（`a-z`、`A-Z`）或下划线（`_`）开头
- 可以包含任意数量的：
  - 字母（`a-z`、`A-Z`）
  - 数字（`0-9`）
  - 下划线（`_`）
  - 单引号（`'`）
  - 连字符（`-`）
- 不是[关键字](#keywords)之一

> **语法**
>
> *identifier* ~ `[A-Za-z_][A-Za-z0-9_'-]*`

# 名称

*名称（name）*可以写作[标识符](#identifiers)或[字符串字面量](./string-literals.md)。

> **语法**
>
> *name* → *identifier* | *string*

名称用于[属性集](./syntax.md#attrs-literal)、[`let` 绑定](./syntax.md#let-expressions)以及 [`inherit`](./syntax.md#inheriting-attributes) 中。
只要两个名称表示相同的字符序列，它们就是相同的，无论它们写作标识符还是字符串。

# 关键字

以下关键字是保留字，不能用作[标识符](#identifiers)：

- [`assert`](./syntax.md#assertions)
- [`else`][if]
- [`if`][if]
- [`in`][let]
- [`inherit`](./syntax.md#inheriting-attributes)
- [`let`][let]
- [`or`](./operators.md#attribute-selection)（参见注释）
- [`rec`](./syntax.md#recursive-sets)
- [`then`][if]
- [`with`](./syntax.md#with-expressions)

[if]: ./syntax.md#conditionals
[let]: ./syntax.md#let-expressions

> **注意**
>
> 出于向后兼容的原因，Nix 语言求值器目前允许在某些上下文中把 `or` 用作名称。
> 建议用户不要依赖这一点。
>
> `or` 作为名称的解析方式存在长期存在的问题，而要解决这些问题就必须对语言进行破坏性变更。
