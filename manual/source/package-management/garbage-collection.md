# 垃圾回收

诸如升级（`-u`）和卸载（`-e`）之类的 `nix-env` 操作实际上从不从系统中删除软件包。它们所做的（如前所示）只是创建一个新的用户环境，其中不再包含指向「已删除」软件包的符号链接。

当然，由于磁盘空间并非无限，未被使用的软件包迟早应当被移除。你可以通过运行 Nix 垃圾回收器来做到这一点。它会从 Nix store 中移除任何不被任何 profile 的任何 generation 直接或间接使用的软件包。

但请注意，只要旧的 generation 仍然引用某个软件包，该软件包就不会被删除。毕竟，否则我们就无法执行回滚了。因此，为了让垃圾回收真正有效，你还应当删除（部分）旧的 generation。当然，只有在你确定自己不再需要回滚时才应该这样做。

要删除当前 profile 的所有旧（非当前）generation：

```console
$ nix-env --delete-generations old
```

除了 `old` 之外，你也可以指定一组 generation，例如：

```console
$ nix-env --delete-generations 10 11 14
```

要删除所有早于指定天数的 generation（当前 generation 除外），请使用 `d` 后缀。例如：

```console
$ nix-env --delete-generations 14d
```

将删除所有早于两周的 generation。

删除了合适的旧 generation 之后，你可以按如下方式运行垃圾回收器：

```console
$ nix-store --gc
```

垃圾回收器的行为受 Nix 配置文件中 `keep-derivations`（默认：true）和 `keep-outputs`（默认：false）选项的影响。默认设置会确保保留所有作为垃圾回收器根（garbage collector root）构建时依赖的 derivation（派生），以及所有作为运行时依赖的输出路径。其余的 derivation 或路径都会被回收。（这通常正是你想要的行为，但在开发过程中，保留输出可能更有意义，以确保重新构建的时间足够短。）如果你拿不准，也可以先查看哪些文件会被删除：

```console
$ nix-store --gc --print-dead
```

类似地，选项 `--print-live` 会显示*不会*被删除的路径。

还有一个方便的小工具 `nix-collect-garbage`，当以 `-d`（`--delete-old`）开关调用时，它会删除 `/nix/var/nix/profiles` 中所有 profile 的所有旧 generation。因此

```console
$ nix-collect-garbage -d
```

是一种快速简便的系统清理方式。
