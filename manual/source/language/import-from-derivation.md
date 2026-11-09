# 从 derivation 导入（Import From Derivation）

Nix 表达式的值可以依赖于某个 [store object] 的内容。

[store object]: @docroot@/store/store-object.md

把一个求值为[存储路径](@docroot@/store/store-path.md)的表达式 `expr` 传给任何会读取文件系统的内置函数，即构成 Import From Derivation（IFD，从 derivation 导入）：

- [`import`](./builtins.md#builtins-import)` expr`
- [`builtins.readFile`](./builtins.md#builtins-readFile)` expr`
- [`builtins.readFileType`](./builtins.md#builtins-readFileType)` expr`
- [`builtins.readDir`](./builtins.md#builtins-readDir)` expr`
- [`builtins.pathExists`](./builtins.md#builtins-pathExists)` expr`
- [`builtins.filterSource`](./builtins.md#builtins-filterSource)` f expr`
- [`builtins.path`](./builtins.md#builtins-path)` { path = expr; }`
- [`builtins.hashFile`](./builtins.md#builtins-hashFile)` t expr`
- `builtins.scopedImport x drv`

当需要访问该存储路径时，求值会被暂停，对应的 store object 会被[实现（realise）]，然后求值继续进行。

[realised]: @docroot@/glossary.md#gloss-realise

这会带来性能上的影响：
只有当所有需要的 store object 都被实现之后，求值才能完成。
由于 Nix 语言求值器是顺序执行的，它一次只能发现一个需要读取的存储路径。
虽然实现（realisation）本身总是并行的，但在这种情况下，它无法对所有需要的存储路径一次性并行进行，因此比其他情况慢得多。

在求值期间实现 store object 的行为可以通过把 [`allow-import-from-derivation`](../command-ref/conf-file.md#conf-allow-import-from-derivation) 设为 `false` 来禁用。
在没有 IFD 的情况下，可以确保求值是完整的，并且 Nix 能在开始任何实现之前生成构建计划。

## 示例

在下面的 Nix 表达式中，内层的 derivation `drv` 会生成一个内容为 `hello` 的文件。

```nix
# IFD.nix
let
  drv = derivation {
    name = "hello";
    builder = "/bin/sh";
    args = [ "-c" "echo -n hello > $out" ];
    system = builtins.currentSystem;
  };
in "${builtins.readFile drv} world"
```

```shellSession
nix-instantiate IFD.nix --eval --read-write-mode
```

```
building '/nix/store/348q1cal6sdgfxs8zqi9v8llrsn4kqkq-hello.drv'...
"hello world"
```

derivation 的输出内容必须先被[实现]，之后才能用 [`readFile`](./builtins.md#builtins-readFile) 读取。
只有这样，求值才能继续并产生最终结果。

## 图示

作为初步近似，下面的数据流图展示了当 Nix 表达式的值依赖于实现某个 [store object] 时，求值和构建是如何交替进行的。
方框是数据结构，箭头上的标注是转换过程。

```
+----------------------+             +------------------------+
| Nix evaluator        |             | Nix store              |
|  .----------------.  |             |                        |
|  | Nix expression |  |             |                        |
|  '----------------'  |             |                        |
|          |           |             |                        |
|       evaluate       |             |                        |
|          |           |             |                        |
|          V           |             |                        |
|    .------------.    |             |                        |
|    | derivation |    |             |  .------------------.  |
|    | expression |----|-instantiate-|->| store derivation |  |
|    '------------'    |             |  '------------------'  |
|                      |             |           |            |
|                      |             |        realise         |
|                      |             |           |            |
|                      |             |           V            |
|  .----------------.  |             |    .--------------.    |
|  | Nix expression |<-|----read-----|----| store object |    |
|  '----------------'  |             |    '--------------'    |
|          |           |             |                        |
|       evaluate       |             |                        |
|          |           |             |                        |
|          V           |             |                        |
|    .------------.    |             |                        |
|    |   value    |    |             |                        |
|    '------------'    |             |                        |
+----------------------+             +------------------------+
```

更详细地说，下面的时序图展示了表达式是如何被逐步求值的，以及求值在哪些地方被阻塞以等待构建产物的出现。

```
.-------.     .-------------.                        .---------.
|Nix CLI|     |Nix evaluator|                        |Nix store|
'-------'     '-------------'                        '---------'
    |                |                                    |
    |evaluate IFD.nix|                                    |
    |--------------->|                                    |
    |                |                                    |
    |  evaluate `"${readFile drv} world"`                 |
    |                |                                    |
    |    evaluate `readFile drv`                          |
    |                |                                    |
    |   evaluate `drv` as string                          |
    |                |                                    |
    |                |instantiate /nix/store/...-hello.drv|
    |                |----------------------------------->|
    |                :                                    |
    |                :  realise /nix/store/...-hello.drv  |
    |                :----------------------------------->|
    |                :                                    |
    |                                                     |--------.
    |                :                                    |        |
    |      (evaluation blocked)                           |  echo hello > $out
    |                :                                    |        |
    |                                                     |<-------'
    |                :        /nix/store/...-hello        |
    |                |<-----------------------------------|
    |                |                                    |
    |  resume `readFile /nix/store/...-hello`             |
    |                |                                    |
    |                |   readFile /nix/store/...-hello    |
    |                |----------------------------------->|
    |                |                                    |
    |                |               hello                |
    |                |<-----------------------------------|
    |                |                                    |
    |      resume `"${"hello"} world"`                    |
    |                |                                    |
    |        resume `"hello world"`                       |
    |                |                                    |
    | "hello world"  |                                    |
    |<---------------|                                    |
.-------.     .-------------.                        .---------.
|Nix CLI|     |Nix evaluator|                        |Nix store|
'-------'     '-------------'                        '---------'
```
