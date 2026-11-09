# 内置函数

本节列出 Nix 语言求值器中内置的值和函数。
所有内置函数（built-in）都可以通过全局 [`builtins`](#builtins-builtins) 常量访问。

一些内置函数也直接暴露在全局作用域中：

- [`derivation`](#builtins-derivation)
- `derivationStrict`
- [`abort`](#builtins-abort)
- [`baseNameOf`](#builtins-baseNameOf)
- [`break`](#builtins-break)
- [`dirOf`](#builtins-dirOf)
- [`false`](#builtins-false)
- [`fetchGit`](#builtins-fetchGit)
- `fetchMercurial`
- [`fetchTarball`](#builtins-fetchTarball)
- [`fetchTree`](#builtins-fetchTree)
- [`fromTOML`](#builtins-fromTOML)
- [`import`](#builtins-import)
- [`isNull`](#builtins-isNull)
- [`map`](#builtins-map)
- [`null`](#builtins-null)
- [`placeholder`](#builtins-placeholder)
- [`removeAttrs`](#builtins-removeAttrs)
- [`scopedImport`](#builtins-scopedImport)
- [`throw`](#builtins-throw)
- [`toString`](#builtins-toString)
- [`true`](#builtins-true)

<!-- This tip (use `lib` instead) is a "layer violation", but serves an important social role. -->

> **提示**
>
> **应该使用 `builtins` 还是 `lib`？**
>
> 内置函数被设计为一个稳定的接口，表达式可以长期依赖它，
> 例如，旧版本的 Nixpkgs 能够持续可复现地求值。
>
> 另一方面，这也意味着它们积累了一些 Nix 无法改变的古怪行为，
> 但像 Nixpkgs `lib` 这样的函数库*可以*改进、替换或弃用这些行为，
> 因为在需要可复现性的地方，它的源代码是固定的。
>
> 因此，虽然直接使用 `builtins` 并没有错，
> 例如在小型的、不依赖 Nixpkgs 的项目中，
> 但如果使用像 `lib` 这样的函数库作为函数的主要来源，你会获得更好的体验，
> 因为它会隐藏有问题的函数、修复其他函数，
> 并通过未来的弃用（这仍然相当少见）帮助你改进代码。

<dl>
  <dt id="builtins-derivation"><a href="#builtins-derivation"><code>derivation <var>attrs</var></code></a></dt>
  <dd><p><var>derivation（派生）</var>在
         <a href="derivations.md">其专门的章节</a>中描述。</p></dd>
