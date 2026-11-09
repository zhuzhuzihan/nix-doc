# 文件系统对象（File System Object）

Nix 使用一个简化的文件系统模型，它由文件系统对象构成。
每个文件系统对象都是以下之一：

 - [**普通文件**]{#regular}

   - 内容是一个可能为空的字节序列
   - 一个布尔值，表示[可执行](https://en.m.wikipedia.org/wiki/File-system_permissions#Permissions)权限

 - [**目录**]{#directory}

   从名称到子文件系统对象的映射

 - [**符号链接**]{#symlink}

   一个任意字符串，称为符号链接的*目标（target）*。

   一般而言，Nix 不给符号链接赋予任何语义。
   然而某些操作可能会做出额外的假设，并尝试利用目标来找到另一个文件系统对象。

   > 如果你不熟悉这个 Unix 概念，请参阅[维基百科关于符号链接的文章](https://en.m.wikipedia.org/wiki/Symbolic_link)了解背景信息。

文件系统对象及其子对象构成一棵树。
一个孤立的文件或符号链接也可以作为根文件系统对象。

Nix 不编码任何其他文件系统概念，例如[硬链接](https://en.m.wikipedia.org/wiki/Hard_link)、[权限](https://en.m.wikipedia.org/wiki/File-system_permissions)、时间戳或其他元数据。

## 文件系统对象的示例

一个普通文件：

```
50 B, executable: false
```

一个可执行文件：

```
122 KB, executable: true
```

一个符号链接：

```
-> /usr/bin/sh
```

一个有内容的目录：

```
├── bin
│   └── hello: 35 KB, executable: true
└── share
    ├── info
    │   └── hello.info: 36 KB, executable: false
    └── man
        └── man1
            └── hello.1.gz: 790 B, executable: false
```

一个包含符号链接和其他目录的目录：

```
├── bin -> share/go/bin
├── nix-support/
└── share/
```
