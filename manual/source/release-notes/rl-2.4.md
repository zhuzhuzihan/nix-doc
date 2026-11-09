# Release 2.4 (2021-11-01)

这是两年多以来的首个发布版本，是自 2.3 发布以来 195 位贡献者提交的 2800 多个 commit 的成果。

## 亮点

* Nix 的 **错误消息** 得到了大幅改进。例如，求值错误现在会指出错误发生的位置：

  ```
  $ nix build
  error: undefined variable 'bzip3'

         at /nix/store/449lv242z0zsgwv95a8124xi11sp419f-source/flake.nix:88:13:

             87|           [ curl
             88|             bzip3 xz brotli editline
               |             ^
             89|             openssl sqlite
  ```

* **`nix` 命令** 经过了大量打磨，如今几乎已与旧的命令行界面（`nix-*` 命令）达到功能对等。它的目标是比旧 CLI [更现代、更一致、更好用](../development/cli-guideline.md)。它仍被标记为实验性，但其界面在未来的发布中应该不会再有大的变化。

* **Flakes** 是一种新的格式，用于以更易发现、可组合、一致且可复现的方式打包基于 Nix 的项目。一个 flake 就是一个仓库或 tarball，其中包含一个名为 `flake.nix` 的文件，该文件指定对其他 flake 的依赖，并返回任意 Nix 资产，例如软件包、Nixpkgs overlays、NixOS 模块或 CI 测试。新的 `nix` CLI 主要围绕 flake 构建；例如，`nix run nixpkgs#hello` 这样的命令会运行来自 `nixpkgs` flake 的 `hello` 应用。

  Flakes 目前被标记为实验性。入门介绍请参阅[这篇博客文章](https://www.tweag.io/blog/2020-05-25-flakes/)。关于 flake 语法和语义的详细信息，请参阅 [`nix flake` 手册页](../command-ref/new-cli/nix3-flake.md)。

* Nix 的 store 现在支持 **内容寻址（content-addressed）**，即存储路径中的哈希部分是该路径内容的哈希。此前 Nix 只能构建 **输入寻址（input-addressed）** 的存储路径，其哈希根据 derivation（派生）依赖图计算得出。内容寻址可以实现去重、构建系统中的提前截断（early cutoff）以及非特权闭包复制。这仍是[一项实验特性](https://discourse.nixos.org/t/content-addressed-nix-call-for-testers/12881)。

* Nix 手册已被转换为 Markdown，使贡献更加容易。此外，每个 `nix` 子命令现在都有手册页，记录了每一个选项。

* 新增一项设置，允许有选择地启用 **实验特性**。这使我们能够更快地把不稳定特性合入 Nix，并进行更频繁的发布。

## 其他特性

* 有许多新的 `nix` 子命令：

  - `nix develop` 旨在取代 `nix-shell`。它具有若干新特性：

    * 它会自动把输出环境变量（如 `$out`）设置为可写的位置（如 `./outputs/out`）。

    * 它可以把环境保存到一个 profile 中。这对离线工作很有用。

    * 它可以直接运行特定的阶段（phase）。例如，`nix develop --build` 会运行 `buildPhase`。

    - 它允许通过 `--redirect` 标志把 Nix store 中的依赖「重定向」到任意目录。如果你想同时修改一个软件包 *和* 它的某些依赖，这会很有用。

  - `nix print-dev-env` 打印某个 derivation 定义的环境变量和 bash 函数。这对使用 bash 以外 shell 的用户很有用（尤其是配合 `--json`）。

  - `nix shell` 此前名为 `nix run`，旨在取代 `nix-shell -p`，但没有 `stdenv` 的开销。它只是启动一个 shell，其中某些软件包已被加入 `$PATH`。

  - `nix run`（不要与已更名为 `nix shell` 的旧子命令混淆）会运行一个「应用（app）」——即指定了要运行命令的 flake 输出——或某个软件包中的同名程序。例如，`nix run nixpkgs#hello` 会运行 `nixpkgs` 中 `hello` 软件包的 `hello` 程序。

  - `nix flake` 是 flake 相关操作的容器，例如创建新的 flake、查询 flake 的内容或更新 flake 锁文件。

  - `nix registry` 允许你查询和更新 flake 注册表（registry），它把诸如 `nixpkgs` 这样的标识符映射到具体的 flake URL。

  - `nix profile` 旨在取代 `nix-env`。它的主要优势是会记录已安装软件包的来源信息（例如一个软件包确切来自哪个 flake 版本）。它还有一些实用的子命令：

    * `nix profile history` 显示 profile 的每个版本之间添加、升级或移除了哪些软件包。

    * `nix profile diff-closures` 显示 profile 各版本闭包之间的变化，让你能够发现依赖的增删或体积变化。

    **警告**：一个 profile 在用 `nix profile` 更新之后，就无法再配合 `nix-env` 使用了。

  - `nix store diff-closures` 显示两个存储路径的闭包之间的差异，包括闭包中依赖的版本和大小。

  - `nix store make-content-addressable` 将任意闭包重写为内容寻址形式。这样的路径可以在不需要签名的情况下复制到其他 store。

  - `nix bundle` 使用 [`nix-bundle` 程序](https://github.com/matthewbauer/nix-bundle)把一个闭包转换为自解压可执行文件。

  * 还有其他各种旧 CLI 的替代命令，例如 `nix store gc`、`nix store delete`、`nix store repair`、`nix nar dump-path`、`nix store prefetch-file`、`nix store prefetch-tarball`、`nix key` 和 `nix daemon`。

* Nix 现在为 flake 输出提供了 **求值缓存（evaluation cache）**。例如，第二次执行 `nix run nixpkgs#firefox` 命令时不需要再对 `firefox` 属性求值，因为它已经在求值缓存中。这得益于 flake 封闭的（hermetic）求值模型。

  中间结果不会被缓存。

* 新的 `--offline` 标志会禁用 substituter，并把所有本地缓存的 tarball 和仓库视为最新。

* 新的 `--refresh` 标志会把所有本地缓存的 tarball 和仓库视为过期。

* 许多 `nix` 子命令现在都有 `--json` 选项，用于产生机器可读的输出。

* `nix repl` 新增了 `:doc` 命令，用于显示内置函数的文档（例如 `:doc builtins.map`）。

* 二进制缓存 store 现在有了 `index-debug-info` 选项，可为 DWARF debuginfo 文件建立索引，供 [`dwarffs`](https://github.com/edolstra/dwarffs) 使用。

* 为支持 flake，Nix 现在有一种可扩展的源码树抓取机制。目前它有以下后端：

  * Git 仓库

  * Mercurial 仓库

  * GitHub 和 GitLab 仓库（一种优化，抓取速度比 Git 更快）

  * Tarball

  * 任意目录

  抓取器基础设施通过 flake 输入规范和 `fetchTree` 内置函数暴露。

* **语言变更**：唯一的新语言特性是路径中现在可以使用反引用（antiquotation），例如用 `./${foo}` 代替 `./. + foo`。

* **新的内置函数**：

  - `builtins.fetchTree` 允许使用抓取器基础设施支持的任意后端抓取源码树。它涵盖了 `fetchGit`、`fetchMercurial` 和 `fetchTarball` 等现有内置函数的功能。

  - `builtins.getFlake` 抓取一个 flake 并返回其输出属性。不要在 flake 内部使用此函数！请改用 flake 输入。

  - `builtins.floor` 和 `builtins.ceil` 分别对浮点数向下和向上取整。

* 对递归 Nix 的实验性支持。这意味着 Nix derivation 现在可以调用 Nix 来构建其他 derivation。它尚未达到稳定状态，也缺乏完善的[文档](https://github.com/NixOS/nix/commit/c4d7c76b641d82b2696fef73ce0ac160043c18da)。

* 新的实验特性 `no-url-literals` 会禁用 URL 字面量。这有助于实现 [RFC 45](https://github.com/NixOS/rfcs/pull/45)。

* Nix 现在使用 `libarchive` 来解压和解包 tarball 与 zip 文件，因此不再需要 `tar`。

* substituter 的优先级现在可以通过 `priority` substituter 设置覆盖（例如 `--substituters 'http://cache.nixos.org?priority=100 daemon?priority=10'`）。

* `nix edit` 现在支持非 derivation 属性，例如 `nix edit .#nixosConfigurations.bla`。

* `nix` 命令现在为 `bash`、`zsh` 和 `fish` 提供命令行补全。由于获取补全的支持内置在 `nix` 中，因此很容易为其他 shell 添加支持。

* 新的 `--log-format` 标志用于选择 Nix 输出的外观。默认为简洁的进度指示器。另有一种供其他程序使用的 `internal-json` 输出格式。

* `nix eval` 新增了 `--apply` 标志，可将一个函数应用到求值结果上。

* `nix eval` 新增了 `--write-to` 标志，允许它把一个由字符串叶子组成的嵌套属性集写入对应的目录树。

* 内存方面的改进：许多向 store 添加路径或在 store 之间复制路径的操作现在以恒定内存运行。

* 许多 `nix` 命令现在支持 `--derivation` 标志，可对 `.drv` 文件本身而非其输出进行操作。

* 新增了一种名为 `dummy://` 的 store，它不支持构建或添加路径。当你想使用 Nix 求值器但没有 Nix store 时，这会很有用。

* `ssh-ng://` store 现在允许在远程进行 substitute，就像 `ssh://` 早已支持的那样。

* 当以带省略号（ellipsis）的方式自动调用函数时，现在会传递所有参数。

* `nix-shell` 的新特性：

  - 如果设置了 `NIX_SHELL_PRESERVE_PROMPT`，它会保留 `PS1` 环境变量。

  - 使用 `-p` 时，它会把所有 `--arg` 作为 Nixpkgs 参数传递。

  - 支持结构化属性（structured attributes）。

* `nix-prefetch-url` 新增了 `--executable` 标志。

* 在 `x86_64` 系统上，[`x86_64` 微架构级别](https://lwn.net/Articles/844831/)会被映射为额外的系统类型（例如 `x86_64-v1-linux`）。

* 新的 `--eval-store` 标志允许你在求值时使用与构建或存放构建结果不同的 store。这主要在你想要查询某个内容是否存在于只读 store（例如二进制缓存）中时有用：

  ```
  # nix path-info --json --store https://cache.nixos.org \
    --eval-store auto nixpkgs#hello
  ```

  （这里 `auto` 表示本地 store。）

* Nix daemon 新增了一种低延迟的闭包复制机制。这在 `ssh-ng://` 等远程 store 上构建时很有用。

* 插件现在可以注册 `nix` 子命令。

* `nix-store --add-root` 的 `--indirect` 标志已成为空操作。从现在起 `--add-root` 总是生成间接 GC root。

## 不兼容变更

* `nix` 命令现在被标记为一项实验特性。这意味着如果你想使用它，需要在 `nix.conf` 中添加

  ```
  experimental-features = nix-command
  ```

  或者在命令行上传递 `--extra-experimental-features nix-command`。

* `nix` 命令不再支持引用 channel 中软件包的语法。这意味着以下写法不再有效：

  ```console
  nix build nixpkgs.hello # Nix 2.3
  ```

  作为替代，你可以使用 `#` 语法从 flake 中选择一个软件包，例如：

  ```console
  nix build nixpkgs#hello
  ```

  或者，如果你想使用 `NIX_PATH` 环境变量中的 `nixpkgs` channel：

  ```console
  nix build -f '<nixpkgs>' hello
  ```

* 旧的 `nix run` 已更名为 `nix shell`，同时新增了一个运行默认命令的 `nix run`。因此，不再使用

  ```console
  nix run nixpkgs.hello -c hello # Nix 2.3
  ```

  而应使用

  ```console
  nix shell nixpkgs#hello -c hello
  ```

  或者，如果要运行的命令与软件包同名，直接使用

  ```console
  nix run nixpkgs#hello
  ```

* 现在禁止通过出现在任何命令（包括 `nix` 的子命令）的第一个非标志参数之后的命令行标志来修改 `plugin-files` 设置。例如，`nix-instantiate default.nix --plugin-files ""` 现在必须改为 `nix-instantiate --plugin-files "" default.nix`。

* 我们不再发布源码 tarball。如果你想从源码构建，请基于 Git 仓库中的 tag 构建。

## Contributors（贡献者）

本次发布由以下贡献者共同完成：
Adam Höse,
Albert Safin,
Alex Kovar,
Alex Zero,
Alexander Bantyev,
Alexandre Esteves,
Alyssa Ross,
Anatole Lucet,
Anders Kaseorg,
Andreas Rammhold,
Antoine Eiche,
Antoine Martin,
Arnout Engelen,
Arthur Gautier,
aszlig,
Ben Burdette,
Benjamin Hipple,
Bernardo Meurer,
Björn Gohla,
Bjørn Forsman,
Bob van der Linden,
Brian Leung,
Brian McKenna,
Brian Wignall,
Bruce Toll,
Bryan Richter,
Calle Rosenquist,
Calvin Loncaric,
Carlo Nucera,
Carlos D'Agostino,
Chaz Schlarp,
Christian Höppner,
Christian Kampka,
Chua Hou,
Chuck,
Cole Helbling,
Daiderd Jordan,
Dan Callahan,
Dani,
Daniel Fitzpatrick,
Danila Fedorin,
Daniël de Kok,
Danny Bautista,
DavHau,
David McFarland,
Dima,
Domen Kožar,
Dominik Schrempf,
Dominique Martinet,
dramforever,
Dustin DeWeese,
edef,
Eelco Dolstra,
Ellie Hermaszewska,
Emilio Karakey,
Emily,
Eric Culp,
Ersin Akinci,
Fabian Möller,
Farid Zakaria,
Federico Pellegrin,
Finn Behrens,
Florian Franzen,
Félix Baylac-Jacqué,
Gabriella Gonzalez,
Geoff Reedy,
Georges Dubus,
Graham Christensen,
Greg Hale,
Greg Price,
Gregor Kleen,
Gregory Hale,
Griffin Smith,
Guillaume Bouchard,
Harald van Dijk,
illustris,
Ivan Zvonimir Horvat,
Jade,
Jake Waksbaum,
jakobrs,
James Ottaway,
Jan Tojnar,
Janne Heß,
Jaroslavas Pocepko,
Jarrett Keifer,
Jeremy Schlatter,
Joachim Breitner,
Joe Pea,
John Ericson,
Jonathan Ringer,
Josef Kemetmüller,
Joseph Lucas,
Jude Taylor,
Julian Stecklina,
Julien Tanguy,
Jörg Thalheim,
Kai Wohlfahrt,
keke,
Keshav Kini,
Kevin Quick,
Kevin Stock,
Kjetil Orbekk,
Krzysztof Gogolewski,
kvtb,
Lars Mühmel,
Leonhard Markert,
Lily Ballard,
Linus Heckemann,
Lorenzo Manacorda,
Lucas Desgouilles,
Lucas Franceschino,
Lucas Hoffmann,
Luke Granger-Brown,
Madeline Haraj,
Marwan Aljubeh,
Mat Marini,
Mateusz Piotrowski,
Matthew Bauer,
Matthew Kenigsberg,
Mauricio Scheffer,
Maximilian Bosch,
Michael Adler,
Michael Bishop,
Michael Fellinger,
Michael Forney,
Michael Reilly,
mlatus,
Mykola Orliuk,
Nathan van Doorn,
Naïm Favier,
ng0,
Nick Van den Broeck,
Nicolas Stig124 Formichella,
Niels Egberts,
Niklas Hambüchen,
Nikola Knezevic,
oxalica,
p01arst0rm,
Pamplemousse,
Patrick Hilhorst,
Paul Opiyo,
Pavol Rusnak,
Peter Kolloch,
Philipp Bartsch,
Philipp Middendorf,
Piotr Szubiakowski,
Profpatsch,
Puck Meerburg,
Ricardo M. Correia,
Rickard Nilsson,
Robert Hensing,
Robin Gloster,
Rodrigo,
Rok Garbas,
Ronnie Ebrin,
Rovanion Luckey,
Ryan Burns,
Ryan Mulligan,
Ryne Everett,
Sam Doshi,
Sam Lidder,
Samir Talwar,
Samuel Dionne-Riel,
Sebastian Ullrich,
Sergei Trofimovich,
Sevan Janiyan,
Shao Cheng,
Shea Levy,
Silvan Mosberger,
Stefan Frijters,
Stefan Jaax,
sternenseemann,
Steven Shaw,
Stéphan Kochen,
SuperSandro2000,
Suraj Barkale,
Taeer Bar-Yam,
Thomas Churchman,
Théophane Hufschmitt,
Timothy DeHerrera,
Timothy Klim,
Tobias Möst,
Tobias Pflug,
Tom Bereknyei,
Travis A. Everett,
Ujjwal Jain,
Vladimír Čunát,
Wil Taylor,
Will Dietz,
Yaroslav Bolyukin,
Yestin L. Harrison,
YI,
Yorick van Pelt,
Yuriy Taraday 以及
zimbatm。
