# 数据类型

Nix 语言中的每个值都属于以下类型之一：

* [整数](#type-int)
* [浮点数](#type-float)
* [布尔值](#type-bool)
* [字符串](#type-string)
* [路径](#type-path)
* [空值](#type-null)
* [属性集](#type-attrs)
* [列表](#type-list)
* [函数](#type-function)
* [外部值](#type-external)

## 基本类型

### 整数 {#type-int}

Nix 语言中的_整数_是有符号 64 位整数。

非负整数可以写作[整数字面量](syntax.md#number-literal)。
负整数通过[算术取负运算符](./operators.md#arithmetic)创建。
函数 [`builtins.isInt`](builtins.md#builtins-isInt) 可用于判断一个值是否为整数。

### 浮点数 {#type-float}

Nix 语言中的_浮点数_是 64 位 [IEEE 754](https://en.wikipedia.org/wiki/IEEE_754) 浮点数。

大多数非负浮点数可以写作[浮点数字面量](syntax.md#number-literal)。
负浮点数通过[算术取负运算符](./operators.md#arithmetic)创建。
函数 [`builtins.isFloat`](builtins.md#builtins-isFloat) 可用于判断一个值是否为浮点数。

### 布尔值 {#type-bool}

Nix 语言中的_布尔值_是 _true_ 或 _false_ 之一。

<!-- TODO: mention the top-level environment -->

这些值可作为 [`builtins`](builtins.md#builtins-builtins) 的属性使用，即 [`builtins.true`](builtins.md#builtins-true) 和 [`builtins.false`](builtins.md#builtins-false)。
函数 [`builtins.isBool`](builtins.md#builtins-isBool) 可用于判断一个值是否为布尔值。

### 字符串 {#type-string}

Nix 语言中的_字符串_是一个不可变的、有限长度的字节序列，同时带有一个[字符串上下文](string-context.md)。
Nix 既不假设也不支持以原生方式处理字符编码。

不带字符串上下文的字符串值可以写作[字符串字面量](string-literals.md)。
函数 [`builtins.isString`](builtins.md#builtins-isString) 可用于判断一个值是否为字符串。

### 路径 {#type-path}

Nix 语言中的_路径_是一个不可变的、有限长度的、以 `/` 开头的字节序列，表示一个 POSIX 风格的规范化文件系统路径。
路径值与字符串值是不同的类型，即使它们包含相同的字节序列。
产生路径的操作会像标准 C 函数 [`realpath`] 那样简化结果，但不会解析符号链接。

[`realpath`]: https://pubs.opengroup.org/onlinepubs/9699919799/functions/realpath.html

路径适合用来引用本地文件，而且通常比字符串更可取。
- 路径值不包含末尾或重复的斜杠、`.` 或 `..`。
- 相对路径字面量会自动相对于其[基准目录]进行解析。
- 工具可以识别路径字面量并提供额外的功能，例如自动补全、重构自动化和跳转到文件。

[base directory]: @docroot@/glossary.md#gloss-base-directory

一个路径值要有效，并不要求该路径处确实存在文件；但是通过[字符串插值]或[字符串与路径拼接]转换为字符串的路径必须能解析到一个可读的文件或目录，该文件或目录会被复制进 Nix store。
例如，求值 `"${./foo.txt}"` 会把同一目录下的 `foo.txt` 复制进 Nix store，并得到字符串 `"/nix/store/<hash>-foo.txt"`。
诸如 [`import`] 之类的操作也可能要求路径能解析到可读的文件或目录。

[string interpolation]: string-interpolation.md#interpolated-expression
[string-and-path concatenation]: operators.md#string-and-path-concatenation
[`import`]: builtins.md#builtins-import

> **注意**
>
> Nix 语言假设在求值 Nix 表达式期间，所有输入文件都保持_不变_。
> 例如，假设你在一次 `nix repl` 会话中在插值字符串里使用了某个文件路径。
> 稍后在同一个会话中，在修改了文件内容之后，再次求值带有该文件路径的插值字符串可能不会返回新的[存储路径]，因为 Nix 可能不会重新读取文件内容。
> 需要时可用 `:r` 重置 repl。

[store path]: @docroot@/store/store-path.md

路径值可以写作[路径字面量](syntax.md#path-literal)。
函数 [`builtins.isPath`](builtins.md#builtins-isPath) 可用于判断一个值是否为路径。

### 空值 {#type-null}

Nix 语言中只有一个 _null_ 类型的值。

<!-- TODO: mention the top-level environment -->

该值可作为 [`builtins`](builtins.md#builtins-builtins) 属性集的属性使用，即 [`builtins.null`](builtins.md#builtins-null)。

## 复合值

### 属性集 {#type-attrs}

<!-- TODO(@rhendric, #10970): fill this out -->

属性集可以用[属性集字面量](syntax.md#attrs-literal)构造。
函数 [`builtins.isAttrs`](builtins.md#builtins-isAttrs) 可用于判断一个值是否为属性集。

### 列表 {#type-list}

<!-- TODO(@rhendric, #10970): fill this out -->

列表可以用[列表字面量](syntax.md#list-literal)构造。
函数 [`builtins.isList`](builtins.md#builtins-isList) 可用于判断一个值是否为列表。

## 函数 {#type-function}

<!-- TODO(@rhendric, #10970): fill this out -->

函数可以用[函数表达式](syntax.md#functions)构造。
函数 [`builtins.isFunction`](builtins.md#builtins-isFunction) 可用于判断一个值是否为函数。

## 外部值 {#type-external}

_外部值_是由 Nix [插件](../command-ref/conf-file.md#conf-plugin-files)创建的不透明值。
这样的值可以在 Nix 表达式中被替换使用，但只能由插件代码创建和操作。
