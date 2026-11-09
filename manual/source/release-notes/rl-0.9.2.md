# Release 0.9.2 (2005-09-21)

本缺陷修复版本修复了 Mac OS X 上的两个问题：

  - 如果 Nix 链接的是静态链接版本的 ATerm 或 Berkeley DB 库，运行时会出现动态链接错误。

  - `nix-pull` 和 `nix-push` 会因管道与子进程相关的竞态条件而间歇性失败，错误消息形如 `open2: open(GLOB(0x180b2e4), >&=9) failed: Bad
            file descriptor at /nix/bin/nix-pull line 77`（issue `NIX-14`）。
