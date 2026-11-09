# Release 2.9 (2022-05-30)

* 使用新的 `--debugger` 标志运行 Nix 时，如果求值过程中抛出异常，或者调用了 `builtins.break`，它将启动一个 repl 会话。在那里你可以检查变量的值并求值 Nix 表达式。在调试模式下，以下新的 repl 命令可用：

  ```
  :env          Show env stack
  :bt           Show trace stack
  :st           Show current trace
  :st <idx>     Change to another trace in the stack
  :c            Go until end of program, exception, or builtins.break().
  :s            Go one step
  ```

  更多关于调试器的信息请阅读[这里](https://www.zknotes.com/note/5970)。

* Nix 现在提供了与 zsh 的 `run-help` 功能更好的集成。它现在以可自动加载的 shell 函数 `run-help-nix` 的形式包含在 Nix 的安装中。它会从当前输入的命令中识别 Nix 子命令，并引导用户查阅相关的 man 手册页。

* `nix repl` 新增了构建并链接（`:bl`）命令，它在构建 derivation（派生）的同时创建 GC root 符号链接。

* `builtins.toFile` 产生的路径现在即使在受限求值（restricted evaluation）下也允许被导入或读取。注意这在只读 store 上不可行。

* `nix build` 新增了 `--print-out-paths` 标志，用于打印产生的输出路径。这与 `nix-build` 的默认行为一致。

* 你现在可以使用 `installable^outputs` 语法指定 `nix` 应操作 derivation 的哪些输出，例如 `nixpkgs#glibc^dev,static` 或 `nixpkgs#glibc^*`。默认情况下，`nix` 会使用 derivation 的 `meta.outputsToInstall` 属性（如果存在）所指定的输出，否则使用全部输出。

* `builtins.fetchTree`（以及 Flakes 输入）现在除了目录 tarball 之外，还可以通过 `http(s)` 和 `file` 协议获取普通文件。
