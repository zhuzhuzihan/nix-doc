# 选项

以下选项可用于所有 `nix-store` 操作，但不一定总是有效果。

- <span id="opt-add-root">[`--add-root`](#opt-add-root)</span> *path*

  将实化（realisation，即 `--realise` 和
  `--force-realise`）的结果注册为垃圾回收器的一个 GC root。*path* 将被创建为指向生成的存储路径的符号链接。此外，还会在 `/nix/var/nix/gcroots/auto/` 中创建一个唯一命名的指向 *path* 的符号链接。例如：

  ```console
  $ nix-store --add-root /home/eelco/bla/result --realise ...

  $ ls -l /nix/var/nix/gcroots/auto
  lrwxrwxrwx    1 ... 2005-03-13 21:10 dn54lcypm8f8... -> /home/eelco/bla/result

  $ ls -l /home/eelco/bla/result
  lrwxrwxrwx    1 ... 2005-03-13 21:10 /home/eelco/bla/result -> /nix/store/1r11343n6qd4...-f-spot-0.0.10
  ```

  因此，当 `/home/eelco/bla/result` 被删除时，`auto`
  目录中的 GC root 会变成悬空符号链接，垃圾回收器会忽略它。

  > **警告**
  >
  > 注意，GC root 不能被移动或重命名，因为
  > `auto` 目录中的符号链接仍然指向
  > 旧位置。

  如果有多个结果，则会创建多个符号链接，第一个之后的符号链接会按顺序编号（例如，`foo`、`foo-2`、`foo-3`，依此类推）。
