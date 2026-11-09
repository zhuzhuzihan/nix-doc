# 查找路径（lookup path）

> **语法**
>
> *lookup-path* = `<` *identifier* [ `/` *identifier* ]... `>`

查找路径是带有可选路径后缀的标识符，当该标识符匹配 [`builtins.nixPath`](@docroot@/language/builtins.md#builtins-nixPath) 中的某个搜索路径条目时，它会解析为一个[路径值](@docroot@/language/types.md#type-path)。
查找路径解析的算法在 [`builtins.findFile`](@docroot@/language/builtins.md#builtins-findFile) 的文档中描述。

> **示例**
>
> ```nix
> <nixpkgs>
>```
>
>     /nix/var/nix/profiles/per-user/root/channels/nixpkgs

> **示例**
>
> ```nix
> <nixpkgs/nixos>
>```
>
>     /nix/var/nix/profiles/per-user/root/channels/nixpkgs/nixos
