# Release 1.6 (2013-09-10)

除了常规的缺陷修复之外，本版本还带来了若干新特性：

  - 命令 `nix-build --run-env` 已更名为 `nix-shell`。

  - `nix-shell` 现在是在交互式 shell *内部* source `$stdenv/setup`，而不是在父 shell 中。这确保了 `stdenv` 定义的 shell 函数可以在交互式 shell 中使用。

  - `nix-shell` 新增标志 `--pure` 用于清空环境变量，使你获得一个更接近"真实" Nix 构建的环境。

  - `nix-shell` 现在会设置 shell 提示符（`PS1`），确保 Nix shell 与你的常规 shell 可以区分开。

  - `nix-env` 不再需要 `*` 参数来匹配所有软件包，因此 `nix-env -qa` 等价于 `nix-env -qa '*'`。

  - `nix-env -i` 新增标志 `--remove-all`（`-r`），用于从 profile 中移除所有先前的软件包。这使得进行类似于 NixOS `environment.systemPackages` 的声明式软件包管理变得更加容易。例如，如果你有一个如下所示的规格文件 `my-packages.nix`：
    
        with import <nixpkgs> {};
        [ thunderbird
          geeqie
          ...
        ]
    
    那么在修改这个文件之后，你可以运行：
    
        $ nix-env -f my-packages.nix -ir
    
    来把你的 profile 更新为与该规格一致。

  - '`with`' 语言构造现在更加惰性。只有当某个变量确实可能引用其参数中的属性时，它才会对参数求值。例如，下面这段代码现在可以工作了：
    
        let
          pkgs = with pkgs; { foo = "old"; bar = foo; } // overrides;
          overrides = { foo = "new"; };
        in pkgs.bar
    
    它求值为 `"new"`，而此前会报"无限递归"错误。

  - Nix 现在拥有真正的整数算术运算符。例如，你可以写 `x + y` 而不是 `builtins.add x y`，写 `x < y` 而不是 `builtins.lessThan x y`。比较运算符也可以作用于字符串。

  - 在 64 位系统上，Nix 整数现在是 64 位而非 32 位。

  - 使用 Nix daemon（守护进程）时，在支持设置 CPU 亲和性的系统上，`nix-daemon` worker 进程现在会与客户端运行在相同的 CPU 上。这在某些系统上带来了显著的提速。

  - 当 Nix 求值器发生栈溢出时，在某些系统上你现在会得到一个正确的错误信息（而不是"Segmentation fault"）。

  - 除了目录之外，现在还可以通过（如今名不副实的）选项 `build-chroot-dirs` 在 chroot 中 bind-mount 普通文件。

本版本包含 Domen Kožar、Eelco Dolstra、Florian Friesdorf、Gergely Risko、Ivan Kozik、Ludovic Courtès 和 Shea Levy 的贡献。
