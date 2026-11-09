# Release 2.15 (2023-04-11)

* 在命令行上接受 installable 的命令现在可以通过 `--stdin` 标志从标准输入读取它们。这主要用于路径数量庞大、超出操作系统参数上限的情况。

* `nix-hash` 命令现在支持 Base64 和 SRI。使用标志 `--base64` 或 `--sri` 把输出哈希的格式指定为 Base64 或 SRI，并使用 `--to-base64` 或 `--to-sri` 分别把哈希转换为 Base64 或 SRI 格式。

  由于哈希格式的选择不再是二选一，还新增了 `--base16` 标志用于显式指定 Base16 格式——它仍是默认格式。

* 此前，带 `.drv` 后缀的 [installable](../command-ref/new-cli/nix.md#installables) 会被特殊处理，解释为给定 [store derivation](@docroot@/glossary.md#gloss-store-derivation) 的全部输出路径；该特殊处理已被移除，现在它会被当作它所表示的字面存储路径。

  Nix 2.13 中引入的用于存储路径的新 `^` 语法允许显式引用 derivation（派生）的输出路径。
  相比现已移除的 `.drv` 特殊处理，使用它更好也更清晰。

  例如，
  ```shell-session
  $ nix path-info /nix/store/fpq78s2h8ffh66v2iy0q1838mhff06y8-glibc-2.33-78.drv
  ```

  现在给出的是 derivation 本身的信息，而

  ```shell-session
  $ nix path-info /nix/store/fpq78s2h8ffh66v2iy0q1838mhff06y8-glibc-2.33-78.drv^*
  ```
  给出的是它每个输出的信息。

* 实验性命令 `nix describe-stores` 已被移除。

* Nix store 及其设置现在记录在 [`nix help-stores`](@docroot@/command-ref/new-cli/nix3-help-stores.md) 中。

* `nix-store` 和 `nix-env` 各操作（operation）的文档现在可以在手册的独立页面上查阅。
  其中包含所有可指定的通用选项以及影响这些命令的通用环境变量。

  这些页面可以用 `man` 离线查看：

  * `man nix-store-<operation>` 和 `man nix-env-<operation>`
  * `nix-store --help --<operation>` 和 `nix-env --help --<operation>`。

* Nix 作为客户端使用时，现在会检查 store（服务器端）是否信任该客户端。
  （store 一直都需要检查它是否信任客户端，但现在客户端也会被告知 store 的决定。）
  这对编写与（非 legacy-ssh）远程 Nix store 交互的脚本很有用。

  `nix store ping` 和 `nix doctor` 现在会显示这一信息。

* 新命令 `nix derivation add` 允许在不涉及 Nix 语言的情况下把 derivation 加入 store。
  它的存在是为了补齐我们的基础工具/plumbing 命令集，并提供一种低门槛的方式来试验 Nix Store 的替代前端。
  它使用与 `nix derivation show` 相同的 JSON 布局，并且是它的逆操作。

* `nix show-derivation` 已更名为 `nix derivation show`。
  这与 `nix derivation add` 保持一致，并避免了顶层命名空间的膨胀。
  不过，出于兼容性考虑，旧名称仍作为别名保留。

* `nix derivation {add,show}` 的 JSON 格式现在把 derivation 名称作为一个顶层字段。
  这总体上有用，但对 `add` 方向尤其必要，否则在某些情况下我们将不得不通过带外方式传入名称。
