# Release 1.8 (2014-12-14)

  - 破坏性变更：为解决一个竞态条件，远程构建钩子机制现在在远程机器上使用 `nix-store --serve`。这要求构建 slave 更新到 Nix 1.8。

  - Nix 现在改用 HTTPS 而不是 HTTP 来访问默认的二进制缓存 `cache.nixos.org`。

  - `nix-env` 的选择器现在是正则表达式。例如，你可以执行
    
        $ nix-env -qa '.*zip.*'
    
    来查询所有名称中包含 `zip` 的软件包。

  - `nix-store --read-log` 现在可以获取远程构建日志。如果某个构建日志在本地不可用，'nix-store -l' 现在会尝试从 nix.conf 中 'log-servers' 选项列出的服务器下载它。例如，如果你有如下配置选项
    
        log-servers = http://hydra.nixos.org/log
    
    那么它会尝试从 `http://hydra.nixos.org/log/存储路径的基本名称` 获取日志。这让你可以做到类似这样的事情：
    
        $ nix-store -l $(which xterm)
    
    即使 `xterm` 不是在本地构建的，也能拿到日志。

  - 新增内置函数：`attrValues`、`deepSeq`、`fromJSON`、`readDir`、`seq`。

  - `nix-instantiate --eval` 现在有一个 `--json` 标志，以 JSON 格式打印求值结果。

  - `nix-copy-closure` 现在在远端使用 `nix-store --serve` 来发送或接收 closure。这修复了 `nix-copy-closure` 与垃圾回收器之间的一个竞态条件。

  - derivation（派生）可以指定新的特殊属性 `allowedRequisites`，它的含义与 `allowedReferences` 类似。但它不仅仅强制显式指定直接引用，而是要求 derivation 递归地指定其产出所使用的全部依赖（因此得名 requisites，即"所需之物"）。

  - 在 Mac OS X 上，Nix 现在在从大小写敏感的文件系统导入 closure 时会处理大小写冲突。这对在 Mac OS X 上运行 NixOps 尤其有用。

  - Nix daemon（守护进程）新增配置选项 `allowed-users`（指定允许连接到 daemon 的用户和组）和 `trusted-users`（指定可以执行特权操作（例如指定不受信任的二进制缓存）的用户和组）。

  - 配置选项 `build-cores` 现在默认为可用 CPU 核心数。

  - 当 Nix 以 root 身份调用时，现在默认使用构建用户。这可以防止构建意外地以 root 身份运行。

  - Nix 现在包含 systemd unit 和 Upstart job。

  - `nix-store --optimise` 的速度得到提升。

  - 语言变更：`==` 运算符现在会忽略字符串上下文（string context，即字符串所携带的"依赖"信息）。

  - Nix 现在会过滤掉标准错误输出中的 Nix 专用 ANSI 转义序列。它们本应是不可见的，但某些终端还是会把它们显示出来。

  - 多个命令现在会自动把输出通过管道交给由 `PAGER` 环境变量指定的分页器。

  - 多项改进降低了求值器的内存消耗。

本版本包含 Adam Szkoda、Aristid Breitkreuz、Bob van der Linden、Charles Strahan、darealshinji、Eelco Dolstra、Gergely Risko、Joel Taylor、Ludovic Courtès、Marko Durkovic、Mikey Ariel、Paul Colomiets、Ricardo M. Correia、Ricky Elrod、Robert Helgesson、Rob Vermaas、Russell O'Connor、Shea Levy、Shell Turner、Sönke Hahn、Steve Purcell、Vladimír Čunát 和 Wout Mertens 的贡献。
