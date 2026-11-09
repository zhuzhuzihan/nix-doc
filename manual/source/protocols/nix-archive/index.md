# Nix Archive（NAR）格式

这是 [Nix Archive] 格式的完整规范。
Nix Archive 格式紧贴[文件系统对象][file system object]树的抽象规范，
因为它正是为序列化该数据结构而设计的。

[Nix Archive]: @docroot@/store/file-system-object/content-address.md#serial-nix-archive
[file system object]: @docroot@/store/file-system-object.md

本规范的格式接近[扩展巴科斯–瑙尔范式](https://en.wikipedia.org/wiki/Extended_Backus%E2%80%93Naur_form)，但有一个例外：`str(..)` 函数/参数化规则会对字符串做长度前缀和填充。
这使得最终得到的二进制格式更易于解析。

普通用户*并不*需要了解这些信息。
但对于那些想确切了解 Nix 如何工作的人，例如想要重新实现它的人，这些信息可能有用。

```ebnf
nar = str("nix-archive-1"), nar-obj;

nar-obj = str("("), nar-obj-inner, str(")");

nar-obj-inner
  = str("type"), str("regular") regular
  | str("type"), str("symlink") symlink
  | str("type"), str("directory") directory
  ;

regular = [ str("executable"), str("") ], str("contents"), str(contents);

symlink = str("target"), str(target);

(* side condition: directory entries must be ordered by their names *)
directory = { directory-entry };

directory-entry = str("entry"), str("("), str("name"), str(name), str("node"), nar-obj, str(")");
```

`str` 函数/参数化规则定义如下：

- `str(s)` = `int(|s|), pad(s);`

- `int(n)` = 数字 `n` 的 64 位小端序表示

- `pad(s)` = 字节序列 `s`，用 0 填充至 8 字节的倍数

## Kaitai Struct 规范

Nix Archive（NAR）格式还使用 [Kaitai Struct](https://kaitai.io/)（一种用于定义二进制数据结构的接口描述语言（IDL））进行了形式化描述。

> Kaitai Struct 提供一种与语言无关、机器可读的规范，可编译为多种编程语言（如 C++、Python、Java、Rust）的解析器。

```yaml
{{#include nar.ksy}}
```

该规范的源文件可在[这里](https://github.com/nixos/nix/blob/master/src/nix-manual/source/protocols/nix-archive/nar.ksy)找到。欢迎对该规范做出贡献和改进。
