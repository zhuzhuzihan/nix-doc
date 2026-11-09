# 存储路径的完整计算规则

这是关于[存储路径]如何计算的完整规范。

本规范的格式接近[扩展巴科斯–瑙尔范式](https://en.wikipedia.org/wiki/Extended_Backus%E2%80%93Naur_form)（EBNF），但在少数地方必须有所偏离，例如哈希函数——出于规范的目的，我们将其视为双向的。

普通用户*并不*需要了解这些信息 --- 存储路径可以当作黑盒对待，它们由其所指的存储对象的属性计算得出。
但对于那些想确切了解 Nix 如何工作的人，例如想要重新实现它的人，这些信息可能有用。

[存储路径]: @docroot@/store/store-path.md

## 存储路径本体

```ebnf
store-path = store-dir "/" digest "-" name
```
其中

- `name` = 存储对象的名称。

- `store-dir` = [存储目录的路径](@docroot@/store/store-path.md#store-directory-path)

- `digest` = `fingerprint` 压缩至 160 位的 [SHA-256] 哈希的 [Nix32](@docroot@/protocols/nix32.md) 表示。

  哈希压缩算法定义请参见 [Nix 论文](https://edolstra.github.io/pubs/phd-thesis.pdf)的第 5.1 节。

## 指纹

- ```ebnf
  fingerprint = type ":sha256:" inner-digest ":" store ":" name
  ```

  注意，其中同时包含了 store 的位置和名称，以确保二者中任何一者的变更都会反映在哈希中
  （例如，`/nix/store/<digest>-name1` 与 `/nix/store/<digest>-name2`，或 `/gnu/store/<digest>-name1`，不会拥有相同的哈希部分）。

- `type` = 以下之一：

  - ```ebnf
    | "text" { ":" store-path }
    ```

    这用于以
    ["Text"](@docroot@/store/store-object/content-address.md#method-text)
    方法对存储对象进行内容寻址。
    可选的尾部存储路径是该存储对象的引用（references）。

  - ```ebnf
    | "source" { ":" store-path } [ ":self" ]
    ```

    这用于以
    ["Nix Archive"](@docroot@/store/store-object/content-address.md#method-nix-archive)
    方法对存储对象进行内容寻址，
    当哈希算法为 [SHA-256] 时。
    与 "Text" 情形一样，可以通过路径引用存储对象。
    此外，还可以有一个可选的 `:self` 标签来表示自引用。

  - ```ebnf
    | "output:" id
    ```

    用于由 derivation（派生）构建的输出，或未使用上述两种情形之一的内容寻址存储对象。
    明确地说，后者目前包括以下方法：

    - [Flat](@docroot@/store/store-object/content-address.md#method-flat)
    - [Git](@docroot@/store/store-object/content-address.md#method-git)
    - [Nix Archive](@docroot@/store/store-object/content-address.md#method-nix-archive)，当哈希算法不是 [SHA-256] 时

    `id` 是输出的名称（通常是 "out"）。
    对于内容寻址存储对象，`id` 总是 "out"。

- `inner-digest` = `inner-fingerprint` 的 SHA-256 哈希的 base-16 表示。
  base-16 编码使用小写十六进制数字。

## 内部指纹

- `inner-fingerprint` = 根据 `type` 取以下之一：

  - 若 `type` = `"text:" ...`：

    写入所得存储路径的字符串。

  - 若 `type` = `"source:" ...`：

    该存储对象的[文件系统对象](@docroot@/store/file-system-object.md)的 [Nix Archive (NAR)] 序列化。

  - 若 `type` = `"output:" id`：

    - 对于输入寻址的 derivation 输出：

      ["完全掩码的 derivation"](@docroot@/store/derivation/outputs/input-address.md#input-masked-drv)的 [ATerm](@docroot@/protocols/derivation-aterm.md#input-address-encoding) 序列化，其中固定输出（fixed-output）输入被替换为其内容地址，而 derivation 自身的输出路径被置空。

    - 对于内容寻址存储路径：

      ```ebnf
      "fixed:out:" rec algo ":" hash ":"
      ```

      其中

      - `rec` = 以下之一：

        - ```ebnf
          | ""
          ```
          （空字符串）用于扁平（单文件）序列化的哈希

        - ```ebnf
          | "r:"
          ```
          用于 [Nix Archive (NAR)]（任意文件系统对象）序列化的哈希

        - ```ebnf
          | "git:"
          ```
          用于 [Git blob/tree](https://git-scm.com/book/en/v2/Git-Internals-Git-Objects) [Merkle 树](https://en.wikipedia.org/wiki/Merkle_tree)格式的哈希

      - ```ebnf
        algo = "md5" | "sha1" | "sha256"
        ```

      - `hash` = 路径哈希或路径内容扁平哈希的 base-16 表示（对于固定输出 derivation，则是路径的预期内容）。

      注意，无论存储路径的名称部分是什么，`id` 都为 `"out"`。
      还要注意，NAR + SHA-256 不得使用这一情形，而必须使用 `type` = `"source:" ...` 情形。

[Nix Archive (NAR)]: @docroot@/store/file-system-object/content-address.md#serial-nix-archive
[SHA-256]: https://en.m.wikipedia.org/wiki/SHA-256

### 历史说明

`type` = `"source:" ...` 与 `type` = `"output:out"` 两种文法在目的上存在技术性重叠，
二者都可以表示经 SHA-256 NAR 序列化哈希的数据。

最初采用这种名称计算方式是为了防止名称冲突（出于安全考虑）。
例如，当时的想法是：不应该可能构造出一个 derivation，其输出路径与复制的源码路径发生碰撞。
前者会有以 `output:out:` 开头的 `inner-fingerprint`，而后者会有以 `source:` 开头的 `inner-fingerprint`。

然而自 `64519cfd657d024ae6e2bb74cb21ad21b886fd2a`（2008 年）起，人们决定将 derivation 产生的数据与手动哈希的内容寻址数据如此区分开并无用处。
现在，以 SHA-256 + NAR 序列化进行内容寻址的数据一律使用 `source:...` 构造方式，无论它是如何产生的（手动还是通过 derivation）。
这使得可以自由地在使用[固定输出 derivation](@docroot@/glossary.md#gloss-fixed-output-derivation) 进行获取，与带外获取后手动添加之间切换。
这也消除了文法中的歧义。
