# Release 2.1 (2018-09-02)

这主要是一个修复缺陷的版本。它还在某些情况下降低了内存消耗。此外，它包含以下新特性：

  - Nix 安装器在 macOS 上不再默认进行多用户（Multi-User）安装。你仍然可以指示安装器以多用户模式运行。

  - Nix 安装器现在支持在运行 systemd 的 Linux 计算机上执行多用户安装。你可以通过向安装器传递 `--daemon` 标志来选择多用户安装：`sh <(curl -L https://nixos.org/nix/install) --daemon`。

    多用户安装器无法处理带 SELinux 的系统。如果你的系统启用了 SELinux，你可以强制安装器以单用户模式运行。

  - 新增内置函数：`builtins.bitAnd`、`builtins.bitOr`、`builtins.bitXor`、`builtins.fromTOML`、`builtins.concatMap`、`builtins.mapAttrs`。

  - S3 二进制缓存 store 现在支持上传大于 5 GiB 的 NAR。

  - S3 二进制缓存 store 现在支持通过 `endpoint` 选项上传到 S3 兼容的服务。

  - 从二进制缓存中消失的 NAR 中恢复时，不再需要 `--fallback` 标志。

  - `nix-daemon` 现在会尊重 `--store`。

  - `nix run` 现在会尊重 `nix-support/propagated-user-env-packages`。

本版本包含 Adrien Devresse、Aleksandr Pashkov、Alexandre Esteves、Amine Chikhaoui、Andrew Dunham、Asad Saeeduddin、aszlig、Ben Challenor、Ben Gamari、Benjamin Hipple、Bogdan Seniuc、Corey O'Connor、Daiderd Jordan、Daniel Peebles、Daniel Poelzleithner、Danylo Hlynskyi、Dmitry Kalinkin、Domen Kožar、Doug Beardsley、Eelco Dolstra、Erik Arvstedt、Félix Baylac-Jacqué、Gleb Peregud、Graham Christensen、Guillaume Maudoux、Ivan Kozik、John Arnold、Justin Humm、Linus Heckemann、Lorenzo Manacorda、Matthew Justin Bauer、Matthew O'Gorman、Maximilian Bosch、Michael Bishop、Michael Fiano、Michael Mercier、Michael Raskin、Michael Weiss、Nicolas Dudebout、Peter Simons、Ryan Trinkle、Samuel Dionne-Riel、Sean Seefried、Shea Levy、Symphorien Gibol、Tim Engler、Tim Sears、Tuomas Tynkkynen、volth、Will Dietz、Yorick van Pelt 和 zimbatm 的贡献。
