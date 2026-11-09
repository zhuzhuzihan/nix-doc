# Release 2.8 (2022-04-19)

* 新的实验性命令：`nix fmt`，它将 `formatter.<system>` Flakes 输出所定义的格式化工具应用到 Flakes 中的 Nix 表达式上。

* 多种 Nix 命令现在可以使用 `--file -` 从标准输入读取表达式。

* 新的实验性内置函数 `builtins.fetchClosure`，它在求值时从一个二进制缓存复制闭包，并将其重写为内容寻址形式（如果尚未如此）。与 `builtins.storePath` 类似，它允许导入预先构建好的存储路径；区别在于它不需要用户配置二进制缓存和受信任的公钥。

  只有在启用实验特性 `fetch-closure` 之后，此函数才可用。

* 新的实验特性：*非纯 derivation（派生）*。这类 derivation 每次构建都可能产生不同的结果。以下是一个示例：

  ```nix
  stdenv.mkDerivation {
    name = "impure";
    __impure = true; # marks this derivation as impure
    buildCommand = "date > $out";
  }
  ```

  对这个表达式运行两次 `nix build` 会构建该 derivation 两次，产生两个不同的内容寻址存储路径。与固定输出 derivation（fixed-output derivations）类似，非纯 derivation 可以访问网络。只有固定输出 derivation 和非纯 derivation 可以依赖于非纯 derivation。

* `nix store make-content-addressable` 已更名为 `nix store make-content-addressed`。

* `nixosModule` Flakes 输出属性已按照 Nix 2.7 中 `.default` 的重命名方式进行了更名。

  * `nixosModule` → `nixosModules.default`

  与之前一样，旧的输出仍可继续使用，但 `nix flake check` 会对此发出警告。

* `nix run` 现在对可接受的内容更加严格：`apps` Flakes 输出的成员现在必须是应用（app，定义见[手册](https://nix.dev/manual/nix/stable/command-ref/new-cli/nix3-run.html#apps)），而 `packages` 或 `legacyPackages` 的成员必须是 derivation（而非应用）。
