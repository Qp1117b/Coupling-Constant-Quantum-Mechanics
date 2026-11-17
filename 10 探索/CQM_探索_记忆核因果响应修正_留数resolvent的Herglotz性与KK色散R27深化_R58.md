# CQM 探索：记忆核因果响应修正——留数 resolvent 的 Herglotz 性、KK 色散与 R27 深化——R58

> **定位**：探索稿（非权威源），v0.1，2026-11-17，第三十六轮。承接 R57（自伴生成元 $\hat{\mathcal G}=\hat{\mathcal D}^2+\tfrac14$）、R27/O1（竖直 $\zeta$ 核不是正测度 Laplace 核，不能直接当耗散响应）。本轮做一个**有理有据的修正完善**：分清两种"因果响应对象"——竖直 $\zeta$ 核（R27 已排除）vs 留数导出的自伴 resolvent（本轮）。后者是 Herglotz/Stieltjes 函数，满足正确的 Kramers-Kronig 色散，且退化为 BCS 单极点响应。
>
> **克制拟合声明**：全部零参数——resolvent、Herglotz 性、KK Hilbert 变换、单模退化均为标准数学/物理；数值 6000 零点缓存。脚本 `.calc/herglotz.py`（gitignore）。

---

## 第零部分：一句话结论（含对 R27 的深化）

R27 判定"竖直 $\zeta$ 核 $K=\zeta(2\sigma_0-i2\omega_0t)$ 不是正测度 Laplace 核、不能直接套耗散 KK/FDT"——本轮**不推翻而是深化**：若改用**留数导出的自伴 resolvent**（R57 生成元 $\hat{\mathcal G}=\hat{\mathcal D}^2+\tfrac14$ 的 resolvent）

$$
G_{\rm res}(z)=\sum_n\frac{w_n}{\mathfrak c_n-z},\qquad \mathfrak c_n=\tfrac14+\gamma_n^2,\qquad w_n=-2\,\mathrm{Re}\frac{1}{\rho_n(\rho_n+1)}>0,
\tag{R58.1}
$$

则它**是** Herglotz/Stieltjes 函数（$\mathrm{Im}\,G_{\rm res}(z)>0$，$\mathrm{Im}\,z>0$），满足 KK 色散关系（Hilbert 重构误差数值精度内为 0），并有正谱测度（3000/3000 权重 $>0$）。数值：$G_{\rm res}(0)=7.3\times10^{-5}$。**结论**：CQM 记忆核的"因果响应"不是竖直 ζ 核（R27 排除），而是留数 resolvent——两种对象严格分清。单模极限退化为标准洛伦兹对（$\pm\sqrt{\mathfrak c_1}=\pm14.14$），即 BCS/Eliashberg 单极点响应。新增判据 R58a/b/c。

---

## 第一节：退化门槛（先过）

| 门槛 | CQM 表述 | 本轮关系 | 状态 |
|:---|:---|:---|:---|
| BCS | 配对限制支单阶段 DM.23–24 | 单模 resolvent $\to$ 单洛伦兹（标准单极点响应） | ✅ |
| 迈斯纳 | $\rho_s\propto n_s$ | resolvent 是响应论对象，不改平衡 $\rho_s$ | ✅ |
| Z2/Z3 | $\mathfrak c_n,w_n,z$ 无量纲 | 物理频率标度仍外生 | ✅ |

---

## 第二节：外部文献（逐条标源，分栏）

| 编号 | 出处 | 外部结论 | 接口 |
|:---|:---|:---|:---|
| W1 | Kramers–Kronig 关系（Kronig 1926；David Tong 线性响应讲义；UVA EM 讲义） | 因果响应 $\chi$ 上半平面解析，实/虚部由 Hilbert 变换联系 | resolvent 的色散关系 |
| W2 | Kubo, *Rep. Prog. Phys.* **29**, 255 (1966); FDT 综述 | 迟滞/延迟 Green 函数上半平面解析；$\mathrm{Im}\chi''$ = 耗散谱 | 因果对象辨析 |
| W3 | Bernstein 定理（1928）；本库 R27 | 正测度 Laplace 变换完全单调、无零点；竖直 ζ 核有零点 → 非此类 | 本轮修正的出发点 |
| W4 | Stieltjes/Herglotz 函数理论（谱理论讲义 ETH/kowalski） | resolvent $\int d\mu(\lambda)/(\lambda-z)$ 是 Herglotz 函数，$\mathrm{Im}>0$ | 正确因果对象 |
| W5 | 本库 R57/R56 稿 | 生成元 $\hat{\mathcal G}$；留数振幅 $1/[\rho(\rho+1)]$ | 直接承接 |

> **分栏**：W1–W4 为外部数学/物理结论，仅作对照；CQM 修正落点见下。

---

## 第三节：理想模型与图像（两种因果对象辨析）

### §3.1 修正的核心：分清两个对象

$$
\underbrace{K_{\rm vertical}(t)=\zeta(2\sigma_0-i2\omega_0t)}_{\text{R27 排除: 有零点,非正测度 Laplace}}\quad\ne\quad
\underbrace{G_{\rm res}(z)=\sum_n\frac{w_n}{\mathfrak c_n-z}}_{\text{本轮: 正测度 resolvent, Herglotz}}.
\tag{R58.2}
$$

- 竖直 ζ 核：直接作为时间关联/红外谱权重 → 违反 Bernstein（R27），不能套耗散 KK。
- 留数 resolvent：自伴生成元 $\hat{\mathcal G}$ 的 resolvent，谱测度 $w_n>0$ → Herglotz，满足 KK。

### §3.2 图像：resolvent 的 Herglotz 性

```
  Im z > 0 (上半平面)
     │   G_res(z) = sum w_n/(c_n - z),  c_n 在实轴 (1/4+gamma_n^2)
     │   Im G_res(z) > 0  everywhere  <- Herglotz (因果解析)
     │   poles at c_n on real axis (自伴谱)
     │
     ├─ Im G_res(omega+i0) = pi * sum w_n delta(omega - c_n)  (耗散谱, 正)
     ├─ Re G_res = (1/pi) P int Im G_res(w')/(w'-w) dw'  (KK)
     │
     └─ 单模: G = w/(c-z) -> ImG = 洛伦兹 (BCS/Eliashberg 单极点)
```

---

## 第四节：判决性计算（零参数）

### §4.1 正谱测度与 Herglotz 性

权重 $w_n=-2\mathrm{Re}[1/(\rho_n(\rho_n+1))]$：3000/3000 全正（min $1.6\times10^{-7}$，max $9.85\times10^{-3}$）——**正谱测度**成立。上半平面各测试点：

| $z$ | $\mathrm{Im}\,G_{\rm res}(z)$ |
|:---|:---|
| $1+i$ | $+{\rm small}>0$ ✓ |
| $100+10i$ | $+1\times10^{-5}>0$ ✓ |
| $-50+0.5i$ | $>0$ ✓ |
| $500+100i$ | $+6\times10^{-5}>0$ ✓ |

**判决**：$\mathrm{Im}\,G_{\rm res}>0$ 处处成立——Herglotz 函数，正确的因果解析性。

### §4.2 KK 色散关系

对展宽 $\varepsilon=30$ 的 resolvent，用 FFT Hilbert 变换重构实部：mean$|\mathrm{Re}G_{\rm Hilbert}-\mathrm{Re}G|=0.0000$（数值精度内）。**判决**：KK 色散成立。

### §4.3 求和规则与 BCS 退化

- $G_{\rm res}(0)=\sum w_n/\mathfrak c_n=7.3\times10^{-5}$（有限正值，纯数）。
- 单模极限：$G=w/(\mathfrak c-z)\Rightarrow\mathrm{Im}\,G$ 为 $\pm\sqrt{\mathfrak c_1}=\pm14.14$ 的洛伦兹对——标准单极点 Eliashberg/Debye 响应，**无 GUE 结构**（GUE 只在多模叠加时出现）。

---

## 第五节：新判据 R58（三条）

- **R58a（正确因果对象）**：CQM 记忆核的因果响应须用留数 resolvent $G_{\rm res}$（Herglotz），不是竖直 ζ 核（R27 排除）。若某实验按竖直 ζ 核拟合耗散谱且声称因果，则与 R27 冲突。
- **R58b（正谱测度）**：权重 $w_n=-2\mathrm{Re}[1/(\rho_n(\rho_n+1))]$ 须全正（本轮 3000/3000）；否则 resolvent 非 Herglotz，因果性失败。
- **R58c（KK + 单模退化）**：$G_{\rm res}$ 须满足 KK 色散；多模（GUE）→ 谱刚性与 GUE 指纹，单模 → 洛伦兹（BCS 退化）。若 BCS 端仍见多峰 GUE 结构，则退化失败。

> 与 R57（生成元方程）、R27（两核不相容）、R48（SFF）测不同对象：R58 测**因果响应对象的正确形式与 KK 色散**。

---

## 第六部分：退化守住

| 对象 | 本轮处理 |
|:---|:---|
| BCS（DM.23–24） | 单模 resolvent → 单洛伦兹（标准单极点响应）；✅ |
| 迈斯纳（R37） | resolvent 不改 $\rho_s$；✅ |
| Z2/Z3 | 全无量纲；频率标度外生；✅ |
| R27/O1 | **深化非推翻**：竖直 ζ 核仍排除；留数 resolvent 是新对象（不矛盾） |
| R57/R56 | 不变；resolvent 建立在生成元谱 + 留数振幅上 |
| 缺口 | 不升级 |

---

## 第七部分：边界与开放问题

1. **修正性质**：本轮修正"KK 能否用于 CQM"的答案——竖直 ζ 核否（R27），留数 resolvent 是；这是对 R27 的深化，非推翻。
2. **resolvent vs 记忆核**：$G_{\rm res}$ 是响应论对象，与记忆核 $K(t)$（时间关联）相关但不同；两者关系（resolvent 是 $K$ 的 Laplace/Stieltjes 变换的某种）需进一步形式化，本轮给出谱测度层面。
3. **谱测度来源**：$w_n$ 由留数导出（正性是关键），非任意正测度——这保留了 CQM 的数论特性（区别于一般记忆主导框架）。
4. **求和规则数值**：$G_{\rm res}(0)=7.3\times10^{-5}$ 是 N=3000 截断值，严格值是 $N\to\infty$ 极限（慢收敛）。
5. **未做**：lean、网站、完整理论文档、参数拟合；无文档需删（删除须你确认）。

---

## 参考文献与脚本

- [W1] Kramers–Kronig（Kronig 1926；D. Tong 线性响应讲义 davidtong.org；UVA EM 讲义）。
- [W2] R. Kubo, *Rep. Prog. Phys.* **29**, 255 (1966); FDT 综述。
- [W3] S. Bernstein (1928); 本库 R27 稿（`CQM_探索_记忆主导普适类的谱类判决_两核不相容_Z2外部实例与Uemura两段.md`）。
- [W4] Stieltjes/Herglotz 函数（谱理论讲义，ETH kowalski）。
- [W5] 本库 R57/R56 稿。
- CQM 侧：生成元 $\hat{\mathcal G}$、留数振幅见 `06 超导/CQM_超导核心理论.md`。
- 脚本 `.calc/herglotz.py`（gitignore）；零点缓存 `.calc/zeros.npy`。
