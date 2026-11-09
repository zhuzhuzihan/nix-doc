# 单用户模式

在单用户模式下，所有访问 `prefix/var/nix/db` 中数据库或修改 `prefix/store` 中 Nix store 的 Nix 操作，都必须在拥有这些目录的用户 ID 下执行。该用户通常是 root。（如果通过 RPM 软件包安装，默认的所有者事实上正是 root。）不过，在单用户机器上，把这些目录 `chown` 给你的普通用户账户通常更为方便，这样你就不必总是 `su` 到 root。
