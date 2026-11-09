# 字符串字面量

*字符串字面量（string literal）*表示一个[字符串](types.md#type-string)值。

> **语法**
>
> *expression* → *string*
>
> *string* → `"` ( *string_char*\* [*interpolation_element*][string interpolation] )* *string_char*\* `"`
>
> *string* → `''` ( *indented_string_char*\* [*interpolation_element*][string interpolation] )* *indented_string_char*\* `''`
>
> *string* → *uri*
>
> *string_char* ~ `[^"$\\]|\$(?!\{)|\\.`
>
> *indented_string_char* ~ `[^$']|\$\$|\$(?!\{)|''[$']|''\\.|'(?!')`
>
> *uri* ~ `[A-Za-z][+\-.0-9A-Za-z]*:[!$%&'*+,\-./0-9:=?@A-Z_a-z~]+`

字符串有三种写法。

最常见的方式是用双引号把字符串括起来，例如 `"foo bar"`。
字符串可以跨多行。
其他表达式的结果可以通过把它们括在 `${ }` 中而包含进字符串，这一特性称为[字符串插值]。

[string interpolation]: ./string-interpolation.md

以下字符必须通过在前面加反斜杠（`\`）转义才能在字符串中表示：

- 双引号（`"`）

> **示例**
>
> ```nix
> "\""
> ```
>
>     "\""

- 反斜杠（`\`）

> **示例**
>
> ```nix
> "\\"
> ```
>
>     "\\"

- 美元符号后跟一个左花括号（`${`）——即 "dollar-curly"

> **示例**
>
> ```nix
> "\${"
> ```
>
>     "\${"

换行符、回车符和制表符可以分别写作 `\n`、`\r` 和 `\t`。

"双美元花括号"（`$${`）可以直接按字面书写。

> **示例**
>
> ```nix
> "$${"
> ```
>
>     "$\${"

字符串值输出到终端时会使用 Nix 特有的转义方式。
写入文件的字符串将包含转义所编码的字符。

书写字符串字面量的第二种方式是*缩进字符串（indented string）*，它由成对的*双单引号*（`''`）括起来，如下所示：

```nix
''
This is the first line.
This is the second line.
  This is the third line.
''
```

这种字符串字面量会智能地剥离每行开头的缩进。
准确地说，它会从每一行中剥离与整个字符串的最小缩进量相等的空格数（空行的缩进不计入）。
例如，第一行和第二行缩进了两个空格，而第三行缩进了四个空格。
因此，每行都会被剥离两个空格，得到的字符串是

```nix
"This is the first line.\nThis is the second line.\n  This is the third line.\n"
```

> **注意**
>
> 如果起始的 `''` 所在行没有非空白文本，那么 `''` 之后的空白和换行符会被忽略。

> **警告**
>
> 作为前缀的制表符不会被剥离。
>
> > **示例**
> >
> > 下面的缩进字符串以制表符作为前缀：
> >
> > <pre><code class="nohighlight">''
> > 	all:
> > 		@echo hello
> > ''
> > </code></pre>
> >
> >     "\tall:\n\t\t@echo hello\n"

缩进字符串支持[字符串插值]。

以下内容必须转义才能在缩进字符串中表示：

- `$` 通过在前面加两个单引号（`''`）来转义

> **示例**
>
> ```nix
> ''
>   ''$
> ''
> ```
>
>     "$\n"

- `''` 通过在前面加一个单引号（`'`）来转义

> **示例**
>
> ```nix
> ''
>   '''
> ''
> ```
>
>     "''\n"

这些特殊字符按如下方式转义：
- 换行符（`\n`）：`''\n`
- 回车符（`\r`）：`''\r`
- 制表符（`\t`）：`''\t`

`''\` 可以转义任何其他字符。

"dollar-curly"（`${`）可以按如下方式书写：
> **示例**
>
> ```nix
> ''
>   echo ''${PATH}
> ''
> ```
>
>     "echo ${PATH}\n"

> **注意**
>
> 这与在双引号字符串中转义 dollar-curly 的语法（`"\${"`）不同。请留意当前需要的是哪一种。

"双美元花括号"（`$${`）可以直接按字面书写。

> **示例**
>
> ```nix
> ''
>   $${
> ''
> ```
>
>     "$\${\n"

缩进字符串的主要用处在于：它允许多行字符串字面量遵循其外围 Nix 表达式的缩进；而且对于表示 shell 脚本、配置文件等语言的字符串来说，通常需要更少的转义，因为 `''` 远比 `"` 少见。
示例：

```nix
stdenv.mkDerivation {
...
postInstall =
  ''
    mkdir $out/bin $out/etc
    cp foo $out/bin
    echo "Hello World" > $out/etc/foo.conf
    ${if enableBar then "cp bar $out/bin" else ""}
  '';
...
}
```

最后，作为一种便利，[RFC 2396](http://www.ietf.org/rfc/rfc2396.txt) 附录 B 中定义的 *URI* 可以*原样*书写，无需加引号。
例如，字符串 `"http://example.org/foo.tar.bz2"` 也可以写作
`http://example.org/foo.tar.bz2`。
