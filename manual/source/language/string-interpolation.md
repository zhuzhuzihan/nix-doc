# 字符串插值

字符串插值（string interpolation）是一项语言特性：[字符串]、[路径]或[属性名][attribute set]中可以包含以 `${ }`（美元符号加花括号）括起来的表达式。

这样的结构称为*插值字符串（interpolated string）*，其中的表达式称为[插值表达式](#interpolated-expression)。

[string]: ./types.md#type-string
[path]: ./types.md#type-path
[attribute set]: ./types.md#type-attrs

> **语法**
>
> *interpolation_element* → `${` *expression* `}`

## 示例

### 字符串

与其写

```nix
"--with-freetype2-library=" + freetype + "/lib"
```

（其中 `freetype` 是一个 [derivation 表达式]），你可以改为写

[derivation expression]: @docroot@/glossary.md#gloss-derivation-expression

```nix
"--with-freetype2-library=${freetype}/lib"
```

后者会被自动转换成前者。

一个更复杂的例子（来自 [Qt](http://www.trolltech.com/products/qt) 的 Nix 表达式）：

```nix
configureFlags = "
  -system-zlib -system-libpng -system-libjpeg
  ${if openglSupport then "-dlopen-opengl
    -L${mesa}/lib -I${mesa}/include
    -L${libXmu}/lib -I${libXmu}/include" else ""}
  ${if threadSupport then "-thread" else "-no-thread"}
";
```

注意，Nix 表达式和字符串可以任意嵌套；
在这个例子中，外层字符串包含多个插值表达式，这些插值表达式本身又包含字符串（例如 `"-thread"`），其中一些字符串又包含插值表达式（例如 `${mesa}`）。

要在普通字符串中书写字面的 `${`，请用反斜杠（`\`）转义它。

> **示例**
>
> ```nix
> "echo \${PATH}"
> ```
>
>     "echo ${PATH}"

要在缩进字符串中书写字面的 `${`，请用两个单引号（`''`）转义它。

> **示例**
>
> ```nix
> ''
>   echo ''${PATH}
> ''
> ```
>
>     "echo ${PATH}\n"

`$${` 可以在任何字符串中按字面书写。

> **示例**
>
> 在 Make 中，文件名或配方（recipe）中的 `$` 表示为 `$$`，参见 [GNU `make`：变量引用的基础](https://www.gnu.org/software/make/manual/html_node/Reference.html#Basics-of-Variable-References)。
> 这可以直接在 Nix 语言的字符串中表达：
>
> ```nix
> ''
>   MAKEVAR = Hello
>   all:
>   	@export BASHVAR=world; echo $(MAKEVAR) $${BASHVAR}
> ''
> ```
>
>     "MAKEVAR = Hello\nall:\n\t@export BASHVAR=world; echo $(MAKEVAR) $\${BASHVAR}\n"

详情参见[字符串文档][string]。

### 路径

与其写

```nix
./. + "/" + foo + "-" + bar + ".nix"
```

或

```nix
./. + "/${foo}-${bar}.nix"
```

你可以改为写

```nix
./${foo}-${bar}.nix
```

### 属性名

<!--
FIXME: these examples are redundant with the main page on attribute sets.
figure out what to do about that
-->

属性名可以是插值字符串。

> **示例**
>
> ```nix
> let name = "foo"; in
> { ${name} = 123; }
> ```
>
>     { foo = 123; }

属性可以用插值字符串来选择。

> **示例**
>
> ```nix
> let name = "foo"; in
> { foo = 123; }.${name}
> ```
>
>     123

# 插值表达式

被插值的表达式必须求值为以下之一：

- 一个[字符串]
- 一个[路径]
- 一个带有 `__toString` 属性或 `outPath` 属性的[属性集]

  - `__toString` 必须是一个函数，它接受属性集本身并返回一个字符串
  - `outPath` 必须是一个字符串

  这包括 [derivation 表达式](./derivations.md)和 [flake 输入](@docroot@/command-ref/new-cli/nix3-flake.md#flake-inputs)（实验性）。

字符串插值为它自身。

插值表达式中的路径会先被复制进 Nix store，所得的字符串就是新建的 [store object](@docroot@/store/store-object.md) 的[存储路径]。

[store path]: @docroot@/store/store-path.md

> **示例**
>
> ```console
> $ mkdir foo
> ```
>
> 在插值表达式中引用这个空目录：
>
> ```nix
> "${./foo}"
> ```
>
>     "/nix/store/2hhl2nz5v0khbn06ys82nrk99aa1xxdw-foo"

derivation 插值为它的第一个[输出](./derivations.md#attr-outputs)的[存储路径]。

> **示例**
>
> ```nix
> let
>   pkgs = import <nixpkgs> {};
> in
> "${pkgs.hello}"
> ```
>
>     "/nix/store/qnlr7906z0mrl2syrkdbpicffq02nw07-hello-2.12.1"

属性集插值为其中 `__toString` 函数作用于属性集本身的返回值。

> **示例**
>
> ```nix
> let
>   a = {
>     value = 1;
>     __toString = self: toString (self.value + 1);
>   };
> in
> "${a}"
> ```
>
>     "2"

属性集也可以插值为它的 `outPath` 属性的值。

> **示例**
>
> ```nix
> let
>   a = { outPath = "foo"; };
> in
> "${a}"
> ```
>
>     "foo"

如果属性集中同时存在 `__toString` 和 `outPath`，则 `__toString` 优先。

> **示例**
>
> ```nix
> let
>   a = { __toString = _: "yes"; outPath = throw "no"; };
> in
> "${a}"
> ```
>
>     "yes"

如果两者都不存在，则会抛出错误。

> **示例**
>
> ```nix
> let
>   a = {};
> in
> "${a}"
> ```
>
>     error: cannot coerce a set to a string: { }
>
>            at «string»:4:2:
>
>                 3| in
>                 4| "${a}"
>                  |  ^
