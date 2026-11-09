# 验证构建的可重现性

你可以使用 Nix 的 `diff-hook` 设置来比较构建结果。注意，这个 hook 只在结果不同时才会被执行；它并不用于判定结果是否相同。

出于演示目的，我们将使用下面这个 Nix 文件 `deterministic.nix` 进行测试：

```nix
let
  inherit (import <nixpkgs> {}) runCommand;
in {
  stable = runCommand "stable" {} ''
    touch $out
  '';

  unstable = runCommand "unstable" {} ''
    echo $RANDOM > $out
  '';
}
```

此外，`nix.conf` 中包含：

    diff-hook = /etc/nix/my-diff-hook
    run-diff-hook = true

其中 `/etc/nix/my-diff-hook` 是一个可执行文件，内容为：

```bash
#!/bin/sh
exec >&2
echo "For derivation $3:"
/run/current-system/sw/bin/diff -r "$1" "$2"
```

diff hook 由执行构建的同一用户和用户组运行。但是，diff hook 对刚构建出的存储路径（store path）没有写权限。

# 抽查构建的确定性

通过向构建命令传入 `--check`，可以验证 Nix store 中已经存在的某个路径。

如果构建通过且是确定性的，Nix 会以状态码 0 退出：

```console
$ nix-build ./deterministic.nix --attr stable
this derivation will be built:
  /nix/store/z98fasz2jqy9gs0xbvdj939p27jwda38-stable.drv
building '/nix/store/z98fasz2jqy9gs0xbvdj939p27jwda38-stable.drv'...
/nix/store/yyxlzw3vqaas7wfp04g0b1xg51f2czgq-stable

$ nix-build ./deterministic.nix --attr stable --check
checking outputs of '/nix/store/z98fasz2jqy9gs0xbvdj939p27jwda38-stable.drv'...
/nix/store/yyxlzw3vqaas7wfp04g0b1xg51f2czgq-stable
```

如果构建不是确定性的，Nix 会以状态码 1 退出：

```console
$ nix-build ./deterministic.nix --attr unstable
this derivation will be built:
  /nix/store/cgl13lbj1w368r5z8gywipl1ifli7dhk-unstable.drv
building '/nix/store/cgl13lbj1w368r5z8gywipl1ifli7dhk-unstable.drv'...
/nix/store/krpqk0l9ib0ibi1d2w52z293zw455cap-unstable

$ nix-build ./deterministic.nix --attr unstable --check
checking outputs of '/nix/store/cgl13lbj1w368r5z8gywipl1ifli7dhk-unstable.drv'...
error: derivation '/nix/store/cgl13lbj1w368r5z8gywipl1ifli7dhk-unstable.drv' may
not be deterministic: output '/nix/store/krpqk0l9ib0ibi1d2w52z293zw455cap-unstable' differs
```

在 Nix 守护进程的日志中，我们将看到：

```
For derivation /nix/store/cgl13lbj1w368r5z8gywipl1ifli7dhk-unstable.drv:
1c1
< 8108
---
> 30204
```

将 `--check` 与 `--keep-failed` 结合使用会让 Nix 把第二次构建的输出保存在一个特殊的 `.check` 路径中：

```console
$ nix-build ./deterministic.nix --attr unstable --check --keep-failed
checking outputs of '/nix/store/cgl13lbj1w368r5z8gywipl1ifli7dhk-unstable.drv'...
note: keeping build directory '/tmp/nix-build-unstable.drv-0'
error: derivation '/nix/store/cgl13lbj1w368r5z8gywipl1ifli7dhk-unstable.drv' may
not be deterministic: output '/nix/store/krpqk0l9ib0ibi1d2w52z293zw455cap-unstable' differs
from '/nix/store/krpqk0l9ib0ibi1d2w52z293zw455cap-unstable.check'
```

尤其请注意 `/nix/store/krpqk0l9ib0ibi1d2w52z293zw455cap-unstable.check` 这个输出。Nix 已经把构建结果复制到了该目录，你可以在那里查看它。

> []{#check-dirs-are-unregistered} **注意**
> 
> Check 路径不受垃圾回收保护，该路径会在下一次垃圾回收时被删除。
> 
> 该路径保证在 `diff-hook` 执行期间一直存在，但在此之后的任何时间都可能被删除。
> 
> 如果这个比较是作为自动化工具的一部分进行的，请使用 diff hook，或者让你自己的工具能够处理「构建不是确定性的、同时 check 路径也不存在」的情况。

`--check` 只有在该 derivation 已经在本系统上构建过的情况下才能使用。如果该 derivation 尚未构建，Nix 将报错：

    error: some outputs of '/nix/store/hzi1h60z2qf0nb85iwnpvrai3j2w7rr6-unstable.drv' 
    are not valid, so checking is not possible

此时请先不带 `--check` 运行构建，然后再带上 `--check` 重试。
