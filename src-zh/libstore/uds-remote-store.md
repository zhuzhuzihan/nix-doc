R"(

**Store URL 格式**: `daemon`, `unix://`*path*

此 Store 类型通过与监听在 Unix 域套接字 *path* 上的 Nix daemon（守护进程）通信来访问 Nix Store。

当 *path* 未指定时（即 `daemon` 伪 URL 或不带路径的 `unix://`），套接字路径按以下方式确定：

1. 环境变量 [`NIX_DAEMON_SOCKET_PATH`]，如果已设置。

2. 否则，使用 [`state`](#store-local-daemon-store-state) 目录中的 `daemon-socket/socket`。

[`NIX_DAEMON_SOCKET_PATH`]: @docroot@/command-ref/env-common.md#env-NIX_DAEMON_SOCKET_PATH

)"
