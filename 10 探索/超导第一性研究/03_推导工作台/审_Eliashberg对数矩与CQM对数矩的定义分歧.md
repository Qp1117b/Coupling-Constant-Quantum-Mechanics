# 审：Eliashberg $\omega_{\log}$（Webb 式3）与 CQM $\omega_{\log}$（目标.3）是两个不同的矩——第57轮口径错位的更深根

**状态**：工作台审查卡；不改主链权威式、不动缺口编号与状态栏、不动账面。
**触发**：用户"发现不对劲再回过头有理有据修正"。在回查第57轮 Karakozov 前因子时发现的更深口径问题。
**文献依据**（已 webfetch 全文核对）：
- Webb 2015 式(3)：$\omega_{\ln}\equiv\exp\big[\frac{2}{\lambda}\int_0^\infty d\nu\,\ln\nu\,\frac{\alpha^2(\nu)F(\nu)}{\nu}\big]$；
- Webb 2015 式(4)：$\lambda\equiv2\int_0^\infty d\nu\,\frac{\alpha^2(\nu)F(\nu)}{\nu}$；
- Marsiglio Eq7（Einstein 谱）：$\alpha^2F(\nu)=(\lambda\omega_E/2)\delta(\nu-\omega_E)$；
- CQM (目标.3)：$\omega_{\log}^{\rm amp}=\exp\int_0^1 3y^2\ln(\omega_D y)dy=\omega_D e^{-1/3}$（3D Debye **电子态密度**权重 $3y^2$）。

---

## 一、两个"对数矩"的权重根本不同

把 Webb 式(3) 写成归一化形式：$\omega_{\ln}=\exp\int \ln\nu\, w_{\rm ph}(\nu)d\nu$，其中
$$w_{\rm ph}(\nu)=\frac{(2/\lambda)\,\alpha^2F(\nu)/\nu}{\int(2/\lambda)\,\alpha^2F(\nu)/\nu\,d\nu}=\frac{\alpha^2F(\nu)/\nu}{\lambda/2}=\frac{\alpha^2F(\nu)/\nu}{\int\alpha^2F(\nu)/\nu\,d\nu}.\tag{E.1}$$
即 Eliashberg 对数矩的权重是 **$\alpha^2F(\nu)/\nu$（声子谱除以频率）**，归一化由 $\lambda/2=\int\alpha^2F/\nu$（式4）给出。

**Debye 声子谱** $\alpha^2F(\nu)\propto\nu^2$（$\nu<\nu_D$）⇒ $w_{\rm ph}(\nu)\propto\nu$（即 $2y\,dy$ 权重！）⇒
$$\omega_{\ln}^{\rm Debye}=\exp\int_0^1 2y\ln(\nu_D y)dy=\nu_D e^{-1/2}.\tag{E.2}$$
**Einstein 谱** $\alpha^2F=(\lambda\omega_E/2)\delta(\nu-\omega_E)$ ⇒ $\omega_{\ln}=\omega_E e^{0}=\omega_E$。

而 CQM (目标.3) 的 $\omega_{\log}=\omega_D e^{-1/3}$ 用 **$3y^2$ 权重**——那是 **3D 电子态密度** $\propto\sqrt\epsilon$（$\epsilon$ 测度）或声子态密度 $\propto\nu^2$ 本身，**不是** $\alpha^2F/\nu\propto\nu$。

| 量 | 权重 | Debye 结果 |
|:---|:---|:---|
| Eliashberg $\omega_{\ln}$（Webb 式3） | $\alpha^2F/\nu\propto\nu$（即 $2y$） | $\nu_D e^{-1/2}$ |
| CQM $\omega_{\log}$（目标.3） | $3y^2$（电子态密度/声子 DOS） | $\omega_D e^{-1/3}$ |

**两者相差 $e^{1/6}$**——恰是第57轮 Karakozov 因子的同一数值！这不是巧合：第57轮把 $e^{-1/6}$ 当"截断↔对数矩换算"，实际上它同时纠缠了两个不同的矩定义。

## 二、对第57轮的影响

第57轮写：$1.13e^{-1/2}\theta_D=1.13e^{-1/6}(e^{-1/3}\theta_D)=1.13e^{-1/6}\omega_{\log}^{\rm CQM}$，并称与 Eq37（Einstein 谱，$1.13/\sqrt e\,\omega_E$）"精确重合"。现在看清：

- Eq37 的 $\omega_E$ 在 Einstein 谱下**就是** $\omega_{\ln}$（E.2 的特例）；
- 若要把 Eq37 推广到 Debye 谱，正确的替换是 $\omega_E\to\omega_{\ln}^{\rm Debye}=\nu_D e^{-1/2}$，**不是** $\omega_D e^{-1/3}$；
- 第57轮用的 $\omega_{\log}^{\rm CQM}=e^{-1/3}\theta_D$ 是**电子态密度矩**，与 Eliashberg 的 $\alpha^2F/\nu$ 矩差 $e^{1/6}$。

所以第57轮"精确重合"的恒等式两边用的都不是 Eliashberg 真正会用的量——它把 CQM 的电子态密度矩塞进 Eliashberg 前因子位置。**方向**（前因子需 $e^{-1/2}$ 型修正）可能对（Combescot 普适性），但**用的矩对象错了**。

## 三、这意味着什么（不夸大）

1. **不改主链权威式**：(目标.2)(目标.3) 是 CQM 自己的定义，自洽；本卡不要求把它们改成 $e^{-1/2}$（那会牵动整个 2D/3D 扇区结构，且无授权）；
2. **但必须标注**：CQM $\omega_{\log}$ 与 Eliashberg $\omega_{\ln}$ **不是同一个量**，把 CQM 值代入 Eliashberg 式（第57、58、60、61轮多次做的）是**跨定义代入**，其结果（Eq37 重合、2.7% gap ratio、$\mu^\ast$ 双观测）需加边界："用的是 CQM 矩，非 Eliashberg 标准矩"；
3. **登记缺口** `审-17`（临时编号）：“CQM $\omega_{\log}$（$3y^2$ 矩）与 Eliashberg $\omega_{\ln}$（$\alpha^2F/\nu$ 矩）的对应关系未建立——两矩相差 $e^{1/6}$，跨定义代入标准式的合法性未证”；
4. **gap ratio 2.7% 需重新审视**：第58轮 Mitrović 公式的输入 $T_c/\omega_{\ln}$ 我用了 $\omega_{\ln}\approx e^{-1/3}\theta_D$，若应用 $e^{-1/2}\theta_D$，则 $T_c/\omega_{\ln}$ 整体乘 $e^{-1/6}=0.846$，gap ratio 会变——**需重算**，这是诚实的回头检验。

## 四、立即回头：重算 gap ratio（用正确的 Eliashberg 矩）

第58轮用 $\omega_{\ln}=e^{-1/3}\theta_D$。按 Webb 式(3) 的 Debye 谱，应为 $\omega_{\ln}=e^{-1/2}\theta_D$。两者差 $e^{-1/6}=0.8465$，使 $x=T_c/\omega_{\ln}$ 增大 $e^{1/6}=1.181$ 倍。Mitrović 公式（Webb 式6）的修正项 $\propto x^2$，gap ratio 会系统性**升高**。重算后与实验对比——这是"发现不对劲回头修正"的直接执行。脚本：`审_Eliashberg矩重算gap比.py`。

## 五、不能推出

1. 不能说 CQM $\omega_{\log}$ 等于 Eliashberg $\omega_{\ln}$——权重不同（$3y^2$ vs $2y$）；
2. 不能说第57轮完全错——方向可能对，但用了错的矩对象，证据链不成立；
3. 不能说 gap ratio 2.7% 是最终值——用正确矩重算后可能变；
4. 不能改权威式、状态栏、账面、06 原文。

## 六、交付

- 审查卡（本文件＋`审_Karakozov前因子的谱假设回查.md`）；
- 重算脚本 `04_计算验证/审_Eliashberg矩重算gap比.py`／`.png`／`.csv`；
- 决策 `06_决策记录/2026-11-23_Eliashberg矩定义分歧回查.md`；`成果登记.md`、README、口径表边界注记。

## 七、状态

发现 CQM $\omega_{\log}$（$3y^2$ 矩）与 Eliashberg $\omega_{\ln}$（$\alpha^2F/\nu$ 矩，$e^{-1/2}$）的定义分歧，差 $e^{1/6}$；第57轮及后续跨定义代入需加边界注记；登记两个临时缺口；gap ratio 用正确矩重算。主链权威式、状态栏、账面、06 原文均不动。
