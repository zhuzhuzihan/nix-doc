# Release 2.12 (2022-12-06)

* 在 Linux 上，Nix 现在可以在 user namespace 中运行构建，构建过程以 root（UID 0）身份运行并拥有 65,536 个可用 UID。
  这主要用于在 Nix 构建内部运行诸如 `systemd-nspawn` 之类的容器。示例见 [`tests/systemd-nspawn/nix`][nspawn]。

  [nspawn]: https://github.com/NixOS/nix/blob/67bcb99700a0da1395fa063d7c6586740b304598/tests/systemd-nspawn.nix.

  构建可以通过设置 derivation（派生）属性来启用它：

  ```
  requiredSystemFeatures = [ "uid-range" ];
  ```

  `uid-range` [system feature] 要求启用 [`auto-allocate-uids`] 设置。

  [system feature]: ../command-ref/conf-file.md#conf-system-features

* Nix 现在可以为构建自动挑选 UID，从而无需创建 `nixbld*` 用户账户。参见 [`auto-allocate-uids`]。

  [`auto-allocate-uids`]: ../command-ref/conf-file.md#conf-auto-allocate-uids

* 在 Linux 上，Nix 对在 cgroup 中运行构建提供实验性支持。参见
  [`use-cgroups`](../command-ref/conf-file.md#conf-use-cgroups)。

* `<nix/fetchurl.nix>` 现在接受一个额外的参数 `impure`，默认为 `false`。如果将其设为 `true`，`hash` 和 `sha256` 参数将被忽略，且产生的 derivation 会将 `__impure` 设为 `true`，从而成为一个非纯（impure）derivation。

* 如果对带有上下文（context）的文件调用 `builtins.readFile`，则只会保留出现在文件内容中的那部分上下文。这避免了大量虚假错误——字符串仅仅因为是从某个存储路径读出的就带上了上下文
  ([#7260](https://github.com/NixOS/nix/pull/7260))。

* `nix build --json` 现在会打印关于顶层 derivation 的一些统计信息，例如启用 cgroup 时的 CPU 统计。
