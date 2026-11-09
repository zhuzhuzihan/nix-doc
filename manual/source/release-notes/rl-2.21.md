# Release 2.21.0 (2024-03-11)

- 修复 fixed-output derivation 的沙箱逃逸问题（CVE-2024-27297）

  相互配合的 Nix derivation（派生）可以通过抽象命名空间中的 Unix 域套接字，向彼此发送指向 Nix store 中文件的文件描述符。这允许一个 derivation 在 Nix 已将该路径注册为"有效"且不可变并写入 Nix 数据库之后，修改另一个 derivation 的输出。尤其是，这允许 fixed-output derivation 的输出被修改成与其预期内容不同的内容。

  现在不会再出现这种情况了。

- CLI 选项 `--arg-from-file` 与 `--arg-from-stdin` [#10122](https://github.com/NixOS/nix/pull/10122)

  新的 CLI 选项 `--arg-from-file` *name* *path* 将文件 *path* 的内容作为字符串值，通过函数参数 *name* 传递给 Nix 表达式。类似地，新选项 `--arg-from-stdin` *name* 从标准输入读取该字符串的内容。

- `nix repl` 的简洁错误打印 [#9928](https://github.com/NixOS/nix/pull/9928)

  此前，如果列表或属性集的某个元素在求值时抛出错误，`nix repl` 会将整个错误（包括源代码位置信息）内联打印出来。这样的输出笨拙且难以阅读：

  ```
  nix-repl> { err = builtins.throw "uh oh!"; }
  { err = «error:
         … while calling the 'throw' builtin
           at «string»:1:9:
              1| { err = builtins.throw "uh oh!"; }
               |         ^

         error: uh oh!»; }
  ```

  现在，只会显示错误消息本身，输出可读性大大提高。
  ```
  nix-repl> { err = builtins.throw "uh oh!"; }
  { err = «error: uh oh!»; }
  ```

  不过，如果被求值的整个表达式抛出错误，则会像你期望的那样打印源代码位置和（如适用）堆栈跟踪：

  ```
  nix-repl> builtins.throw "uh oh!"
  error:
         … while calling the 'throw' builtin
           at «string»:1:1:
              1| builtins.throw "uh oh!"
               | ^

         error: uh oh!
  ```

- `--debugger` 现在可以访问 `let` 表达式中的绑定 [#8827](https://github.com/NixOS/nix/issues/8827) [#9918](https://github.com/NixOS/nix/pull/9918)

  `let` 表达式绑定中的断点和错误现在可以在调试器中访问这些绑定。此前只有 `let` 表达式的主体才能访问这些绑定。

- 设置了 `debugger-on-trace` 时，调用 `builtins.trace` 会进入 `--debugger` [#9914](https://github.com/NixOS/nix/pull/9914)

  如果设置了 `debugger-on-trace` 选项并给出了 `--debugger`，`builtins.trace` 调用的行为将类似于 `builtins.break`，并进入调试 REPL。这对于确定警告从何处发出非常有用。

- 调试器打印源代码位置信息 [#9913](https://github.com/NixOS/nix/pull/9913)

  `--debugger` 现在会打印源代码位置信息，而不是源代码位置信息的指针。之前：

  ```
  nix-repl> :bt
  0: while evaluating the attribute 'python311.pythonForBuild.pkgs'
  0x600001522598
  ```

  之后：

  ```
  0: while evaluating the attribute 'python311.pythonForBuild.pkgs'
  /nix/store/hg65h51xnp74ikahns9hyf3py5mlbbqq-source/overrides/default.nix:132:27

     131|
     132|       bootstrappingBase = pkgs.${self.python.pythonAttr}.pythonForBuild.pkgs;
        |                           ^
     133|     in
  ```

- `--debugger` 在 `let` 表达式和函数调用中能更可靠地启动 [#6649](https://github.com/NixOS/nix/issues/6649) [#9917](https://github.com/NixOS/nix/pull/9917)

  此前，如果你尝试在调试器中求值以下文件：

  ```nix
  let
    a = builtins.trace "before inner break" (
      builtins.break "hello"
    );
    b = builtins.trace "before outer break" (
      builtins.break a
    );
  in
    b
  ```

  Nix 能正确地在 `builtins.break a` 处进入调试器，但如果你执行 `:continue`，它会完全跳过 `builtins.break "hello"` 表达式。

  现在，Nix 会正确地在两个断点处都进入调试器。

- 不再支持嵌套调试器 [#9920](https://github.com/NixOS/nix/pull/9920)

  此前，在调试器中求值一个抛出错误的表达式会进入第二个嵌套的调试器：

  ```
  nix-repl> builtins.throw "what"
  error: what


  Starting REPL to allow you to inspect the current state of the evaluator.

  Welcome to Nix 2.18.1. Type :? for help.

  nix-repl>
  ```

  现在，它只会像 `nix repl` 一样打印错误消息：

  ```
  nix-repl> builtins.throw "what"
  error:
         … while calling the 'throw' builtin
           at «string»:1:1:
              1| builtins.throw "what"
               | ^

         error: what
  ```

- 打印表达式时函数参数顺序保持一致 [#9874](https://github.com/NixOS/nix/pull/9874)

  函数参数现在按字典序打印，而不是基于内部创建时序的符号顺序。

- 修复 `inherit` 的重复属性错误位置 [#9874](https://github.com/NixOS/nix/pull/9874)

  当 `inherit` 导致重复属性错误时，错误位置此前没有被正确报告：错误被归到 inherit 语句本身或绑定块的起始处，而不是出错的属性名上。

- `inherit (x) ...` 仅对 `x` 求值一次 [#9847](https://github.com/NixOS/nix/pull/9847)

  `inherit (x) a b ...` 现在对表达式 `x` 只求值一次，供所有被继承的属性使用，而不是每个被继承的属性各求值一次。
  这通常没有可测量的影响，但有副作用的表达式（如 `builtins.trace`）会被重复执行，而开销较大的表达式（如 derivation）可能导致可测量的性能下降。

- 存储路径（store path）允许以 `.` 开头 [#912](https://github.com/NixOS/nix/issues/912) [#9091](https://github.com/NixOS/nix/pull/9091) [#9095](https://github.com/NixOS/nix/pull/9095) [#9120](https://github.com/NixOS/nix/pull/9120) [#9121](https://github.com/NixOS/nix/pull/9121) [#9122](https://github.com/NixOS/nix/pull/9122) [#9130](https://github.com/NixOS/nix/pull/9130) [#9219](https://github.com/NixOS/nix/pull/9219) [#9224](https://github.com/NixOS/nix/pull/9224) [#9867](https://github.com/NixOS/nix/pull/9867)

  Nix 2.4 中允许路径以点开头纯属意外。Nix 团队一直认为这是一个 bug，但由于用户此后依赖了这一行为，造成了不必要的麻烦。
  从现在起，以点开头是被支持的。名称 `.` 和 `..` 不被允许，以 `.-` 或 `..-` 开头的名称也不被允许。

  拒绝以点开头的 Nix 版本[在该 issue 中](https://github.com/NixOS/nix/issues/912#issuecomment-1919583286)有说明。

- `nix repl` 美化打印（pretty-print）值 [#9931](https://github.com/NixOS/nix/pull/9931)

  `nix repl` 现在会美化打印值：

  ```
  {
    attrs = {
      a = {
        b = {
          c = { };
        };
      };
    };
    list = [ 1 ];
    list' = [
      1
      2
      3
    ];
  }
  ```

- `nix profile remove` 与 `nix profile upgrade` 引入 `--regex` 和 `--all` [#10166](https://github.com/NixOS/nix/pull/10166)

  此前 `nix profile remove` 和 `nix profile upgrade` 的命令行参数是使用正则表达式匹配软件包条目的。
  例如：

  ```
  nix profile remove '.*vim.*'
  ```

  这会移除所有名称中包含 `vim` 的软件包。

  在大多数情况下，人们只用单个软件包名称来移除和升级软件包。将这种方式与正则表达式混用有时会导致意外行为。例如，`python3.1` 可能匹配到 `python311`。

  为了避免意外行为，这些参数现在只进行精确名称匹配。

  仍然可以通过新的 `--regex` 标志使用正则表达式进行匹配：

  ```
  nix profile remove --regex '.*vim.*'
  ```

  使用正则表达式最有用的场景之一是升级全部软件包。此前需要这样实现：

  ```
  nix profile upgrade '.*'
  ```

  随着引入 `--all` 标志，这一操作现在变得更直接：

  ```
  nix profile upgrade --all
  ```

- 减少了 `--debugger` 的视觉干扰 [#9919](https://github.com/NixOS/nix/pull/9919)

  之前：
  ```
  info: breakpoint reached


  Starting REPL to allow you to inspect the current state of the evaluator.

  Welcome to Nix 2.20.0pre20231222_dirty. Type :? for help.

  nix-repl> :continue
  error: uh oh


  Starting REPL to allow you to inspect the current state of the evaluator.

  Welcome to Nix 2.20.0pre20231222_dirty. Type :? for help.

  nix-repl>
  ```

  之后：

  ```
  info: breakpoint reached

  Nix 2.20.0pre20231222_dirty debugger
  Type :? for help.
  nix-repl> :continue
  error: uh oh

  nix-repl>
  ```

- `nix repl` 中的循环检测更简单也更可靠 [#8672](https://github.com/NixOS/nix/issues/8672) [#9926](https://github.com/NixOS/nix/pull/9926)

  `nix repl`、`nix eval`、`builtins.trace` 以及其他所有打印值之处的循环检测现在更简单了，并与 `nix-instantiate --eval` 输出中的循环检测保持一致。

  之前：

  ```
  nix eval --expr 'let self = { inherit self; }; in self'
  { self = { self = «repeated»; }; }
  ```

  之后：

  ```
  { self = «repeated»; }
  ```

- 调试器中 `while evaluating the attribute` 错误现在包含位置信息 [#9915](https://github.com/NixOS/nix/pull/9915)

  之前：

  ```
  0: while evaluating the attribute 'python311.pythonForBuild.pkgs'
  0x600001522598
  ```

  之后：

  ```
  0: while evaluating the attribute 'python311.pythonForBuild.pkgs'
  /nix/store/hg65h51xnp74ikahns9hyf3py5mlbbqq-source/overrides/default.nix:132:27

     131|
     132|       bootstrappingBase = pkgs.${self.python.pythonAttr}.pythonForBuild.pkgs;
        |                           ^
     133|     in
  ```

- macOS 上的栈大小增大了 [#9860](https://github.com/NixOS/nix/pull/9860)

  此前，Nix 在 Linux 上会把栈大小设置为 64MiB，但在 macOS 上保持默认栈大小（约 8KiB）。现在，macOS 上的栈大小也被正确设置为 64MiB，这将减少深度递归 Nix 表达式导致的栈溢出段错误。
