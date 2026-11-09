# Release 0.9 (2005-09-16)

注意：本版本的 Nix 使用 Berkeley DB 4.3 而非 4.2。数据库会自动升级，但你要小心，不要使用仍然依赖 Berkeley DB 4.2 的旧版本 Nix。特别是，如果你使用的是通过 Nix 安装的 Nix，你应当先运行：

    $ nix-store --clear-substitutes

  - 补丁序列的解包现在快得多，因为我们不再对中间路径进行冗余的解包和重新打包。

  - Nix 现在使用 Berkeley DB 4.3。

  - `derivation` 原语更加惰性。依赖的 derivation（派生）的属性可以相互引用（只要对由 `derivation` 计算出的 `outPath` 和 `drvPath` 属性没有数据依赖）。
    
    例如，表达式 `derivation
            attrs` 现在求值结果为（本质上）
    
        attrs // {
          type = "derivation";
          outPath = derivation! attrs;
          drvPath = derivation! attrs;
        }
    
    其中 `derivation!` 是一个执行实际 derivation 实例化的 primop（也就是说，它做的是 `derivation` 过去做的事情）。这样做的好处是，`nix-env -qa` 和 `nix-env -i` 等命令可以快得多，因为它们不再需要实例化所有 derivation，而只需要 `name` 属性。
    
    此外，它还允许 derivation 之间循环引用，例如：
    
        webServer = derivation {
          ...
          hostName = "svn.cs.uu.nl";
          services = [svnService];
        };
         
        svnService = derivation {
          ...
          hostName = webServer.hostName;
        };
    
    在此之前，这会产生一个黑洞（无限递归）。

  - 如果未指定 Nix 表达式，`nix-build` 现在默认使用 `./default.nix`。

  - `nix-instantiate` 应用于求值结果为函数的 Nix 表达式时，如果该函数的所有参数都有默认值，就会自动调用该函数。

  - Nix 现在使用 libtool 构建动态库。这减小了可执行文件的体积。

  - 新的列表拼接运算符 `++`。例如，`[1 2 3] ++
    [4 5
            6]` 求值结果为 `[1 2 3 4 5
            6]`。

  - 一些目前未写入文档的 primop，用于支持使用 Nix 进行底层构建管理（即把 Nix 用作 Make 的替代品）。参见 `r3578` 和 `r3580` 的提交消息。

  - 若干缺陷修复和性能改进。
