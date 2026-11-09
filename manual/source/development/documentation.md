# 贡献文档

对文档的改进非常受欢迎，也是着手为 Nix 做贡献的好方式。

你可以通过以下方式提供帮助：
- 处理[与文档相关的未关闭 issue](https://github.com/NixOS/nix/issues?q=is%3Aissue+is%3Aopen+label%3Adocumentation)
- 评审[与文档相关的 pull request](https://github.com/NixOS/nix/pulls?q=is%3Apr+is%3Aopen+label%3Adocumentation)

对文档构建配置进行渐进式重构，使其更快或更易于理解和维护，同样受欢迎。

## 构建手册

从头构建手册：

```console
nix-build -E '(import ./.).packages.${builtins.currentSystem}.nix.doc'
```

或者

```console
nix build .#nix-manual
```

然后打开 `./result/share/doc/nix/manual/index.html`。


要增量构建手册，请[进入开发 shell](./building.md) 并在配置时启用 `doc-gen`：

**如果使用交互式 `nix develop`：**

```console
$ nix develop
$ mesonFlags="$mesonFlags -Ddoc-gen=true" mesonConfigurePhase
```

**如果使用 direnv：**

```console
$ direnv allow
$ bash -c 'source $stdenv/setup && mesonFlags="$mesonFlags -Ddoc-gen=true" mesonConfigurePhase'
```

然后构建手册：

```console
$ cd build
$ meson compile manual
```

HTML 手册将生成在 `build/src/nix-manual/manual/index.html`。

## 风格指南

本风格指南的目标是使得
- 手册易于搜索和浏览以获取相关信息
- 文档源码易于编辑
- 文档变更易于评审

你会发现目前这套规范还没有被一致地贯彻。
在对现有文档进行增改时，请遵循本指南。
除非变更可以通过程序化手段实施且易于验证，否则不要进行大规模改动。

### 语言

本手册是[参考文档](https://diataxis.fr/reference/)。
其典型使用模式是查找孤立的信息片段。
因此，它应当力求正确、一致、完整，并且一目了然、易于导航。

- 力求清晰和简洁。

  请花时间阅读[平实语言指南](https://www.plainlanguage.gov/guidelines/)以了解细节。

- 如实描述主题。

  尤其是，不要做价值判断或推荐。
  如有疑问，请检查代码或添加测试。

- 提供完整且精简的示例，并对它们加以解释。

  读者应当能够原样尝试示例，并得到与手册中所示相同的结果。
  始终用文字描述给定示例做了什么。

  非平凡的示例可能需要额外的解释，尤其是当它们用到了给定上下文之外的概念时。

- 始终在正文中解释代码示例。

  代码示例中的注释要非常节制地使用，例如仅用于突出某个特定方面。
  读者在浏览查找信息时往往只是扫视大量代码。

  尤其是初学者，会觉得阅读看起来复杂的代码很费力，因此可能干脆避开它。

  如果一段代码示例似乎需要大量行内解释，请考虑换成更简单的示例。
  如果做不到，就把示例拆分为多个部分，分别解释，最后再展示合并后的结果。
  这应当是最后手段，因为那相当于就该主题写一篇[教程](https://diataxis.fr/tutorials/)。

- 使用英式英语。

  这是一个有些武断的选择，目的是强制保持一致性，同时考虑到大多数 Nix 用户和开发者来自欧洲。

### 链接与锚点

参考文档必须可以按任意顺序阅读。
不能指望读者具备关于 Nix 的任何特定前置知识。
虽然目录可以提供指引、全文搜索可以提供帮助，但他们最有可能通过合理的交叉引用找到所需内容。

- 链接到技术术语

  当提到 Nix 特有的概念、命令、选项、设置项等时，请链接到相应的文档。
  也要链接到外部工具或概念，尤其是当其含义可能有歧义时。
  你可能还想链接到较不常见的技术术语的定义。

  这样读者就不必主动搜索定义，也更有可能自行发现相关信息。

  > **注意**
  >
  > `man` 和 `--help` 页面不会显示链接。
  > 请使用恰当的链接文字，使阅读终端输出的读者能够推断出搜索关键词。

- 不要在发布之间破坏现有的 URL。

  互联网上存在无数指向手册旧版本的链接。
  我们希望人们在遵循流行建议时能够找到最新的文档。

  - 移动文件时，更新 [nixos.org 上的重定向](https://github.com/NixOS/nixos-homepage/blob/master/netlify.toml)。

    当把信息从 Nix 手册迁移到其他资源时，这一点尤为重要。

  - 更改锚点时，更新[客户端侧重定向](https://github.com/NixOS/nix/blob/master/doc/manual/redirects.js)

  目前的配置方式很繁琐，欢迎大家帮忙改进自动化流程。

构建过程会检查失效的内部链接。
这发生在流程的后期，因此[构建整个手册](#building-the-manual)并不适合快速迭代。
[`mdbook-linkcheck`] 尚未实现 [URI 片段]的检查。

[`mdbook-linkcheck`]: https://github.com/Michael-F-Bryan/mdbook-linkcheck
[URI fragments]: https://en.wikipedia.org/wiki/URI_fragment

### Markdown 约定

手册以 markdown 编写，在 Web 上用 [mdBook](https://github.com/rust-lang/mdBook) 渲染，在 `man` 页面和 `--help` 输出中用 [lowdown](https://github.com/kristapsdz/lowdown) 渲染。

关于受支持的 markdown 特性，请参考：
- [mdBook 文档](https://rust-lang.github.io/mdBook/format/markdown.html)
- [lowdown 文档](https://kristaps.bsd.lv/lowdown/)

请遵守以下约定以便于评审：

- 每行写一句话。

  这能让长句立刻显现出来，也便于评审变更和直接提出修改建议。

- 少量使用引用式链接，以提高源码可读性。
  把定义放在其首次使用位置的附近。

  示例：

  ```
  A [store object] contains a [file system object] and [references] to other store objects.

  [store object]: @docroot@/store/store-object.md
  [file system object]: @docroot@/architecture/file-system-object.md
  [references]: @docroot@/glossary.md#gloss-reference
  ```

- 使用如下形式的 admonition（提示块）：

  ```
  > **Note**
  >
  > This is a note.
  ```

  按如下方式突出示例：

  ````
  > **Example**
  >
  > ```console
  > $ nix --version
  > ```
  ````

  按如下方式突出语法定义，使用 [EBNF](https://en.wikipedia.org/wiki/Extended_Backus%E2%80%93Naur_form) 记法：

  ````
  > **Syntax**
  >
  > *attribute-set* = `{` [ *attribute-name* `=` *expression* `;` ... ] `}`
  ````

### `@docroot@` 变量

`@docroot@` 为出现在可复用片段或其他没有自身基础路径的文档中的链接提供基础路径。

如果一个失效链接出现在被插入到不同目录下多个生成文件中的片段里，请使用 `@docroot@` 来引用 `doc/manual/source` 目录。

如果 `@docroot@` 字面量出现在 [`mdbook-linkcheck`] 工具的错误信息中，则需要将 `@docroot@` 替换应用到提及它的那个生成源文件上。
参见[手册的 Makefile] 中现有的 `@docroot@` 逻辑。
用于手册的常规 markdown 文件有自己的基础路径，它们可以使用相对路径来代替 `@docroot@`。

## API 文档

[Doxygen API 文档]可在线查阅。
你也可以自行构建并查看：

[Doxygen API documentation]: https://hydra.nixos.org/job/nix/master/internal-api-docs/latest/download-by-type/doc/internal-api-docs

```console
$ nix build .#hydraJobs.internal-api-docs
$ xdg-open ./result/share/doc/nix/internal-api/html/index.html
```

或者在 `nix-shell` 或 `nix develop` 内部：

```console
$ configurePhase
$ ninja src/internal-api-docs/html
$ xdg-open src/internal-api-docs/html/index.html
```

## C API 文档

注意，C API 尚未稳定。
[C API 文档]可在线查阅。
你也可以自行构建并查看：

[C API documentation]: https://hydra.nixos.org/job/nix/master/external-api-docs/latest/download-by-type/doc/external-api-docs

```console
$ nix build .#hydraJobs.external-api-docs
$ xdg-open ./result/share/doc/nix/external-api/html/index.html
```

或者在 `nix-shell` 或 `nix develop` 内部：

```
$ configurePhase
$ ninja src/external-api-docs/html
$ xdg-open src/external-api-docs/html/index.html
```

如果你使用 direnv，或者想在临时 shell 中运行 `configurePhase`，请使用：

```bash
nix-shell -A devShells.x86_64-linux.native-clangStdenv --command 'appendToVar mesonFlags "-Ddoc-gen=true"; mesonConfigurePhase'
```
