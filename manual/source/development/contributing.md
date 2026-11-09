# 贡献

## 添加 release note

`doc/manual/rl-next` 包含所有未发布变更的 release note 条目。

对用户可见的变更都应附带 release note。

### 添加条目

下面是一个完整条目的样子。文件名不会并入文档中。

```
---
synopsis: Basically a title
issues: 1234
prs: 1238
---

Here's one or more paragraphs that describe the change.

- It's markdown
- Add references to the manual using [links like this](@_at_docroot@/example.md)
```
<!-- for the raw markdown readers: that means using @docroot@ -->

重大变更应添加以下头部，使其移到顶部。

```
significance: significant
```

<!-- Keep an eye on https://codeberg.org/fgaz/changelog-d/issues/1 -->
另请参阅[格式文档](https://github.com/haskell/cabal/blob/master/CONTRIBUTING.md#changelog)。

### 构建过程

正式发布版本有一个预先生成的 `rl-MAJOR.MINOR.md`，并且没有 `rl-next.md`。

## 分支

- [`master`](https://github.com/NixOS/nix/commits/master)

  主开发分支。所有变更都在此获得批准并合并。
  开发变更时，请基于最新的 `master` 创建分支。

  维护者会尽力[使其保持适合发布的状态](#reverting)。

- [`maintenance-*.*`](https://github.com/NixOS/nix/branches/all?query=maintenance)

  这些分支仅用于回移（backport），同样[保持](#reverting)在适合发布的状态。

  参见 [`maintainers/backporting.md`](https://github.com/NixOS/nix/blob/master/maintainers/backporting.md)

- [`latest-release`](https://github.com/NixOS/nix/tree/latest-release)

  最新次要版本的最新补丁发布。

  参见 [`maintainers/release-process.md`](https://github.com/NixOS/nix/blob/master/maintainers/release-process.md)

- [`backport-*-to-*`](https://github.com/NixOS/nix/branches/all?query=backport)

  通常是由回移（backport）动作创建的分支。

  参见 [`maintainers/backporting.md`](https://github.com/NixOS/nix/blob/master/maintainers/backporting.md)

- [_其他_](https://github.com/NixOS/nix/branches/all)

  不符合上述模式的分支应为功能分支。

## 回退

如果某项变更被发现是误合并的，或包含回归，它可能会被回退。
回退并不是对贡献的否定，而只是高效开发过程的一部分。
它确保开发持续顺畅进行，将不确定性降到最低，并减少额外开销。
如果维护者需要过度担心避免回退，他们就无法合并足够多的变更。
把回退视为开发过程中正常的一部分，对每个人都有好处。

不过，走回头路可能令人沮丧，因此维护者会在你下次尝试时给予格外多的支持。
