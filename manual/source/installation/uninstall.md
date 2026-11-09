# 卸载 Nix

## 多用户

移除[多用户安装](./installing-binary.md#multi-user-installation)的方法取决于操作系统。

### Linux

如果你使用的是带 systemd 的 Linux：

1. 移除 Nix daemon 服务：

   ```console
   sudo systemctl stop nix-daemon.service
   sudo systemctl disable nix-daemon.socket nix-daemon.service
   sudo systemctl daemon-reload
   ```

2. 移除 Nix 创建的文件：

   ```console
   sudo rm -rf /etc/nix /etc/profile.d/nix.sh /etc/tmpfiles.d/nix-daemon.conf /nix ~/.local/share/nix ~/.local/state/nix ~/.cache/nix ~/.nix-defexpr ~/.nix-profile ~/.nix-channels ~root/.nix-channels ~root/.nix-defexpr ~root/.nix-profile ~root/.cache/nix
   ```

3. 移除构建用户及其组：

   ```console
   for i in $(seq 1 32); do
     sudo userdel nixbld$i
   done
   sudo groupdel nixbld
   ```

4. 以下文件中可能还存在对 Nix 的引用：
   - `/etc/bash.bashrc`
   - `/etc/bashrc`
   - `/etc/profile`
   - `/etc/zsh/zshrc`
   - `/etc/zshrc`

   你可以将它们移除。

### FreeBSD

1. 停止并移除 Nix daemon 服务：

   ```console
   sudo service nix-daemon stop
   sudo rm -f /usr/local/etc/rc.d/nix-daemon
   sudo sysrc -x nix_daemon_enable
   ```

2. 移除 Nix 创建的文件：

   ```console
   sudo rm -rf /etc/nix /usr/local/etc/profile.d/nix.sh /nix ~/.local/share/nix ~/.local/state/nix ~/.cache/nix ~/.nix-defexpr ~/.nix-profile ~/.nix-channels ~root/.nix-channels ~root/.nix-defexpr ~root/.nix-profile ~root/.cache/nix
   ```

3. 移除构建用户及其组：

   ```console
   for i in $(seq 1 32); do
     sudo pw userdel nixbld$i
   done
   sudo pw groupdel nixbld
   ```

4. 以下位置可能还存在对 Nix 的引用：
   - `/usr/local/etc/bashrc`
   - `/usr/local/etc/zshrc`
   - 用户主目录中的 shell 配置文件

   你可以将它们移除。

### macOS

> **更新到 macOS 15 Sequoia**
>
> 如果你最近更新到了 macOS 15 Sequoia，并且在运行 Nix 命令时遇到
> ```console
> error: the user '_nixbld1' in the group 'nixbld' does not exist
> ```
> 错误，请参阅 GitHub issue [NixOS/nix#10892](https://github.com/NixOS/nix/issues/10892)，了解在不重新安装的情况下修复安装的方法。

1. 如果系统级 shell 初始化文件自安装 Nix 以来未被修改过，可以使用安装器所做的备份：

   ```console
   sudo mv /etc/zshrc.backup-before-nix /etc/zshrc
   sudo mv /etc/bashrc.backup-before-nix /etc/bashrc
   sudo mv /etc/bash.bashrc.backup-before-nix /etc/bash.bashrc
   ```

   否则，请编辑 `/etc/zshrc`、`/etc/bashrc` 和 `/etc/bash.bashrc`，删除 source `nix-daemon.sh` 的那些行，它们看起来应该像这样：

   ```bash
   # Nix
   if [ -e '/nix/var/nix/profiles/default/etc/profile.d/nix-daemon.sh' ]; then
     . '/nix/var/nix/profiles/default/etc/profile.d/nix-daemon.sh'
   fi
   # End Nix
   ```

2. 停止并移除 Nix daemon 服务：

   ```console
   sudo launchctl unload /Library/LaunchDaemons/org.nixos.nix-daemon.plist
   sudo rm /Library/LaunchDaemons/org.nixos.nix-daemon.plist
   sudo launchctl unload /Library/LaunchDaemons/org.nixos.darwin-store.plist
   sudo rm /Library/LaunchDaemons/org.nixos.darwin-store.plist
   ```

   这会停止 Nix daemon，并防止它在下次启动系统时被启动。

3. 移除 `nixbld` 组和 `_nixbuildN` 用户：

   ```console
   sudo dscl . -delete /Groups/nixbld
   for u in $(sudo dscl . -list /Users | grep _nixbld); do sudo dscl . -delete /Users/$u; done
   ```

   这将移除所有已无用途的构建用户。

4. 使用 `sudo vifs` 编辑 fstab，删除在 `/nix` 上挂载 Nix Store 卷的那一行，它看起来像

   ```
   UUID=<uuid> /nix apfs rw,noauto,nobrowse,suid,owners
   ```
   或

   ```
   LABEL=Nix\040Store /nix apfs rw,nobrowse
   ```

   操作方式是用方向键将光标移到相应行上，按 `dd` 删除该行，然后按 `:wq` 保存文件。

   这将阻止 Nix Store 卷被自动挂载。

5. 编辑 `/etc/synthetic.conf`，删除 `nix` 那一行。
   如果这是文件中唯一的一行，你可以把整个文件删掉：

   ```bash
   if [ -f /etc/synthetic.conf ]; then
     if [ "$(cat /etc/synthetic.conf)" = "nix" ]; then
       sudo rm /etc/synthetic.conf
     else
       sudo vi /etc/synthetic.conf
     fi
   fi
   ```

   这将阻止创建空的 `/nix` 目录。

6. 移除 Nix 添加到系统中的文件（store 除外）：

   ```console
   sudo rm -rf /etc/nix /var/root/.nix-profile /var/root/.nix-defexpr /var/root/.nix-channels ~/.nix-profile ~/.nix-defexpr ~/.nix-channels ~/.local/share/nix ~/.local/state/nix ~/.cache/nix
   ```


7. 移除 Nix Store 卷：

   ```console
   sudo diskutil apfs deleteVolume /nix
   ```

   这将移除 Nix Store 卷以及添加到该 store 中的所有内容。

   如果输出显示该命令未能移除卷，你应当确认没有处于 _已卸载_ 状态的 Nix Store 卷。
   请在以下命令的输出中查找名为 "Nix Store" 的卷：

   ```console
   diskutil list
   ```

   如果你 _确实_ 找到了 "Nix Store" 卷，请使用该 store 卷的 `diskXsY` 标识符运行 `diskutil apfs deleteVolume` 将其删除。

   如果你收到卷正被内核占用的错误，请重启系统，并在启动任何其他进程之前立即删除该卷。

> **注意**
>
> 完成本节中的步骤之后，你仍会留下一个空的 `/nix` 目录。
> 这是卸载成功的预期表现。
> 这个空的 `/nix` 目录会在下次重启时消失。
>
> 你无需重启即可完成 Nix 的卸载。
> 卸载已经完成。
> macOS（Catalina 及更高版本）直接管控根目录，其只读根文件系统会阻止你手动删除这个空的 `/nix` 挂载点。

## 单用户

要移除 Nix 的[单用户安装](./installing-binary.md#single-user-installation)，运行：

```console
rm -rf /nix ~/.nix-channels ~/.nix-defexpr ~/.nix-profile ~/.local/share/nix ~/.local/state/nix ~/.cache/nix
```
你还可以手动移除 `~/.profile` 中对 Nix 的引用。
