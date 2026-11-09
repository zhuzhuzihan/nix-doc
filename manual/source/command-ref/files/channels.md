## Channels

包含指向 Nix channel 的符号链接的目录，由 [`nix-channel`] 管理：

- 普通用户为 `$XDG_STATE_HOME/nix/profiles/channels`
- `root` 用户为 `$NIX_STATE_DIR/profiles/per-user/root/channels`

[`nix-channel`] 使用一个 [profile](@docroot@/command-ref/files/profiles.md) 来存储 channel。
该 profile 包含指向这些 channel 内容的符号链接。

## 已订阅的 channel

已订阅 channel 的列表存储在以下位置：

- `~/.nix-channels`
- 如果 [`use-xdg-base-directories`] 设置为 `true`，则为 `$XDG_STATE_HOME/nix/channels`

格式如下：

```
<url> <name>
...
```

[`nix-channel`]: @docroot@/command-ref/nix-channel.md
[`use-xdg-base-directories`]: @docroot@/command-ref/conf-file.md#conf-use-xdg-base-directories
