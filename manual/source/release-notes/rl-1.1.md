# Release 1.1 (2012-07-18)

本版本包含以下改进：

  - 在 Linux 上进行 chroot 构建时，Nix 现在使用 Linux 内核提供的多种 namespace 特性来改进构建隔离。具体而言：

      - 私有网络 namespace 确保 builder 无法与外部世界通信（反之亦然）：每个构建只能看到一个私有的 loopback 接口。这也意味着两个并发构建可以监听同一端口（例如作为测试的一部分）而互不冲突。
    
      - PID namespace 使每个构建以 PID 1 启动。chroot 外部的进程对内部的进程不可见。反之，chroot 内部的进程*可以*从外部看到（尽管 PID 不同）。
    
      - IPC namespace 防止 builder 使用 SysV IPC 机制（共享内存、消息队列、信号量）与外部进程通信。它还确保所有 IPC 对象在 builder 退出时被销毁。
    
      - UTS namespace 确保 builder 看到的主机名是 `localhost` 而不是实际主机名。
    
      - 私有挂载 namespace 此前已被 Nix 使用，以确保用于搭建 chroot 的 bind-mount 会被自动清理。

  - 构建日志现在使用 `bzip2` 压缩。命令 `nix-store
                    -l` 会即时解压它们。可以通过将选项 `build-compress-log` 设为 `false` 来禁用此功能。

  - 可以通过将新选项 `build-keep-log` 设为 `false` 来禁止在 `/nix/var/log/nix/drvs` 中创建构建日志。例如，这对 Hydra 构建机很有用。

  - Nix 现在在 `/nix/var/nix/db/reserved` 中预留了一些空间，以确保磁盘满时垃圾回收器仍能成功运行。这是必要的，因为磁盘满时 SQLite 事务会失败。

  - 新增了一个基本的 `fetchurl` 函数。它并非要取代 Nixpkgs 中的 `fetchurl`，但对引导（bootstrapping）很有用；例如，它将使我们能够去掉 Nixpkgs 源码树中的引导二进制文件，改为直接下载。使用方式为 `import <nix/fetchurl.nix> { url =
                    url; sha256 =
                    "hash"; }`。（Shea Levy）

  - 改进了 RPM spec 文件。（Michel Alexandre Salim）

  - Nix daemon（守护进程）支持通过 `systemd` 进行基于套接字的按需激活。

  - 为 nix.conf5 新增了 manpage。

  - 使用 Nix daemon 时，`nix-env -qa` 中的 `-s` 标志现在快得多。
