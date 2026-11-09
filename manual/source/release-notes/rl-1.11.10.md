# Release 1.11.10 (2017-06-12)

本版本修复了 Nix 的"构建用户"构建隔离机制中的一个安全缺陷。此前，Nix builder 能够创建属于 `nixbld` 用户的 setuid 二进制文件。攻击者随后可以利用这样的二进制文件获得 `nixbld` 身份，并干扰在同一 UID 下运行的后续构建。

为防止此问题，Nix 现在禁止 builder 创建 setuid 和 setgid 二进制文件。在 Linux 上，这是通过一个 seccomp BPF 过滤器实现的。注意这会带来较小的性能损失（例如构建 GNU Hello 时约为 1%）。借助 seccomp，我们现在还阻止扩展属性和 POSIX ACL 的创建，因为它们无法在 NAR 格式中表示，并且（就 POSIX ACL 而言）允许绕过常规的 Nix store 权限。在 macOS 上，该限制通过现有的沙箱机制实现：当常规沙箱被禁用时，它现在使用一个"允许一切、仅禁止创建 setuid/setgid 二进制文件"的最小 profile。在其他平台上，"构建用户"机制现在被禁用。

感谢 Linus Heckemann 发现并报告此缺陷。
