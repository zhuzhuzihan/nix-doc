# Store Derivation 与 Deriving Path

除了作为[内容寻址 store]发挥作用之外，Nix store 层还充当一个[构建系统]。
其他系统（如 Git 或 IPFS）也存储和传输不可变数据，但它们并不关心这些数据是*如何*被创建的。

这正是 Nix 独树一帜的地方。
*Derivation*（派生）表示单个构建步骤，而 *deriving path* 则用于在这些构建步骤被构建之前引用它们的*输出*。
<!-- The two concepts need to be introduced together because, as described below, each depends on the other. -->

## Store Derivation {#store-derivation}

derivation 是一种规格说明，用于在精确定义的输入上运行一个可执行文件，以产出一个或多个[存储对象][store object]。
这些存储对象被称为该 derivation 的*输出*。

derivation 会被*构建*：此时按照规格启动进程，并在其退出时要求它留下文件，这些文件（经后处理之后）将成为该 derivation 的输出。
该过程在[构建](@docroot@/store/building.md)中有详细描述。

<!--
Some of these things are described directly below, but we envision with more material the exposition will probably want to migrate to separate pages benough this.
See outputs spec for an example of this one that migrated to its own page.
-->

一个 derivation 由以下部分组成：

 - 一个名称（name）

 - 一个[输入规格][inputs]，即一组 [deriving path][deriving path]

 - 一个[输出规格][outputs]，指明应产出哪些输出，以及关于它们的各种元数据。

 - 可执行文件将要运行的["system" 类型][system]（例如 `x86_64-linux`）。

 - [进程创建字段]：用于启动执行构建步骤的任意进程。

[store derivation]: #store-derivation
[inputs]: #inputs
[input]: #inputs
[outputs]: ./outputs/index.md
[output]: ./outputs/index.md
[process creation fields]: #process-creation-fields
[builder]: #builder
[args]: #args
[env]: #env
[system]: #system
[content-addressed store]: @docroot@/glossary.md#gloss-content-addressed-store
[build system]: @docroot@/glossary.md#gloss-build-system

### 引用 derivation {#derivation-path}

derivation 总是通过它们被编码到的存储对象的[存储路径]来引用。
关于这种编码如何工作，以及对于一个给定的 derivation 我们最终会得到什么样的存储路径，请参见[编码一节](#derivation-encoding)。

编码 derivation 的存储对象的存储路径，为简洁起见常被称为 *derivation path*。

## Deriving Path {#deriving-path}

Deriving path 是引用那些可能已、也可能尚未被 [realised（实例化）][realise]的[存储对象][store object]的一种方式。
它有两种形式：

- [*常量（constant）*]{#deriving-path-constant}：就是一个[存储路径]。
  可以通过把它复制进 store 使其[有效][validity]：可以来自求值器、命令行界面或另一个 store。

- [*输出（output）*]{#deriving-path-output}：一个二元组，由指向 [store derivation] 的[存储路径]和一个[输出]名称组成。

用伪代码表示：

```typescript
type OutputName = String;

type ConstantPath = {
  path: StorePath;
};

type OutputPath = {
  drvPath: StorePath;
  output: OutputName;
};

type DerivingPath = ConstantPath | OutputPath;
```

Deriving path 之所以必要，是因为一般来说——尤其是对[内容寻址 derivation][content-addressing derivation]——[输出]的[存储路径]无法预先得知。
我们可以用输出 deriving path 来引用这样的输出，而不是引用我们还不知道的存储路径。

[deriving path]: #deriving-path
[validity]: @docroot@/glossary.md#gloss-validity

## Derivation 的组成部分

derivation 由以下小节所记述的各个部分构成。

### 输入 {#inputs}

输入是一组 [deriving path][deriving path]，引用执行此构建步骤所需的全部存储对象。

[进程创建字段]中大概会包含许多[存储路径][store path]：

 - 可执行文件的路径通常以存储路径开头
 - 参数和环境变量中很可能包含许多其他存储路径。

但 Nix 并不以某种方式扫描所有其他字段来寻找输入，而是要求所有输入被显式地收集在输入字段中。相反，确保其他字段中引用的每个存储对象（例如通过存储路径引用）都被包含在这个输入字段中，是 derivation 的创建者（例如求值器）的职责。

### System {#system}

[`builder`](#builder) 可执行文件预期运行的系统类型。

Nix 要把某个给定 derivation 调度到某个 [Nix 实例]上，必要条件是该 derivation 的 "system" 与该实例的 [`system` 配置选项]或 [`extra-platforms` 配置选项]相匹配。

通过在每个 derivation 中放置 `system`，Nix 允许*异构*构建计划，其中并非所有步骤都能在同一台机器或同类机器上运行。
Nix 可以调度构建，通过把[构建请求转发](@docroot@/advanced-topics/distributed-builds.md)给其他 Nix 实例，自动在其他平台上构建。

[`system` configuration option]: @docroot@/command-ref/conf-file.md#conf-system
[`extra-platforms` configuration option]: @docroot@/command-ref/conf-file.md#conf-extra-platforms

[content-addressing derivation]: @docroot@/glossary.md#gloss-content-addressing-derivation
[realise]: @docroot@/glossary.md#gloss-realise
[store object]: @docroot@/store/store-object.md
[store path]: @docroot@/store/store-path.md

### 进程创建字段 {#process-creation-fields}

这三个字段描述如何启动将执行构建的进程（连同其自身的任何子进程）。
你可能会注意到，这正是 `execve` 系统调用所需的全部要素。

#### Builder {#builder}

这是将执行构建并产出[输出]的可执行文件的路径。

#### 参数 {#args}

传给 [`builder`](#builder) 可执行文件的命令行参数。

注意这些是第一个参数之后的参数。
传给 `builder` 的第一个参数将是 `builder` 的值，遵循 Unix 上的通常惯例。
细节参见 [Wikipedia](https://en.wikipedia.org/wiki/Argv)。

#### 环境变量 {#env}

将传给 [builder](#builder) 可执行文件的环境变量。

每个环境变量还带有一个[*pass as file*（以文件传递）]{#pass-as-file}标志。
设置该标志后，值不再直接通过环境传递，而是写入构建目录中的一个临时文件，并设置一个与原变量同名但带 `Path` 后缀的环境变量，指向该文件的路径。
例如，设置了 *pass as file* 的变量 `big` 会导致一个环境变量 `bigPath`，指向包含 `big` 值的文件。
这对大值很有用，因为大多数操作系统对进程环境的大小有限制（通常是几百 KB）。

当使用[结构化属性](#structured-attrs)时，该标志没有效果，因为那时属性根本不通过环境传递，也就没有需要规避的大小限制。

#### 结构化属性 {#structured-attrs}

Nix 还对在 derivation 中嵌入 JSON 提供了特殊支持。

结构化属性免除了[*pass as file*](#pass-as-file)标志的必要，因为 JSON 文件没有大小限制，与进程环境不同。
它们还允许以结构化的方式表达[选项](#options)和[输出检查](outputs/index.md#output-checks)，而不是以字符串编码进环境变量。

环境变量 `NIX_ATTRS_JSON_FILE` 在构建和 [`nix-shell`](@docroot@/command-ref/nix-shell.md) 中都指向该文件的确切位置。

为方便 Bash 构建器，Nix 会写出一个脚本，为所有可用 Bash 表示的属性初始化对应的 shell 变量。
环境变量 `NIX_ATTRS_SH_FILE` 在构建和 [`nix-shell`](@docroot@/command-ref/nix-shell.md) 中都指向该脚本的确切位置。
这包括非嵌套的（关联）数组。
例如，属性 `hardening.format = true` 最终成为 Bash 关联数组元素 `${hardening[format]}`。

### 选项 {#options}

derivation 携带若干*选项*，影响它们的构建与调度方式。
历史上，这些选项是用特别命名的[环境变量](#env)或[结构化属性](#structured-attrs)编码的；不过它们本身就是 derivation 的字段。

适用于单个输出的选项——[输出检查](outputs/index.md#output-checks)与[引用扫描](outputs/index.md#reference-scanning)——在 [derivation 输出](outputs/index.md)文档中记述。
其余选项适用于整个 derivation：

- [*export references graph*（导出引用图）]{#export-references-graph}：
  一个从文件名到 [deriving path][deriving path] 集合的映射。
  对每个条目，给定存储对象的*引用图*——它们[闭包]中的每个存储对象及其引用——会提供给构建器：
  以构建目录中给定名称的文件形式（采用 [`nix-store --register-validity`](@docroot@/command-ref/nix-store/register-validity.md) 所能理解的文本格式，deriver 字段留空且不含哈希），
  或者，在使用[结构化属性](#structured-attrs)时，以 JSON 属性文件中给定键下的形式（作为存储对象信息列表）。
  <!-- TODO: link a schema for the structured-attributes list-of-store-object-infos format. It cannot simply link the store object info JSON schema, because this format is frozen (it is part of the derivation semantics, consumed by existing builders) and differs slightly from that evolving format. -->


  这使构建器能够对其输入的闭包做一些处理。

  > **用法提示**
  >
  > 使用此功能的构建器示例包括 NixOS 中生成用于引导 Linux 的初始内存盘（一个包含引导脚本闭包的 `cpio` 归档）的构建器，
  > 以及安装光盘的 ISO-9660 镜像（其中填入了一个包含可引导 NixOS 配置闭包的 Nix store）。

- [*required system features*（必需系统特性）]{#required-system-features}：
  除了 [system](#system) 类型匹配之外，Nix 的 [`system-features`](@docroot@/command-ref/conf-file.md#conf-system-features) 中还必须具备的一组特性，该 derivation 才能被调度到其上。

- [*prefer local build*（优先本地构建）]{#prefer-local-build}：
  提示该 derivation 在本地构建最便宜：当[启用分布式构建](@docroot@/command-ref/conf-file.md#conf-builders)时，如果可能，它将在本地构建而不是转发到远程机器。

- [*allow substitutes*（允许 substitute）]{#allow-substitutes}：
  该 derivation 的输出是否可以通过 [substitute](@docroot@/glossary.md#gloss-substitute)（替代）获取。
  禁用时，该 derivation 总是被构建（本地或远程）；这对那些构建比 substitute 更便宜的 derivation 有用。
  Nix 可以通过 [`always-allow-substitutes`](@docroot@/command-ref/conf-file.md#conf-always-allow-substitutes) 配置选项忽略此选项。

  > **注意**
  >
  > 禁用时，必须有某个 Nix 实例能够在指定的 [system](#system) 类型上运行 [builder](#builder)，因为该 derivation 无法被 substitute。

- [*impure environment variables*（不纯环境变量）]{#impure-env-vars}：
  从调用用户的环境传给构建器的一组环境变量，否则构建器将从清空的环境开始。
  仅允许用于[固定输出 derivation][fixed-output derivation]，在那里这类不纯性是可以容忍的，因为输出（的哈希）预先已知。
  对所有其他 derivation 则被忽略。

  > **警告**
  >
  > 这些变量取自构建进程自身的环境：
  > 通过 daemon 构建时取自 daemon 的环境，否则才取自调用命令（如 `nix-build`）的环境。

  如果启用了 [`configurable-impure-env` 实验性特性](@docroot@/development/experimental-features.md#xp-feature-configurable-impure-env)，
  这些环境变量还可以通过 [`impure-env`](@docroot@/command-ref/conf-file.md#conf-impure-env) 配置选项加以控制。

- 沙箱相关选项：

  - [*no chroot*（无 chroot）]{#no-chroot}：
    该 derivation 请求在[无沙箱](@docroot@/command-ref/conf-file.md#conf-sandbox)的情况下构建。
    然而，只有在某些配置下这一愿望才会真正得到尊重。
    Nix 可能干脆使构建失败，而不是尝试在无沙箱的情况下执行它。

  - [*additional sandbox profile*（附加沙箱配置）]{#additional-sandbox-profile}：
    （仅限 Darwin）附加的沙箱配置文本，在沙箱内授予构建额外权限。

  - [*impure host dependencies*（不纯的宿主依赖）]{#impure-host-deps}：
    （仅限 Darwin）在沙箱内可用的一组宿主系统路径。

  - [*allow local networking*（允许本地网络）]{#allow-local-networking}：
    （仅限 Darwin）构建是否可以在沙箱内访问本地网络。

[closure]: @docroot@/glossary.md#gloss-closure
[fixed-output derivation]: @docroot@/glossary.md#gloss-fixed-output-derivation

### 占位符（Placeholder）

占位符是在[进程创建字段]中使用的、指向[存储对象]的不透明值，用于那些我们还不知道[存储路径]的存储对象。
它们是 `/<hash>` 形式的字符串，可嵌入这些字段的字符串中的任何位置；我们正在[考虑](https://github.com/NixOS/nix/issues/12361)添加类似存储路径的占位符。

> **注意**
>
> 输出 Deriving Path 的存在是为了解决与占位符相同的问题——即引用那些我们还不知道存储路径的存储对象。
> 它们也有带 `^` 的字符串语法，[在编码一节中描述](#deriving-path-encoding)。
> 我们本可以用那个语法代替 `/<hash>` 作为占位符，但它对人类可读，这会造成问题。

占位符有两种类型，对应出现这一问题的两种情形：

- [输出占位符]{#output-placeholder}：

  这是针对 derivation 自身输出的占位符。

- [输入占位符]{#input-placeholder}：

  这是针对 derivation 的非常量[输入]的占位符，
  即作为[输出 derived path] 的输入。

> **说明**
>
> 一般而言，我们需要 [realise] 一个[存储对象]，才能确保拥有它的存储对象。
> 但对这两种情形，这要么不可能，要么不实际：
>
> - 在输出的情形下不可能：
>
>   在拥有正确的 derivation 之前我们无法构建输出，而在拥有输出路径之前我们又无法拥有正确的 derivation（除非使用占位符）。
>
> - 在输入的情形下不实际：
>
>   如果我们总是先构建一个依赖，然后按存储路径引用其输出，就会失去让 derivation 图描述由多个构建步骤组成的完整构建计划的能力。

## 编码

### Derivation {#derivation-encoding}

有两种格式，分别记述：

- 传统的 ["ATerm" 格式](@docroot@/protocols/derivation-aterm.md)

- 实验性的、仍在开发且不断变化的 [JSON 格式](@docroot@/protocols/json/derivation/index.md)

每个 derivation 都有一个规范选择的编码，用于把它序列化为存储对象。
这确保存在一个规范的[存储路径]用于引用该 derivation，如[引用 derivation](#derivation-path)所述。

> **注意**
>
> 目前，每个 derivation 的规范编码都是 "ATerm" 格式，
> 但对于尚不稳定的 derivation 类型，这一点可能改变。

无论使用哪种格式，把 derivation 序列化为存储对象时，该存储对象都会被内容寻址。

在常见情形下，指向存储对象的输入要么是：

- 内容寻址的源对象的[常量 deriving path](#deriving-path-constant)，它们是"初始输入"而非某个其他 derivation 的输出

- 其他 derivation 的输出

如果那些其他 derivation *也*遵守这一常见情形（其传递输入亦然），那么序列化后的 derivation 的整个闭包都将是内容寻址的。

### Deriving Path {#deriving-path-encoding}

- *constant*

  常量 deriving path 的编码与底层存储路径的编码相同。
  因此，每个已编码的存储路径同时也是一个有效的已编码（常量）deriving path。

- *output*

  输出 deriving path 的编码由以下部分组成：

  - 指向一个 derivation 的存储路径的编码

  - 一个 `^` 分隔符（在某些遗留场景中为 `!`）

  - 前述所引 derivation 的某个输出的名称

  > **示例**
  >
  > ```
  > /nix/store/lxrn8v5aamkikg6agxwdqd1jz7746wz4-firefox-98.0.2.drv^out
  > ```
  >
  > 它的解析方式如下：
  >
  > ```
  > /nix/store/lxrn8v5aamkikg6agxwdqd1jz7746wz4-firefox-98.0.2.drv^out
  > |------------------------------------------------------------| |-|
  > store path (usual encoding)                                    output name
  >                                                           |--|
  >                                                           note the ".drv"
  > ```

## 将模型扩展为高阶 {#dynamic}

**实验性特性**：[`dynamic-derivations`](@docroot@/development/experimental-features.md#xp-feature-dynamic-derivations)

到目前为止，我们一直用存储路径来引用 derivation。
这之所以可行，是因为我们隐含地假设所有 derivation 都是*静态*创建的——由某种带外机制创建，然后手动插入 store。
但如果 derivation 也可以在 Nix 内部动态创建呢？
换言之，如果 derivation 可以是其他 derivation 的输出呢？

> **注意**
>
> 用"Build Systems à la carte"的术语来说，我们是把 Nix store 层泛化为一个"Monadic"而非"Applicative"构建系统。

我们应当如何引用这样的 derivation？
deriving path 就可以，与我们引用其他 derivation 输出的方式相同。
但动态 derivation 的输出呢？
（即：如何引用一个 derivation 的输出，而这个 derivation 本身又是某个 derivation 的输出？）
为此，我们需要泛化 deriving path 的定义，把用于引用 derivation 的存储路径替换为一个嵌套的 deriving path：

```diff
 type OutputPath = {
-  drvPath: StorePath;
+  drvPath: DerivingPath;
   output: OutputName;
 };
```

现在，`OutputPath` 的 `drvPath` 字段本身就是一个 `DerivingPath` 而不是 `StorePath`。

有了这个改动，更新后的定义如下：

```typescript
type OutputName = String;

type ConstantPath = {
  path: StorePath;
};

type OutputPath = {
  drvPath: DerivingPath;
  output: OutputName;
};

type DerivingPath = ConstantPath | OutputPath;
```

在这个扩展模型下，`DerivingPath` 由此归纳地构成：以一个根 `ConstantPath` 开始，包裹零个或多个外层 `OutputPath`。

### 编码 {#deriving-path-encoding-higher-order}

编码以自然的方式调整：递归地用相同的 deriving path 编码来编码 `drv` 字段。
其结果是，最终字符串的末尾可以出现一串 `^<output-name>`，而不止一个。

> **示例**
>
> ```
> /nix/store/lxrn8v5aamkikg6agxwdqd1jz7746wz4-firefox-98.0.2.drv^foo.drv^bar.drv^out
> |----------------------------------------------------------------------------| |-|
> inner deriving path (usual encoding)                                           output name
> |--------------------------------------------------------------------| |-----|
> even more inner deriving path (usual encoding)                         output name
> |------------------------------------------------------------| |-----|
> innermost constant store path (usual encoding)                 output name
> ```

[Nix instance]: @docroot@/glossary.md#gloss-nix-instance
