# Release 2.26.0 (2025-01-22)

- 支持相对路径输入 [#10089](https://github.com/NixOS/nix/pull/10089)

  Flakes 现在可以使用相对路径引用同一仓库中的其他 Flakes，例如
  ```nix
  inputs.foo.url = "path:./foo";
  ```
  会使用所引用 flake 的 `foo` 子目录中的 flake。更多信息请参阅关于 [`path` flake 输入类型](@docroot@/command-ref/new-cli/nix3-flake.md#path-fetcher)的文档。

  此特性要求对锁文件格式做出更改。旧版本的 Nix 将无法使用包含相对路径输入锁的锁文件。

- Flake 锁文件生成现在忽略本地注册表 [#12019](https://github.com/NixOS/nix/pull/12019)

  在解析 `flake.nix` 文件中像 `nixpkgs` 这样的间接 flake 引用时，Nix 将不再使用系统和用户 flake 注册表。它只会使用全局 flake 注册表，以及通过 `--override-flake` 在命令行上给出的覆盖项。

  这避免了如下事故：用户在本地注册表中存在把 `nixpkgs` 映射到本地文件系统中某个 `path:` flake 的覆盖项，而这些覆盖最终进入了已提交并推送给其他用户的锁文件。

  将来，我们可能会在锁文件生成期间完全移除对注册表的使用。显式指定 flake 输入的 URL 是更好的做法。例如，与其写
  ```nix
  {
    outputs = { self, nixpkgs }: { ... };
  }
  ```
  不如写
  ```nix
  {
    inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-24.11";
    outputs = { self, nixpkgs }: { ... };
  }
  ```

- `nix copy` 支持 `--profile` 与 `--out-link` [#11657](https://github.com/NixOS/nix/pull/11657)

  `nix copy` 命令现在拥有与 `nix build` 类似的 `--profile` 和 `--out-link` 标志。`--profile` 使某个 profile 指向顶层存储路径，而 `--out-link` 创建指向顶层存储路径的符号链接。

  例如，在从远程机器上的 NixOS 系统闭包更新本地 NixOS 系统 profile 时，以前需要
  ```
  # nix copy --from ssh://server $path
  # nix build --profile /nix/var/nix/profiles/system $path
  ```
  现在则可以执行
  ```
  # nix copy --from ssh://server --profile /nix/var/nix/profiles/system $path
  ```
  这样做的好处是避免了 *path* 不作为垃圾回收器 root、因而可能被并发的 `nix store gc` 进程删除的时间窗口。

- `nix-instantiate --eval` 现在支持 `--raw` [#12119](https://github.com/NixOS/nix/pull/12119)

  `nix-instantiate --eval` 命令现在支持 `--raw` 标志；使用该标志时，求值结果必须是字符串，它将被原样打印，不带引号或转义。

- 改进 `NIX_SSHOPTS` 解析，更好地处理 SSH 选项 [#5181](https://github.com/NixOS/nix/issues/5181) [#12020](https://github.com/NixOS/nix/pull/12020)

  `NIX_SSHOPTS` 环境变量的解析得到了改进，可以正确处理空格和引号。
  此前，被错误拆分的 SSH 选项可能导致诸如 `nix-copy-closure` 之类的命令失败，
  尤其是在使用 `-o ProxyCommand="ssh -W %h:%p ..."` 这类复杂 SSH 调用时。

  此变更引入了一个 `shellSplitString` 函数，确保
  `NIX_SSHOPTS` 以与 shell 行为一致的方式解析，从而解决常见的解析错误。

  例如，以下内容现在可以按预期工作：

  ```bash
  export NIX_SSHOPTS='-o ProxyCommand="ssh -W %h:%p ..."'
  ```

  此更新提升了各 Nix CLI 中使用 `NIX_SSHOPTS` 的 SSH 相关操作的可靠性。

- Nix 现在使用 Meson 构建

  如 [RFC 132](https://github.com/NixOS/rfcs/pull/132) 所提议，Nix 的构建系统现在使用 Meson/Ninja。旧的基于 Make 的构建系统已被移除。

- 求值缓存现在对脏的 Git 工作目录生效 [#11992](https://github.com/NixOS/nix/pull/11992)

## 贡献者

本发布版本得益于以下 45 位贡献者：

- Anatoli Babenia [**(@abitrolly)**](https://github.com/abitrolly)
- Domagoj Mišković [**(@allrealmsoflife)**](https://github.com/allrealmsoflife)
- Yaroslav Bolyukin [**(@CertainLach)**](https://github.com/CertainLach)
- bryango [**(@bryango)**](https://github.com/bryango)
- tomberek [**(@tomberek)**](https://github.com/tomberek)
- Matej Urbas [**(@mupdt)**](https://github.com/mupdt)
- elikoga [**(@elikoga)**](https://github.com/elikoga)
- wh0 [**(@wh0)**](https://github.com/wh0)
- Félix [**(@picnoir)**](https://github.com/picnoir)
- Valentin Gagarin [**(@fricklerhandwerk)**](https://github.com/fricklerhandwerk)
- Gavin John [**(@Pandapip1)**](https://github.com/Pandapip1)
- Travis A. Everett [**(@abathur)**](https://github.com/abathur)
- Vladimir Panteleev [**(@CyberShadow)**](https://github.com/CyberShadow)
- Ilja [**(@suruaku)**](https://github.com/suruaku)
- Jason Yundt [**(@Jayman2000)**](https://github.com/Jayman2000)
- Mike Kusold [**(@kusold)**](https://github.com/kusold)
- Andy Hamon [**(@andrewhamon)**](https://github.com/andrewhamon)
- Brian McKenna [**(@puffnfresh)**](https://github.com/puffnfresh)
- Greg Curtis [**(@gcurtis)**](https://github.com/gcurtis)
- Andrew Poelstra [**(@apoelstra)**](https://github.com/apoelstra)
- Linus Heckemann [**(@lheckemann)**](https://github.com/lheckemann)
- Tristan Ross [**(@RossComputerGuy)**](https://github.com/RossComputerGuy)
- Dominique Martinet [**(@martinetd)**](https://github.com/martinetd)
- h0nIg [**(@h0nIg)**](https://github.com/h0nIg)
- Eelco Dolstra [**(@edolstra)**](https://github.com/edolstra)
- Shahar "Dawn" Or [**(@mightyiam)**](https://github.com/mightyiam)
- NAHO [**(@trueNAHO)**](https://github.com/trueNAHO)
- Ryan Hendrickson [**(@rhendric)**](https://github.com/rhendric)
- the-sun-will-rise-tomorrow [**(@the-sun-will-rise-tomorrow)**](https://github.com/the-sun-will-rise-tomorrow)
- Connor Baker [**(@ConnorBaker)**](https://github.com/ConnorBaker)
- Cole Helbling [**(@cole-h)**](https://github.com/cole-h)
- Jack Wilsdon [**(@jackwilsdon)**](https://github.com/jackwilsdon)
- Martin Häcker [**(@dwt)**](https://github.com/dwt)
- Martin Fischer [**(@not-my-profile)**](https://github.com/not-my-profile)
- John Ericson [**(@Ericson2314)**](https://github.com/Ericson2314)
- Graham Christensen [**(@grahamc)**](https://github.com/grahamc)
- Sergei Zimmerman [**(@xokdvium)**](https://github.com/xokdvium)
- Siddarth Kumar [**(@siddarthkay)**](https://github.com/siddarthkay)
- Sergei Trofimovich [**(@trofi)**](https://github.com/trofi)
- Robert Hensing [**(@roberth)**](https://github.com/roberth)
- Mutsuha Asada [**(@momeemt)**](https://github.com/momeemt)
- Parker Jones [**(@knotapun)**](https://github.com/knotapun)
- Jörg Thalheim [**(@Mic92)**](https://github.com/Mic92)
- dbdr [**(@dbdr)**](https://github.com/dbdr)
- myclevorname [**(@myclevorname)**](https://github.com/myclevorname)
- Philipp Otterbein
