# 前提条件

  此列表及其中的版本下限按“尽力维护”的原则更新。如有疑问，请查看 `meson.build` 文件。

  - Meson 构建系统（<https://github.com/mesonbuild/meson>）。

  - Ninja（<https://ninja-build.org/>）。

  - 支持 C++23 的 GCC 或 Clang 版本（任何比 Clang 19 或 GCC 14 更新的版本都很可能可用）。

  - 用于定位依赖的 `pkg-config`。
    如果你的发行版没有提供，可以从 <http://www.freedesktop.org/wiki/Software/pkg-config> 获取。

  - 用于计算加密哈希的 OpenSSL 库。
    如果你的发行版没有提供，可以从 <https://www.openssl.org> 获取。

  - 提供 Brotli 压缩算法实现的 `libbrotlienc` 和 `libbrotlidec` 库。
    可以从官方仓库 <https://github.com/google/brotli> 下载。

  - cURL 库。
    如果你的发行版没有提供，可以从 <https://curl.haxx.se/> 获取。

  - SQLite 嵌入式数据库库，版本 3.6.19 或更高。
    如果你的发行版没有提供，请从 <http://www.sqlite.org/> 安装。

  - 用于减少求值器内存消耗的 [Boehm 垃圾收集器（`bdw-gc`）](http://www.hboehm.info/gc/)（可选）。
    要启用它，请安装 `pkgconfig` 和 Boehm 垃圾收集器，并向 `meson setup` 传递选项 `-Dlibexpr:gc=enabled`。

  - `boost` 库，版本 1.87.0 或更高。
    可以从官方网站 <https://www.boost.org/> 获取。

  - `editline` 库，版本 1.14.0 或更高。
    可以从其仓库 <https://github.com/troglobit/editline> 获取。

  - 用于验证从二进制缓存获取内容的加密签名的 `libsodium` 库。
    可以从官方网站 <https://libsodium.org> 获取。

  - 用于构建解析器的较新版本的 Bison 和 Flex。
    （这是因为 Nix 需要 Bison 提供 C++ 模板支持、Flex 提供可重入支持。）

  - `libseccomp` 用于在 Linux 上提供系统调用过滤。
    这是一个可选依赖，可以通过向 `meson setup` 命令传递 `-Dlibstore:seccomp-sandboxing=disabled` 选项来禁用
    （除非你的系统不支持 `libseccomp`，否则不建议这样做）。
    要获取该库，请访问 <https://github.com/seccomp/libseccomp>。

  - 仅在 64 位 x86 机器上，使用 `libcpuid` 库来确定支持哪些微架构级别
    （例如，判断是否应在附加系统类型中包含 `x86_64-v2-linux`）。
    该库可从其主页 <http://libcpuid.sourceforge.net> 获取。
    这是一个可选依赖，可以通过向 `meson setup` 脚本提供 `-Dlibutil:cpuid=disabled` 选项来禁用。

  - 除非指定了 `meson setup build -Dunit-tests=false`，否则需要 GoogleTest（GTest）和 RapidCheck，它们分别可在
    <https://google.github.io/googletest/> 和 <https://github.com/emil-e/rapidcheck> 获取。
