# Nix 语言

Nix 语言专为便捷地创建和组合 [derivation（派生）](@docroot@/glossary.md#gloss-derivation) 而设计——derivation（派生）是对如何利用现有文件内容来生成新文件的精确描述。

> **注意**
>
> 这些页面是按参考手册的形式编写的。
> 如果你正在学习 Nix，nix.dev 上有一份很好的 [Nix 语言入门](https://nix.dev/tutorials/nix-language)。

这门语言的特点是：

- *领域专用*

  Nix 语言是为处理文本文件而专门构建的。
  它最具代表性的特性有：

  - [文件系统路径原语](@docroot@/language/types.md#type-path)，用于访问源文件
  - [缩进字符串](@docroot@/language/string-literals.md)与[字符串插值](@docroot@/language/string-interpolation.md)，用于创建文件内容
  - [带上下文的字符串](@docroot@/language/string-context.md)，用于透明地关联文件

  它内置了[内建函数](@docroot@/language/builtins.md)，可与 Nix store（Nix 存储库）(@docroot@/store/index.md) 集成；Nix store 负责管理文件，并支持实现（realise）在 Nix 语言中声明的 derivation（派生）。

- *声明式*

  没有顺序执行步骤的概念。
  操作之间的依赖关系仅通过数据来建立。

- *纯函数式*

  值在计算过程中不会改变。
  只要输入不变，函数总是产生相同的输出。

- *函数式*

  函数与其他值并无二致。
  函数可以被赋给名字、作为参数传递，或由函数返回。

- *惰性*

  值只在需要时才会被计算。

- *动态类型*

  类型错误只会在表达式求值时才被检测出来。

# 概览

以下通过示例对语言特性做一个并不完整的概览。

<table>
 <tr>
  <th>
   示例
  </th>
  <th>
   描述
  </th>
 </tr>
 <tr>
  <td>


   *基本值（[原语](@docroot@/language/types.md#primitives)）*


  </td>
  <td>



  </td>
 </tr>
 <tr>
  <td>

   `"hello world"`

  </td>
  <td>

   一个[字符串](@docroot@/language/types.md#type-string)

  </td>
 </tr>
 <tr>
  <td>

   ```
   ''
     multi
      line
       string
   ''
   ```

  </td>
  <td>

   <!-- FIXME: using two no-break spaces, because apparently mdBook swallows the second regular space! -->
   一个多行字符串。会去除公共的前导空白。求值结果为 `"multi\n line\n  string"`。

  </td>
 </tr>
 <tr>
  <td>

   `# Explanation`

  </td>
  <td>

   一条[注释](@docroot@/language/syntax.md#comments)。

  </td>
 </tr>
 <tr>
  <td>

   `"hello ${ { a = "world"; }.a }"`

   `"1 2 ${toString 3}"`

   `"${pkgs.bash}/bin/sh"`

  </td>
  <td>

   [字符串插值](@docroot@/language/string-interpolation.md)（展开为 `"hello world"`、`"1 2 3"`、`"/nix/store/<hash>-bash-<version>/bin/sh"`）

  </td>
 </tr>
 <tr>
  <td>

   `true`, `false`

  </td>
  <td>

   [布尔值](@docroot@/language/types.md#type-bool)

  </td>
 </tr>
 <tr>
  <td>

   `null`

  </td>
  <td>

   [空值](@docroot@/language/types.md#type-null)

  </td>
 </tr>
 <tr>
  <td>

   `123`

  </td>
  <td>

   一个[整数](@docroot@/language/types.md#type-int)

  </td>
 </tr>
 <tr>
  <td>

   `3.141`

  </td>
  <td>

   一个[浮点数](@docroot@/language/types.md#type-float)

  </td>
 </tr>
 <tr>
  <td>

   `/etc`

  </td>
  <td>

   一个绝对[路径](@docroot@/language/types.md#type-path)

  </td>
 </tr>
 <tr>
  <td>

   `./foo.png`

  </td>
  <td>

   一个相对于包含此 Nix 表达式的文件的[路径](@docroot@/language/types.md#type-path)

  </td>
 </tr>
 <tr>
  <td>

   `~/.config`

  </td>
  <td>

   一个主目录[路径](@docroot@/language/types.md#type-path)。求值结果为 `"<user's home directory>/.config"`。

  </td>
 </tr>
 <tr>
  <td>

   `<nixpkgs>`

  </td>
  <td>

   一个用于查找 Nix 文件的[查找路径](@docroot@/language/constructs/lookup-path.md)。其值由 [`$NIX_PATH` 环境变量](../command-ref/env-common.md#env-NIX_PATH)决定。

  </td>
 </tr>
 <tr>
  <td>

   *复合值*

  </td>
  <td>



  </td>
 </tr>
 <tr>
  <td>

   `{ x = 1; y = 2; }`

  </td>
  <td>

   一个[属性集](@docroot@/language/types.md#type-attrs)，包含名为 `x` 和 `y` 的属性

  </td>
 </tr>
 <tr>
  <td>

   `{ foo.bar = 1; }`

  </td>
  <td>

   一个嵌套属性集，等价于 `{ foo = { bar = 1; }; }`

  </td>
 </tr>
 <tr>
  <td>

   `rec { x = "foo"; y = x + "bar"; }`

  </td>
  <td>

   一个[递归属性集](@docroot@/language/syntax.md#recursive-sets)，等价于 `{ x = "foo"; y = "foobar"; }`。

  </td>
 </tr>
 <tr>
  <td>

   `[ "foo" "bar" "baz" ]`

   `[ 1 2 3 ]`

   `[ (f 1) { a = 1; b = 2; } [ "c" ] ]`

  </td>
  <td>

   包含三个元素的[列表](@docroot@/language/types.md#type-list)。

  </td>
 </tr>
 <tr>
  <td>

   *运算符*

  </td>
  <td>



  </td>
 </tr>
 <tr>
  <td>

   `"foo" + "bar"`

  </td>
  <td>

   字符串拼接

  </td>
 </tr>
 <tr>
  <td>

   `1 + 2`

  </td>
  <td>

   整数相加

  </td>
 </tr>
 <tr>
  <td>

   `"foo" == "f" + "oo"`

  </td>
  <td>

   相等性判断（求值结果为 `true`）

  </td>
 </tr>
 <tr>
  <td>

   `"foo" != "bar"`

  </td>
  <td>

   不等性判断（求值结果为 `true`）

  </td>
 </tr>
 <tr>
  <td>

   `!true`

  </td>
  <td>

   布尔取反

  </td>
 </tr>
 <tr>
  <td>

   `{ x = 1; y = 2; }.x`

  </td>
  <td>

   [属性选择](@docroot@/language/types.md#type-attrs)（求值结果为 `1`）

  </td>
 </tr>
 <tr>
  <td>

   `{ x = 1; y = 2; }.z or 3`

  </td>
  <td>

   带默认值的[属性选择](@docroot@/language/types.md#type-attrs)（求值结果为 `3`）

  </td>
 </tr>
 <tr>
  <td>

   `{ x = 1; y = 2; } // { z = 3; }`

  </td>
  <td>

   合并两个属性集（右侧属性集的属性优先）

  </td>
 </tr>
 <tr>
  <td>

   *控制结构*

  </td>
  <td>



  </td>
 </tr>
 <tr>
  <td>

   `if 1 + 1 == 2 then "yes!" else "no!"`

  </td>
  <td>

   [条件表达式](@docroot@/language/syntax.md#conditionals)。

  </td>
 </tr>
 <tr>
  <td>

   `assert 1 + 1 == 2; "yes!"`

  </td>
  <td>

   [断言](@docroot@/language/syntax.md#assertions)检查（求值结果为 `"yes!"`）。

  </td>
 </tr>
 <tr>
  <td>

   `let x = "foo"; y = "bar"; in x + y`

  </td>
  <td>

   变量定义。参见 [`let` 表达式](@docroot@/language/syntax.md#let-expressions)。

  </td>
 </tr>
 <tr>
  <td>

   `with builtins; head [ 1 2 3 ]`

  </td>
  <td>

   将给定属性集中的所有属性加入作用域（求值结果为 `1`）。

   详情及变量遮蔽的注意事项请参见 [`with` 表达式](@docroot@/language/syntax.md#with-expressions)。

  </td>
 </tr>
 <tr>
  <td>

   `inherit pkgs src;`

  </td>
  <td>

   将变量加入当前作用域（属性集或 `let` 绑定）。
   脱糖（desugar）后为 `pkgs = pkgs; src = src;`。
   参见[属性继承](@docroot@/language/syntax.md#inheriting-attributes)。

  </td>
 </tr>
 <tr>
  <td>

   `inherit (pkgs) lib stdenv;`

  </td>
  <td>

   将括号中属性集里的属性加入当前作用域（属性集或 `let` 绑定）。
   脱糖后为 `lib = pkgs.lib; stdenv = pkgs.stdenv;`。
   参见[属性继承](@docroot@/language/syntax.md#inheriting-attributes)。

  </td>
 </tr>
 <tr>
  <td>

   *[函数](@docroot@/language/syntax.md#functions)（lambda）*

  </td>
  <td>



  </td>
 </tr>
 <tr>
  <td>

   `x: x + 1`

  </td>
  <td>

   一个[函数](@docroot@/language/syntax.md#functions)，接受一个整数并返回其加 1 的结果。

  </td>
 </tr>
 <tr>
  <td>

   `x: y: x + y`

  </td>
  <td>

   柯里化的[函数](@docroot@/language/syntax.md#functions)，等价于 `x: (y: x + y)`。可以像接受两个参数并返回其和的函数那样使用。

  </td>
 </tr>
 <tr>
  <td>

   `(x: x + 1) 100`

  </td>
  <td>

   一次[函数](@docroot@/language/syntax.md#functions)调用（求值结果为 101）

  </td>
 </tr>
 <tr>
  <td>

   `let inc = x: x + 1; in inc (inc (inc 100))`

  </td>
  <td>

   将一个[函数](@docroot@/language/syntax.md#functions)绑定到变量，随后按名字调用（求值结果为 103）

  </td>
 </tr>
 <tr>
  <td>

   `{ x, y }: x + y`

  </td>
  <td>

   一个[函数](@docroot@/language/syntax.md#functions)，接受一个含有必需属性 `x` 和 `y` 的属性集，并将它们拼接起来

  </td>
 </tr>
 <tr>
  <td>

   `{ x, y ? "bar" }: x + y`

  </td>
  <td>

   一个[函数](@docroot@/language/syntax.md#functions)，接受一个含有必需属性 `x` 和可选属性 `y` 的属性集，`y` 的默认值为 `"bar"`

  </td>
 </tr>
 <tr>
  <td>

   `{ x, y, ... }: x + y`

  </td>
  <td>

   一个[函数](@docroot@/language/syntax.md#functions)，接受一个含有必需属性 `x` 和 `y` 的属性集，并忽略其他任何属性

  </td>
 </tr>
 <tr>
  <td>

   `{ x, y } @ args: x + y`

   `args @ { x, y }: x + y`

  </td>
  <td>

   一个[函数](@docroot@/language/syntax.md#functions)，接受一个含有必需属性 `x` 和 `y` 的属性集，并将整个属性集绑定到 `args`

  </td>
 </tr>
 <tr>
  <td>

   *内建函数*

  </td>
  <td>



  </td>
 </tr>
 <tr>
  <td>

   `import ./foo.nix`

  </td>
  <td>

   加载并返回给定文件中的 Nix 表达式。
   参见 [import](@docroot@/language/builtins.md#builtins-import)。

  </td>
 </tr>
 <tr>
  <td>

   `map (x: x + x) [ 1 2 3 ]`

  </td>
  <td>

   对列表的每个元素应用一个函数（求值结果为 `[ 2 4 6 ]`）。
   参见 [`map`](@docroot@/language/builtins.md#builtins-map)。

  </td>
 </tr>
</table>
