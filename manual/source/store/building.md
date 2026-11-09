# 构建（Building）

正如 [derivation 主页面](./derivation/index.md)所讨论的：

> derivation（派生）是一种规格说明，用于在精确定义的输入上运行一个可执行文件，以产出一个或多个[存储对象][store object]。

本页描述的是*构建*一个 derivation，即按照 derivation 中的指令实际运行该可执行文件。
derivation 的某些要素是不言自明的。
例如，derivation 中指定的参数确实就是传给可执行文件的参数。
然而在其他情况下，Nix 还会对所有 derivation 执行一些额外的公共步骤——主要是为了搭建构建环境和收集构建出的输出。

构建过程的首要设计考量是*确定性*。
常规操作系统在设计时通常没有考虑确定性。
但要让 Nix 的构建缓存成为一个透明的抽象，确定性是必需的。

> **说明**
>
> 例如，没有人希望稍微修改一个 derivation 之后，却发现它因为一个毫不相关的原因而无法构建了，原因是原始 derivation *也*已经无法构建，只是对原始 derivation 的缓存命中把这一点掩盖了。
> 我们希望构建成功一次之后能持续成功，以鼓励人们无畏地修改旧的构建配方。
> 确定性正是让曾经可用的东西继续可用的关键。

构建的生命周期可以分解为 3 个部分：

1. 以适当的环境启动构建器进程，包括正确的进程参数、环境变量和文件系统状态。

2. 等待构建器进程退出并收集其退出状态。
   退出码 0 表示成功；其他任何情况都是构建失败。
   （严格来说，Nix 是通过等待标准输出和标准错误流关闭来检测进程退出的。
   如果构建器显式关闭了这些流却不退出，Nix 会将其杀死，并判定构建失败。
   因此进程应当*不*显式关闭这些标准流而直接退出，让进程的退出隐式关闭它们。）

   Nix 还会记录进程的标准输出和标准错误，但这只是为了方便人类阅读，并不影响系统的行为。
   （构建器进程并不知道其标准输出和标准错误的消费者对伪终端主端做了什么，只知道这些流确实被消费了，因此缓冲区不会填满等，对每个标准输出流的写入也会持续成功。
   实践中，Nix 会把日志存放在 `/nix/var/log/nix`）

3. 处理输出。

   传统上，这发生在构建器退出之后：构建器进程应当为 derivation 应产出的每个输出留下文件，然后处理这些文件，把它们变成真正的存储对象。
   或者，构建器也可以在运行期间向 Nix 发送消息，创建文件系统对象并将它们与输出名称关联。
   这使得输出可以在构建过程中并发处理，使输出可以依赖于其他新创建的存储对象，还解决了内容寻址以及输出间引用中的一些棘手问题。
   如果处理成功，得到的存储对象就作为一次成功构建的（结果）与该 derivation 关联。

步骤 (3) 由 Nix 完成，或者在构建之外进行（传统情形下，对构建器退出或被杀后留下的惰性数据进行操作），或者与构建并发进行（IPC 情形）。
然而步骤 (1) 最好不从 Nix 的视角、而从构建进程的视角来描述。

> **说明**
>
> 归根结底，对确定性而言重要的是构建进程能够观察到什么：它能看见哪些资源（文件、网络等），哪些系统调用成功或失败，等等。
> Nix 可以通过许多不同的沙箱策略（命名空间、虚拟机、chroot 等）来实现这一点，但进程不应能分辨它们之间的区别。
> 因此我们从进程的视角、而不是 Nix 的视角来规定构建，着眼于*做什么*，而非*怎么做*。

## 哪些 derivation 可以被构建

实际上只有一部分 derivation 处于可构建状态。
特别地，只有[*resolved*（已解析）](./resolution.md)的 derivation 才能被构建。
也就是说，依赖其他 derivation 的 derivation 尚不能构建，因为那些其他 derivation 可能还没有被构建。
如果那些其他 derivation 确实都已构建，我们可以通过解析（resolve）该 derivation 来见证这一事实，把该 derivation 的全部输入引用转换为普通的存储路径。

> **注意**
>
> 注意 [input-addressing](derivation/outputs/input-address.md) 的 derivation 是以 improper 方式解析的。
> 如链接页面所讨论的，当前的 input-addressing 算法不遵守 derivation 的解析等价关系（\\(\\sim_\mathrm{Drv}\\))。
> 这意味着如果 Nix 以 proper 方式解析一个输入寻址的 derivation，解析后的 derivation 将具有不同的输入地址，违背预期。
> 因此 Nix 对该 derivation 进行 improper 解析，保留其原始的输入寻址输出路径，创建一个既是 resolved 的、又被指示在原本预期路径创建输出的无效 derivation。

## 构建器进程的环境

本节描述 [`builder`](./derivation/index.md#builder) 是如何被执行的。

> **实现细节**
>
> Nix 会阻止多个 [Nix 实例][Nix instance]同时执行同一个构建，例如通过获取独占的文件锁。

### 文件系统

构建器应当能访问一个受限的文件系统，其中只有特定的对象可用。
被呈现出来的最重要的文件是该（已解析）derivation 的输入（其他存储对象）。
此外，还会呈现一些其他文件。

#### Store 输入

构建器将面对这样一个文件系统：其中的 [store 目录][store directory path]包含输入的[闭包]。
特别地，考虑一个恰好只包含这个闭包的 store。
按照[在操作系统文件系统中呈现存储对象](./store-path.md#exposing)文档中规定的规则，这个 store 被呈现到文件系统。
这精确定义了构建器进程应当可见的 store 的文件系统布局。

> **注意**
>
> 历史上，由于操作系统文件系统虚拟化能力的限制，以及希望避免复制或移动文件，Nix 向构建器呈现了*至少*以下 store 内容，此外还可能呈现任意其他存储对象。
> 在所谓的*无沙箱*（unsandboxed）构建中，它至今仍可以这样做。
>
> 这类构建应当被视为不推荐的，但对于非捣乱的 derivation，其效果比想象中没那么糟。
> 这是因为存储路径相当不可预测，所以行为良好的程序不太可能偶然撞见一个它本不该知道的存储对象。
>
> 随着操作系统发展出更好的文件系统原语，多年来对禁用沙箱的需求已大大减少，这一趋势未来仍将继续。

输出被期望在该 store 目录中创建，就好像它们是有效的存储对象一样。
（在构建器执行期间它们只是文件，但在[处理输出](#processing-outputs)期间它们会被变成正式的存储对象。）
每个输出的[环境变量](#env-vars)指明了构建器应当把它们写到哪里；
Nix 确保在构建器运行时这些路径尚不存在。

> **注意**
>
> 在沙箱构建中，确保输出在 store 目录中不存在是轻而易举的。
> 在无沙箱构建中，总的来说这更难。
> 最坏的情况下，derivation 会被实际重写以改用不同的输出路径，之后再把这些输出重写回预期的输出路径。
> 在内容寻址的情形下，无论如何都需要重写；但在输入寻址的情形下，这是显著的退化，因为输入寻址的意义就在于通过预先知道输出路径来避免重写。

[realised]: @docroot@/glossary.md#gloss-realise
[closure]: @docroot@/glossary.md#gloss-closure
[store directory path]: ./store-path.md#store-directory-path

### 其他文件系统状态

- 构建器进程的当前工作目录将是一个全新的临时目录。
  进程启动时它最初是空的，只有少量输入文件例外：

  - 如果启用了 [`__structuredAttrs`](@docroot@/language/advanced-attributes.md#adv-attr-structuredAttrs)：会有 `.attrs.json`（以 JSON 表示的 derivation 属性）和 `.attrs.sh`（同一内容的 Bash 兼容渲染）。
    环境变量 `NIX_ATTRS_JSON_FILE` 和 `NIX_ATTRS_SH_FILE` 分别指向这两个文件。

  - 如果使用了 [`passAsFile`](@docroot@/language/advanced-attributes.md#adv-attr-passAsFile)（仅在不使用 `__structuredAttrs` 时）：对每个列出的属性名，会有一个文件 `.attr-<hash>`，其中 `<hash>` 是属性名的 [Nix32](@docroot@/protocols/nix32.md) 编码 SHA-256 哈希。
    环境变量 `<name>Path` 指向包含该属性值的文件。

  在沙箱构建中，该目录位于沙箱内一个确定性的路径（由 [`sandbox-build-dir`](@docroot@/command-ref/conf-file.md#conf-sandbox-build-dir) 设置控制，默认为 `/build`）。
  另请参见面向宿主侧位置的各 store 的 [`build-dir`](@docroot@/store/types/local-store.md#store-local-store-build-dir) 设置。

- 用于基本操作的基础设备节点（null 设备、随机数生成、作为伪终端的标准流）

  （伪终端严格来说并非必需，因为标准流只是被动记录日志，并不是为了交互。
  但它仍然有助于诱导程序输出更友好的日志，例如带颜色等。）

- 在 Linux 上：通过 `/proc` 提供的进程信息

- 最小的用户和组身份信息

- 仅限环回的网络配置，主机名设为 `localhost`

> **注意**
>
> 固定输出 derivation（fixed-output derivation）可以访问额外的操作系统状态，以便与外部世界通信，例如域名解析和 TLS 证书校验。
> 这是必需的，因为允许这些 derivation 访问网络，而常规 derivation 则被完全沙箱化。

### 环境变量 {#env-vars}

环境会被清空并设置为 derivation 属性，如上所述。

对大多数 derivation 类型而言，其中至少必须包含：

- 对 `outputs` 中声明的每个输出，设置相应的环境变量，指向该输出在 Nix store 中的预期路径。
  每个输出路径由所有构建输入的密码学哈希、`name` 属性和输出名拼接而成。
  （如果输出名是 `out`，则省略。）

此外，还设置了以下变量：

- `NIX_BUILD_TOP` 包含本次构建的临时目录路径。

- 同时，`TMPDIR`、`TEMPDIR`、`TMP`、`TEMP` 也被设为指向该临时目录。
  这是为了防止构建器不小心把临时文件写到其他任何地方。
  那样做可能被其他进程干扰。

- `PATH` 被设为 `/path-not-set`，以防止 shell 将其初始化为内置默认值。

- `HOME` 被设为 `/homeless-shelter`。
   （在没有沙箱的情况下，这会阻止程序用 `/etc/passwd` 之类的途径寻找用户的家目录，从而避免引入不纯性。）
   通常，当设置了 `HOME` 时，它就会被用作家目录的位置，即使它指向一个不存在的路径。

- `NIX_STORE` 被设为顶层 Nix [store 目录路径]（通常是 `/nix/store`）。

- 如果 derivation 的 `__structuredAttrs` 设为 `true`，则设置 `NIX_ATTRS_JSON_FILE` 与 `NIX_ATTRS_SH_FILE`。
  该行为的详细说明见[关于 structured attrs 的小节](@docroot@/language/advanced-attributes.md#adv-attr-structuredAttrs)。

### 参数

构建器会被传入 derivation 属性 `args` 所指定的参数。

## 处理输出

处理输出有两种方法。但首先，让我们介绍两种方法共同的要求。

无论使用哪种方法，每个输出都必须变成一个有效的存储对象。
这包括两个步骤：

- **规范化文件权限**

  文件必须符合[在操作系统文件系统中呈现](./file-system-object/os-file-system.md)一节所述的模型。
  例如，时间戳和权限会被规范化。

- [**计算引用**]{#scanning-for-references}

  Nix 通过查找每个输入的[摘要][store path digest]，扫描每个输出路径中对输入存储对象的[引用]。
  （扫描时忽略名称部分和 [store 目录路径]；一个输入的哈希部分，只要其后既不跟 `-`、其前也不接 `/`，仍然会被扫描为引用。）
  由于这些是潜在的运行时依赖，Nix 会把它们登记为出现它们的输出存储对象的引用。

  可以用 [*unsafe discard references*](derivation/outputs/index.md#unsafe-discard-references) 设置按输出禁用这种扫描。

### 传统（构建后）处理

在传统方法中，构建器进程退出时应当已为 derivation 应产出的每个输出留下文件。
这些文件必须经过处理，以变成真正的存储对象。
如果处理成功，这些存储对象就作为一次成功构建的（结果）与该 derivation 关联。

Nix 也会以同样的方式扫描输出之间的引用，因为输出之间允许互相引用。
各输出的引用必须构成一个[有向无环图](@docroot@/glossary.md#gloss-directed-acyclic-graph)。
（这不是针对输出的特殊限制；对所有存储对象的引用来说普遍如此。）

对于输出路径预先固定的 derivation（即 [input-addressing] derivation 或 [fixed content-addressing] derivation），构建期间会尽可能使用每个输出的实际最终存储路径。
而对于 [floating content-addressing] derivation，最终存储路径按定义无法预先得知。
因此必须改用草稿存储路径。
扫描会使用这些草稿路径，但随后任何包含此类扫描到的草稿路径的待成输出，都必须被重写为改用所论输出的最终（内容寻址的）路径。

除输出间引用外，在内容寻址的情形下，为支持自引用也需要重写。
一个输出可能包含其自身存储路径的摘要，这就是自引用。
安全的哈希函数不允许轻易计算支持"原生"自引用所需的准不动点，因此我们改用哨兵值替换所有本应作为自引用的地方，然后重写哨兵值为最终的存储路径摘要。
表面上，这种哈希后的重写破坏了内容地址，但由于自引用很容易识别，该重写可以被逆转以还原原始的被哈希数据，从而最终仍能校验内容地址。

此时，文件系统数据已处于规范形式，每个输出的有效无环引用数据也已计算完毕，于是这些输出作为正式的存储对象被加入 store。
此外，这些存储对象（至少在它们是[内容寻址][content-addressing]的情况下）可以在 [build trace] 中以成功构建记录的形式与该 derivation 关联。

> **实现细节**
>
> Nix 通常会在每次构建（无论成败）之后清理并删除临时构建目录。
> 然而构建器并不知道 Nix 是否这样做，因为它会在构建目录被清理之前就已退出，而且（构建失败后）再次运行时它也不会看到任何旧的构建目录。
> 可以指定 [`--keep-failed`](@docroot@/command-ref/opt-common.md#opt-keep-failed) 选项，在构建失败的情况下保留构建目录。

### 通过 IPC 并发处理

在这种方法中，构建器在构建期间通过进程间通信（IPC）与 Nix 交流。

> **实现细节**
>
> 当前实现 `builder-rpc-v0` 通过 Nix daemon 套接字的一种受限形式暴露其接口。
> 构建器既可以用自己对 Nix 协议的实现来使用它，也可以使用 `nix store add` 和 `nix store submit-output` 命令。
>
> 在其 [`requiredSystemFeatures`](@docroot@/language/advanced-attributes.md#adv-attr-requiredSystemFeatures) 集合中包含 `builder-rpc-v0` 的 derivation
> 将不会在其环境中收到输出路径，而是被期望用上述命令或协议提交所有输出。

构建器不是留下文件等 Nix 在退出后处理，而是显式请求 daemon 逐个创建存储对象，然后发送命令把输出名称分配给刚创建的存储对象。

对每个存储对象创建请求，引用扫描照常进行，但待扫描的潜在引用集合更大：既包括全部输入（和从前一样），也包括所有先前添加的存储对象。
这意味着，如果输出 `bar` 应当引用输出 `foo`，则应先创建 `foo`，再创建 `bar`。

所有被创建的存储对象都是内容寻址的（IPC 方式不支持输入寻址的输出）。
存储对象创建时，其内容地址存储路径会由 Nix 计算，并通过 IPC 响应消息返回。
随后构建器就知道在后续存储对象中应使用什么存储路径，才能让引用扫描捕获到它们。

这种总体做法有几个优点：

- **Nix 侧无需重写**

  对内容寻址的输出，构建器负责按引用顺序添加输出，在后添加的输出中使用先前添加时的存储路径。
  这避免了上文所述修正输出间引用时本会需要的脆弱重写。
  与 Nix 本身不同，构建器可以自由利用领域特定知识把事情做得更好。例如它可以

  - 解压、重写、再重新压缩 man 手册页，以免遗漏被压缩隐藏的引用。

  - 确保在为待签名数据（如 Apple 二进制文件）签名之前重写数据，以免误使任何签名失效。

- **流水线化**

  只需要部分输出（例如 "dev" 或 "headers" 输出）的下游构建可以在所有输出就绪之前就开始。
  Nix 尚未实现这一点，但它可以且应当实现。

这种方法的主要*缺点*是它尚不支持自引用。
与无环的输出间引用不同，自引用从根本上需要重写。
输出间引用的情形在传统方法中之所以是一个挑战，只是因为所有输出被同时提交；而自引用的情形则是根本性的挑战，原因在于哈希函数安全性的含义，如上所述。
无论批量的（传统）还是串行的（IPC）输出提交，都无法回避安全哈希函数的这一根本性质。
我们可以像传统构建后处理那样，仅为自引用添加这种重写支持，但我们尚未这样做，因为 IPC 方式的意义恰恰在于免除 Nix 以不健全的方式重写黑盒数据的任何义务。

[references]: ./store-object.md#references
[store path digest]: ./store-path.md#digest
[store object]: ./store-object.md
[Nix instance]: @docroot@/glossary.md#gloss-nix-instance
[content-addressing]: ./derivation/outputs/content-address.md
[input-addressing]: ./derivation/outputs/input-address.md
[fixed content-addressing]: ./derivation/outputs/content-address.md#fixed
[floating content-addressing]: ./derivation/outputs/content-address.md#floating
[build trace]: ./build-trace.md
