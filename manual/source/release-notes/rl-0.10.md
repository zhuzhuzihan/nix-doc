# Release 0.10 (2006-10-06)

> **注意**
> 
> 本版本的 Nix 使用 Berkeley DB 4.4 而非 4.3。数据库会自动升级，但你要小心，不要使用仍然使用 Berkeley DB 4.3 的旧版本 Nix。特别是，如果你使用的是通过 Nix 安装的 Nix，你应当先运行
> 
>     $ nix-store --clear-substitutes
> 
> 。

> **警告**
> 
> 此外，数据库 schema 为修复一个性能问题而略有改动（见下文）。当你第一次运行任何 Nix 0.10 命令时，数据库会被自动升级。此操作不可逆。

  - `nix-env` 易用性改进：
    
      - `nix-env
                                                        --query` 新增选项 `--compare-versions`（或 `-c`），允许你将已安装的软件包版本与可用版本进行比较，反之亦然。查看你是否与订阅 channel 中的内容保持同步的一个简单方式是 `nix-env -qc \*`。
    
      - `nix-env --query` 现在接受一个软件包名称列表作为参数，以显示关于它们的信息，就像 `--install` 等一样：例如 `nix-env -q gcc`。注意，要显示所有 derivation（派生），你需要指定 `\*`。
    
      - `nix-env -i
                                                        pkgname` 现在会安装 *pkgname* 的最高可用版本，而不是安装所有可用版本（那样很可能产生冲突）（`NIX-31`）。
    
      - `nix-env (-i|-u) --dry-run` 现在会确切显示哪些缺失路径将被构建或 substitute。
    
      - `nix-env -qa --description` 显示软件包的人类可读描述，前提是它们具有 `meta.description` 属性（Nixpkgs 中大多数软件包还没有该属性）。

  - 新的语言特性：
    
      - 引用扫描（在每次构建后发生）现在快得多，并且占用恒定的内存量。
    
      - 字符串插值。诸如
        
            "--with-freetype2-library=" + freetype + "/lib"
        
        的表达式现在可以写成
        
            "--with-freetype2-library=${freetype}/lib"
        
        你可以在 `${...}` 内写任意表达式，而不仅仅是标识符。
    
      - 多行字符串字面量。
    
      - 字符串拼接现在可以涉及 derivation，如示例 `"--with-freetype2-library="
                                                        + freetype + "/lib"`。此前这不可能，因为我们需要注册：使用这种字符串的 derivation 依赖于 `freetype`。求值器现在会正确传播这一信息。因此，子路径运算符（`~`）已被弃用。
    
      - 函数参数的默认值现在可以引用其他函数参数；也就是说，所有参数都在默认值的作用域内（`NIX-45`）。
    
      - 大量新的内建原语，例如列表操作和整数算术函数。完整列表见手册。所有 primop 现在都在集合 `builtins` 中可用，从而可以以向后兼容的方式检测某个 primop 是否可用。
    
      - 真正的 let 表达式：`let x = ...;
                                                        ... z = ...; in ...`。

  - 新命令 `nix-pack-closure` 和 `nix-unpack-closure`，可用于轻松地将一个存储路径及其全部依赖传输到另一台机器。当你机器上有某个软件包并想复制到别处时非常方便。

  - XML 支持：
    
      - `nix-env -q --xml` 以 XML 表示打印已安装或可用的软件包，便于其他工具处理。
    
      - `nix-instantiate --eval-only
                                                        --xml` 打印结果项的 XML 表示。（新标志 `--strict` 强制对结果进行"深度"求值，即列表元素和属性被递归求值。）
    
      - 在 Nix 表达式中，primop `builtins.toXML` 将一个项转换为 XML 表示。这主要用于向 builder 传递结构化信息。

  - 你现在可以使用 `--attr` / `-A` 标志在 `nix-env`、`nix-instantiate` 和 `nix-build` 中无歧义地指定要构建或安装哪个 derivation，该标志接受一个属性名作为参数。（与 `subversion-1.4.0` 这类符号性软件包名不同，属性集中的属性名是唯一的。）例如，对 Nixpkgs 中的某个软件包快速进行测试构建的方式是 `nix-build
            pkgs/top-level/all-packages.nix -A
            foo`。`nix-env -q
            --attr` 显示与每个 derivation 对应的属性名。

  - 如果 `nix-env`、`nix-instantiate` 或 `nix-build` 使用的顶层 Nix 表达式求值结果为一个函数，且其所有参数都有默认值，则该函数会被自动调用。此外，新的命令行开关 `--arg
            name
            value` 可用于在命令行上指定函数参数。

  - `nix-install-package --url
            URL` 允许直接从给定 URL 安装软件包。

  - Nix 现在可以在 HTTP 代理服务器之后工作；只需适当地设置标准环境变量 `http_proxy`、`https_proxy`、`ftp_proxy` 或 `all_proxy`。Nixpkgs 中的 `fetchurl` 等函数也遵循这些变量。

  - `nix-build -o
            symlink` 允许将指向构建结果的符号链接命名为 `result` 以外的名字。

  - 平台支持：
    
      - 支持 64 位平台，前提是使用[经过适当修补的 ATerm 库](http://bugzilla.sen.cwi.nl:8080/show_bug.cgi?id=606)。此外，现在支持大于 2 GiB 的文件。
    
      - 新增对 Cygwin（Windows，`i686-cygwin`）、Intel Mac OS X（`i686-darwin`）和 PowerPC Linux（`powerpc-linux`）的支持。
    
      - SMP 和多核机器的用户会很高兴：并行执行的构建数量现在可以在配置文件的 `build-max-jobs` 设置中指定。

  - 垃圾回收器改进：
    
      - 打开的文件（例如正在运行的程序）现在被用作垃圾回收器的根。这可以防止已卸载的程序在仍在运行时被垃圾回收。检测这些额外运行时根的脚本（`find-runtime-roots.pl`）本质上是系统相关的，但它应当能在 Linux 以及所有拥有 `lsof` 实用工具的平台上工作。
    
      - `nix-store --gc`（又名 `nix-collect-garbage`）会在标准输出上打印释放的字节数。`nix-store
                                                        --gc --print-dead` 显示一次实际的垃圾回收将释放多少字节。
    
      - `nix-collect-garbage -d` 在调用实际的垃圾回收器（`nix-store
                                                        --gc`）之前删除*所有* profile 的所有旧代际。这是清除 Nix store 中所有旧软件包的简便方法。
    
      - `nix-store` 现在有一个操作 `--delete`，用于从 Nix store 中删除特定路径。除非指定 `--ignore-liveness`，否则它不会删除可达的（非垃圾）路径。

  - 使用 Berkeley DB 4.4 的进程注册表（process registry）特性从崩溃的 Nix 进程中恢复。

  - 修复了 `referer` 表的一个性能问题，该表存储 `references` 表的逆（即它告诉你哪些存储路径引用了给定路径）。维护这张表可能需要平方级的时间，以及平方级的 Berkeley DB 日志文件空间（尤其是在运行垃圾回收器时）（`NIX-23`）。

  - Nix 现在除了 `INT` 信号外还会捕获 `TERM` 和 `HUP` 信号。因此你现在可以执行 `killall
            nix-store` 而不会触发数据库恢复。

  - `bsdiff` 更新到版本 4.3。

  - 表达式求值和 `nix-env -qa` 的显著性能改进，全部归功于 [Valgrind](http://valgrind.org/)。内存使用降低了约 8 倍。通过对路径哈希做记忆化带来了大幅提速。

  - 大量缺陷修复，特别是：
    
      - 确保磁盘满时垃圾回收器能够成功运行（`NIX-18`）。
    
      - `nix-env` 现在会锁定 profile，以防止对同一 profile 的并发 `nix-env` 操作之间的竞态（`NIX-7`）。
    
      - 移除了 `nix-env -i` 中误导性的消息（例如 ``installing
                                                        `foo'`` 之后跟着 ``uninstalling
                                                        `foo'``）（`NIX-17`）。

  - Nix 源码发行包现在小得多，因为我们不再包含 Berkeley DB 源码发行版的完整副本（只包含我们需要的部分）。

  - 头文件现在会被安装，以便外部程序可以使用 Nix 库。
