# Release 2.7 (2022-03-07)

* 当你在命令行上输入错误时，Nix 现在会给出一些有用的提示。例如，如果你输入 `nix build nixpkgs#thunderbrd`，它会建议你使用 `thunderbird`。

* 若干「默认」Flakes 输出属性已被重命名。具体如下：

  * `defaultPackage.<system>` → `packages.<system>.default`
  * `defaultApps.<system>` → `apps.<system>.default`
  * `defaultTemplate` → `templates.default`
  * `defaultBundler.<system>` → `bundlers.<system>.default`
  * `overlay` → `overlays.default`
  * `devShell.<system>` → `devShells.<system>.default`

  旧的 Flakes 输出属性仍然可用，但 `nix flake check` 会对它们发出警告。

* 破坏性 API 变更：`nix bundle` 现在支持形如 `bundler.<system>.<name>= derivation: another-derivation;` 的 bundler。这为在打包过程中检查求值信息提供了额外的功能支持。一个新的[代码仓库](https://github.com/NixOS/bundlers)中实现了多种 bundler。

* `nix store ping` 现在会报告远程 Nix daemon（守护进程）的版本。

* `nix flake {init,new}` 现在会显示哪些文件已被创建的信息。

* 模板现在可以定义 `welcomeText` 属性，它会在执行 `nix flake {init,new} --template <template>` 时打印出来。
