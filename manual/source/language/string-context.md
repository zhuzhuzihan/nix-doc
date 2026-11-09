# 字符串上下文

> **注意**
>
> 这是一个进阶主题。
> Nix 语言的设计使得程序员无需有意识地处理字符串上下文，甚至无需知道它们的存在。

Nix 语言中的字符串并不像其他语言中的字符串那样只是一个字符序列。
它实际上是一个由字符序列和*字符串上下文（string context）*组成的二元组。
字符串上下文是一个（无序的）*字符串上下文元素（string context element）*的集合。

字符串上下文的用途是收集通过
[字符串拼接](./operators.md#string-concatenation)、
[字符串插值](./string-interpolation.md)
等类似操作附加到字符串上的非字符串值。
其设计思想是：用户在通过 Nix 表达式创建文本文件时可以引用其他文件，而不必手动跟踪确切的路径。
Nix 会确保所有被引用的文件都是可访问的——即所有[存储路径](@docroot@/glossary.md#gloss-store-path)都是[有效的](@docroot@/glossary.md#gloss-validity)。

> **注意**
>
> 在符合惯用法的 Nix 语言代码中，字符串上下文是*不会*被显式操作的。

字符串上下文元素有几种不同的形式：

- [派生路径（deriving path）]{#string-context-element-derived-path}

  这种类型的字符串上下文元素是一个[派生路径](@docroot@/glossary.md#gloss-deriving-path)。
  它可以是[常量（constant）](#string-context-constant)类型或[输出（output）](#string-context-output)类型，与派生路径的类型相对应。

  - [常量字符串上下文元素]{#string-context-constant}

    > **示例**
    >
    > [`builtins.storePath`] 会创建一个带有单个常量字符串上下文元素的字符串：
    >
    > ```nix
    > builtins.getContext (builtins.storePath "/nix/store/ikwkxz4wwlp2g1428n7dy729cg1d9hin-hello-2.10")
    > ```
    > 求值结果为
    > ```nix
    > {
    >   "/nix/store/ikwkxz4wwlp2g1428n7dy729cg1d9hin-hello-2.10" = {
    >     path = true;
    >   };
    > }
    > ```

    [deriving path]: @docroot@/glossary.md#gloss-deriving-path
    [store path]: @docroot@/glossary.md#gloss-store-path
    [`builtins.storePath`]: ./builtins.md#builtins-storePath

  - [输出字符串上下文元素]{#string-context-output}

    > **示例**
    >
    > 字符串上下文的行为最好用一个仍是实验性的内置函数 [`builtins.outputOf`] 来演示。
    > 这个示例在稳定版 Nix 中*无法*运行！
    >
    > ```nix
    > builtins.getContext
    >   (builtins.outputOf
    >     (builtins.storePath "/nix/store/fvchh9cvcr7kdla6n860hshchsba305w-hello-2.12.drv")
    >     "out")
    > ```
    > 求值结果为
    > ```nix
    > {
    >   "/nix/store/fvchh9cvcr7kdla6n860hshchsba305w-hello-2.12.drv" = {
    >     outputs = [ "out" ];
    >   };
    > }
    > ```

    [`builtins.outputOf`]: ./builtins.md#builtins-outputOf

- [*derivation deep*]{#string-context-element-derivation-deep}

  *derivation deep* 是一个进阶特性，旨在与
  [`exportReferencesGraph` derivation 属性](./advanced-attributes.html#adv-attr-exportReferencesGraph)配合使用。
  *derivation deep* 字符串上下文元素是一个 derivation 路径，它同时指向该 derivation 的输出和该 derivation 的整个构建闭包：
  即它的所有输出、该 derivation 所依赖的所有其他 derivation，以及这些 derivation 的所有输出。

  > **示例**
  >
  > 说明 *derivation deep* 字符串上下文的最佳方式是使用 [`builtins.addDrvOutputDependencies`]。
  > 取一个指向某个 derivation 的普通常量字符串上下文元素，并把它转换为一个 "Derivation deep" 字符串上下文元素。
  >
  > ```nix
  > builtins.getContext
  >   (builtins.addDrvOutputDependencies
  >     (builtins.storePath "/nix/store/fvchh9cvcr7kdla6n860hshchsba305w-hello-2.12.drv"))
  > ```
  > 求值结果为
  > ```nix
  > {
  >   "/nix/store/fvchh9cvcr7kdla6n860hshchsba305w-hello-2.12.drv" = {
  >     allOutputs = true;
  >   };
  > }
  > ```

  [`builtins.addDrvOutputDependencies`]: ./builtins.md#builtins-addDrvOutputDependencies
  [`builtins.unsafeDiscardOutputDependency`]: ./builtins.md#builtins-unsafeDiscardOutputDependency

## 检查字符串上下文

最基本的，[`builtins.hasContext`] 可以判断一个字符串是否带有非空的上下文。

当需要更细粒度的信息时，可以使用 [`builtins.getContext`]。
它会创建一个表示字符串上下文的[属性集]，可以像平常一样对其进行检查。

[`builtins.hasContext`]: ./builtins.md#builtins-hasContext
[`builtins.getContext`]: ./builtins.md#builtins-getContext
[attribute set]: ./types.md#type-attrs

## 清除字符串上下文

[`builtins.unsafeDiscardStringContext`](./builtins.md#builtins-unsafeDiscardStringContext) 会创建一个字符串的副本，但带有一个空的字符串上下文。
返回的字符串可以用在更多的场景中，例如某些要求字符串上下文为空的运算符。
在这些用例中要求显式丢弃字符串上下文，有助于确保字符串上下文元素不会因疏忽而丢失。
"unsafe" 标记只是为了提醒：Nix 通常保证依赖会被跟踪，而返回的字符串已经丢失了这些依赖。

## 构造字符串上下文

[`builtins.appendContext`] 会创建一个字符串的副本，但带有额外的字符串上下文元素。
上下文由一个[属性集]显式指定，其格式与 [`builtins.hasContext`] 产生的格式相同。
可以这样构造一个带有任意上下文的字符串：

1. 创建一个带有目标字符串上下文元素的字符串。
   （字符串的内容无关紧要。）
2. 用 [`builtins.getContext`] 获取它的上下文。
3. 将它与一个基础字符串以及多次 [`builtins.appendContext`] 调用结合起来。

[`builtins.appendContext`]: ./builtins.md#builtins-appendContext
