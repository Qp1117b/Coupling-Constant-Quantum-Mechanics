# 环 7／`审-1`：局域 \(f(\mathcal H_{ij})\) 映射的普适 no-go（无需奇偶与单调）

**前件**：主链 (6.1)(6.2) \(\mathcal H_{ij}=\tau_i-\tau_j\)（梯度、上闭链）；环 8 (8.1)(8.2) \(C_{ij}=f(\varepsilon_i-\varepsilon_j),C_{ii}=1,C\mathbf1=\mathbf1\)；06 DM.2／DM.3 同型。已有的 R-02 no-go 只在 \(f\) **奇且严格单调**时成立。本轮问：若 \(f\) 任意（不要求奇、单调、连续），只要求 \(C_ij\) 是 \(\mathcal H_{ij}\) 的**局域函数**且逐行和为 1，是否可能？

**结论先行**：

1. 对 \(N\ge3\)，逐行和为常数对任意节点固有时矢量成立，强制 \(f\) 满足泛函方程
   \[
   f(u)+f(u+v)=f(-u)+f(v)\qquad\forall u,v\in\mathbb R.\tag{A1.1}
   \]
2. **该方程唯一解是常数**。证明只用两次代入 \(v=0\)：
   \[
   2f(u)=f(-u)+f(0),\quad 2f(-u)=f(u)+f(0)\ \Longrightarrow\ f(u)=f(0).\tag{A1.2}
   \]
   不需要奇偶性、单调性、连续性、可测性。这是比 R-02 更强的 no-go。
3. 于是分两种写法，都无解：
   - **无独立对角项**：\(C_{ij}=f(\mathcal H_{ij})\) 含 \(i=j\)。\(C_{ii}=1\Rightarrow f(0)=1\Rightarrow f\equiv1\Rightarrow C\mathbf1=N\mathbf1\ne\mathbf1\)（\(N\ge2\)）；
   - **有独立对角项**：\(C=\delta+g(\mathcal H)\)，\(C_{ii}=1\Rightarrow g(0)=0\Rightarrow g\equiv0\Rightarrow C=I\)，差异方差 \(\langle(\delta C_{ij})^2\rangle=0\)，环 9 的配对强度来源消失（与 R-04 同型）。
   \[
   \boxed{\text{局域 }f(\mathcal H_{ij})+C_{ii}=1+C\mathbf1=\mathbf1\ \Longrightarrow\ \text{无非平凡解（}N\ge2\text{）}.}\tag{A1.3}
   \]
4. **判定**：`审-1` 不是“还没算出 \(f\) 的显式”，而是**在局域函数类内不可解**。可行的非平凡 \(C\) 必须放弃“\(C_{ij}\) 只是 \(\mathcal H_{ij}\) 的局域函数”这一前提：已选矩阵分支 \(C=I+B\)、\(B_{ij}=f(\lambda_{ij})\)（\(\lambda\) 为独立边量、反对称、非梯度）正是这一 escaping route；但它不再接 \(\mathcal H\)，且 \(\theta=\alpha\lambda\) 的 `G19` 未闭合。
5. **`M5` 的状态**：单函数 \(f\) 在节点差分支已被 (A1.3) 一般性地排除；矩阵分支中 \(f\) 的显式仍缺，但那是**另一个自变量**的问题，不是 `审-1` 的累积层。本轮不升状态。

## 一、泛函方程的推导

令 \(N=3\)，节点固有时 \(\tau=(\tau_a,\tau_b,\tau_c)\)。由 \(C\mathbf1=\mathbf1\)：

$$
f(\tau_a-\tau_b)+f(\tau_a-\tau_c)=1-f(0),\quad
f(\tau_b-\tau_a)+f(\tau_b-\tau_c)=1-f(0),\quad\text{（第三行同理）}.\tag{A1.4}
$$

记 \(u=\tau_a-\tau_b\)、\(v=\tau_b-\tau_c\)，则 \(\tau_a-\tau_c=u+v\)，代入前两行并相等即得 (A1.1)。该推导只用 \(C\mathbf1=\mathbf1\) 对**任意** \(\tau\) 成立；\(N>3\) 时固定其余节点同样成立。

(A1.2) 的证明：在 (A1.1) 中取 \(v=0\) 得 \(2f(u)=f(-u)+f(0)\)；取 \(u\mapsto-u,v=0\) 得 \(2f(-u)=f(u)+f(0)\)；两式联立消去 \(f(-u)\) 得 \(3f(u)=3f(0)\)。

**外部对照**：(A1.1) 属条件 Cauchy 型方程（Abelian 群上的函数方程），标准处理见 Forti–Paganosti 的方法与 Aczél 类结果；本轮只用到代入 \(v=0\) 的初等推理，不需引用外部正则性定理。

## 二、两种写法的排除

**写法一（无 δ）**：\(C_{ij}=f(\tau_i-\tau_j)\) 对角元 \(f(0)\)。06 DM.2 要求 \(C_{ii}=1\)，故 \(f(0)=1\)；由常数解 \(f\equiv1\)，\(C=J\)（全 1 矩阵），行和 \(N\ne1\)（\(N\ge2\)）。矛盾。

**写法二（有 δ）**：\(C_{ij}=\delta_{ij}+g(\tau_i-\tau_j)\)，\(g(0)=0\)。由常数解 \(g\equiv0\)，\(C=I\)。此时 \(\delta C_{ij}=0\)，DM.5 的 \(\langle(\delta C)^2\rangle\) 消失，环 9／环 10 的配对强度没有来源。这不是“小簇退化”，而是任意 \(N\) 的代数结论。

注意：若**放弃** \(C_{ii}=1\) 而只保留 \(C\mathbf1=\mathbf1\)，则常数解 \(f\equiv1/N\) 给 \(C=J/N\)，满足行和 1；但 06 DM.2 的 \(C_{ii}=1\) 是权威定义，不能擅自放弃。这说明 no-go 的力量来自**两条约束的合取**。

▸**不能推出**：由本轮推出矩阵分支已被证明（它换掉了自变量）；由本轮推出 \(f\) 在矩阵分支中的显式；由本轮推出环 6 的 (6.1)(6.2) 需改写（H 保持梯度，见 `环06_相位连接审计.md`）；由本轮推出状态可升。

## 三、Lean 承载

`05_Lean验证/Audit1NoGo.lean` 承载：

- `constant_of_functional_eq`：由 (A1.1) 推出 \(f\) 为常数（核心 no-go）；
- `constant_solution`：常数解确实满足 (A1.1)；
- `constant_implies_independent_of_H`：常数 ⇒ \(C\) 与 \(\mathcal H\) 无关；
- `row_sum_three`、`odd_zero_diag_collapse`、`odd_zero_diag_not_row_one`：两种写法的排除。

未形式化：(A1.1) 从 \(C\mathbf1=\mathbf1\) 的推导（三点代数的纸面步骤）、矩阵分支的边量替换。无 `axiom`、`sorry`、`admit`、`native_decide`、`unsafe`。

## 四、数值核对

脚本 `04_计算验证/环07_审1no-go.py`，400 组随机三点固有时：

- 常数族：仅在 \(c=1/3\) 时逐行和残差为 \(0.000000\)（对应 \(C=J/3\)，但违反 \(C_{ii}=1\)）；
- 非常数族：线性 \(f(x)=kx\) 最小残差 \(1.922408\)、\(\tanh(kx)\) 为 \(1.862110\)、\(1/(1+kx^2)\) 为 \(1.974013\)，均不为零，且随参数扫描不趋零。

图像核对“只有常数函数给出与 \(\tau\) 无关的行和”，不是拟合。

## 五、状态与缺口

**状态**：(A1.1)(A1.2)(A1.3)【标准数学＋Lean】；判定【本轮结论】。

**缺口**：

- `审-1`：局域映射分支**判定为不可解**（强于“未算出 \(f\)”）；仍**不闭合**，因为参数化需矩阵分支与 `G19`；
- `M5`：节点差分支的 \(f\) 已被排除；矩阵分支的 \(f\) 显式仍缺；
- `G19`：\(\theta=\alpha\lambda\) 未定；
- `临-1`：\(\varepsilon\) 的驱动源未给；
- 数据对照（07 协议）未执行；状态栏未动。

▸**不能推出**：由本轮推出矩阵分支已闭合或已写入主链；由本轮推出环 7 (7.3) 的 \(f^{-1}\) 在矩阵分支中可用；由本轮推出 `M5` 状态可升；由数值残差推出外部函数的普适性质。
