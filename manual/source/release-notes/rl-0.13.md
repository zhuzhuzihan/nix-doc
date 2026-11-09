# Release 0.13 (2009-11-05)

这主要是一个缺陷修复版本，同时也有一些新特性：

  - 用于编写嵌套属性集的语法糖。与其写
    
        {
          foo = {
            bar = 123;
            xyzzy = true;
          };
          a = { b = { c = "d"; }; };
        }
    
    你可以写
    
        {
          foo.bar = 123;
          foo.xyzzy = true;
          a.b.c = "d";
        }
    
    例如，这在 NixOS 配置文件中很有用。

  - 支持由 Hydra（基于 Nix 的持续构建系统）生成的 Nix channel。（Hydra 会即时生成 NAR 归档，因此这些归档的大小和哈希事先未知。）

  - 在 `x86_64-linux` 的 Nix 安装上直接支持 `i686-linux` 构建。这是通过 `personality()` 系统调用实现的，它使 `uname` 在子进程中返回 `i686`。

  - 对 `chroot` 支持的多项改进。在 `chroot` 中构建现在工作得相当好。

  - 当 Nix 尝试构建某个路径而另一个进程已在构建同一路径时，不再阻塞，而是先尝试构建另一个可构建的路径。这提升了并行度。

  - 支持 NAR 归档中的大文件（\> 4 GiB）。

  - 远程构建机制的多项（性能）改进。

  - 新的 primop：`builtins.addErrorContext`（向堆栈跟踪添加字符串——对调试很有用）、`builtins.isBool`、`builtins.isString`、`builtins.isInt`、`builtins.intersectAttrs`。

  - OpenSolaris 支持。（Sander van der Burg）

  - 除非使用 `--show-trace` 选项，否则不再显示堆栈跟踪。

  - 递归属性集中 `inherit
                    (e) ...` 的作用域规则已改变。表达式 *e* 现在可以引用包含它的集合中定义的属性。
