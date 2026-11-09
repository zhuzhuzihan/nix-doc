# 可锁定 HTTP Tarball 协议

Tarball flake 可以作为普通 tarball 通过 HTTP 或文件系统（针对 `file://` URL）提供。除非服务器实现了可锁定 HTTP Tarball 协议，否则确保 URL 始终产生相同 tarball 内容是用户自己的责任。

HTTP 服务器可以返回一个适用于 lock 文件的「不可变」（immutable）HTTP URL。这使得用户可以在 `flake.nix` 中指定一个请求 flake 最新版本的 tarball flake 输入（例如 `https://example.org/hello/latest.tar.gz`），而 `flake.lock` 会记录一个内容不会变化的 URL（例如 `https://example.org/hello/<revision>.tar.gz`）。为此，服务器必须返回一个 `rel` 属性设置为 `immutable` 的 [HTTP `Link` 头](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Link)，如下所示：

```
Link: <flakeref>; rel="immutable"
```

（注意 *flakeref* 两侧必需的 `<` 和 `>` 字符。）

*flakeref* 必须是一个 tarball flakeref。它可以包含 tarball flake 属性 `narHash`、`rev`、`revCount` 和 `lastModified`。如果包含 `narHash`，其值必须是解包后 tarball 的 [NAR 哈希][Nix Archive]（通过 `nix hash path` 计算）。Nix 会依据 `narHash` 属性检查返回的 tarball 内容。当 tarball flake 是某个具备这些属性的 fetcher 类型（如 Git 或 GitHub）的镜像时，`rev` 和 `revCount` 属性很有用。Nix 不会检查它们。

```
Link: <https://example.org/hello/442793d9ec0584f6a6e82fa253850c8085bb150a.tar.gz
  ?rev=442793d9ec0584f6a6e82fa253850c8085bb150a
  &revCount=835
  &narHash=sha256-GUm8Uh/U74zFCwkvt9Mri4DSM%2BmHj3tYhXUkYpiv31M%3D>; rel="immutable"
```

（本示例中的换行仅为清晰起见，实际响应中不得包含。）

对于 tarball flake，flake 属性 `lastModified` 的值定义为 tarball 内最新文件的时间戳。

## Gitea 与 Forgejo 支持

Gitea 自 v1.22.1 起、Forgejo 自 v7.0.4/v8.0.0 起支持该协议，并可与以下 flake URL 模式配合使用：

```
https://<domain name>/<owner>/<repo>/archive/<reference or revision>.tar.gz
```

> **示例**
>
>
> ```nix
> # flake.nix
> {
>    inputs = {
>      foo.url = "https://gitea.example.org/some-person/some-flake/archive/main.tar.gz";
>      bar.url = "https://gitea.example.org/some-other-person/other-flake/archive/442793d9ec0584f6a6e82fa253850c8085bb150a.tar.gz";
>      qux = {
>        url = "https://forgejo.example.org/another-person/some-non-flake-repo/archive/development.tar.gz";
>        flake = false;
>      };
>    };
>    outputs = { foo, bar, qux }: { /* ... */ };
> }
```

[Nix Archive]: @docroot@/store/file-system-object/content-address.md#serial-nix-archive
