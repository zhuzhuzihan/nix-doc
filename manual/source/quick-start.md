# 快速上手

本章面向不喜欢阅读文档的急性子。如需更深入的信息，请参阅后续章节。

1. 安装 Nix：

   ```console
   $ curl -L https://nixos.org/nix/install | sh
   ```

   安装脚本会使用 `sudo`，因此请确保你拥有足够的权限。

   有关其他安装方式，请参见详细的[安装说明](installation/index.md)。

1. 无需永久安装即可运行软件：

   ```console
   $ nix-shell --packages cowsay lolcat
   ```

   该命令会下载指定的软件包及其全部依赖，并把你带入一个 Bash shell，其中这些软件包提供的命令均可使用。这不会影响你的正常环境：

   ```console
   [nix-shell:~]$ cowsay Hello, Nix! | lolcat
   ```

   退出 shell 后，这些程序就会消失：

   ```console
   [nix-shell:~]$ exit
   $ lolcat
   lolcat: command not found
   ```

1. 在 [search.nixos.org](https://search.nixos.org/) 上搜索更多软件包并试用。

1. 释放存储空间：

   ```console
   $ nix-collect-garbage
   ```
