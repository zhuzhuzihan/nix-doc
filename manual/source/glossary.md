# 术语表

- [`∅`]{#gloss-empty-set}

  空集符号。在 profile 历史的语境中，它表示某个软件包在特定版本的 profile 中不存在。

- [`ε`]{#gloss-epsilon}

  epsilon 符号。在软件包的语境中，它表示版本号为空。更准确地说，表示该 derivation（派生）没有版本属性。

- [base directory（基准目录）]{#gloss-base-directory}

  相对路径的解析起点。

  - 对于文件中的表达式，基准目录是包含该文件的目录。
    这类似于 [base URL](https://datatracker.ietf.org/doc/html/rfc1808#section-3.3) 的基准目录。
    <!-- which is sufficient for resolving non-empty URLs -->

  <!--
    The wording here may look awkward, but it's for these reasons:
      * "with --expr": it's a flag, and not an option with an accompanying value
      * "written in": the expression itself must be written as an argument,
        whereas the more natural "passed as an argument" allows an interpretation
        where the expression could be passed by file name.
    -->
  - 对于通过命令行参数与 [`--expr`](@docroot@/command-ref/opt-common.html#opt-expr) 编写的表达式，基准目录是当前工作目录。

  [base directory]: #gloss-base-directory

- [binary cache（二进制缓存）]{#gloss-binary-cache}

  *二进制缓存*（binary cache）是一种使用不同格式的 Nix store：其元数据和签名保存在 `.narinfo` 文件中，而不是 [Nix 数据库][Nix database]中。这种不同的格式简化了通过网络提供存储对象的服务，但它本身不能执行构建。二进制缓存的例子包括 S3 存储桶和 [NixOS 二进制缓存](https://cache.nixos.org)。

- [build system（构建系统）]{#gloss-build-system}

  构建系统（build system）是对一类软件的统称：它们通过自动化地调用编译器、链接器等工具来辅助软件的构建。

  Nix 可以作为一个通用的构建系统使用。
  它不了解任何特定的编程语言或工具链。
  这些细节在 [derivation 表达式](#gloss-derivation-expression)中指定。

- [closure（闭包）]{#gloss-closure}

  一个存储路径（store path）的闭包是指从该存储路径直接或间接「可达」的存储路径的集合；也就是说，它是该路径在*引用*关系下的闭包。对于一个软件包而言，其 derivation 的闭包等价于构建期依赖，而其[输出路径][output path]的闭包等价于运行期依赖。要正确部署，就必须部署完整的闭包，否则运行时可能出现文件缺失。命令 `nix-store --query --requisites ` 可以打印出存储路径的闭包。

  举例来说，如果路径 `P` 上的[存储对象][store object]包含一个指向路径 `Q` 上存储对象的[引用][reference]，那么 `Q` 就在 `P` 的闭包中。进一步，如果 `Q` 引用了 `R`，那么 `R` 也在 `P` 的闭包中。

  详情参见[引用](@docroot@/store/store-object.md#references)。

  [closure]: #gloss-closure

- [content address（内容寻址）]{#gloss-content-address}

  [*content address*（内容地址）](https://en.wikipedia.org/wiki/Content-addressable_storage)是一种引用不可变数据的安全方式。
  该引用直接从被引用数据的内容计算得出，这意味着引用是
  [*tamper proof*（防篡改）的](https://en.wikipedia.org/wiki/Tamperproofing)
  ——数据的任何变化都必然计算出不同的内容地址。

  关于 Nix 如何使用内容地址，参见：

    - [对文件系统对象进行内容寻址](@docroot@/store/file-system-object/content-address.md)
    - [对存储对象进行内容寻址](@docroot@/store/store-object/content-address.md)
    - [内容寻址 derivation](#gloss-content-addressing-derivation)

  Software Heritage 关于[*内在与外在标识符*](https://www.softwareheritage.org/2020/07/09/intrinsic-vs-extrinsic-identifiers)的文章，也是了解内容寻址相对于其他引用方案之价值的一篇很好的入门材料。

  除了内容寻址之外，Nix store 还使用[按输入寻址](#gloss-input-addressed-store-object)。

- [content-addressed storage（内容寻址存储）]{#gloss-content-addressed-store}

  这是业界对采用[内容寻址](#gloss-content-address)的存储与检索系统的称呼。Nix store 还具有[按输入寻址](#gloss-input-addressed-store-object)和元数据。

- [content-addressed store object（内容寻址存储对象）]{#gloss-content-addressed-store-object}

  一种[存储对象][store object]，它是[内容寻址](#gloss-content-address)的，即其[存储路径][store path]由其内容决定。
  这包括 derivation 本身、[内容寻址 derivation](#gloss-content-addressing-derivation)的输出，以及[固定输出 derivation](#gloss-fixed-output-derivation)的输出。

  详情参见[对存储对象进行内容寻址](@docroot@/store/store-object/content-address.md)。

- [content-addressing derivation（内容寻址 derivation）]{#gloss-content-addressing-derivation}

  将
  [`__contentAddressed`](./language/advanced-attributes.md#adv-attr-__contentAddressed)
  属性设置为 `true` 的 derivation。

- [derivation（派生）]{#gloss-derivation}

  derivation 可以被看作一个[纯函数](https://en.wikipedia.org/wiki/Pure_function)，它从已有的存储对象产生新的[存储对象][store object]。

  derivation 的实现方式是[在沙箱中运行的操作系统进程](@docroot@/store/building.md)。
  该沙箱默认只允许读取被指定为输入的存储对象，并且只允许写入指定的[输出][output]，这些输出随后会[被捕获为存储对象](@docroot@/store/building.md#processing-outputs)。

  derivation 通常以 [derivation 表达式][derivation expression]的形式在 [Nix 语言][Nix language]中指定，并被[实例化][instantiate]为一个 [store derivation]。
  从 store derivation 获得存储对象有多种方式，统称为[实现（realisation）][realise]。

  [derivation]: #gloss-derivation

- [derivation expression（derivation 表达式）]{#gloss-derivation-expression}

  使用 [Nix 语言][Nix language]中的 [`derivation` 原语](./language/derivations.md)对 [store derivation] 的描述。

  [derivation expression]: #gloss-derivation-expression

- [derivation path（derivation 路径）]{#gloss-derivation-path}

  唯一标识一个 [store derivation] 的[存储路径][store path]。

  详情参见[引用 store derivation](@docroot@/store/derivation/index.md#derivation-path)。

  不要与 [deriving path] 混淆。

  [derivation path]: #gloss-derivation-path

- [deriver]{#gloss-deriver}

  产生某个[输出路径][output path]的 [store derivation]。

  输出路径的 deriver 可以通过 [`nix-store --query`](@docroot@/command-ref/nix-store/query.md) 的 `--deriver` 选项查询。

- [deriving path]{#gloss-deriving-path}

  Deriving path 是一种引用[存储对象][store object]的方式，所指的存储对象可能尚未被[实现][realise]。

  详情参见 [deriving path](./store/derivation/index.md#deriving-path)。

  不要与 [derivation path] 混淆。

- [directed acyclic graph（有向无环图）]{#gloss-directed-acyclic-graph}

  [有向无环图](https://en.wikipedia.org/wiki/Directed_acyclic_graph)（DAG）是一种边被赋予方向的图（「a 到 b」与「b 到 a」是不同的边），并且任何由边连接而成的路径都不会构成环。

  DAG 对 Nix 而言非常重要。
  特别是，[存储对象][store object]之间的非自身[引用][reference]构成一个环。

- [experimental feature（实验性特性）]{#gloss-experimental-feature}

  尚未稳定的功能，由具名的实验性特性开关保护。
  这些开关通过 [`experimental-features`](./command-ref/conf-file.html#conf-experimental-features) 设置来启用或禁用。

  关于实验性特性的目的与生命周期，参见贡献指南中的[相关章节](@docroot@/development/experimental-features.md)。

- [file system object（文件系统对象）]{#gloss-file-system-object}

  Nix 用于表示简化文件系统数据的数据模型。

  详情参见[文件系统对象](@docroot@/store/file-system-object.md)。

  [file system object]: #gloss-file-system-object

- [fixed-output derivation（固定输出 derivation）]{#gloss-fixed-output-derivation}（FOD）

  一种 [store derivation]，其[输出][output]的密码学哈希通过 [`outputHash`](./language/advanced-attributes.md#adv-attr-outputHash) 属性预先确定，并且其 [`builder`](@docroot@/language/derivations.md#attr-builder) 可执行文件可以访问网络。

- [hermetic（密封性）]{#gloss-hermetic}

  当一个求值或构建过程的所有可能影响它的输入可以被机械地确定下来时，该过程就是密封的（hermetic）。
  在构建层面，这通过沙箱实现；在求值层面，则通过限制非纯访问（如[纯求值](@docroot@/command-ref/conf-file.md#conf-pure-eval)）并结合对所获取输入的[锁定](#gloss-locking)或[固定](#gloss-pinning)来实现，并在[纯获取](@docroot@/command-ref/conf-file.md#pure-fetch)上传递地应用。

- [IFD]{#gloss-ifd}

  [从 derivation 导入（Import From Derivation）](./language/import-from-derivation.md)

- [impure derivation（非纯 derivation）]{#gloss-impure-derivation}

  [一项实验性特性](@docroot@/development/experimental-features.md#xp-feature-impure-derivations)，允许将 derivation 显式标记为非纯，
  从而使其总是被重新构建，且其输出不会被后续的实现（realise）调用复用。

- [input-addressed store object（按输入寻址的存储对象）]{#gloss-input-addressed-store-object}

  通过构建一个非[内容寻址](#gloss-content-addressing-derivation)、
  非[固定输出](#gloss-fixed-output-derivation)
  的 derivation 而产生的存储对象。

  详情参见 [derivation 输出的按输入寻址](store/derivation/outputs/input-address.md)。

- [installable（可安装项）]{#gloss-installable}

  可以在 Nix store 中被实现（realise）的东西。

  详情参见 [`nix` 命令](./command-ref/new-cli/nix.md)（实验性）的 [installables](./command-ref/new-cli/nix.md#installables)。

- [instantiate（实例化）]{#gloss-instantiate}，instantiation（实例化过程）

  将 [derivation 表达式][derivation expression]翻译为一个 [store derivation]。

  参见 [`nix-instantiate`](./command-ref/nix-instantiate.md)，它从一个求值结果为 derivation 的 Nix 表达式生成 store derivation。

  [instantiate]: #gloss-instantiate

- [locking（锁定）]{#gloss-locking}

  在软件包管理中，*锁定*（locking）是创建锁文件的概念或过程。锁文件将每个可变的求值输入映射到一个不可变的引用，使未来的求值解析到相同的不可变版本，而不是可变引用当前指向的内容。

- [Nix Archive（NAR）]{#gloss-nar}

  *N*ix *AR*chive（Nix 归档）。这是对 Nix store 中路径的一种序列化表示。它可以包含普通文件、目录和符号链接。NAR 使用 `nix-store --dump` 和 `nix-store --restore` 来生成和解包。

  详情参见 [Nix Archive](store/file-system-object/content-address.html#serial-nix-archive)。

- [Nix database（Nix 数据库）]{#gloss-nix-database}

  一个 SQlite 数据库，用于追踪[存储对象][store object]之间的[引用][reference]关系。
  这是[本地存储][local store]的一个实现细节。

  默认位置：`/nix/var/nix/db`。

  [Nix database]: #gloss-nix-database

- [Nix expression（Nix 表达式）]{#gloss-nix-expression}

  [Nix 语言][Nix language]的一次语法上合法的使用。

  > **示例**
  >
  > 一个 `.nix` 文件的内容构成一个 Nix 表达式。

  Nix 表达式指定 [derivation 表达式][derivation expression]，后者被[实例化][instantiate]到 Nix store 中成为 [store derivation]。
  这些 derivation 随后可以被[实现][realise]以产生[输出][output]。

  > **示例**
  >
  > 使用 Nix 构建和部署软件，需要编写 Nix 表达式来描述[软件包][package]及其组合。

- [Nix instance（Nix 实例）]{#gloss-nix-instance}
  <!-- ambiguous -->
  1. 一套 Nix 的安装，包括一个[存储][store]的存在，以及在该存储之上运作的 Nix 软件包管理器。
     本地 Nix 安装和[远程构建机](@docroot@/advanced-topics/distributed-builds.md)是 Nix 实例的两个例子。
  2. 一个正在运行的 Nix 进程，例如 `nix` 命令。

- [output（输出）]{#gloss-output}

  由 [store derivation] 产生的一个[存储对象][store object]。
  详情参见 [`derivation` 函数的 `outputs` 参数](@docroot@/language/derivations.md#attr-outputs)。

  [output]: #gloss-output

- [output closure（输出闭包）]{#gloss-output-closure}\
  某个[输出路径][output path]的[闭包][closure]。它只包含从该输出[可达][reachable]的内容。

- [output path（输出路径）]{#gloss-output-path}

  指向某个 [store derivation] 的[输出][output]的[存储路径][store path]。

  [output path]: #gloss-output-path

- [package（软件包）]{#package}

  软件包（package）；为特定目的而归在一起的一组文件，以及元数据。

  Nix 将文件表示为[文件系统对象][file system object]，而文件之间的归属关系则被编码为包含这些文件系统对象的[存储对象][store object]之间的[引用][reference]。

  [Nix 语言][Nix language]允许用包含以下内容的[属性集](@docroot@/language/types.md#type-attrs)来表示软件包：
  - 指向软件包文件的属性，通常以 [derivation 输出](#gloss-output)的形式出现，
  - 带有元数据的属性，例如关于该软件包应如何使用的信息。

  这些属性集的具体形态取决于约定。

  [package]: #package

- [pinning（固定）]{#gloss-pinning}

  与[锁定](#gloss-locking)类似，但一个 pin 只锁定单个输入。
  一个 pinning 方案可以管理一组 pin，
  但其服务于自下而上的目的，即按需固定某个输入的引用，
  而锁定则意味着一种自上而下的方式，所有 pin 都被「强制」收敛到一处。
  这种「强制收敛」通常通过编程语言模块系统等高层机制实现。
  Nix 没有如此严格的模块系统，因为即使是一个 Flakes 也可以自行使用固定或锁定的表达式。
  它并不依赖锁定是完备的，而是依赖一种传递性的获取性质；参见[密封性](#gloss-hermetic)。

- [profile]{#gloss-profile}

  指向用户当前*用户环境*（user environment）的符号链接，例如
  `/nix/var/nix/profiles/default`。

- [purity（纯度）]{#gloss-purity}

  即「相同的 Nix derivation 在运行时总是产生相同的输出」这一假设。一般来说这一点无法保证（例如，构建器可能依赖网络或系统时间等外部输入），但 Nix 模型假定了这一点。

- [reachable（可达）]{#gloss-reachable}

  如果存储路径 `Q` 位于*引用*关系的*闭包*之中，则称 `Q` 从另一个存储路径 `P` 可达。

  详情参见[引用](@docroot@/store/store-object.md#references)。

- [realise（实现）]{#gloss-realise}，realisation（实现过程）

  确保某个[存储路径][store path]是[有效][validity]的。

  可以通过以下方式实现：
  - 从 [substituter][substituter] 获取预构建的[存储对象][store object]
  - [构建](@docroot@/store/building.md)相应的 [store derivation]
  - 委托给[远程机器](@docroot@/command-ref/conf-file.md#conf-builders)并取回输出

  关于该算法的详细描述，参见 [`nix-store --realise`](@docroot@/command-ref/nix-store/realise.md)。

  另见 [`nix-build`](./command-ref/nix-build.md) 与 [`nix build`](./command-ref/new-cli/nix3-build.md)（实验性）。

  [realise]: #gloss-realise

- [reference（引用）]{#gloss-reference}

  从一个[存储对象][store object]指向另一个存储对象的边。

  详情参见[引用](@docroot@/store/store-object.md#references)。

  [reference]: #gloss-reference

  详情参见[引用](@docroot@/store/store-object.md#references)。

- [referrer（引用者）]{#gloss-referrer}

  从一个[存储对象][store object]指向另一个存储对象的反向边。

- [requisite（必需项）]{#gloss-requisite}

  从某个给定的[存储对象][store object]出发，经由路径（引用链）而[可达][reachable]的存储对象。
  [闭包][closure]就是所有必需项的集合。

  详情参见[引用](@docroot@/store/store-object.md#references)。

- [store（存储）]{#gloss-store}

  [存储对象][store object]的集合，以及操作该集合的各种运算。
  详情参见 [Nix Store](./store/index.md)。

  存储有多种类型，详情参见 [Store Types](./store/types/index.md)。

  [store]: #gloss-store

- [store derivation]{#gloss-store-derivation}

  以[存储对象][store object]形式表示的 [derivation][derivation]。

  详情参见 [Store Derivation](@docroot@/store/derivation/index.md#store-derivation)。

  [store derivation]: #gloss-store-derivation

- [store object（存储对象）]{#gloss-store-object}

  [存储][store]内容的一部分。

  一个存储对象由一个[文件系统对象][file system object]、指向其他存储对象的[引用][reference]，以及其他元数据组成。
  它可以通过一个[存储路径][store path]来引用。

  详情参见 [Store Object](@docroot@/store/store-object.md)。

  [store object]: #gloss-store-object

- [store path（存储路径）]{#gloss-store-path}

  某个[存储对象][store object]在文件系统中的位置，即 Nix store 目录的直接子路径。

  > **示例**
  >
  > `/nix/store/jf6gn2dzna4nmsfbdxsd7kwhsk6gnnlr-git-2.38.1`

  详情参见 [Store Path](@docroot@/store/store-path.md)。

  [store path]: #gloss-store-path

- [string interpolation（字符串插值）]{#gloss-string-interpolation}

  在[字符串][string]、[路径][path]或[属性名][attribute name]中展开被 `${ }` 包围的表达式。

  详情参见[字符串插值](./language/string-interpolation.md)。

  [string]: ./language/types.md#type-string
  [path]: ./language/types.md#type-path
  [attribute name]: ./language/types.md#type-attrs

- [SRI]{#gloss-sri}

  [子资源完整性（Subresource Integrity）](https://www.w3.org/TR/SRI/)（SRI）是一项关于完整性元数据的 [W3C 规范](https://developer.mozilla.org/en-US/docs/Web/Security/Subresource_Integrity)。
  Nix 使用 SRI 哈希格式（`<algorithm>-<Base64 hash>`）来指定内容哈希，这种方式是自描述的，因为哈希算法本身就是格式的一部分。

  [SRI]: #gloss-sri

- [substitute（替代）]{#gloss-substitute}

  substitute（替代）是保存在 [Nix 数据库][Nix database]中的一条命令调用，它描述了如何绕过正常的构建机制（即 derivation）来获得一个存储对象。通常，substitute 通过从某个服务器下载存储对象的预构建版本来获得该存储对象。

- [substituter]{#gloss-substituter}

  一个额外的[存储][store]{#gloss-store}，Nix 可以从它获取存储对象，而不必自行构建。
  substituter 通常是一个[二进制缓存](#gloss-binary-cache)，但任何存储都可以充当 substituter。

  详情参见 [`substituters` 配置选项](./command-ref/conf-file.md#conf-substituters)。

  [substituter]: #gloss-substituter

- [user environment（用户环境）]{#gloss-user-env}

  一个自动生成的存储对象，由一组指向「活跃」应用程序（即其他存储路径）的符号链接组成。这些由 [`nix-env`](./command-ref/nix-env.md) 自动生成。参见 *profile*。

- [validity（有效性）]{#gloss-validity}

  如果一个存储路径的[闭包][closure]中的所有[存储对象][store object]都可以从[存储][store]中读取，则该存储路径是有效的。

  对于[本地存储][local store]，这意味着：
  - 该存储路径指向该[存储][store]中一个实际存在的[存储对象][store object]。
  - 该存储路径在 [Nix 数据库][Nix database]中被列为有效。
  - 该存储路径的[闭包][closure]中的所有路径都是有效的。

  [validity]: #gloss-validity
  [local store]: @docroot@/store/types/local-store.md

[Nix language]: ./language/index.md
