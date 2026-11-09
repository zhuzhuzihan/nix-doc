# Name

`nix --repair-path` - 从 substituter 重新下载路径

# 概要

`nix-store` `--repair-path` *paths…*

# 描述

`--repair-path` 操作尝试通过可用的 substituter 重新下载指定路径来"修复"它们。如果没有可用的 substitute，则无法进行修复。

> **警告**
>
> 在修复期间，存在一个极小的时间窗口：旧路径（如果存在）被移开并用新路径替换。如果修复在中间被中断，系统可能会处于损坏状态（例如，如果路径包含像 GNU C 库这样的关键系统组件）。

# 示例

```console
$ nix-store --verify-path /nix/store/dj7a81wsm1ijwwpkks3725661h3263p5-glibc-2.13
path `/nix/store/dj7a81wsm1ijwwpkks3725661h3263p5-glibc-2.13' was modified!
  expected hash `2db57715ae90b7e31ff1f2ecb8c12ec1cc43da920efcbe3b22763f36a1861588',
  got `481c5aa5483ebc97c20457bb8bca24deea56550d3985cda0027f67fe54b808e4'

$ nix-store --repair-path /nix/store/dj7a81wsm1ijwwpkks3725661h3263p5-glibc-2.13
fetching path `/nix/store/d7a81wsm1ijwwpkks3725661h3263p5-glibc-2.13'...
…
```
