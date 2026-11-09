# 附录：数学记号

本手册中有多处使用形式化的"证明树"，以[自然演绎](https://en.wikipedia.org/wiki/Natural_deduction)的方式定义各种[关系](https://en.wikipedia.org/wiki/Relation_(mathematics))。

以下语法以及元变量到语法范畴的指派将在这些小节中使用。

\\begin{align}
s, t &\in \text{store-path} \\\\
o &\in \text{output-name} \\\\
i, p &\in \text{deriving-path} \\\\
d &\in \text{derivation}
\\end{align}

\\begin{align}
\text{deriving-path} \quad p &::= s \mid (p, o)
\\end{align}
