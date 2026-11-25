# 目标区：从 BKT 跳变与渗流刚度推导 Uemura 标度及其失效条件

**前件**：环 19 已给两条可用结果——重整化刚度的普适跳变 (19P.11) \(\Upsilon_R(T_{\rm BKT}^-)=2k_BT_{\rm BKT}/\pi\)，与渗流刚度读出 (19P.20) \(\Upsilon_{\rm eff}(T)=\Upsilon_{\rm bond}w(T)\Phi(p_{\rm pair}(T))\)。环 10 给 \(w(T)\) 的精确 Debye 形式，环 15 给 \(p_{\rm pair}(T)\) 的条件 chi-square 尾。本轮**不新增环号**，只在“目标区”把已有结果接到现象学标度；目标区不是环，按 `10 探索/AGENTS.md` §1 第 10 问处理。

**结论先行**：

1. 由跳变条件与因子化 \(\Upsilon_R=g_{\rm ren}\Upsilon_{\rm bare}\) 得**恒等式**
   \[
   T_c=\frac{\pi}{2k_B}\,\Upsilon_{\rm bare}(0)\,Q(T_c),\qquad
   Q(T_c)\equiv r(T_c)\,g_{\rm ren}(T_c),
   \tag{U.1}
   \]
   其中 \(r(T)=\Upsilon_{\rm bare}(T)/\Upsilon_{\rm bare}(0)\)，\(g_{\rm ren}=\Upsilon_R/\Upsilon_{\rm bare}\le1\)。这是**恒等式**，不是拟合。
2. 若 \(Q(T_c)\) 在一族材料内近似常数，则 \(T_c\propto\Upsilon_{\rm bare}(0)\)。外部实验的 Uemura 关系 \(\rho_s(0)\propto T_c\) 正是这一形式；CQM 给出它的**成立条件**而非把它当公理：
   \[
   \boxed{T_c\simeq\frac{\pi g_{\rm ren}}{2k_B}\,\Upsilon_{\rm bare}(0)\quad\Longleftrightarrow\quad
   w(T_c)\simeq1,\ \Phi(p_{\rm pair}(T_c))\simeq\Phi(p_{\rm pair}(0)).}
   \tag{U.2}
   \]
   斜率是 \(\pi g_{\rm ren}/(2k_B)\le\pi/(2k_B)\)；\(g_{\rm ren}=1\) 只对应涡旋核心能趋于无穷的极限。故 CQM **不预言普适斜率 \(\pi/2\)**，只预言斜率 \(\le\pi/2\) 且在同一材料族内近似常数（见 §六）。
3. 这三个条件在**欠掺杂／小 \(\Upsilon(0)\)** 区同时成立：\(T_c\) 小使 \(w\to1\)；\(T_c\ll T^*\) 使 \(p_{\rm pair}\) 几乎不动；核心能大使 \(g_{\rm ren}\to1\)。故 CQM **推出 Uemura 线**，且在掺杂增大时因 \(w(T_c)<1\)、\(\Phi\) 下降、涡旋重整化增强而**预言偏离**——这与外部“Uemura 只在欠掺杂区成立”一致。
4. 上界（无条件）：
   \[
   \boxed{T_c\le\frac{\pi}{2k_B}\,\Upsilon_{\rm bare}(0)\le\frac{\pi}{2k_B}\,\Upsilon_0.}
   \tag{U.3}
   \]
   注意 (U.3) 与环 19 的 \(T_c\le\min\{T_{\rm BKT}^{\rm pure},T_{\rm pair}(p_c)\}\) 是**两个独立上界**，取小者。
5. **Homes 律 \(\rho_s\propto\sigma_{\rm dc}T_c\) 不能由 CQM 推出**：\(\sigma_{\rm dc}\) 是正常态输运量，属链外-F，CQM 链无此对象；环 4 的 \(\Theta(T)\) 是固有时流速涨落，不是电导。只能写“若外部把 \(\sigma_{\rm dc}\) 与 \(\Theta\) 对应，则可得形式类比”，但这属**禁止的引入**，不写进链。

## 一、推导：跳变条件给恒等式

跳变 (19P.11) 在 \(T_c=T_{\rm BKT}\) 写为

$$
\Upsilon_R(T_c^-)=\frac{2k_BT_c}{\pi}.\tag{U.4}
$$

定义重整化因子与裸刚度比

$$
g_{\rm ren}(T)\equiv\frac{\Upsilon_R(T)}{\Upsilon_{\rm bare}(T)},\qquad
r(T)\equiv\frac{\Upsilon_{\rm bare}(T)}{\Upsilon_{\rm bare}(0)}.\tag{U.5}
$$

由 (19P.12) 的 \(K_R\le K_0\) 得 \(0<g_{\rm ren}\le1\)；由 \(w\le1\)、\(\Phi\le1\) 与二者单调降得 \(0<r\le1\)。代入 (U.4)：

$$
\frac{2k_BT_c}{\pi}=\Upsilon_R(T_c^-)
=g_{\rm ren}(T_c)\,\Upsilon_{\rm bare}(T_c)
=g_{\rm ren}(T_c)\,r(T_c)\,\Upsilon_{\rm bare}(0),\tag{U.6}
$$

即 (U.1)。把 (19P.20) 展开：

$$
\Upsilon_{\rm bare}(0)=\Upsilon_0\,\Phi\bigl(p_{\rm pair}(0)\bigr),\qquad
r(T)=\underbrace{w(T)}_{\le1}\,
\underbrace{\frac{\Phi(p_{\rm pair}(T))}{\Phi(p_{\rm pair}(0))}}_{\le1\text{（当 }p_{\rm pair}(T)\le p_{\rm pair}(0)\text{）}}.\tag{U.7}
$$

注意 \(p_{\rm pair}(T)\) 单调降由环 15 的方向定理给；\(\Phi\) 单调增由 (19P.19) 给，故第二因子 \(\le1\)。这在 CQM 链内闭合，不需要外部输入。

(U.1) 的**物理内容**：\(T_c\) 由零温刚度 \(\Upsilon_{\rm bare}(0)\) 乘以一个“热力学损耗因子” \(Q\le1\) 定。BCS 给 \(T_c\sim\omega_D e^{-1/\lambda}\)，不含 \(\Upsilon(0)\)；CQM 给的是**相位主导**的线性关系。两者不矛盾：CQM 的 \(\Upsilon(0)\) 已含 \(J_0\)（外生能标），故 (U.1) 仍是**形状关系**，不给绝对温标。

## 二、Uemura 线的成立区与失效机制

外部标准（Uemura 等，PRL **62**, 2317 (1989)；arXiv:cond-mat/0212643）给欠掺杂区

$$
T_c\propto\frac{n_s}{m^*}\propto\rho_s(0),\tag{U.8}
$$

最佳掺杂与过掺杂区偏离。CQM 对三个因子的逐项判定：

| 因子 | 欠掺杂（小 \(\Upsilon_0\)、小 \(T_c\)） | 掺杂增大 |
|:---|:---|:---|
| \(w(T_c)\) | \(T_c\ll\omega_D\Rightarrow w=1-\frac{\pi^2}{3}(T_c/\omega_D)^2\simeq1\) | \(w<1\) 且下降 |
| \(\Phi(p_{\rm pair}(T_c))/\Phi(p_{\rm pair}(0))\) | \(T_c\ll T^*\Rightarrow p_{\rm pair}(T_c)\simeq p_{\rm pair}(0)\Rightarrow\simeq1\) | \(p_{\rm pair}\) 下降，\(\Phi\) 输入近阈区，比值掉得很快（\(t_\Upsilon\approx1.3\)） |
| \(g_{\rm ren}(T_c)\) | 涡旋逸度小，RG 流未显著降刚度，\(\simeq1\) | 涡旋涨落增强，\(g_{\rm ren}<1\) |

故 \(Q\to1\) 给 (U.2) 的线性区；三者中任一显著小于 1 就产生**向下偏离**。CQM 的具体预言：

$$
\boxed{\frac{T_c}{\Upsilon_{\rm bare}(0)}\ \text{随}\ \Upsilon_0\ \text{增大而下降};
\qquad
\frac{dT_c}{d\Upsilon_0}>0\ \text{但}\ \frac{d^2T_c}{d\Upsilon_0^2}<0\ \text{（在小 }\Upsilon_0\text{ 线性段之后）}.}
\tag{U.9}
$$

(U.9) 的可证伪性：若实验在欠掺杂区给出严格线性且斜率 \(=\pi/(2k_B)\)（在 \(\rho_s\leftrightarrow\Upsilon\) 的外部对应下），支持 (U.2)；若斜率明显小于 \(\pi/(2k_B)\)，说明 \(g_{\rm ren}(T_c)<1\) 或外部对应有额外因子，不支持“裸刚度即 \(\rho_s\)”。

**外部对应的边界**：\(\rho_s(0)\propto\Upsilon_{\rm bare}(0)\) 来自 London 关系，是外部结论；CQM 链只有“\(\Upsilon\) 定出 \(\lambda_L\)”的目标声明（环 15／目标区，链外-B 未闭合）。因此 (U.8) 与 (U.2) 的符合只到**标度形状**，不证明 CQM 已推出 \(\lambda_L\)。这是本轮的硬边界。

## 三、Homes 律为什么不能推

外部另有 Homes 律（Nature **430**, 539 (2004)，DOI `10.1038/nature02673`）

$$
\rho_s(0)\propto\sigma_{\rm dc}(T_c)\,T_c.\tag{U.10}
$$

外部模型（Imry–Strongin–Homes，PRL **109**, 067003 (2012)，DOI `10.1103/PhysRevLett.109.067003`）指出：Uemura 与 Homes 是同一颗粒超导模型的两个极限，Uemura 对应大晶粒／高电阻（欠掺杂），Homes 对应小晶粒／低电阻（最佳─过掺杂）。这只是**外部对照**，CQM 不能照搬：

- CQM 无 \(\sigma_{\rm dc}\) 对象；正常态输运属链外-F；
- 环 4 的 \(\Theta(T)\) 是 \(v_\tau\) 涨落的非相干通道，不是电导；把它等同于 \(\sigma_{\rm dc}\) 是引入 CQM 未涉及的量，违反 `不虚构`；
- 因此本轮只推 Uemura 形状的 (U.1)–(U.9)，Homes 律登记为**外部现象、不可由当前闭合链推出**。

▸**不能推出**：由 (U.2) 推出 CQM 已给 \(T_c\) 的绝对值；由 Uemura 线的符合推出 \(\rho_s=\Upsilon_{\rm bare}\) 已在 CQM 内证明；由 (U.9) 推出 Homes 律；由本轮推出链外-B 的电磁响应已闭合。

## 四、外部文献基线与分层

| 层级 | 内容 | 出处 |
|:---|:---|:---|
| 【外部已证／实验】 | 欠掺杂 Uemura 线 \(T_c\propto n_s/m^*\)；最佳─过掺杂偏离 | Uemura et al., PRL **62**, 2317 (1989)；arXiv:cond-mat/0212643 |
| 【外部已证／实验】 | Homes 律 \(\rho_s\propto\sigma_{\rm dc}T_c\) | Homes et al., Nature **430**, 539 (2004)，DOI `10.1038/nature02673` |
| 【外部模型对照】 | 颗粒模型的两个极限分别给 Uemura／Homes；Uemura 极限就是 2D XY 刚度关系 | Imry, Strongin & Homes, PRL **109**, 067003 (2012)，DOI `10.1103/PhysRevLett.109.067003` |
| 【外部标准】 | 2D 相位刚度与 BKT 普适跳变 | Nelson, arXiv:cond-mat/9502114（环 19 已用） |
| 【外部预印本，仅对照】 | 弛豫率谱（TDOS）给 \(K(t)\sim1/t\) 与 \(T_c\) 的红外谱权重标度；单作者预印本，非确立结论 | Chae, arXiv:2602.22626v7 (2026) |
| 【CQM 构造】 | \(\Upsilon_{\rm bare}=\Upsilon_0w\Phi\)、\(g_{\rm ren}\) 的因子化、\(p_{\rm pair}\) 的 chi-square 尾 | 环 10／15／19 工作台 |
| 【CQM 严格】 | (U.1)–(U.7)、(U.9) 的条件严格部分 | 本轮＋Lean |

TDOS 预印本尤其要标注：它给“无特定玻色媒介、由慢模谱权重定 \(T_c\)”的**外部构造**，与 CQM 的记忆核起点（环 14）在问题上相邻，但 CQM 尚未从链内推出 TDOS，**不得**把它当 CQM 已证；本轮仅登记为对照与后续候选（下一轮 `临-25` 可检验）。

## 五、Lean 承载

`05_Lean验证/UemuraScale.lean` 承载：

- `uemura_identity`：由跳变与 \(g,r\) 定义推出 (U.1)（纯代数）；
- `uemura_upper`：\(r\le1\wedge g\le1\Rightarrow T_c\le\pi\Upsilon_0/(2k_B)\)；
- `uemura_linear_of_const_Q`：\(Q\) 常数 ⇒ \(T_c\) 关于 \(\Upsilon_0\) 线性；
- `uemura_strictMono_in_U0`：\(Q>0\) 固定 ⇒ 严格单调增；
- `uemura_Q_le_one`、`uemura_Q_eq_one_iff`：\(Q=1\) 当且仅当 \(r=1\wedge g=1\)；
- `uemura_breakdown_witness`：显式数值例子，两个不同 \(\Upsilon_0\) 给不同 \(Q\)，故全局线性不成立；
- `uemura_bounds_combine`：与环 19 上界取小的合并。

Lean 不证明：\(\rho_s\leftrightarrow\Upsilon\) 的外部对应、Uemura／Homes 实验律、BKT 普适性、\(\Phi\) 的幂律。无 `axiom`、`sorry`、`admit`、`native_decide`、`unsafe`。

## 六、数值核对

脚本 `04_计算验证/目标区_Uemura.py`（复用环 19 的 Debye 权重与 \(\Phi\)，\(n_{\rm cell}=4\)、\(\sigma_c^2/Z=0.2\)、\(c=2\)）：

- \(p_{\rm pair}(0)=0.938448\)、\(\Phi(p_{\rm pair}(0))=0.808142\)（审-4 回改后；旧值 0.843010 已废弃）；
- RG 分离点 \(K_c=1.023\)（\(c=2\)），在自洽 \(T_c\) 上由普适跳变恒等式给 \(g_{\rm ren}=(2/\pi)/K_c=0.622281\)，且**在同一材料族内为常数**（因为 \(y_0=e^{-cK_0}\) 只依赖 \(K_0\)，分离点 \(K_c\) 不依赖 \(\Upsilon_0\)）；这是斜率 \(<1\) 的来源，不是拟合；
- 小 \(\Upsilon_0\) 段斜率 \(T_c/\Upsilon_{\rm bare}(0)=0.970533,0.943706,0.902577,\ldots\)，而 \(\pi g_{\rm ren}/2=0.977477\)：两者在端点附近一致，向下偏离随 \(\Upsilon_0\) 增大；
- \(\Upsilon_0=4\) 时斜率降到约 \(0.129\)，\(Q=0.129378\)；\(\Upsilon_0=0.05\) 时 \(Q=0.617861\)。\(Q\le1\) 全程成立；
- 核对：全部 \(T_c\le\pi\Upsilon_{\rm bare}(0)/2\)（(U.3)），全部 \(dT_c/d\Upsilon_0>0\)，割线斜率单调下降（(U.9)）。

四面板图：A 为 \(T_c\) 对 \(\Upsilon_{\rm bare}(0)\) 与 \(\pi/2\) 参考线（实际低 \(\Upsilon_0\) 斜率由 \(g_{\rm ren}\) 定）；B 为 \(Q\le1\)；C 为三个损耗通道 \(w\)、\(\Phi\) 比、\(g_{\rm ren}\)；D 为割线斜率下降。图像只作解析形状核对，不拟合实验数据。

## 七、状态与缺口

**状态**：(U.1)–(U.7)【条件严格】（条件于环 19 的跳变与因子化；(U.7) 的不等式方向由环 10／15 单调性给）；(U.2)(U.9)【构造＋条件判定】；(U.8)(U.10)【外部实验】；(U.3)【条件严格】。

**缺口**：

- `链外-B`：\(\Upsilon\leftrightarrow\lambda_L\leftrightarrow\rho_s\) 的电磁读出未闭合，Uemura 对照只在标度形状；
- `M6`：\(\Upsilon_0\) 的绝对值仍外生，(U.1) 不给绝对 \(T_c\)；
- `临-25`：\(g_{\rm ren}\) 的动态来源（涡旋逸度 \(y_0(T)\) 与核心能）未定；本轮只把它当读出因子；
- `审-4`：\(p_{\rm pair}\)（座）与 \(\Phi\)（键）的口径未统一；
- 链外-F：\(\sigma_{\rm dc}\) 不在链内，Homes 律不可推；
- TDOS 预印本的外部构造与 CQM 记忆核的关系未证，仅登记为下一轮 `临-25` 的对照候选；
- 数据对照（07 协议）未执行；本轮不声称与实验数值一致。

▸**不能推出**：由 (U.1) 推出 \(T_c\) 的绝对值；由 Uemura 线的形状符合推出 \(\rho_s=\Upsilon_{\rm bare}\) 的 CQM 证明；由 (U.9) 推出 Homes 律；由 TDOS 预印本推出 CQM 的记忆核谱；由本轮推出链外-B／链外-F 已闭合。
