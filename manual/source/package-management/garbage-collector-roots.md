# 垃圾回收器根

垃圾回收器的根（root）是在目录 `prefix/nix/var/nix/gcroots` 中有符号链接指向的所有存储路径（store path）。例如，以下命令使路径 `/nix/store/d718ef...-foo` 成为垃圾回收器的一个根：

```console
$ ln -s /nix/store/d718ef...-foo /nix/var/nix/gcroots/bar
```

也就是说，执行此命令之后，垃圾回收器将不会移除 `/nix/store/d718ef...-foo` 及其任何依赖。

`prefix/nix/var/nix/gcroots` 的子目录会被递归搜索。指向存储路径的符号链接算作根；指向非存储路径的符号链接会被忽略，除非该非存储路径本身又是指向某个存储路径的符号链接。
