# 语言结构

本节介绍 Nix 语言的语法和语义。

## 基本字面量

### 字符串 {#string-literal}

参见[字符串字面量](string-literals.md)。

### 数字 {#number-literal}

<!-- TODO(@rhendric, #10970): split this into int and float -->

  数字可以是*整数*（如 `123`）或*浮点数*（如 `123.43` 或 `.27e13`）。

  Nix 语言中的整数是 64 位[二进制补码]有符号整数，取值范围为 -9223372036854775808 到 9223372036854775807（含两端）。

  [二进制补码]: https://en.wikipedia.org/wiki/Two%27s_complement

  注意，负数字面量实际上被解析为对正数字面量的一元取负。
  这意味着最小整数 `-9223372036854775808` 不能按原样写成字面量，因为正数 `9223372036854775808` 已经超出最大范围一位。

  语义参见[算术]和[比较]运算符。

  [算术]: ./operators.md#arithmetic
  [比较]: ./operators.md#comparison

### 路径 {#path-literal}

  *路径*可以用路径字面量来表示，例如 `./builder.sh`。

  路径字面量必须至少包含一个斜杠才会被识别为路径。
  例如，`builder.sh` 就不是路径：
  它被解析为一个从变量 `builder` 中选取属性 `sh` 的表达式。

  路径字面量相对于其[基准目录](@docroot@/glossary.md#gloss-base-directory)解析。
  路径字面量也可以以斜杠开头来引用绝对路径。

  > **注意**
  >
  > 绝对路径会降低表达式的可移植性。
  > 当某个函数要把路径字面量转换为绝对路径字符串写进配置文件时，建议改用字符串字面量。
  > 这样可以避免对求值期间是否会使用该位置的文件产生混淆，也可以避免某些函数意外地试图把该位置的所有内容复制进 Nix store。

  如果路径的第一个组成部分是 `~`，则路径的其余部分被解释为相对于用户主目录的路径。
  例如，对于主目录为 `/home/edolstra` 的用户，`~/foo` 等价于 `/home/edolstra/foo`。
  以 `~` 开头的路径字面量在[纯](@docroot@/command-ref/conf-file.md#conf-pure-eval)求值模式中不允许使用。

  路径字面量除了可以被[插值进其他表达式]之外，本身也可以包含[字符串插值]。

  [字符串插值]: ./string-interpolation.md
  [插值进其他表达式]: ./string-interpolation.md#interpolated-expression

  要使结果被识别为路径，至少要有一个斜杠（`/`）出现在任何插值表达式*之前*。

  `a.${foo}/b.${bar}` 是一个语法上合法的数字除法运算。
  `./a.${foo}/b.${bar}` 则是一个路径。

  [查找路径](./constructs/lookup-path.md)字面量（如 `<nixpkgs>`）同样会解析为路径值。

## 列表 {#list-literal}

列表通过把以空白分隔的一系列值括在方括号中来构成。例如，

```nix
[ 123 ./foo.nix "abc" (f { x = y; }) ]
```

这定义了一个包含四个元素的列表，最后一个元素是调用函数 `f` 的结果。注意，函数调用必须用圆括号括起来。如果省略了圆括号，例如，

```nix
[ 123 ./foo.nix "abc" f { x = y; } ]
```

结果将是一个包含五个元素的列表，第四个元素是一个函数，第五个是一个属性集。

注意，列表只在值上是惰性的，而在长度上是严格的。

列表中的元素可以通过 [`builtins.elemAt`](./builtins.md#builtins-elemAt) 访问。

## 属性集 {#attrs-literal}

属性集是由称为*属性*的“名称-值”对组成的集合。

属性集用花括号（`{ }`）括起来书写。
属性名与属性值之间用等号（`=`）分隔。
每个值可以是任意表达式，并以分号（`;`）结束

属性名是一个不带上下文的字符串，用一个 [name]（[标识符](./identifiers.md#identifiers)或[字符串字面量](string-literals.md)）表示。

[name]: ./identifiers.md#names

> **语法**
>
> *attrset* → `{` { *name* `=` *expr* `;` } `}`

属性可以按任意顺序出现。
每个属性名在同一个属性集中只能出现一次。

> **示例**
>
> 这定义了一个属性集，其属性名为：
> - `x`，值为 `123`，一个整数
> - `text`，值为 `"Hello"`，一个字符串
> - `y`，其值是将函数 `f` 应用于属性集 `{ bla = 456; }` 的结果
>
> ```nix
> {
>   x = 123;
>   text = "Hello";
>   y = f { bla = 456; };
> }
> ```

嵌套属性集中的属性可以用*属性路径*来书写。

> **语法**
>
> *attrset* → `{` { *attrpath* `=` *expr* `;` } `}`

<div id="attrpath-literal"></div>
属性路径是以点分隔的 [name] 列表。

> **语法**
>
> *attrpath* = *name* { `.` *name* }

<!-- -->

> **示例**
>
> ```nix
> { a.b.c = 1; a.b.d = 2; }
> ```
>
>     {
>       a = {
>         b = {
>           c = 1;
>           d = 2;
>         };
>       };
>     }

属性名也可以通过 [`inherit` 关键字](#inheriting-attributes)来隐式设置。

> **示例**
>
> ```nix
> { inherit (builtins) true; }
> ```
>
>     { true = true; }

属性可以通过 [`.` 运算符](./operators.md#attribute-selection)访问。

示例：

```nix
{ a = "Foo"; b = "Bar"; }.a
```

求值为 `"Foo"`。

可以在属性选择中使用 `or` 关键字来提供默认值。

示例：

```nix
{ a = "Foo"; b = "Bar"; }.c or "Xyzzy"
```

```nix
{ a = "Foo"; b = "Bar"; }.c.d.e.f.g or "Xyzzy"
```

由于该属性集中没有 `c` 属性，两者都会求值为 `"Xyzzy"`。

你可以使用任意双引号字符串作为属性名：

```nix
{ "$!@#?" = 123; }."$!@#?"
```

```nix
let bar = "bar"; in
{ "foo ${bar}" = 123; }."foo ${bar}"
```

两者都求值为 `123`。

属性名支持[字符串插值]：

```nix
let bar = "foo"; in
{ foo = 123; }.${bar}
```

```nix
let bar = "foo"; in
{ ${bar} = 123; }.foo
```

两者都求值为 `123`。

在一种特殊情况下，如果属性集声明中的某个属性名求值为 `null`（通常这是一个错误，因为 `null` 不能被强制转换为字符串），那么该属性只是不会被加入属性集：

```nix
{ ${if foo then "bar" else null} = true; }
```

如果 `foo` 求值为 `false`，这会求值为 `{}`。

拥有 [`__functor`]{#attr-__functor} 属性且其值可调用（即它本身是一个函数，或是一个带有可调用 `__functor` 属性值的属性集）的属性集，可以像函数一样被应用，此时属性集本身作为第一个参数传入，例如：

```nix
let add = { __functor = self: x: x + self.x; };
    inc = add // { x = 1; }; # inc 为 { x = 1; __functor = (...) }
in inc 1 # 等价于 `add.__functor add 1`，即 `1 + self.x`
```

求值为 `2`。例如，这可以用来在不要求调用方特殊处理的情况下为函数附加元数据，或者实现某种形式的面向对象编程。

## 递归属性集

递归属性集与普通的[属性集](./types.md#type-attrs)类似，但其属性之间可以相互引用。

> *rec-attrset* = `rec {` [ *name* `=` *expr* `;` `]`... `}`

示例：

```nix
rec {
  x = y;
  y = 123;
}.x
```

求值为 `123`。

注意，如果没有 `rec`，绑定 `x = y;` 将引用外围作用域中的变量 `y`（如果存在），若不存在这样的变量则该表达式无效。也就是说，在普通（非递归）属性集中，属性不会被加入词法作用域；而在递归属性集中会被加入。

递归属性集当然也带来了无限递归的危险。例如，表达式

```nix
rec {
  x = y;
  y = x;
}.x
```

会因 `infinite recursion encountered` 错误消息而崩溃。

## let 表达式

let 表达式允许你为一个表达式定义局部变量。

> *let-in* = `let` [ *identifier* = *expr* `;` ]... `in` *expr*

示例：

```nix
let
  x = "foo";
  y = "bar";
in x + y
```

求值为 `"foobar"`。

let 表达式还有一种更旧的语法，不应在新代码中使用：

> *let* = `let` `{` *identifier* = *expr* `;` [ *identifier* = *expr* `;`]...  `}`

在这种形式中，`{` `}` 之间的属性集是递归的。

其中一个属性必须具有特殊名称 `body`，
它是整个表达式的结果。

示例：

```nix
let {
  foo = bar;
  bar = "baz";
  body = foo;
}
```

求值为 "baz"。

## 继承属性

在定义[属性集](./types.md#type-attrs)或 [let 表达式](#let-expressions)时，从外围词法作用域复制变量往往很方便（例如，当你想传递属性时）。
这可以用 `inherit` 关键字来简写。

示例：

```nix
let x = 123; in
{
  inherit x;
  y = 456;
}
```

等价于

```nix
let x = 123; in
{
  x = x;
  y = 456;
}
```

两者都求值为 `{ x = 123; y = 456; }`。

> **注意**
>
> 这之所以有效，是因为 `x` 由 `let` 结构加入了词法作用域。

也可以从另一个属性集继承属性。

示例：

在来自 `all-packages.nix` 的下面这个片段中，

```nix
graphviz = (import ../tools/graphics/graphviz) {
  inherit fetchurl stdenv libpng libjpeg expat x11 yacc;
  inherit (xorg) libXaw;
};

xorg = {
  libX11 = ...;
  libXaw = ...;
  ...
}

libpng = ...;
libjpg = ...;
...
```

用于调用 `../tools/graphics/graphviz` 中定义的函数的那个属性集，从外围作用域继承了许多变量（`fetchurl` … `yacc`），同时还从 `xorg` 属性集继承了 `libXaw`（X Athena Widgets）。

概括一下，片段

```nix
...
inherit x y z;
inherit (src-set) a b c;
...
```

等价于

```nix
...
x = x; y = y; z = z;
a = src-set.a; b = src-set.b; c = src-set.c;
...
```

适用于在 let 表达式中定义局部变量或定义属性集的场合。

在 `let` 表达式中，`inherit` 可用于选择性地把某个属性集的特定属性引入作用域。例如


```nix
let
  x = { a = 1; b = 2; };
  inherit (builtins) attrNames;
in
{
  names = attrNames x;
}
```

等价于

```nix
let
  x = { a = 1; b = 2; };
in
{
  names = builtins.attrNames x;
}
```

两者都求值为 `{ names = [ "a" "b" ]; }`。

## 函数

函数具有如下形式：

```nix
pattern: body
```

模式（pattern）规定了函数的参数必须是什么样子，
并把函数体中的变量绑定到参数（的各个部分）。共有三种模式：

  - 如果模式是单个标识符，则该函数匹配任意参数。示例：

    ```nix
    let negate = x: !x;
        concat = x: y: x + y;
    in if negate true then concat "foo" "bar" else ""
    ```

    注意，`concat` 是一个接受一个参数并返回另一个接受一个参数的函数的函数。这允许部分参数化（即只填写函数的一部分参数）；例如，

    ```nix
    map (concat "foo") [ "bar" "bla" "abc" ]
    ```

    求值为 `[ "foobar" "foobla" "fooabc" ]`。

  - 形如 `{ name1, name2, …, nameN }` 的*属性集模式*匹配包含所列属性的属性集，
    并把这些属性的值绑定到函数体中的变量。例如，函数

    ```nix
    { x, y, z }: z + y + x
    ```

    只能用恰好包含属性 `x`、`y` 和 `z` 的属性集来调用，不允许有其他属性。如果想允许额外的参数，可以使用省略号（`...`）：

    ```nix
    { x, y, z, ... }: z + y + x
    ```

    这适用于任何至少包含这三个指定属性的属性集。

  - 可以为属性提供*默认值*，此时这些属性允许缺失。
    默认值通过 `name ?  e` 来指定，其中 *e* 是任意表达式。例如，

    ```nix
    { x, y ? "foo", z ? "bar" }: z + y + x
    ```

    指定了一个只要求名为 `x` 的属性、但可选地接受 `y` 和 `z` 的函数。

  - `@` 模式提供了一种引用被匹配的整个值的手段：

    ```nix
    args@{ x, y, z, ... }: z + y + x + args.a
    ```

    但也可以写作：

    ```nix
    { x, y, z, ... } @ args: z + y + x + args.a
    ```

    这里 `args` 绑定到*按原样传入*的参数，然后再与模式 `{ x, y, z, ... }` 进行匹配。
    `@` 模式主要在与省略号（`...`）一起使用时才有意义，
    因为这样可以通过 `args.a` 访问作为额外属性传给函数的属性名 `a`。

    > **警告**
    >
    > `args@` 把名字 `args` 绑定到传给函数的那个属性集。
    > 特别要注意，`args` *不*包含函数属性集模式中用 `?` 指定的任何默认值。
    >
    > 例如
    >
    > ```nix
    > let
    >   f = args@{ a ? 23, ... }: [ a args ];
    > in
    >   f {}
    > ```
    >
    > 等价于
    >
    > ```nix
    > let
    >   f = args @ { ... }: [ (args.a or 23) args ];
    > in
    >   f {}
    > ```
    >
    > 并且两个表达式都会求值为：
    >
    > ```nix
    > [ 23 {} ]
    > ```

  - 函数引入的所有绑定在整个函数表达式中都处于作用域内，而不仅在函数体中。
    因此它们可以用于默认值。

    > **示例**
    >
    > 某个参数（`x`）被用在另一个参数（`y`）的默认值中：
    >
    > ```nix
    > let
    >   f = { x, y ? [x] }: { inherit y; };
    > in
    >   f { x = 3; }
    > ```
    >
    > 求值为：
    >
    > ```nix
    > {
    >   y = [ 3 ];
    > }
    > ```

    > **示例**
    >
    > `@` 模式的绑定 `args` 被用在参数 `x` 的默认值中：
    >
    > ```nix
    > let
    >   f = args@{ x ? args.a, ... }: x;
    > in
    >   f { a = 1; }
    > ```
    >
    > 求值为：
    >
    > ```nix
    > 1
    > ```

注意，函数没有名字。如果想给函数起名字，可以把它绑定到一个属性，例如：

```nix
let concat = { x, y }: x + y;
in concat { x = "foo"; y = "bar"; }
```

## 条件表达式

条件表达式形如：

```nix
if e1 then e2 else e3
```

其中 *e1* 是一个应当求值为布尔值（`true` 或 `false`）的表达式。

## 断言

断言通常用于检查特性与依赖之间是否满足某些要求。它们形如：

```nix
assert e1; e2
```

其中 *e1* 是一个应当求值为布尔值的表达式。如果求值为 `true`，则返回 *e2*；否则表达式求值中止并打印回溯信息。

下面是 Subversion 软件包的一个 Nix 表达式，展示了断言的用法：。

```nix
{ localServer ? false
, httpServer ? false
, sslSupport ? false
, pythonBindings ? false
, javaSwigBindings ? false
, javahlBindings ? false
, stdenv, fetchurl
, openssl ? null, httpd ? null, db4 ? null, expat, swig ? null, j2sdk ? null
}:

assert localServer -> db4 != null; ①
assert httpServer -> httpd != null && httpd.expat == expat; ②
assert sslSupport -> openssl != null && (httpServer -> httpd.openssl == openssl); ③
assert pythonBindings -> swig != null && swig.pythonSupport;
assert javaSwigBindings -> swig != null && swig.javaSupport;
assert javahlBindings -> j2sdk != null;

stdenv.mkDerivation {
  name = "subversion-1.1.1";
  ...
  openssl = if sslSupport then openssl else null; ④
  ...
}
```

值得注意的点有：

1.  这条断言规定，如果 Subversion 要支持本地仓库，就需要 Berkeley DB。因此，如果调用 Subversion 函数时把 `localServer` 参数设为 `true` 而 `db4` 参数设为 `null`，则求值失败。

    注意，`->` 是[逻辑蕴涵](https://en.wikipedia.org/wiki/Truth_table#Logical_implication)布尔运算。

2.  这是一个更微妙的条件：如果 Subversion 构建时带 Apache（`httpServer`）支持，那么 Subversion 使用的 Expat 库（一个 XML 库）应当与 Apache 使用的相同。这是因为在这种配置下，Subversion 的代码最终会与 Apache 的代码链接在一起；如果 Expat 库不匹配，可能会出现构建期或运行期的链接错误或不兼容。

3.  这条断言规定，Subversion 要支持 SSL（以便访问 `https` URL），就必须传入一个 OpenSSL 库。此外还规定，*如果*启用了 Apache 支持，那么 Apache 的 OpenSSL 应与 Subversion 的一致。（注意，如果未启用 Apache 支持，我们并不关心 Apache 的 OpenSSL。）

4.  这里的条件表达式其实与断言关系不大，但值得指出：它确保当 SSL 支持被禁用时，即使传入了一个非 `null` 的值，Subversion 的 derivation（派生）也不依赖于 OpenSSL。这避免了 OpenSSL 变化时对 Subversion 的不必要重建。

## with 表达式

*with 表达式*，

```nix
with e1; e2
```

把属性集 *e1* 引入表达式 *e2* 的词法作用域。
例如，

```nix
let as = { x = "foo"; y = "bar"; };
in with as; x + y
```

求值为 `"foobar"`，因为 `with` 把 `as` 的 `x` 和 `y` 属性加进了表达式 `x + y` 的词法作用域。`with` 最常见的用法是与 `import` 函数配合使用。例如，

```nix
with (import ./definitions.nix); ...
```

这使得文件 `definitions.nix` 中定义的所有属性都可用，就像它们是在 `let` 表达式中局部定义的一样。

`with` 引入的绑定不会遮蔽（shadow）通过其他方式引入的绑定，例如：

```nix
let a = 3; in with { a = 1; }; let a = 4; in with { a = 2; }; ...
```

建立的作用域与

```nix
let a = 1; in let a = 2; in let a = 3; in let a = 4; in ...
```

相同。

来自外层 `with` 表达式的变量*会*被遮蔽：

```nix
with { a = "outer"; };
with { a = "inner"; };
a
```

确实会求值为 `"inner"`。

## 注释

- 行内注释以 `#` 开头，一直延续到行尾。

  > **示例**
  >
  > ```nix
  > # 一个数字
  > 2 # 等于 1 + 1
  > ```
  >
  > ```console
  > 2
  > ```

- 块注释以 `/*` 开头，一直延续到下一个 `*/` 出现为止。

  > **示例**
  >
  > ```nix
  > /*
  > Block comments
  > can span multiple lines.
  > */ "hello"
  > ```
  >
  > ```console
  > "hello"
  > ```

  这意味着块注释不能嵌套。

  > **示例**
  >
  > ```nix
  > /* /* nope */ */ 1
  > ```
  >
  > ```console
  > error: syntax error, unexpected '*'
  >
  >        at «string»:1:15:
  >
  >             1| /* /* nope */ *
  >              |               ^
  > ```

  可以考虑对嵌套注释进行转义，并在后处理时再反转义。

  > **示例**
  >
  > ```nix
  > /* /* nested *\/ */ 1
  > ```
  >
  > ```console
  > 1
  > ```
