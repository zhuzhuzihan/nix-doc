# Release 0.16 (2010-08-17)

本版本包含以下改进：

  - Nix 表达式求值器在大多数情况下现在快得多：与旧实现相比通常[快 3 到 8 倍](http://www.mail-archive.com/nix-dev@cs.uu.nl/msg04113.html)。它的内存占用也更少。它不再依赖 ATerm 库。

  - 支持在 builder 内部配置并行度。构建脚本一直能够并行执行多个构建动作（例如运行 `make -j
                            2`），但这并不理想，因为并行执行的动作数量无法配置。Nix 现在新增选项 `--cores
                            N` 以及配置项 `build-cores =
                            N`，它们会在调用 builder 时将环境变量 `NIX_BUILD_CORES` 设为 *N*。builder 可以自行决定使用该变量进行并行构建，例如调用 `make -j
                            N`。在 Nixpkgs 中，可以通过将 derivation（派生）属性 `enableParallelBuilding` 设为 `true` 来按软件包启用此功能。

  - `nix-store -q` 现在通过 `--xml` 标志支持 XML 输出。

  - 若干缺陷修复。
