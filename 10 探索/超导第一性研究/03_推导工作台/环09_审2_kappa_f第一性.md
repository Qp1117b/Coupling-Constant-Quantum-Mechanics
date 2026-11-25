# 环 9／`审-2`：$\kappa_f$ 的几何来源——亏角—钟速的对数响应

**状态**：工作台推导卡；未写入主链正文、06、08 台账。
**触发**：上一轮把 `M5` 的绝对归一归到外生 $\kappa_f$（审-2）。本轮问：$\kappa_f$ 是否真的"无定义"，还是能由 FG 接口给一个几何表达式？

**一句话**：能。把 DM.5 的 $\kappa_f$ 读作**亏角—钟速对数响应** $\kappa_f=-\partial_\varepsilon\ln v_\tau$，由 FG 接口 $v_\tau=\sqrt{1-\varepsilon/2\pi}$ 得

$$\kappa_f(\varepsilon_0)=\frac{1}{4\pi\bigl(1-\varepsilon_0/2\pi\bigr)},\qquad \kappa_f(0)=\frac{1}{4\pi}\approx0.0795775.$$

同时矩阵分支的线性尺度满足 $c=4\pi(1-\varepsilon_0/2\pi)\kappa_f$；取几何 $\kappa_f$ 后 $c\equiv1$ 在**所有**工作点成立，锚点给 $\kappa_f=1/(4\pi)$。**这是【构造＋条件严格】：关键识别是 DM.2 的连接 $C_{ij}$ 与环 5 的 $\lambda_{ij}=\ln v_{\tau,j}-\ln v_{\tau,i}$ 同一；不承认该识别则 $\kappa_f$ 仍外生。** 本轮把 `审-2` 从"定义缺失"推进为"已给几何表达式与数值，但依赖一条待审的识别"。

---

## 一、前件

1. FG 接口（06 §0.3，【假设】/E4）：
   $$v_\tau(\varepsilon)=\sqrt{1-\varepsilon/(2\pi)}. \tag{K2.1}$$
2. 环 5：$r_{ij}=v_{\tau,j}/v_{\tau,i}=\sqrt{1-\ell_{ij}/2\pi}$、$\lambda_{ij}=\ln r_{ij}=\ln v_{\tau,j}-\ln v_{\tau,i}$；DM.2 注记说 $\varepsilon_i$ 是相邻边亏角的节点代表值。
3. DM.5：$\langle(\delta C_{ij})^2\rangle=\kappa_f^2\langle(\Delta\varepsilon_i-\Delta\varepsilon_j)^2\rangle$，即线性化 $\delta C_{ij}=\kappa_f(\Delta\varepsilon_i-\Delta\varepsilon_j)$，$\kappa_f$ 此前无定义（`审-2`）。
4. 矩阵分支（A12-M.2）：$B_{ij}=f(\lambda_{ij})$、线性系数 $c=f'(0)$；上一轮齐次线性化给 $c$ 只定到尺度（`M5`）。
5. 外部标准（只作工具，不作 CQM 结论）：
   - Grüneisen 参数是"频率对体积的对数导数" $\gamma=-\partial\ln\Theta_D/\partial\ln V$，量纲一、刻画声波对形变的响应（Wikipedia *Grüneisen parameter*；arXiv:2003.07686 的应变—Grüneisen 例子；arXiv:2607.27803 Eq.(8)）。本轮的 $\kappa_f=-\partial_\varepsilon\ln v_\tau$ 是同一类**对数响应**，只是自变量从体积换成亏角；
   - Regge 微积分：绕铰链平行输运的旋转角就是亏角本身（arXiv:1904.01966 §；Phys. Lett. B **1989** 的定义），支持"亏角↔连接"的几何读法，但不替 CQM 证明 DM.2 的矩阵元。

---

## 二、推导：亏角—钟速对数响应

令

$$\phi(\varepsilon)\equiv\ln v_\tau(\varepsilon)=\tfrac12\ln\Bigl(1-\frac{\varepsilon}{2\pi}\Bigr). \tag{K2.2}$$

由环 5，

$$\lambda_{ij}=\phi(\varepsilon_j)-\phi(\varepsilon_i)\simeq\phi'(\varepsilon_0)\,(\varepsilon_j-\varepsilon_i)
=-\phi'(\varepsilon_0)\,(\varepsilon_i-\varepsilon_j). \tag{K2.3}$$

**识别（本轮的构造步骤）**：DM.2 的连接 $C_{ij}$ 在局域零曲率扇区取环 5 的对数连接，即 $\delta C_{ij}=\delta\lambda_{ij}$（在 (K2.3) 的线性阶）。与 DM.5 的 $\delta C_{ij}=\kappa_f(\Delta\varepsilon_i-\Delta\varepsilon_j)$ 比较：

$$\boxed{\ \kappa_f(\varepsilon_0)=-\phi'(\varepsilon_0)=\frac{1}{4\pi\bigl(1-\varepsilon_0/2\pi\bigr)}=\frac{1}{4\pi v_\tau^2(\varepsilon_0)}.\ } \tag{K2.4}$$

**导数核对**（解析严格）：$\phi'(\varepsilon)=\frac12\cdot\frac{-1/(2\pi)}{1-\varepsilon/2\pi}=-\frac{1}{4\pi(1-\varepsilon/2\pi)}$。

---

## 三、三条读出

**1. 零点锚的值**：$\ell_e=0$ ⇒ $\varepsilon_0=0$ ⇒

$$\kappa_f(0)=\frac{1}{4\pi}=0.0795774715\ldots \tag{K2.5}$$

无量纲（$\varepsilon$、$C$ 均无纲），与量纲要求一致。

**2. 矩阵分支的线性系数**：由 $\delta B_{ij}=c\,\delta\lambda_{ij}\simeq-c\phi'(\varepsilon_0)(\varepsilon_i-\varepsilon_j)$ 与 DM.5 比较，

$$c=\frac{\kappa_f}{-\phi'(\varepsilon_0)}=4\pi v_\tau^2(\varepsilon_0)\,\kappa_f. \tag{K2.6}$$

代入 (K2.4) 得 **$c\equiv1$ 对任意工作点成立**——同一条识别既定 $\kappa_f$、又把 $f$ 归一到 $f(x)\approx x$。数值核对发现一个易犯的错误：若把 $\kappa_f$ 固定在锚点值 $1/(4\pi)$ 而让 $\varepsilon_0$ 变化，则 $c=v_\tau^2$ 会随 $\varepsilon_0$ 下降；那不是 (K2.4) 的解，而是"$\kappa_f$ 不随工作点变"的额外假设。(K2.4) 要求 $\kappa_f$ 本身随 $\varepsilon_0$ 上升，从而 $c$ 恒为 $1$。

**3. 物理方向**：$\kappa_f>0$（在 $0\le\varepsilon_0<2\pi$ 上），且随 $\varepsilon_0\to2\pi^-$ 发散。这与 `M6` 的机制一致：亏角越大、钟速对数响应越强、配对差异越大。$v_\tau\to0$ 时响应发散，是 FG 接口的边界，不是新物理。

---

## 四、口径、条件与边界

1. **依赖 FG 接口**（【假设】/E4）：若 FG 形式被改（例如 $v_\tau=1-\varepsilon/4\pi+$ 高阶），(K2.4) 的系数随之改；本轮只给**当前权威 FG 形式下**的值。
2. **识别是构造**：$\delta C=\delta\lambda$ 是把 DM.2 的算符连接与环 5 的几何连接认作同一对象；链内无独立证明。若不承认该识别，$\kappa_f$ 仍外生——这是 `审-2` 剩余的唯一实质内容。
3. **节点 ε 与边 ℓ 的代表值**：DM.2 注记说 $\varepsilon_i$ 是相邻边亏角的代表值；(K2.3) 用同一代表值做局域展开，误差为高阶项，不影响线性系数。
4. **只给线性系数**：$f$ 的高阶项与 $M5$ 的齐次线性系统无关，仍开放。
5. **不动其他缺口**：`E4`、`M5`、`G19`、`审-3` 状态不变。

---

## 五、Lean 承载

`../05_Lean验证/KappaFDerivation.lean`：

- `phi` / `v2`：定义；
- `phi_deriv`：$\phi'(\varepsilon)=-1/(4\pi v_2)$（用 `HasDerivAt` 链则，条件 $v_2>0$）；
- `kappaF_formula` / `kappaF_at_zero` / `kappaF_pos`：几何表达式、$1/(4\pi)$、正性；
- `matrixScale_formula` / `matrixScale_eq_one` / `matrixScale_at_zero`：$c=4\pi v_2\kappa_f$、取几何 $\kappa_f$ 得 $c\equiv1$、锚点同样为 $1$。

未形式化：$\delta C=\delta\lambda$ 的物理识别（构造步骤）、FG 接口本身的证明（E4）、节点 ε 与边 ℓ 的代表值误差（高阶）。无 `axiom`、`sorry`、`admit`、`native_decide`、`unsafe`。

---

## 六、数值核对

`../04_计算验证/环09_审2_kappa_f.py`：

1. $\kappa_f(\varepsilon)=1/[4\pi(1-\varepsilon/2\pi)]$ 随 $\varepsilon$ 的曲线，标出 $\kappa_f(0)=0.0795775$ 与 $\varepsilon\to2\pi$ 的发散；
2. $c(\varepsilon)=1$ 的水平线（取几何 $\kappa_f(\varepsilon)$）；另画"$\kappa_f$ 固定在锚点值"的对照曲线 $c=v_\tau^2$ 以显示那不是 (K2.4) 的解；
3. (K2.3) 的线性化误差：精确 $\Delta\lambda=\phi(\varepsilon_0+\Delta)-\phi(\varepsilon_0)$ vs $-\phi'(\varepsilon_0)\Delta$，相对误差随 $\Delta$ 缩小；
4. $\kappa_f$ 与矩阵尺度 $c$ 的关系族 $c=4\pi(1-\varepsilon/2\pi)\kappa_f$，标出各工作点上的物理解 $(\kappa_f(\varepsilon),\,c=1)$ 都落在各自直线上。

所有曲线由 (K2.2)(K2.4)(K2.6) 直接计算，无拟合。

---

## 七、不能推出

1. **不能推出 DM.2 的算符矩阵元已被证明**：$\delta C=\delta\lambda$ 是构造识别。
2. **不能推出 FG 接口已证**：它仍是假设（E4）。
3. **不能推出 $f$ 的高阶项或 $M5$ 闭合**：只给线性系数。
4. **不能推出绝对 $T_c$**：$\kappa_f$ 只是一处耦合归一，不解决 $J_0$、$A(\varepsilon)$、$N$ 的归一。
5. **不能推出 $\kappa_f$ 与实验耦合常数（如 $\lambda_{\rm ep}$）同一**：链内无该对象；外部 Grüneisen 类比只作结构对照。
6. **不能推出 $\varepsilon_0=0$ 对所有材料成立**：锚点由 $\ell_e=0$ 定义，真实材料的工作点需另定。
7. **不能改 06 DM.2／DM.5、主链状态栏、08 台账**。

---

## 八、状态与缺口

**已确认（解析＋Lean 严格，条件于 FG 与识别）**：

- (K2.4)：$\kappa_f(\varepsilon_0)=1/[4\pi(1-\varepsilon_0/2\pi)]$；
- (K2.5)：$\kappa_f(0)=1/(4\pi)$；
- (K2.6)：$c=4\pi v_\tau^2\kappa_f$，取 (K2.4) 的 $\kappa_f$ 得 $c\equiv1$（锚点亦为 $1$）。

**判定**：`审-2` 从"$\kappa_f$ 无定义"推进为"**已给几何表达式与锚点数值，条件于 FG 接口与 $\delta C=\delta\lambda$ 识别**"；保留编号与未闭合状态（识别待审、FG 属假设）。

**未闭合**：识别的独立证明、FG 地位（E4）、$f$ 高阶项（M5）、$J_0$ 与绝对 $T_c$、`审-3`。
