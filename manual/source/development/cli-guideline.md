# CLI guideline

## 目标

本文档旨在提供清晰的方向，**帮助设计令人愉悦的命令行**体验。文档包含了一系列需要遵循的 guideline，以确保一致且平易近人的用户体验。

## 概述

`nix` 命令为多个子命令提供了单一入口，这些子命令在软件项目的生命周期中为**开发者和系统管理员**提供帮助。我们尤其需要特别关注并帮助 Nix 的新用户。

# `COMMANDS` 的命名

措辞很重要。命名是可用性的重要组成部分。用户会经常与 Nix 交互，因此我们应当**以便于理解为出发点来命名**。

我们建议遵循[最小惊讶原则](https://en.wikipedia.org/wiki/Principle_of_least_astonishment)。这意味着你应该**绝不使用首字母缩写或缩略语**，除非它们已在其他工具中被广泛使用（例如 `nix init`）。如果命令名过长（> 10-12 个字符），那么缩短它是有意义的（例如
“prioritization” → “priority”）。

命令应当**遵循名词-动词的对话结构**。虽然名词-动词的格式从口语角度看似乎是颠倒的（即 `nix store copy` 与 `nix
copy store` 之对比），但它使我们能够按照用户思考完成一个动作的方式来组织命令（先分组，再命令）。

## 命名规则

规则通过限制你的选项来引导你。但并非所有情况都符合规则。在那些情况下，请在[附录 1：命令命名例外](#appendix-1-commands-naming-exceptions)中记录例外并给出原因。这些规则旨在迫使 Nix 开发者不仅审视眼前的命令，还要在其他 `nix` 命令的完整上下文中审视命令。

```shell
$ nix [<GROUP>] <COMMAND> [<ARGUMENTS>] [<OPTIONS>]
```

- `GROUP`、`COMMAND`、`ARGUMENTS` 和 `OPTIONS` 应为小写且使用单数形式。
- `GROUP` 应为**名词**。
- `COMMAND` 应为**动词**。
- `ARGUMENTS` 和 `OPTIONS` 在[*输入*一节](#input)中讨论。

## 分类

有些命令更重要，有些则不那么重要。虽然我们希望所有命令都做到完美，但我们只能投入有限的时间来测试和改进它们。

这种分类尝试按照对新用户的重要性，将命令划分为 3 个类别。新用户是最容易被糟糕的用户体验影响的群体。

- **主要命令**

  用于我们主要用例的命令，最有可能被新用户使用。我们期望在这些命令上注重细节，例如：

    - 正确使用[颜色](#colors)、[emoji](#special-unicode-characters)
      和[文本对齐](#text-alignment)。
    - 选项的[自动补全](#shell-completion)。
    - 显示[下一步可能操作](#next-steps)。
    - 在运行耗时的任务（如构建 / 下载）时展示一些[“提示”](#educate-the-user)，以教会用户 Nix 生态中有趣的知识点。
    - 尽可能把[帮助页面](#help-is-essential)写得最好，并指向外部文档和教程以获取更多信息。

  此类命令的例子：`nix init`、`nix develop`、`nix build`、`nix run`、
  ...

- **低频命令**

  对于低频使用的命令，我们期望的细节关注度较低，但仍需要一些：

    - 正确使用[颜色](#colors)、[emoji](#special-unicode-characters)
      和[文本对齐](#text-alignment)。
    - 选项的[自动补全](#shell-completion)。

  此类命令的例子：`nix edit`、`nix eval`、...

- **工具与脚本命令**

  暴露 `nix` 某些内部功能的命令，主要被其他脚本使用。

    - 选项的[自动补全](#shell-completion)。

  此类命令的例子：`nix store copy`、`nix hash base16`、`nix store
  ping`、...


# 帮助至关重要

帮助应当内建于你的命令行中，以便新用户在需要时能逐步发现新功能。

## 寻求帮助

由于用户寻求帮助没有标准方式，我们依赖于常用工具提供帮助的方式。我们以 `git` 为参考，凡有疑问时都把它视为首选方向。

规则如下：

- 通过 `--help` 或 `help` 命令展示帮助（例如 `nix` `--``help` 或
  `nix help`）。
- 对于非 COMMAND（例如 `nix` `--``help` 和 `nix store` `--``help`），我们**展示**最常见用例的**摘要**。摘要输出到 STDOUT，不使用任何 PAGER。
- 对于 COMMAND（例如 `nix init` `--``help` 或 `nix help init`），我们显示该命令的 man 页面。默认使用 PAGER（与 `git` 相同）。
- 摘要或 man 页面的结尾应有一个 URL，指向更详细文档的在线版本。
- 摘要和 man 页面的结构应与 `git` 相同。

## 预判何时需要帮助

比要求用户主动寻求帮助更好的做法，是预判并预测用户何时可能需要帮助。可能是因为可发现性不足、输入有拼写错误，或者仅仅是借此机会教给用户一些有趣但不太显眼的细节。

### Shell 补全

这种帮助方式最为常见，几乎被用户视为理所当然。我们需要为 `bash`、`zsh` 和 `fish` **提供最佳的 shell 补全**。

补全需要**具备上下文感知能力**，也就是说当用户输入：

```shell
$ nix build n<TAB>
```

时，我们需要显示以 `n` 开头的 flake 列表。

### 错误输入

众所周知，人类总是在犯错。当出现拼写错误——无论有意还是无意——时，我们应当提示最接近的可能选项，或指向能教育用户避免同样错误的文档。这里有几个例子：

在第一个例子中，我们提示用户输入了错误的命令名：


```shell
$ nix int
------------------------------------------------------------------------
  Error! Command `int` not found.
------------------------------------------------------------------------
  Did you mean:
    |> nix init
    |> nix input
```

有时用户会犯错，可能是拼写错误，也可能仅仅因为可发现性不足。我们对这类情况的处理需要具备上下文敏感性。


```shell
$ nix init --template=template#python
------------------------------------------------------------------------
  Error! Template `template#python` not found.
------------------------------------------------------------------------
Initializing Nix project at `/path/to/here`.
      Select a template for you new project:
          |> template#python
             template#python-pip
             template#python-poetry
```

### 下一步

向新手展示可能的下一步以及使用 Nix 的常规开发工作流，其价值无可估量。例如：


```shell
$ nix init --template=template#python
Initializing project `template#python`
          in `/home/USER/dev/new-project`

  Next steps
    |> nix develop   -- to enter development environment
    |> nix build     -- to build your project
```

### 教育用户

我们应当抓住一切机会**教育用户**，但同时必须**极其小心，避免惹恼用户**。在乐于助人和令人厌烦之间只有一线之隔。

教育用户的一个例子是在用户等待时提供*提示*。

```shell
$ nix build
    Started building my-project 1.2.3
 Downloaded python3.8-poetry 1.2.3 in 5.3 seconds
 Downloaded python3.8-requests 1.2.3 in 5.3 seconds
------------------------------------------------------------------------
      Press `v` to increase logs verbosity
         |> `?` to see other options
------------------------------------------------------------------------
      Learn something new with every build...
         |> See last logs of a build with `nix log --last` command.
------------------------------------------------------------------------
  Evaluated my-project 1.2.3 in 14.43 seconds
Downloading [12 / 200]
         |> firefox 1.2.3 [#########>       ] 10Mb/s | 2min left
   Building [2 / 20]
         |> glibc 1.2.3 -> buildPhase: <last log line>
------------------------------------------------------------------------
```

输出中的 **Learn** 部分就是教育用户的地方。你应该只在确知构建会耗时较久时才显示它，避免打扰那些构建只需几秒钟的用户。

每一个这样的功能都应当经过严格的评审和测试，以收集尽可能多的反馈并打磨每一个细节。如果做得好，这可以成为新手和高级用户都会喜爱的出色功能；但如果不完美，它会惹恼用户并留下坏印象。

# 输入

命令的输入通过 `ARGUMENTS` 和 `OPTIONS` 提供。

`ARGUMENTS` 表示函数的必需输入。当选择使用 `ARGUMENTS` 而非 `OPTIONS` 时，请注意随之而来的缺点：

- 用户需要记住 `ARGUMENTS` 的顺序。如果只有一个 `ARGUMENT`，这不是问题。
- 使用 `OPTIONS` 可以提供好得多的自动补全。
- 使用 `OPTIONS` 可以提供好得多的错误信息。
- 使用 `OPTIONS` 意味着要多敲一些键。

我们并不反对使用 `ARGUMENTS`，只是希望每位开发者都权衡其缺点并做出明智选择。

## `OPTIONS` 的命名

除了 `COMMANDS` 命名一节中提到的规则外，唯一的命名约定是标志（flag）的命名。

标志是 `OPTION` 的一种，表示可以打开或关闭的选项。可以说**标志是布尔类型的** `**OPTION**`。

以下是标志 `OPTIONS` 的几个例子：

- `--colors` 与 `--no-colors`（在输出中显示颜色）
- `--emojis` 与 `--no-emojis`（在输出中显示 emoji）

## 未提供输入时进行提示

对于*主要命令*（[按分类](#classification)而言），我们希望命令提升可能输入的可发现性。新用户很可能不知道哪些 `ARGUMENTS` 和 `OPTIONS` 是必需的，也不知道这些选项有哪些可能的取值。

如果用户未提供输入或提供了错误的输入，与其显示错误，不如向用户提示，让其查找并选择正确的输入（见示例）。

当 TTY 未连接到 STDIN 时，当然无需提示。这意味着脚本无需处理提示，而只需处理错误。

适合使用提示并为用户提供交互式选择的场景


```shell
$ nix init
Initializing Nix project at `/path/to/here`.
      Select a template for you new project:
          |> py
             template#python-pip
             template#python-poetry
             [ Showing 2 templates from 1345 templates ]
```

另一个适合添加提示的场景是**危险操作的确认对话框**。例如，当通过 `OPTIONS` 或
`flake.nix` 添加新的 substitutor 时，我们应当（首次）进行提示，让用户确认将要发生什么。


```shell
$ nix build --option substitutors https://cache.example.org
------------------------------------------------------------------------
  Warning! A security related question needs to be answered.
------------------------------------------------------------------------
  The following substitutors will be used to in `my-project`:
    - https://cache.example.org

  Do you allow `my-project` to use above mentioned substitutors?
    [y/N] |> y
```

# 输出

终端输出在很多方面都相当受限，这更应当促使我们深入思考用户体验。与任何设计一样，输出是在简洁与详尽之间、在帮助新手与不打扰高级用户之间的折中。因此，明确优先级非常重要。

Nix 命令行首先应当以新手为出发点来设计。但用户不会永远是新手，曾经有用的东西可能很快变得令人厌烦。在这份 guideline 中，我们没有一条黄金法则能让划清界限、找到最佳折中变得更容易。

我们鼓励的是**构建原型**、进行一些**用户测试**并收集**反馈**，然后重复这个循环几次。

先设计*快乐路径*，只有在打磨完善之后，再继续处理**边缘情况**（错误的处理与展示、某些 `OPTIONS` 对输出的改变等……）

## 遵循最佳实践

不用说，Nix 必须做一个好公民，遵循命令行的最佳实践。

简而言之：**STDOUT 用于输出，STDERR 用于（面向人类的）消息。**

STDOUT 和 STDERR 为你提供了一种向用户输出消息的方式，同时也允许用户将内容重定向到文件。例如：

```shell
$ nix build > build.txt
------------------------------------------------------------------------
  Error! Attribute `bin` missing at (1:94) from string.
------------------------------------------------------------------------

  1| with import <nixpkgs> { }; (pkgs.runCommandCC or pkgs.runCommand) "shell" { buildInputs = [ (surge.bin) ]; } ""
```

由于这条警告位于 STDERR，它最终不会进入文件中。

不过，STDERR 上的内容并非都是错误。例如，你可以运行 `nix
build` 并把日志收集到文件中，同时仍能看到进度。

```
$ nix build > build.txt
  Evaluated 1234 files in 1.2 seconds
 Downloaded python3.8-poetry 1.2.3 in 5.3 seconds
 Downloaded python3.8-requests 1.2.3 in 5.3 seconds
------------------------------------------------------------------------
      Press `v` to increase logs verbosity
         |> `?` to see other options
------------------------------------------------------------------------
      Learn something new with every build...
         |> See last logs of a build with `nix log --last` command.
------------------------------------------------------------------------
  Evaluated my-project 1.2.3 in 14.43 seconds
Downloading [12 / 200]
         |> firefox 1.2.3 [#########>       ] 10Mb/s | 2min left
   Building [2 / 20]
         |> glibc 1.2.3 -> buildPhase: <last log line>
------------------------------------------------------------------------
```

## 错误（进行中）

**TODO**：在我们为*快乐路径*完成实现之后，再考虑如何呈现错误。

## 不只是面向人类

简洁的、机器可读的输出格式同样有用，但不应妨碍打造美观的 CLI 输出。必要时，命令应提供 `--json` 标志，让用户可以轻松解析 CLI 输出并编写脚本。

当 STDOUT 上未检测到 TTY 时，我们应移除所有设计元素（无颜色、无 emoji，使用 ASCII 代替 Unicode 符号）。当 STDERR 上未检测到 TTY 时亦然。此时不应显示进度 / 状态区块，而只打印警告和错误。

## 与用户对话

CLI 并不总是清楚地表明某个操作已经发生。对于用户执行的每个操作，你的 CLI 都应给出平等且恰当的回应，清楚地突出刚刚发生了什么。例如：

```shell
$ nix build
 Downloaded python3.8-poetry 1.2.3 in 5.3 seconds
 Downloaded python3.8-requests 1.2.3 in 5.3 seconds
...
   Success! You have successfully built my-project.
$
```

上面的命令清楚地表明命令已成功完成。而对于 `nix build` 这样可能需要一些时间才能完成的命令，同样重要的是显示命令已经开始执行。

## 文本对齐

文本对齐是头号设计元素，它使所有 Nix 命令呈现为一个家族，而不是拼凑在一起的独立工具。

我们应当遵循的格式是：

```shell
$ nix COMMAND
   VERB_1 NOUN and other words
  VERB__1 NOUN and other words
       |> Some details
```

从上面的示例中可以总结出几条规则：

- 每行应至少以一个空格开头。
- 第一个词应是动词，并且必须右对齐。
- 第二个词应是名词，并且必须左对齐。
- 如果找不到合适的动词 / 名词配对，别担心，尽量让用户易于理解即可。
- 每行的更多细节可以用 `|>` 字符提供，在对齐文本时它充当第一个词

别忘了，你还应当在关闭颜色和 emoji（`--no-colors --no-emojis`）的情况下测试终端输出。

## 暗色 / 亮色

在对比了几个使用不同配色方案的终端之后，我们**建议避免使用暗淡文本**。在许多终端与配色方案的组合下，它与其余文本的差异非常小。有时差异甚至难以察觉，因此依赖它没有太大意义。

**亮色文本在各种终端和配色方案中的支持要好得多**。大多数时候，其差异给人的感觉就像是亮色文本被加粗了。

## 颜色

社会早已让人类习惯于把特定含义与特定颜色关联起来。虽然含义并非普适，但一组简单的颜色被用来表达基本的情绪。

可用于输出的颜色：

- 红色 = 错误、危险、停止
- 绿色 = 成功、良好
- 黄色 / 橙色 = 谨慎前行、警告、进行中
- 蓝色 / 品红 = 稳定、平静

颜色虽好，但当命令行被机器使用（在自动化脚本中）时，你应当去掉颜色。应当有一个全局的 `--no-colors` 选项来移除颜色。

## 特殊（Unicode）字符

大多数终端对 Unicode 字符有良好支持，你应当默认在输出中使用它们。但始终要准备一个仅用 ASCII 字符实现的备用方案，它将在传入 `--ascii` 选项时被使用。请确保你也在没有 Unicode 字符的情况下测试输出

比起展示各种不同的 Unicode 字符，更重要的是**为特定情形建立一套统一的字符集合**。

## Emoji

Emoji 比文本、颜色和特殊字符更能传递情绪。

我们建议**把 emoji 的数量保持在最低限度**。这将使每个 emoji 更加醒目。

鉴于并非所有人都喜欢 emoji，我们应提供 `--no-emojis` 选项来禁用它们。请确保你也在没有 emoji 的情况下测试输出。

## 表格

所有列出某种数据的命令都可以用某种形式的表格实现。重要的是，输出的每一行都是一条单独的数据“条目”。绝不要输出表格边框。边框既嘈杂，也给使用 `grep` 等其他工具进行解析带来巨大痛苦。

注意屏幕宽度。默认只显示几列并附带表头；如需更多列，可以通过以下选项操作表格：

- `--no-headers`：默认显示列标题，但允许隐藏它们。
- `--columns`：以逗号分隔的待添加列名列表。
- `--sort`：允许按列排序，同时支持倒序和多列排序。

## 交互式输出

选择交互式输出是为了在新手和高级用户之间取得平衡。默认输出面向新手，但只需几次按键，就可以切换为高级的自省工具。

### 进度

对于运行时间较长的命令，我们应提供进度概览。
这在 `nix build` 的示例中体现得最为明显：

```shell
$ nix build
    Started building my-project 1.2.3
 Downloaded python3.8-poetry 1.2.3 in 5.3 seconds
 Downloaded python3.8-requests 1.2.3 in 5.3 seconds
------------------------------------------------------------------------
      Press `v` to increase logs verbosity
         |> `?` to see other options
------------------------------------------------------------------------
      Learn something new with every build...
         |> See last logs of a build with `nix log --last` command.
------------------------------------------------------------------------
  Evaluated my-project 1.2.3 in 14.43 seconds
Downloading [12 / 200]
         |> firefox 1.2.3 [#########>       ] 10Mb/s | 2min left
   Building [2 / 20]
         |> glibc 1.2.3 -> buildPhase: <last log line>
------------------------------------------------------------------------
```

### 搜索

当有多个选项可供选择时，使用类似 `fzf` 的模糊搜索。

```shell
$ nix init
Initializing Nix project at `/path/to/here`.
      Select a template for you new project:
          |> py
             template#python-pip
             template#python-poetry
             [ Showing 2 templates from 1345 templates ]
```

### 提示

在某些情况下，我们需要提示用户并告知用户即将发生什么。

```shell
$ nix build --option substitutors https://cache.example.org
------------------------------------------------------------------------
  Warning! A security related question needs to be answered.
------------------------------------------------------------------------
  The following substitutors will be used to in `my-project`:
    - https://cache.example.org

  Do you allow `my-project` to use above mentioned substitutors?
    [y/N] |> y
```

## 详细程度（verbosity）

有多种方式可以控制输出的详细程度。

详细程度级别包括：

- `ERROR`（级别 0）
- `WARN`（级别 1）
- `NOTICE`（级别 2）
- `INFO`（级别 3）
- `TALKATIVE`（级别 4）
- `CHATTY`（级别 5）
- `DEBUG`（级别 6）
- `VOMIT`（级别 7）

命令启动时的默认级别是 `ERROR`。提高详细程度的最简单方式是叠加 `-v` 选项（例如：`-vvv == level 3 == INFO`）。另外还有两个快捷方式：`--debug` 以 `DEBUG` 详细程度级别运行，`--quiet` 以 `ERROR` 详细程度级别运行。

----------

# 附录 1：命令命名例外

`nix init` 和 `nix repl` 已深入人心
