# 高级属性

derivation（派生）可以声明一些不常使用的可选属性。

## 输入

  - [`exportReferencesGraph`]{#adv-attr-exportReferencesGraph}\
    指定 [*export references graph*（导出引用图）](@docroot@/store/derivation/index.md#export-references-graph)选项。
    该属性的值应为一个成对的列表 `[ name1 path1 name2 path2 ...  ]`。
    例如，当构建以下 derivation 时：

    ```nix
    derivation {
      ...
      exportReferencesGraph = [ "libfoo-graph" libfoo ];
    };
    ```

    `libfoo` 的引用图会被放置在临时构建目录中的
    `libfoo-graph` 文件里。

  - [`passAsFile`]{#adv-attr-passAsFile}\
    一个属性名列表，这些属性对应的环境变量应被标记为
    [*pass as file*（以文件传递）](@docroot@/store/derivation/index.md#pass-as-file)。
    例如，如果你有

    ```nix
    passAsFile = ["big"];
    big = "a very long string";
    ```

    那么当 builder 运行时，环境变量 `bigPath`
    将包含一个临时文件的绝对路径，该文件的内容为 `a
    very long string`。

  - [`__structuredAttrs`]{#adv-attr-structuredAttrs}\
    如果特殊属性 `__structuredAttrs` 被设置为 `true`，则其他 derivation
    属性会被序列化为一个 JSON 格式的文件。

    更多细节参见 [derivation 页面中的对应章节](@docroot@/store/derivation/index.md#structured-attrs)。

    > **警告**
    >
    > 如果设置为 `true`，顶层属性 [`allowedReferences`](#adv-attr-allowedReferences)、[`allowedRequisites`](#adv-attr-allowedRequisites)、
    > [`disallowedReferences`](#adv-attr-disallowedReferences) 和 [`disallowedRequisites`](#adv-attr-disallowedRequisites)
    > 将不产生任何效果；请改用 [`outputChecks`](#adv-attr-outputChecks)。

## 输出检查

这些属性用于指定[对 derivation 输出的检查](@docroot@/store/derivation/outputs/index.md#output-checks)。
其背后的概念在该处有文档说明；本节给出在 Nix 语言中指定它们的语法。

这些列表中的存储路径可以以带上下文的字符串形式给出（即通过插值一个 derivation 得到），而 derivation 自身的输出则用其朴素的输出名表示，例如 `"out"`。

  - [`allowedReferences`]{#adv-attr-allowedReferences}\
    指定 [*allowed references*（允许的引用）](@docroot@/store/derivation/outputs/index.md#allowed-references)检查。例如，

    ```nix
    allowedReferences = [];
    ```

    强制要求 derivation 的输出对其输入不能有任何运行时
    依赖。要允许输出对自身有运行时
    依赖，请使用 `"out"` 作为列表项。

  - [`allowedRequisites`]{#adv-attr-allowedRequisites}\
    指定 [*allowed requisites*（允许的传递依赖）](@docroot@/store/derivation/outputs/index.md#allowed-requisites)检查。例如，

    ```nix
    allowedRequisites = [ foobar ];
    ```

    强制要求 derivation 的输出除 `foobar` 之外不能有任何其他
    运行时依赖，并且还强制要求
    `foobar` 自身不引入任何其他依赖。

  - [`disallowedReferences`]{#adv-attr-disallowedReferences}\
    指定 [*disallowed references*（禁止的引用）](@docroot@/store/derivation/outputs/index.md#disallowed-references)检查。例如，

    ```nix
    disallowedReferences = [ foo ];
    ```

    强制要求 derivation 的输出对 derivation `foo` 不能有直接的
    运行时依赖。

  - [`disallowedRequisites`]{#adv-attr-disallowedRequisites}\
    指定 [*disallowed requisites*（禁止的传递依赖）](@docroot@/store/derivation/outputs/index.md#disallowed-requisites)检查。例如，

    ```nix
    disallowedRequisites = [ foobar ];
    ```

    强制要求 derivation 的输出对 `foobar` 不能有任何运行时
    依赖，对任何递归依赖于 `foobar` 的其他 derivation 也不能有。

  - [`outputChecks`]{#adv-attr-outputChecks}\
    当使用[结构化属性](#adv-attr-structuredAttrs)时，`outputChecks`
    属性允许按输出定义检查。

    除了
    [`allowedReferences`](#adv-attr-allowedReferences)、[`allowedRequisites`](#adv-attr-allowedRequisites)、
    [`disallowedReferences`](#adv-attr-disallowedReferences) 和 [`disallowedRequisites`](#adv-attr-disallowedRequisites)
    之外，还可以使用以下属性：

    - `maxSize` 指定 [*max size*（最大大小）](@docroot@/store/derivation/outputs/index.md#max-size)检查。
    - `maxClosureSize` 指定 [*max closure size*（最大闭包大小）](@docroot@/store/derivation/outputs/index.md#max-closure-size)检查。
    - `ignoreSelfRefs` 控制 [*ignore self references*（忽略自引用）](@docroot@/store/derivation/outputs/index.md#ignore-self-refs)行为。

    示例：

    ```nix
    __structuredAttrs = true;

    outputChecks.out = {
      # The closure of 'out' must not be larger than 256 MiB.
      maxClosureSize = 256 * 1024 * 1024;

      # It must not refer to the C compiler or to the 'dev' output.
      disallowedRequisites = [ stdenv.cc "dev" ];
    };

    outputChecks.dev = {
      # The 'dev' output must not be larger than 128 KiB.
      maxSize = 128 * 1024;
    };
    ```

## 其他输出修改

  - [`unsafeDiscardReferences`]{#adv-attr-unsafeDiscardReferences}\
    当使用[结构化属性](#adv-attr-structuredAttrs)时，
    属性 `unsafeDiscardReferences` 是一个属性集，为每个输出名给出一个布尔值。
    如果设置为 `true`，则为该输出启用
    [*unsafe discard references*（不安全地丢弃引用）](@docroot@/store/derivation/outputs/index.md#unsafe-discard-references)
    行为。

    示例：

    ```nix
    __structuredAttrs = true;
    unsafeDiscardReferences.out = true;
    ```

## 构建调度

  - [`preferLocalBuild`]{#adv-attr-preferLocalBuild}\
    如果设置为 `true`，则启用 [*prefer local build*（优先本地构建）](@docroot@/store/derivation/index.md#prefer-local-build)选项。
    这对在本地构建最划算的 derivation 很有用。

  - [`allowSubstitutes`]{#adv-attr-allowSubstitutes}\
    如果设置为 `false`，则禁用 [*allow substitutes*（允许 substitute（替代））](@docroot@/store/derivation/index.md#allow-substitutes)选项，因此 Nix 将总是（在本地或远程）构建这个 derivation，而不是用 substitute（替代）方式获取其输出。
    这对构建比替代获取更划算的 derivation 很有用。

- [`requiredSystemFeatures`]{#adv-attr-requiredSystemFeatures}\
  指定 [*required system features*（所需的系统特性）](@docroot@/store/derivation/index.md#required-system-features)选项：
  Nix 只会在其 [`system-features` 配置](@docroot@/command-ref/conf-file.md#conf-system-features)中设置了相应特性的机器上构建该 derivation。

  例如，设置

  ```nix
  requiredSystemFeatures = [ "kvm" ];
  ```

  可确保该 derivation 只能在具有 `kvm` 特性的机器上构建。

# 非纯 builder 配置

  - [`impureEnvVars`]{#adv-attr-impureEnvVars}\
    指定 [*impure environment variables*（非纯环境变量）](@docroot@/store/derivation/index.md#impure-env-vars)选项：一个环境变量列表，
    这些环境变量应从调用用户的环境中传递给 builder。例如，
    Nixpkgs 中的 `fetchurl` 有这样一行

    ```nix
    impureEnvVars = [ "http_proxy" "https_proxy" ... ];
    ```

    以使其使用用户在环境变量 `http_proxy` 及类似变量中指定的
    代理服务器配置。

## 设置 derivation 类型

如 [derivation 输出与 derivation 的类型](@docroot@/store/derivation/outputs/index.md)中所述，存在多种类型的 derivation / 多种类型的 derivation 输出。
对以下属性的选择决定了我们要构建的是哪种类型的 derivation。

- [`__contentAddressed`]

- [`outputHash`]

- [`outputHashAlgo`]

- [`outputHashMode`]

基于这些属性的以下组合来选择三种类型的 derivation。
所有其他组合都是无效的。

- [按输入寻址的 derivation](@docroot@/store/derivation/outputs/input-address.md)

  这是 `builtins.derivation` 的默认值。
  目前 Nix 只支持一种按输入寻址的方式，因此不需要其他信息。

  也可以包含 `__contentAddressed = false;`，但这并非必需，且会触发实验性特性检查。

- [固定输出 derivation]

  [`outputHash`]、[`outputHashAlgo`] 和 [`outputHashMode`] 三者全部指定。

  <!--

  `__contentAddressed` is ignored, because fixed-output derivations always content-address their outputs, by definition.

  **TODO CHECK**

  -->

- [(浮动)按内容寻址的 derivation](@docroot@/store/derivation/outputs/content-address.md)

  同时指定 [`outputHashAlgo`] 和 [`outputHashMode`]，`__contentAddressed = true;`，并且*不*指定 `outputHash`。

  如果给出了输出哈希，那么 derivation 输出将是「固定」的而非「浮动」的。

以下是关于 `output*` 属性的更多信息，以及它们可以设置的值：

  - [`outputHashMode`]{#adv-attr-outputHashMode}

    该属性指定如何对按内容寻址的 derivation 输出的文件进行摘要以产生内容地址。

    它与 [`outputHashAlgo`](#adv-attr-outputHashAlgo) 配合使用。
    只指定其中一个而不指定另一个是一个错误（除非 [`outputHash` 也被指定且如后文所述包含了其自身的哈希算法）。

    `outputHashMode` 属性决定哈希是如何计算的。
    它必须是以下值之一：

      - [`"flat"`](@docroot@/store/store-object/content-address.md#method-flat)

        这是默认值。

      - [`"recursive"` 或 `"nar"`](@docroot@/store/store-object/content-address.md#method-nix-archive)

        > **兼容性**
        >
        > `"recursive"` 是表示此模式的传统方式，
        > 自 2005 年起就受支持（几乎是 Nix 的整部历史）。
        > `"nar"` 更清晰，并与 Nix 的其他部分（如 CLI）保持一致，
        > 然而对它的支持只在 Nix 2.21 版本中加入。

      - [`"text"`](@docroot@/store/store-object/content-address.md#method-text)

        > **警告**
        >
        > 对 derivation 输出使用此方法属于 [`dynamic-derivations`][xp-feature-dynamic-derivations] 实验性特性。

      - [`"git"`](@docroot@/store/store-object/content-address.md#method-git)

        > **警告**
        >
        > 此方法属于 [`git-hashing`][xp-feature-git-hashing] 实验性特性。

    关于此标志所控制过程的更多信息，参见[按内容寻址的存储对象](@docroot@/store/store-object/content-address.md)。

  - [`outputHashAlgo`]{#adv-attr-outputHashAlgo}

    该属性指定用于对按内容寻址的 derivation 输出的[文件系统对象][file system object]数据进行摘要的哈希算法。

    它与 [`outputHashMode`](#adv-attr-outputHashAlgo) 配合使用。
    只指定其中一个而不指定另一个是一个错误（除非 `outputHash` 也被指定且如后文所述包含了其自身的哈希算法）。

    `outputHashAlgo` 属性指定用于计算哈希的哈希算法。
    它当前可以是 `"blake3"`、`"sha1"`、`"sha256"`、`"sha512"` 或 `null`。

    `outputHashAlgo` 只有在 `outputHash` 遵循 SRI 格式时才能为 `null`，因为在这种情况下，哈希算法的选择由 `outputHash` 决定。

  - [`outputHash`]{#adv-attr-outputHash}

    该属性指定[固定输出 derivation] 的单一输出的输出哈希。

    `outputHash` 属性必须是一个字符串，包含以十六进制或 "nix32" 编码表示的哈希，或者遵循 [SRI](@docroot@/glossary.md#gloss-sri) 所定义的完整性元数据格式。
    ["nix32" 编码](@docroot@/protocols/nix32.md)是 Nix 对 Base32 编码的变体。

    > **注意**
    >
    > [`convertHash`](@docroot@/language/builtins.md#builtins-convertHash) 函数展示了如何在不同编码之间进行转换。
    > [`nix-hash` 命令](../command-ref/nix-hash.md)包含关于获取某些内容哈希以及在不同编码间转换的信息。

  - [`__contentAddressed`]{#adv-attr-__contentAddressed}

    > **警告**
    >
    > 该属性属于一项[实验性特性](@docroot@/development/experimental-features.md)。
    >
    > 要使用该属性，你必须启用
    > [`ca-derivations`][xp-feature-ca-derivations] 实验性特性。
    > 例如，可以在 [nix.conf](../command-ref/conf-file.md) 中添加：
    >
    > ```
    > extra-experimental-features = ca-derivations
    > ```

    这是一个布尔值，默认为 `false`。
    它决定该 derivation 是否为浮动按内容寻址。

[`__contentAddressed`]: #adv-attr-__contentAddressed
[`outputHash`]: #adv-attr-outputHash
[`outputHashAlgo`]: #adv-attr-outputHashAlgo
[`outputHashMode`]: #adv-attr-outputHashMode

[固定输出 derivation]: @docroot@/glossary.md#gloss-fixed-output-derivation
[file system object]: @docroot@/store/file-system-object.md
[store object]: @docroot@/store/store-object.md
[xp-feature-dynamic-derivations]: @docroot@/development/experimental-features.md#xp-feature-dynamic-derivations
[xp-feature-git-hashing]: @docroot@/development/experimental-features.md#xp-feature-git-hashing
