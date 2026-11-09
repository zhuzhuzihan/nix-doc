# Nix Manual 中文版

Nix 官方手册的简体中文翻译仓库。源码拆分自 [NixOS/nix](https://github.com/NixOS/nix) 的 `doc/` 目录（`git subtree split`，保留 3077 个上游 commit 的完整历史）。

在线阅读：<https://nix-doc.mczihan.link>（由 GitHub Pages + Cloudflare 提供加速）

## 翻译范围

- ✅ `manual/source/` 下全部静态章节（语言、命令参考、安装、store 体系、协议、开发指南、发布说明等，231 个文件）
- ⏭️ `manual/rl-next/` 未发布条目保留英文原文
- ⚙️ 命令参考中的选项表、类型与默认值保留英文；代码块逐字节保留

术语约定：derivation（派生）、store path（存储路径）、closure（闭包）、substitute（替代）等核心 Nix 术语首次出现时括注英文，其余沿用英文原名（Nix store、profile、Flakes、GC root 等）。

## 构建

手册的完整构建管线（meson + mdbook + 文档生成脚本）依赖 Nix 完整源码树，因此本仓库的 CI 采用「上游完整树 + 覆盖翻译」方式构建：

```
clone NixOS/nix → 用本仓库 manual/ 覆盖 doc/manual/ → nix build .#manual
```

本地复现：

```console
$ git clone https://github.com/NixOS/nix.git ../nix-upstream
$ rm -rf ../nix-upstream/doc/manual && cp -r manual ../nix-upstream/doc/manual
$ cd ../nix-upstream && git add -A && nix build .#manual
```

## 许可证

与上游一致：[LGPL-2.1-or-later](COPYING)（见 `doc/manual/meson.build` 中的 `license : 'LGPL-2.1-or-later'`）。

## 与上游同步

上游 `doc/` 更新后重新拆分并推送即可：

```console
$ cd /path/to/nix && git fetch origin
$ git subtree split -P doc -b doc-only
$ git push https://github.com/zhuzhuzihan/nix-doc.git doc-only:master --force
```

（注意：force push 会覆盖本仓库的翻译提交，同步上游后需重新套用翻译 diff。）
