# 选项

以下选项适用于所有 `nix-env` 操作，但并不总是有效果。

- `--file` / `-f` *path*

  指定 `--install`、`--upgrade` 和 `--query
  --available` 操作用来获取 derivation（派生）的 Nix 表达式（下文称之为*当前激活的 Nix 表达式*）。默认值为
  `~/.nix-defexpr`。

  如果该参数以 `http://` 或 `https://` 开头，则会被解释为一个 tarball 的 URL，该 tarball 将被下载并解压到临时位置。
  tarball 必须包含一个顶层目录，其中至少有一个名为 `default.nix` 的文件。

- `--profile` / `-p` *path*

  指定那些操作 profile 的命令所使用的 profile（下文称之为*当前激活的 profile*）。
  profile 是一系列被称为 *generation（代）*的用户环境，其中一个是*当前 generation*。

- `--dry-run`

  对于 `--install`、`--upgrade`、`--uninstall`、
  `--switch-generation`、`--delete-generations` 和 `--rollback`
  操作，此标志会让 `nix-env` 打印出*如果未指定此标志*时*将会*执行的操作，而不会实际执行。

  `--dry-run` 还会打印出哪些路径将被
  [substituted](@docroot@/glossary.md)（即下载），以及哪些路径
  将从源码构建（因为没有可用的 substitute）。

- `--system-filter` *system*

  默认情况下，`--query --available` 等操作会显示匹配任意平台的 derivation。
  此选项允许你只使用指定平台 *system* 的 derivation。
