# Name

`nix-instantiate` - 从 Nix 表达式实例化 store derivation

# 概要

`nix-instantiate`
  [`--parse` | `--eval` [`--strict`] [`--raw` | `--json` | `--xml`] ]
  [`--read-write-mode`]
  [`--arg` *name* *value*]
  [{`--attr`| `-A`} *attrPath*]
  [`--add-root` *path*]
  [`--expr` | `-E`]
  *files…*

`nix-instantiate` `--find-file` *files…*

# 描述

命令 `nix-instantiate` 从（高层）Nix 表达式生成 [store derivation]。
它对 *files* 中的每个 Nix 表达式求值（默认为
*./default.nix*）。每个顶层表达式应当求值结果为一个
derivation（派生）、一个 derivation 列表，或一个 derivation 集合。所得
store derivation 的路径会被打印到标准输出。

[store derivation]: @docroot@/glossary.md#gloss-store-derivation

如果 *files* 是字符 `-`，则会从
标准输入读取 Nix 表达式。

# 选项

- `--add-root` *path*

  参见 `nix-store` 中的[对应选项](./nix-store.md)。

- `--parse`

  仅解析输入文件，并将其抽象语法树
  作为 Nix 表达式打印到标准输出。

- `--eval`

  仅解析并求值输入文件，并将所得
  的值打印到标准输出。
  store derivation 不会被序列化并写入 store，而是只做哈希然后丢弃。

  > **警告**
  >
  > 此选项产生的输出可以被解析为一个 Nix 表达式，但该表达式
  > 求值后的结果可能与输入表达式不同。
  > 例如，下面这两个 Nix 表达式打印出相同的结果，尽管
  > 它们的含义不同：
  >
  > ```console
  > $ nix-instantiate --eval --expr '{ a = {}; }'
  > { a = <CODE>; }
  > $ nix-instantiate --eval --expr '{ a = <CODE>; }'
  > { a = <CODE>; }
  > ```
  >
  > 对于人类可读的输出，`nix eval`（实验性）信息量更大：
  >
  > ```console
  > $ nix-instantiate --eval --expr 'a: a'
  > <LAMBDA>
  > $ nix eval --expr 'a: a'
  > «lambda @ «string»:1:1»
  > ```
  >
  > 对于机器可读的输出，`--xml` 选项产生无歧义的
  > 输出：
  >
  > ```console
  > $ nix-instantiate --eval --xml --expr '{ foo = <CODE>; }'
  > <?xml version='1.0' encoding='utf-8'?>
  > <expr>
  >   <attrs>
  >     <attr column="3" line="1" name="foo">
  >       <unevaluated />
  >     </attr>
  >   </attrs>
  > </expr>
  > ```

- `--find-file`

  在 Nix 的搜索路径（由
  `NIX_PATH` 环境变量指定）中查找给定的文件。如果找到，则将相应的
  绝对路径打印到标准输出。例如，如果 `NIX_PATH` 是
  `nixpkgs=/home/alice/nixpkgs`，那么 `nix-instantiate --find-file
  nixpkgs/default.nix` 将打印 `/home/alice/nixpkgs/default.nix`。

- `--strict`

  与 `--eval` 一起使用时，递归地求值列表元素和
  属性。通常，这类子表达式保持未求值状态
  （因为 Nix 语言是惰性的）。

  > **警告**
  >
  > 此选项可能导致不终止（non-termination），因为惰性数据
  > 结构可以无限大。

- `--raw`

  与 `--eval` 一起使用时，求值结果必须是一个字符串，
  该字符串被原样打印，不带引号、转义或末尾换行。

- `--json`

  与 `--eval` 一起使用时，将所得的值打印为抽象语法树的 JSON
  表示，而非 Nix 表达式。

- `--xml`

  与 `--eval` 一起使用时，将所得的值打印为抽象语法树的 XML
  表示，而非 Nix 表达式。
  其 schema 与 [`toXML`
  内建函数](../language/builtins.md)使用的相同。

- `--read-write-mode`

  与 `--eval` 一起使用时，以读写模式执行求值，从而
  需要该模式的 Nix 语言特性仍然可以工作（代价
  是需要对每个被求值的 derivation 进行实例化）。如果
  未启用此选项，最终输出中可能存在未实例化的存储路径。

{{#include ./opt-common.md}}

{{#include ./env-common.md}}

# 示例

从 Nix 表达式实例化 [store derivation]，并使用 `nix-store` 构建它们：

```console
$ nix-instantiate test.nix (instantiate)
/nix/store/cigxbmvy6dzix98dxxh9b6shg7ar5bvs-perl-BerkeleyDB-0.26.drv

$ nix-store --realise $(nix-instantiate test.nix) (build)
...
/nix/store/qhqk4n8ci095g3sdp93x7rgwyh9rdvgk-perl-BerkeleyDB-0.26 (output path)

$ ls -l /nix/store/qhqk4n8ci095g3sdp93x7rgwyh9rdvgk-perl-BerkeleyDB-0.26
dr-xr-xr-x    2 eelco    users        4096 1970-01-01 01:00 lib
...
```

你也可以在命令行上给出 Nix 表达式：

```console
$ nix-instantiate --expr 'with import <nixpkgs> { }; hello'
/nix/store/j8s4zyv75a724q38cb0r87rlczaiag4y-hello-2.8.drv
```

这等价于：

```console
$ nix-instantiate '<nixpkgs>' --attr hello
```

解析和求值 Nix 表达式：

```console
$ nix-instantiate --parse --expr '1 + 2'
1 + 2
```

```console
$ nix-instantiate --eval --expr '1 + 2'
3
```

```console
$ nix-instantiate --eval --xml --expr '1 + 2'
<?xml version='1.0' encoding='utf-8'?>
<expr>
  <int value="3" />
</expr>
```

非严格求值与严格求值的区别：

```console
$ nix-instantiate --eval --xml --expr '{ x = {}; }'
<?xml version='1.0' encoding='utf-8'?>
<expr>
  <attrs>
    <attr column="3" line="1" name="x">
      <unevaluated />
    </attr>
  </attrs>
</expr>

$ nix-instantiate --eval --xml --strict --expr '{ x = {}; }'
<?xml version='1.0' encoding='utf-8'?>
<expr>
  <attrs>
    <attr column="3" line="1" name="x">
      <attrs>
      </attrs>
    </attr>
  </attrs>
</expr>
```
