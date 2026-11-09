# 从源码构建 Nix

Nix 使用 [Meson](https://mesonbuild.com/) 构建。它被拆分成多个 Meson 软件包，这些软件包可选择通过 Meson 的 [subprojects](https://mesonbuild.com/Subprojects.html) 功能合并到单个项目中。

构建过程没有强制性的额外步骤：通用的 Meson 安装说明（例如[这份](https://mesonbuild.com/Quick-guide.html#using-meson-as-a-distro-packager)）应当可以直接使用。

```bash
git clone https://github.com/NixOS/nix.git
cd nix
meson setup build
cd build
ninja
(sudo) ninja install
```

可以通过向 `meson setup build` 传递 `-Dprefix=prefix` 来指定安装路径。默认安装目录是 `/usr/local`。你可以将其改为任何你喜欢的位置，但必须对 *prefix* 路径具有写权限。

Nix 默认将其 *store*（存放软件包的地方）保存在 `/nix/store`。可以使用 `-Dlibstore:store-dir=path` 更改它。

> **警告**
>
> 最好不要更改 Nix store 的默认位置，因为这样做会导致无法使用来自标准 Nixpkgs channel 的预构建二进制文件——也就是说，所有软件包都将需要从源码构建。

Nix 默认将其状态（例如数据库和日志文件）保存在 `/nix/var`。可以使用 `-Dlocalstatedir=path` 更改它。
