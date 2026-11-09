# Release 2.13 (2023-01-17)

* `repeat` 和 `enforce-determinism` 选项已被移除，因为它们在很多情况下早已失效。

* 你现在可以在[旧命令行界面]中使用 [flake references]，例如

   [flake references]: ../command-ref/new-cli/nix3-flake.md#flake-references
   [old command line interface]: ../command-ref/main-commands.md

  ```shell-session
  # nix-build flake:nixpkgs -A hello
  # nix-build -I nixpkgs=flake:github:NixOS/nixpkgs/nixos-22.05 \
      '<nixpkgs>' -A hello
  # NIX_PATH=nixpkgs=flake:nixpkgs nix-build '<nixpkgs>' -A hello
  ```

* 现在一贯使用更常见的术语[string interpolation（字符串插值）](../language/string-interpolation.md)来代替 "antiquotation"（反引号插入）。
  历史发布说明未做更改。

* 错误跟踪（error trace）经过重构，可提供详细的解释和更准确的错误位置。发生错误时，默认会显示跟踪的一段简短摘录。

* 允许在 store derivation installable 中显式选择输出，就像我们对其他类型的 installable 所能做的那样。
  例如，
  ```shell-session
  # nix build /nix/store/fpq78s2h8ffh66v2iy0q1838mhff06y8-glibc-2.33-78.drv^dev
  ```
  现在可以像
  ```shell-session
  # nix build nixpkgs#glibc^dev
  ```
  一样工作了。

* 在 Linux 上，`nix develop` 现在会以与 derivation 实际构建相同的方式为开发 shell 设置
  [*personality*](https://man7.org/linux/man-pages/man2/personality.2.html)。
  这使得 `i686-linux` derivation 的 shell 能在 `x86_64-linux` 上正确工作。

* 你现在可以通过把 `flake-registry` 配置选项设为空字符串来禁用全局 flake 注册表。在运行时也可以通过
  `--flake-registry ""` 达到同样的效果。
