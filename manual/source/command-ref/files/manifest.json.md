## `manifest.json`

manifest 文件记录了由 [`nix profile`](@docroot@/command-ref/new-cli/nix3-profile.md)（实验性）管理的 [profile](./profiles.md) 中所安装软件包的来源信息。

以下示例展示了从 Nixpkgs 安装 `zoom-us` 后该文件可能的样子：

```json
{
  "version": 1,
  "elements": [
    {
      "active": true,
      "attrPath": "legacyPackages.x86_64-linux.zoom-us",
      "originalUrl": "flake:nixpkgs",
      "storePaths": [
        "/nix/store/wbhg2ga8f3h87s9h5k0slxk0m81m4cxl-zoom-us-5.3.469451.0927"
      ],
      "uri": "github:NixOS/nixpkgs/13d0c311e3ae923a00f734b43fd1d35b47d8943a"
    },
    …
  ]
}
```

数组 `elements` 中的每个对象表示一个已安装的软件包，
并包含以下字段：

* `originalUrl`：用户在安装时指定的 [flake 引用](@docroot@/command-ref/new-cli/nix3-flake.md)（例如 `nixpkgs`）。
  这也是 `nix profile upgrade` 将使用的 flake 引用。

* `uri`：`originalUrl` 解析后得到的锁定 flake 引用。

* `attrPath`：提供该软件包的 flake 输出属性。
  注意，这未必是用户指定的属性，而是应用了默认属性路径和前缀之后得到的结果；例如，`hello` 可能解析为
  `packages.x86_64-linux.hello`，而空字符串解析为
  `packages.x86_64-linux.default`。

* `storePath`：Nix store 中包含该软件包的路径。

* `active`：profile 中是否包含指向该软件包文件的符号链接。
  如果设置为 false，该软件包仍保留在 Nix store 中，但在 profile 的符号链接树中"不可见"。
