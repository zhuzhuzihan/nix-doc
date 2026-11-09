# Name

`nix-store` - 操作或查询 Nix store

# 概要

`nix-store` *operation* [*options…*] [*arguments…*]
  [`--option` *name* *value*]
  [`--add-root` *path*]

# 描述

命令 `nix-store` 对 Nix store 执行基础操作。你通常不需要手动运行这个命令。

`nix-store` 恰好接受一个 *operation* 标志，用于指示要执行的子命令。可用的操作如下：

- [`--realise`](./nix-store/realise.md)
- [`--serve`](./nix-store/serve.md)
- [`--gc`](./nix-store/gc.md)
- [`--delete`](./nix-store/delete.md)
- [`--query`](./nix-store/query.md)
- [`--add`](./nix-store/add.md)
- [`--add-fixed`](./nix-store/add-fixed.md)
- [`--verify`](./nix-store/verify.md)
- [`--verify-path`](./nix-store/verify-path.md)
- [`--repair-path`](./nix-store/repair-path.md)
- [`--dump`](./nix-store/dump.md)
- [`--restore`](./nix-store/restore.md)
- [`--export`](./nix-store/export.md)
- [`--import`](./nix-store/import.md)
- [`--optimise`](./nix-store/optimise.md)
- [`--read-log`](./nix-store/read-log.md)
- [`--dump-db`](./nix-store/dump-db.md)
- [`--load-db`](./nix-store/load-db.md)
- [`--register-validity`](./nix-store/register-validity.md)
- [`--print-env`](./nix-store/print-env.md)
- [`--generate-binary-cache-key`](./nix-store/generate-binary-cache-key.md)

这些页面可以离线查看：

- `man nix-store-<operation>`。

  示例：`man nix-store-realise`

- `nix-store --help --<operation>`

  示例：`nix-store --help --realise`
