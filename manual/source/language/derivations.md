# derivation（派生）

最重要的内置函数是 `derivation`，它用于描述一个单一的 store 层[store derivation]。
关于什么是 store derivation，请参阅 [store 章节](@docroot@/store/derivation/index.md)；
本节只关注如何用 Nix 语言创建一个。

这个内置函数接受一个属性集作为输入，其属性指定了该过程的各项输入。
它输出一个属性集，并在求值的过程中作为副作用产生一个 [store derivation]。

[store derivation]: @docroot@/glossary.md#gloss-store-derivation

## 输入属性

### 必需属性

- [`name`]{#attr-name}（[字符串](@docroot@/language/types.md#type-string)）

  derivation 的符号名称。
  它会影响什么，参见 [derivation 输出](@docroot@/store/derivation/outputs/index.md#outputs)。

  [store path]: @docroot@/store/store-path.md

  > **示例**
  >
  > ```nix
  > derivation {
  >   name = "hello";
  >   # ...
  > }
  > ```
  >
  > 该 derivation 的路径将是 `/nix/store/<hash>-hello.drv`。
  > [输出](#attr-outputs)路径的形式将是 `/nix/store/<hash>-hello[-<output>]`

- [`system`]{#attr-system}（[字符串](@docroot@/language/types.md#type-string)）

  参见 [system](@docroot@/store/derivation/index.md#system)。

  > **示例**
  >
  > 声明一个要在特定系统类型上构建的 derivation：
  >
  > ```nix
  > derivation {
  >   # ...
  >   system = "x86_64-linux";
  >   # ...
  > }
  > ```

  > **示例**
  >
  > 声明一个要在执行表达式求值的系统类型上构建的 derivation：
  >
  > ```nix
  > derivation {
  >   # ...
  >   system = builtins.currentSystem;
  >   # ...
  > }
  > ```
  >
  > [`builtins.currentSystem`](@docroot@/language/builtins.md#builtins-currentSystem) 的值来自 [`system` 配置选项]，默认为当前 Nix 安装的系统类型。

- [`builder`]{#attr-builder}（[路径](@docroot@/language/types.md#type-path) | [字符串](@docroot@/language/types.md#type-string)）

  参见 [builder](@docroot@/store/derivation/index.md#builder)。

  > **示例**
  >
  > 使用位于 `/bin/bash` 的文件作为 builder 可执行文件：
  >
  > ```nix
  > derivation {
  >   # ...
  >   builder = "/bin/bash";
  >   # ...
  > };
  > ```

  <!-- -->

  > **示例**
  >
  > 把一个本地文件复制到 Nix store 中，用作 builder 可执行文件：
  >
  > ```nix
  > derivation {
  >   # ...
  >   builder = ./builder.sh;
  >   # ...
  > };
  > ```

  <!-- -->

  > **示例**
  >
  > 使用来自另一个 derivation 的文件作为 builder 可执行文件：
  >
  > ```nix
  > let pkgs = import <nixpkgs> {}; in
  > derivation {
  >   # ...
  >   builder = "${pkgs.python}/bin/python";
  >   # ...
  > };
  > ```

### 可选属性

- [`args`]{#attr-args}（[字符串](@docroot@/language/types.md#type-string)的[列表](@docroot@/language/types.md#type-list)）

  默认值：`[ ]`

  参见 [args](@docroot@/store/derivation/index.md#args)。

  > **示例**
  >
  > 向 Bash 传递参数以解释执行一条 shell 命令：
  >
  > ```nix
  > derivation {
  >   # ...
  >   builder = "/bin/bash";
  >   args = [ "-c" "echo hello world > $out" ];
  >   # ...
  > };
  > ```

- [`outputs`]{#attr-outputs}（[字符串](@docroot@/language/types.md#type-string)的[列表](@docroot@/language/types.md#type-list)）

  默认值：`[ "out" ]`

  derivation 的符号输出。
  每个输出名称都会作为环境变量传递给 [`builder`](#attr-builder) 可执行文件，其值被设置为对应的[存储路径]。

  默认情况下，derivation 只产生一个名为 `out` 的输出。
  不过，derivation 可以产生多个输出。
  这使得关联的 [store object](@docroot@/store/store-object.md) 及其[闭包](@docroot@/glossary.md#gloss-closure)可以被单独复制或垃圾回收。

  > **示例**
  >
  > 想象一个提供动态库、头文件和文档的库软件包。
  > 链接这样一个库的程序在运行时不需要头文件和文档，在构建时也不需要文档。
  > 因此，这个库软件包可以指定：
  >
  > ```nix
  > derivation {
  >   # ...
  >   outputs = [ "lib" "dev" "doc" ];
  >   # ...
  > }
  > ```
  >
  > 这会让 Nix 向 builder 传递环境变量 `lib`、`dev` 和 `doc`，其中包含每个输出预期的存储路径。
  > 对于 Autoconf 风格的软件包，builder 通常会做类似这样的事情：
  >
  > ```bash
  > ./configure \
  >   --libdir=$lib/lib \
  >   --includedir=$dev/include \
  >   --docdir=$doc/share/doc
  > ```

  输出的名称会与 derivation 的名称组合起来，构成该输出的存储路径的[名称部分](@docroot@/store/store-path.md#name)；但如果输出名是 `out`，则只使用 derivation 的名称。

  > **示例**
  >
  >
  > ```nix
  > derivation {
  >   name = "example";
  >   outputs = [ "lib" "dev" "doc" "out" ];
  >   # ...
  > }
  > ```
  >
  > store derivation 的路径将是 `/nix/store/<hash>-example.drv`。
  > 输出路径将是
  > - `/nix/store/<hash>-example-lib`
  > - `/nix/store/<hash>-example-dev`
  > - `/nix/store/<hash>-example-doc`
  > - `/nix/store/<hash>-example`

  你可以通过把 derivation 的某个输出当作属性来选择它，从而引用该输出。
  `outputs` 的第一个元素决定了*默认输出*，它位于顶层。

  > **示例**
  >
  > 按属性名选择一个输出：
  >
  > ```nix
  > let
  >   myPackage = derivation {
  >     name = "example";
  >     outputs = [ "lib" "dev" "doc" "out" ];
  >     # ...
  >   };
  > in myPackage.dev
  > ```
  >
  > 由于 `lib` 是第一个输出，`myPackage` 等价于 `myPackage.lib`。

  <!-- FIXME: refer to the output attributes when we have one -->

- 更多不常用的可选属性，参见[高级属性](./advanced-attributes.md)。

  <!-- FIXME: This should be moved here -->

- 所有其他属性都会作为环境变量传递给 builder。
  属性值按以下方式转换为环境变量：

    - 字符串原样传递。

    - 整数被转换为十进制表示。

    - 浮点数被转换为预设精度的简单十进制或科学计数法表示。

    - *路径*（例如 `../foo/sources.tar`）会导致被引用的文件被复制到 store 中；
      并把它在 store 中的位置放入环境变量。其设计思想是所有源代码都应
      存放在 Nix store 中，因为 derivation 的所有输入都应
      存放在 Nix store 中。

    - *derivation* 会导致该 derivation 在当前 derivation 之前被构建。
      环境变量会被设置为该 derivation 的默认[输出](#attr-outputs)的[存储路径]。

    - 由前面这些类型组成的列表也是允许的。它们只是被简单地
      拼接在一起，以空格分隔。

    - `true` 会作为字符串 `1` 传递；`false` 和 `null` 会作为
      空字符串传递。

<!-- FIXME: add a section on output attributes -->
