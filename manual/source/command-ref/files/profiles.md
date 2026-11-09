## Profiles

一个包含指向 profile 链接的目录，这些 profile 由 [`nix-env`] 和 [`nix profile`] 管理：

- 普通用户为 `$XDG_STATE_HOME/nix/profiles`
- 用户为 `root` 时为 `$NIX_STATE_DIR/profiles/per-user/root`

profile 是一个目录，其中是指向 Nix store 中文件的符号链接。

### 文件系统布局

profile 按如下方式进行版本管理。使用名为 *path* 的 profile 时，*path* 是指向 *path*`-`*N*`-link` 的符号链接，其中 *N* 是该 profile 的版本号。
而 *path*`-`*N*`-link` 又是一个指向 Nix store 中某个路径的符号链接。
例如：

```console
$ ls -l ~alice/.local/state/nix/profiles/profile*
lrwxrwxrwx 1 alice users 14 Nov 25 14:35 /home/alice/.local/state/nix/profiles/profile -> profile-7-link
lrwxrwxrwx 1 alice users 51 Oct 28 16:18 /home/alice/.local/state/nix/profiles/profile-5-link -> /nix/store/q69xad13ghpf7ir87h0b2gd28lafjj1j-profile
lrwxrwxrwx 1 alice users 51 Oct 29 13:20 /home/alice/.local/state/nix/profiles/profile-6-link -> /nix/store/6bvhpysd7vwz7k3b0pndn7ifi5xr32dg-profile
lrwxrwxrwx 1 alice users 51 Nov 25 14:35 /home/alice/.local/state/nix/profiles/profile-7-link -> /nix/store/mp0x6xnsg0b8qhswy6riqvimai4gm677-profile
```

这些符号链接中的每一个都是 Nix 垃圾回收器的一个根。

profile 每个版本对应的存储路径内容，是一棵指向已安装软件包文件的符号链接树，例如：

```console
$ ll -R ~eelco/.local/state/nix/profiles/profile-7-link/
/home/eelco/.local/state/nix/profiles/profile-7-link/:
total 20
dr-xr-xr-x 2 root root 4096 Jan  1  1970 bin
-r--r--r-- 2 root root 1402 Jan  1  1970 manifest.nix
dr-xr-xr-x 4 root root 4096 Jan  1  1970 share

/home/eelco/.local/state/nix/profiles/profile-7-link/bin:
total 20
lrwxrwxrwx 5 root root 79 Jan  1  1970 chromium -> /nix/store/cyxny9d1zjb9l9103fr6j6kavp3bqjxf-chromium-86.0.4240.111/bin/chromium
lrwxrwxrwx 7 root root 87 Jan  1  1970 spotify -> /nix/store/w9182874m1bl56smps3m5zjj36jhp3rn-spotify-1.1.26.501.gbe11e53b-15/bin/spotify
lrwxrwxrwx 3 root root 79 Jan  1  1970 zoom-us -> /nix/store/wbhg2ga8f3h87s9h5k0slxk0m81m4cxl-zoom-us-5.3.469451.0927/bin/zoom-us

/home/eelco/.local/state/nix/profiles/profile-7-link/share/applications:
total 12
lrwxrwxrwx 4 root root 120 Jan  1  1970 chromium-browser.desktop -> /nix/store/sqzyx2l85i6j2a77pnyvglh3bvzwmjjp-chromium-unwrapped-86.0.4240.111/share/applications/chromium-browser.desktop
lrwxrwxrwx 7 root root 110 Jan  1  1970 spotify.desktop -> /nix/store/w9182874m1bl56smps3m5zjj36jhp3rn-spotify-1.1.26.501.gbe11e53b-15/share/applications/spotify.desktop
lrwxrwxrwx 3 root root 107 Jan  1  1970 us.zoom.Zoom.desktop -> /nix/store/wbhg2ga8f3h87s9h5k0slxk0m81m4cxl-zoom-us-5.3.469451.0927/share/applications/us.zoom.Zoom.desktop

…
```

每个 profile 版本都包含一个 manifest 文件：
- [`manifest.nix`](@docroot@/command-ref/files/manifest.nix.md)，由 [`nix-env`](@docroot@/command-ref/nix-env.md) 使用。
- [`manifest.json`](@docroot@/command-ref/files/manifest.json.md)，由 [`nix profile`](@docroot@/command-ref/new-cli/nix3-profile.md)（实验性）使用。

## 用户 profile 链接

指向用户当前 profile 的符号链接：

- `~/.nix-profile`
- 如果 [`use-xdg-base-directories`] 设置为 `true`，则为 `$XDG_STATE_HOME/nix/profile`。

默认情况下，该符号链接指向：

- 普通用户为 `$XDG_STATE_HOME/nix/profiles/profile`
- `root` 用户为 `$NIX_STATE_DIR/profiles/per-user/root/profile`

`PATH` 环境变量应当包含 profile 链接的 `/bin` 子目录（例如 `~/.nix-profile/bin`），用户环境才能对用户可见。
[安装程序](@docroot@/installation/installing-binary.md)默认会进行此设置，除非你启用了 [`use-xdg-base-directories`]。

[`nix-env`]: @docroot@/command-ref/nix-env.md
[`nix profile`]: @docroot@/command-ref/new-cli/nix3-profile.md
[`use-xdg-base-directories`]: @docroot@/command-ref/conf-file.md#conf-use-xdg-base-directories
