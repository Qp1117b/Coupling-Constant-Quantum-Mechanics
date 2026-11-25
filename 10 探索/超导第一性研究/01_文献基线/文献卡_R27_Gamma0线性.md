# 文献卡 R27：$\Gamma_0$ 的温度依赖（逐字引文，供 R27 脚本核查）

> 本卡只存外部原文短引与出处，不升格为链内结论。

## 1. Norman–Randeria–Ding–Campuzano, PRB 57, R11093(R) (1998)

- **出处**：DOI `10.1103/PhysRevB.57.R11093`；全文 `ex7.iphy.ac.cn/downfile/32_PRB_57_R11093.pdf`。
- **摘要逐字**："The filling-in of the pseudogap with increasing T is described by a broadening proportional to T-Tc, which is naturally explained by pairing correlations above Tc."
- **正文逐字**："We find ... $\Gamma_0=0$ below Tc and proportional to T-Tc above."
- **附录逐字**："we obtain the second term in Eq. (2) with $\Gamma_0(T)=8(T-T_c)/\pi$."
- **T\* 判据逐字**："we observe from Fig. 2 that T* corresponds to where $\Delta(T)\approx\Gamma_0(T)$."
- **检索用 ASCII 短引**：`Gamma_0(T)=8(T-T_c)/pi`；`proportional to T-Tc`；`linearly with T`；`T* corresponds to where`。
- **自能形式**：$\Sigma(k,\omega)=-i\Gamma_1+\Delta^2/(\omega+\varepsilon_k+i\Gamma_0)$；$\Gamma_0$ 是**逆对寿命**，低温配对态 $\Gamma_0=0$。
- **样品**：欠掺 Bi2212 $T_c=83$ K，$T^*\sim200$ K；另一欠掺 $T_c=77$ K。

## 2. Kanigel et al., Nature Physics 2, 447–451 (2006)

- **出处**：DOI `10.1038/nphys334`。
- **逐字**："the inelastic broadening parameter $\Gamma_0(T)$ ... is known to increase linearly with T, and T* is determined by $\Gamma_0(T^*)=\Delta(\phi=0)$."
- **逐字**："The pseudogap effectively disappears for T > T*"；"gap does not change, but rather there is a filling-in of low-energy spectral weight"。

## 3. 与项目既有笔记的关系

- README L1264 与 `02_缺口重审/链外重审_六个接口的链内接法.md` §6.3 写 "$\Gamma_0\propto(T/T_c)^2$"——**误引**；两篇原文均为线性 $T-T_c$。R27 加更正注记，状态栏不动。
- 链内 $1-w(T)$ 的 $T^2$（(10B.5)）是 Debye 相位相干权重的**低温展开**，不是对寿命宽度；两者零点位置不同（$\Gamma_0(T_c)=0$，$1-w(T_c)>0$）。
