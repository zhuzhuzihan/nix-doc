# 作用域规则

Nix 语言中的*作用域（scope）*是一个以[名称](./identifiers.md#names)为键的字典，它把每个名称映射到一个表达式以及一个*定义类型*。
定义类型要么是*显式（explicit）*的，要么是*隐式（implicit）*的。
这个字典中的每个条目都是一个*定义*。

以下表达式会创建显式定义：
- [let 表达式](syntax.md#let-expressions)
- [递归属性集字面量](syntax.md#recursive-sets)（`rec`）
- [函数字面量](syntax.md#functions)

隐式定义只会由 [with 表达式](./syntax.md#with-expressions)创建。

每个表达式都被一个作用域所*包围*。
最外层的表达式被[内置的全局作用域](./builtins.md)包围，后者只包含显式定义。
上面列出的表达式通过添加新定义、或以同名定义替换现有定义来*扩展*其外围作用域。
显式定义可以替换任何类型的定义；隐式定义只能替换另一个隐式定义。

上述每个表达式都规定了它的哪些子表达式被扩展后的作用域所包围。
在所有其他情况下，包围某个表达式的作用域同样也是其子表达式的外围作用域。

Nix 语言是[静态作用域（statically scoped）](https://en.wikipedia.org/wiki/Scope_(computer_science)#Lexical_scope)的；
变量的值只由变量的外围作用域决定，而与求值该变量时的动态上下文无关。

> **注意**
>
> 输入到 [Nix REPL](@docroot@/command-ref/new-cli/nix3-repl.md) 中的表达式被一个可以由命令行参数或之前的 REPL 命令扩展的作用域所包围。
> 严格来说，这些扩展作用域的方式并不属于 Nix 语言的一部分。
