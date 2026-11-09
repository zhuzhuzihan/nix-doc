# Release 2.27.0 (2025-03-03)

- `inputs.self.submodules` flake 属性 [#12421](https://github.com/NixOS/nix/pull/12421)

  Git 仓库中的 Flakes 现在可以声明需要启用 Git 子模块：
  ```
  {
    inputs.self.submodules = true;
  }
  ```
  这样一来，flake 的调用者不再需要传递 `submodules = true`。

- Git LFS 支持 [#10153](https://github.com/NixOS/nix/pull/10153) [#12468](https://github.com/NixOS/nix/pull/12468)

  Git 抓取器现在支持大文件存储（Large File Storage，LFS）。可以通过向抓取器传递属性 `lfs = true` 来启用，例如
  ```console
  nix flake prefetch 'git+ssh://git@github.com/Apress/repo-with-large-file-storage.git?lfs=1'
  ```

  一个 flake 也可以声明它需要启用 LFS：
  ```
  {
    inputs.self.lfs = true;
  }
  ```

  作者：[**@b-camacho**](https://github.com/b-camacho)、[**@kip93**](https://github.com/kip93)

- 处理使用 chroot store 且某些输入位于“宿主” `/nix/store` 中的情况 [#12512](https://github.com/NixOS/nix/pull/12512)

  求值器现在会呈现宿主与 chroot 中 `/nix/store` 的“联合”（union）文件系统视图。

  此变更还移除了一些会在 chroot store 中破坏 `builtins.{path,filterSource}` 的临时处理（hack）[#11503](https://github.com/NixOS/nix/issues/11503)。

- `nix flake prefetch` 现在有了 `--out-link` 选项 [#12443](https://github.com/NixOS/nix/pull/12443)

- 为 curl 创建的套接字设置 `FD_CLOEXEC` [#12439](https://github.com/NixOS/nix/pull/12439)

  curl 创建套接字时没有设置 `FD_CLOEXEC`/`SOCK_CLOEXEC`。此前这可能导致使用 `nix shell` 等命令时连接永远保持打开。此变更通过 `CURLOPT_SOCKOPTFUNCTION` 回调来设置 `FD_CLOEXEC` 标志。

- 添加 BLAKE3 哈希算法 [#12379](https://github.com/NixOS/nix/pull/12379)

  Nix 现在以实验性特性（`blake3-hashes`）的形式支持 BLAKE3 哈希算法：

  ```console
  # nix hash file ./file --type blake3 --extra-experimental-features blake3-hashes
  blake3-34P4p+iZXcbbyB1i4uoF7eWCGcZHjmaRn6Y7QdynLwU=
  ```

## 贡献者

本发布版本得益于以下 21 位贡献者：

- Aiden Fox Ivey [**(@aidenfoxivey)**](https://github.com/aidenfoxivey)
- Ben Millwood [**(@bmillwood)**](https://github.com/bmillwood)
- Brian Camacho [**(@b-camacho)**](https://github.com/b-camacho)
- Brian McKenna [**(@puffnfresh)**](https://github.com/puffnfresh)
- Eelco Dolstra [**(@edolstra)**](https://github.com/edolstra)
- Fabian Möller [**(@B4dM4n)**](https://github.com/B4dM4n)
- Illia Bobyr [**(@ilya-bobyr)**](https://github.com/ilya-bobyr)
- Ivan Trubach [**(@tie)**](https://github.com/tie)
- John Ericson [**(@Ericson2314)**](https://github.com/Ericson2314)
- Jörg Thalheim [**(@Mic92)**](https://github.com/Mic92)
- Leandro Emmanuel Reina Kiperman [**(@kip93)**](https://github.com/kip93)
- MaxHearnden [**(@MaxHearnden)**](https://github.com/MaxHearnden)
- Philipp Otterbein
- Robert Hensing [**(@roberth)**](https://github.com/roberth)
- Sandro [**(@SuperSandro2000)**](https://github.com/SuperSandro2000)
- Sergei Zimmerman [**(@xokdvium)**](https://github.com/xokdvium)
- Silvan Mosberger [**(@infinisil)**](https://github.com/infinisil)
- Someone [**(@SomeoneSerge)**](https://github.com/SomeoneSerge)
- Steve Walker [**(@stevalkr)**](https://github.com/stevalkr)
- bcamacho2 [**(@bcamacho2)**](https://github.com/bcamacho2)
- silvanshade [**(@silvanshade)**](https://github.com/silvanshade)
- tomberek [**(@tomberek)**](https://github.com/tomberek)
