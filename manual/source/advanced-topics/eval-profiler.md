# 使用 `eval-profiler`

Nix 求值器（evaluator）支持与 `flamegraph.pl` 兼容的[求值](@docroot@/language/evaluation.md)[性能分析](<https://en.wikipedia.org/wiki/Profiling_(computer_programming)>)。该性能分析器按固定间隔对 Nix 函数调用栈进行采样。它可以通过 [`eval-profiler`](@docroot@/command-ref/conf-file.md#conf-eval-profiler) 设置启用：

```console
$ nix-instantiate "<nixpkgs>" -A hello --eval-profiler flamegraph
```

栈采样频率和输出文件路径可以通过 [`eval-profile-file`](@docroot@/command-ref/conf-file.md#conf-eval-profile-file) 和 [`eval-profiler-frequency`](@docroot@/command-ref/conf-file.md#conf-eval-profiler-frequency) 配置。默认情况下，收集到的 profile 会保存到当前工作目录下的 `nix.profile` 文件中。

收集到的 profile 可以直接供 `flamegraph.pl` 使用：

```console
$ flamegraph.pl nix.profile > flamegraph.svg
```

profile 中的行信息包含[调用点](https://en.wikipedia.org/wiki/Call_site)（call site）的位置以及被调用函数的名称（如果可用）。例如：

```
/nix/store/2q71fdvr4h33g9832hiriwnf20fn630l-source/pkgs/top-level/default.nix:167:5:primop import
```

这里表示 `import` 内建原语（primop）在 `/nix/store/2q71fdvr4h33g9832hiriwnf20fn630l-source/pkgs/top-level/default.nix:167:5` 处被调用。
