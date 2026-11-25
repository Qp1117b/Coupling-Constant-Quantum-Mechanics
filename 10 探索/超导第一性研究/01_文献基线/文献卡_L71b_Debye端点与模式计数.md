# 文献卡 L71b：Debye 端点＝模式计数，$\Theta_D=(\hbar v_s/k_B)(6\pi^2n)^{1/3}$

**检索日期**：2026-11-24
**对应环节**：环 2 `W-3`（截断位置）、环 4 `审-10`（截断＝谱支集）、目标区 $T^*$ 的 $\Theta_D$

## 一、外部结论

| # | 结论 | 出处 |
|:--|:---|:---|
| 1 | Debye 模型的端点由模式计数定：$\int_0^{\omega_D}g(\omega)\,d\omega=3N$，$g\propto\omega^2$ ⇒ $\omega_D=v_s(6\pi^2n)^{1/3}$ | P. Debye, *Ann. Phys.* **344**, 789–839 (1912). DOI 10.1002/andp.19123441404 |
| 2 | 同一式写作 $\Theta_D=(\hbar/k_B)(6\pi^2n)^{1/3}v_s$，其中 $v_s$ 是平均声速，常由弹性常数 $v_l,v_t$ 合成 $v_s=[\tfrac13(2v_t^{-3}+v_l^{-3})]^{-1/3}$ | Kittel, *Introduction to Solid State Physics*, 8th ed., Ch. 5；近期文献直接使用该式由声速定 $\Theta_D$（如 *Materials Today Sustainability* 2024, Eq. 3） |
| 3 | Debye 谱低温 $C_V\propto(T/\Theta_D)^3$；$\Theta_D$ 是"量子效应开始显著"的能标 | 同上；标准教科书结论 |

## 二、可约束的链内环节

- **`W-3` 的截断**：链内 $\omega_D$ 是 $(4.1)$ 的方差测度支集端点。由 #1，它不是"可选位置"，而是**模式计数**的唯一解；由此 $Q=\omega_D/c_s=(6\pi^2n)^{1/3}$ 被钉死，与 `审-10` 的"截断＝谱支集 $\omega_D$"一致。
- **$T^*$ 的 $\Theta_D$**：$(目标.2)$ 的 $1.13e^{-1/2}\hbar\Theta_D$；本卡把 $\Theta_D$ 从"外生独立输入"降为**两个标准材料量** $(v_s,n)$ 的合成。
- **同位素指数**：$\Theta_D\propto v_s\propto M^{-1/2}$（谐波、Born–Oppenheimer 下力常数与 $M$ 无关）⇒ $\partial\ln\Theta_D/\partial\ln M=-1/2$。

## 三、不可越界（红线）

1. 这是**外部标准结果**，CQM 只是承认"截断＝模式计数"，不能写成"CQM 推出了 Debye 温度"。
2. Debye 模型自身有 10%–25% 的误差（真实谱非 $\omega^2$、有光学支）；本卡不据此声称 CQM 精确到该精度以下。
3. 不引入任何以超导数据反解的参数（否则成循环）。

## 四、不能推出

不能推出多原子胞（光学支主导，如 MgB$_2$）的端点仍由单支声速给出；不能推出 $\Theta_D$ 的各向异性修正。
