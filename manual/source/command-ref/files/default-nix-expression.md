## 默认 Nix 表达式

[`nix-env`] 默认使用的 [Nix 表达式](@docroot@/glossary.md#gloss-nix-expression)的来源：

- `~/.nix-defexpr`
- 如果 [`use-xdg-base-directories`] 设置为 `true`，则为 `$XDG_STATE_HOME/nix/defexpr`。

其加载方式如下：

- 如果默认表达式是一个文件，则将其作为 Nix 表达式加载。
- 如果默认表达式是一个包含 `default.nix` 文件的目录，则将该 `default.nix` 文件作为 Nix 表达式加载。
- 如果默认表达式是一个不含 `default.nix` 文件的目录，则其内容（包括文件和子目录）都会作为 Nix 表达式加载。
  这些表达式被合并为一个单一的属性集，每个表达式放在一个与原文件或子目录同名的属性下。
  没有 `default.nix` 文件的子目录会被递归遍历以寻找更多 Nix 表达式，但这些中间目录的名称不会添加到默认 Nix 表达式的属性路径中。

然后，得到的表达式按如下方式解释：

- 如果该表达式是一个属性集，则它被用作默认 Nix 表达式。
- 如果该表达式是一个函数，则会传入一个空集作为参数，其返回值被用作默认 Nix 表达式。

> **示例**
>
> 如果默认表达式包含两个文件 `foo.nix` 和 `bar.nix`，那么默认 Nix 表达式将等价于
>
> ```nix
> {
>   foo = import ~/.nix-defexpr/foo.nix;
>   bar = import ~/.nix-defexpr/bar.nix;
> }
> ```

文件 [`manifest.nix`](@docroot@/command-ref/files/manifest.nix.md) 总是被忽略。

命令 [`nix-channel`] 会将指向当前用户 [channel] 的符号链接放入该目录，即[用户 channel 链接](#user-channel-link)。
这使得所有已订阅的 channel 都可以作为属性在默认表达式中使用。

## 用户 channel 链接

一个确保 [`nix-env`] 能找到当前用户 [channel] 的符号链接：

- `~/.nix-defexpr/channels`
- 如果 [`use-xdg-base-directories`] 设置为 `true`，则为 `$XDG_STATE_HOME/nix/defexpr/channels`。

该符号链接指向：

- 普通用户为 `$XDG_STATE_HOME/nix/profiles/channels`
- `root` 用户为 `$NIX_STATE_DIR/profiles/per-user/root/channels`

在多用户安装中，你还可能看到 `~/.nix-defexpr/channels_root`，它指向 root 用户的 channel。

[`nix-channel`]: @docroot@/command-ref/nix-channel.md
[`nix-env`]: @docroot@/command-ref/nix-env.md
[`use-xdg-base-directories`]: @docroot@/command-ref/conf-file.md#conf-use-xdg-base-directories
[channels]: @docroot@/command-ref/files/channels.md
