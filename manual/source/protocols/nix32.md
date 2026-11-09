# Nix32 编码

Nix32 是 Nix 对 [Base32](https://en.wikipedia.org/wiki/Base32) 编码的变体，用于[存储路径摘要](@docroot@/protocols/store-path.md)、通过 [`nix hash`](@docroot@/command-ref/new-cli/nix3-hash.md) 输出的哈希，以及 derivation 的 [`outputHash`](@docroot@/language/advanced-attributes.md#adv-attr-outputHash) 属性。

## 字母表

Nix32 字母表由以下 32 个字符组成：

```
0 1 2 3 4 5 6 7 8 9 a b c d f g h i j k l m n p q r s v w x y z
```

字母 `e`、`o`、`u` 和 `t` 被省略。

## 字节顺序

Nix32 编码从哈希字节的末尾开始处理（最后一个字节在前），而 base-16 编码则从开头开始处理（第一个字节在前）。

因此，字符串的排序顺序对 base-16 而言主要由前几个字节决定，对 Nix32 而言则主要由最后几个字节决定。
