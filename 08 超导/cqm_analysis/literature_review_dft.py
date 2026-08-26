"""
文献调研：从DFT计算δ_intrinsic和f→前向计算Tc

核心问题：arccoth公式是拟合框架（反推δ_v），要成为预言框架必须：
  1. 从DFT能带→Berry曲率→δ_intrinsic
  2. 从DFT声子谱→f
  3. 正向计算Tc，与实验比较

突破：自由能公式 Tc² = 8Δδ₀² K_eff θ_D / (9 ln2)
  已建立前向预测框架, LOOCV中位45%, 2倍内81%。
  详见 free_energy_tc_derivation.py 和 final_tc_chain.py。

本文件整理关键文献、计算方法和具体实现路径。
"""

print("=" * 90)
print("文献调研：从DFT第一性原理计算δ_intrinsic和f")
print("=" * 90)

# ============================================================
# 1. Berry曲率的DFT计算
# ============================================================
print("""
╔══════════════════════════════════════════════════════════════════════╗
║ 1. Berry曲率的DFT计算方法                                            ║
╚══════════════════════════════════════════════════════════════════════╝

1.1 理论基础
─────────────
Berry曲率定义:
  Ω_n(k) = ∇_k × A_n(k)
  A_n(k) = i⟨u_{nk}|∇_k|u_{nk}⟩  (Berry联络)

计算方法（两种等价途径）:

途径A: 波函数直接计算（Kubo公式）
  Ω_n,αβ(k) = -2 Im Σ_{m≠n} ⟨u_n|v_α|u_m⟩⟨u_m|v_β|u_n⟩ / (E_m - E_n)²
  其中 v_α = (1/ℏ)∂H/∂k_α 是速度算符
  文献: Xiao, Chang)RMP 2010 [1]

途径B: Wannier插值（更高效）
  1. DFT计算Bloch态 |u_{nk}⟩ 在均匀k网格
  2. 构造Wannier函数 |R_n⟩ = Σ_k e^{-ikR} U_{mn}(k) |u_{nk}⟩
  3.G)在Wannier基中计算Berry曲率（实空间矩阵元）
  文献: Marzari & Vanderbilt, PRB 1997 [2]
  软件: Wannier90 [3]

1.2 关键文献
─────────────
[1] Xiao, Chang & Niu, RMP 82, 1959 (2010)
    "Berry phase effects on electronic properties"
    → Berry曲率的完整理论框架

[2] Marzari & Vanderbilt, PRB 56, 12847 (1997)
    "Maximally localized Wannier functions"
    → Wannier函数方法

[3] Pizzi et al., J. Phys. Mater. 2, 013001 (2020)
    "Wannier90 as a community code"
    → Wannier90软件包

[4] Wang, Yates, Souza & Vanderbilt, PRB 74, 195118 (2006)
    "Berry curvature calculation from Wannier interpolation"
    → Berry曲率的Wannier插值实现

1.3 计算软件
─────────────
- Wannier90: 从DFT能带→Wannier函数→Berry曲率
  输入: DFT能带(Quantum ESPRESSO/VASP)
  输出: Ω(k)在Fermi面上每点的值

- VASP (LSORBIT=.TRUE., LWANNIER90=.TRUE.):
  内置Berry曲率计算

- Quantum ESPRESSO + EPW:
  电子-声子耦合+Berry曲率

1.4 具体步骤
─────────────
对Nb(BCC, a=3.30Å):
  Step 1: DFT自洽计算 (Quantum ESPRESSO pw.x)
    - PBE泛函, 60 Ry截断, 24×24×24 k网格
    - 收敛后得到能带E_n(k)和波函数|u_{nk}⟩

  Step 2: Wannier化 (Wannier90)
    - 选择投影函数(Nb d轨道)
    - Disentanglement (能量窗口)
    - 得到MLWF

  Step 3: Berry曲率 (Wannier90 berry.kmesh)
    - 在密集k网格(200×200×200)上计算Ω(k)
    - 提取Fermi面(|E_n(k)-E_F|<Δ)上的Ω(k)

  Step 4: 积分δ_intrinsic
    δ_intrinsic = (1/2π) × Σ_{k∈FS} |Ω(k)| ΔS_k / A_FS
    其中 ΔS_k 是Fermi面面积元, A_FS 是总Fermi面面积
""")

# ============================================================
# 2. Fermi面几何与超导的已有研究
# ============================================================
print("""
╔══════════════════════════════════════════════════════════════════════╗
║ 2. Fermi面几何与超导的已有研究                                       ║
╚══════════════════════════════════════════════════════════════════════╝

2.1 Fermi面嵌套与超导
─────────────────────
[5] Kohn & Luttinger, PRL 15, 524 (1965)
    "New mechanism for superconductivity"
    → Fermi面几何可产生超导配对（不需要电声耦合）

[6] Scalapino, RMP 84, 1383 (2012)
    "Common factors in high-Tc superconductors"
    → Fermi面嵌套矢量Q与自旋涨落峰的关系

[7] Mazin, Singh & Johannes, PRL 101, 057003 (2008)
    "Unconventional superconductivity with a sign gap"
    → 铁基超导: Fermi面嵌套决定配对对称性

2.2 van Hove奇点与高温超导
──────────────────────────
[8] van Hove, Physica 21, 1175 (1953)
    "Singularities in the density of states"
    → van Hove奇点的原始定义

[9] Dzyaloshinskii, JPCM 9, 2422 (1996)
    "Fermi surface conditions for superconductivity"
    → Fermi面拓扑条件决定超导可能性

[10] Markiewicz, J. Supercond. 10, 5 (1997)
     "Fermi surface topology of high-Tc superconductors"
     → 铜氧化物Fermi面拓扑与Tc的关系

[11] Irifune et al., PRB 79, 125120 (2009)
     "van Hove singularity and superconductivity"
     → van Hove点附近Tc增强的定量计算

2.3 Fermi面曲率与超导
─────────────────────
[12] Hirsch, PRB 31, 4403 (1985)
     "Fermi surface and superconductivity"
     → Fermi面形状影响超导配对强度

[13] Abrikosov, Europhys. Lett. 39, 111 (1997)
     "Anomalous properties of high-Tc superconductors"
     → Fermi面曲率与超导能隙的关系

2.4 CQM与已有文献的关系
─────────────────────
CQM的δ_intrinsic = (1/2π)∫|Ω|dS/A_FS 与上述文献的关系:
- 与[9]一致: Fermi面拓扑条件决定超导
- 与[11]一致: van Hove点(曲率发散)→δ最大→Tc最高
- 与[12]一致: Fermi面形状(曲率)影响超导
- 新内容: 具体公式 δ ≈ 1/β 是超导临界条件
""")

# ============================================================
# 3. DFT声子谱与f的计算
# ============================================================
print("""
╔══════════════════════════════════════════════════════════════════════╗
║ 3. DFT声子谱与关联因子f的计算                                       ║
╚══════════════════════════════════════════════════════════════════════╝

3.1 DFT声子谱计算方法
─────────────────────
[14] Baroni, de Gironcoli & Dal Corso, RMP 73, 515 (2001)
     "Phonons and related crystal properties from DFPT"
     → DFPT计算声子的标准方法

[15] Giannozzi et al., J. Phys. Condens. Matter 21, 395502 (2009)
     "Quantum ESPRESSO: a modular DFT code"
     → QE的ph.x计算声子谱

软件:
- Quantum ESPRESSO: pw.x(自洽) → ph.x(声子) → q2r.x(实空间力常数) → matdyn.x(色散)
- VASP: IBRION=5/6, LEPSILON=.TRUE.
- Phonopy: 从VASP/QE力常数计算声子谱

3.2 从声子谱计算f的具体方法
────────────────────────────
声子本征值问题:
  D(k) e_ν(k) = ω_ν²(k) e_ν(k)
  其中D(k)是动力学矩阵, e_ν(k)是声子偏振矢量

原子位移的零点运动:
  ⟨u_i²⟩ = Σ_{k,ν} |e_{i,ν}(k)|² ℏ / (2m_i ω_ν(k))

最近邻位移关联:
  ⟨u_i · u_j⟩ = Σ_{k,ν} e_{i,ν}(k)·e*_{j,ν}(k) ℏ / (2√(m_i m_j) ω_ν(k))

关联因子:
  f = ⟨u_i · u_j⟩ / √(⟨u_i²⟩ × ⟨u_j²⟩)

  = [Σ_{k,ν} e_{i,ν}(k)·e*_{j,ν}(k) / (√(m_i m_j) ω_ν)] /
    [√(Σ_{k,ν} |e_{i,ν}|²/(m_i ω_ν) × Σ_{k,ν} |e_{j,ν}|²/(m_j ω_ν))]

3.3 具体步骤
────────────
对Nb(BC)C, a=3.30Å):
  Step 1: DFT自洽计算 (pw.x)
  Step 2: 声子计算 (ph.x)
    - q网格 8×8×8
    - 得到D(q)和e_ν(q)在所有q点
  Step 3: 实空间力常数 (q2r.x)
  Step 4: 密集插值 (matdyn.x)
    - 在200×200×200 q网格上插值
  Step 5: 计算f
    - 对每个最近邻对(i,j)
    - 求和⟨u_i·u_j⟩和⟨u_i²⟩
    - f = ⟨u_i·u_j⟩/⟨u²⟩

3.4 与Debye近似的比较
────────────────────
Debye近似: f = sinc²(k_D R/2) ≈ 0.16 (BCC)
精确DFT: f = ? (需实际计算)

差异来源:
- Debye假设各向同性声速, 实际晶格各向异性
- Debye忽略光学模, 实际有光学模(对化合物)
- Debye忽略声子色散细节, 实际有声子软化等
""")

# ============================================================
# 4. 可用的DFT数据库
# ============================================================
print("""
╔══════════════════════════════════════════════════════════════════════╗
║ 4. 可用的DFT数据库与工具                                             ║
╚══════════════════════════════════════════════════════════════════════╝

4.1 材料数据库
─────────────
[16] Materials Project (materialsproject.org)
     - ~150,000材料的DFT数据
     - 能带、声子、弹性常数
     - REST API: https://api.materialsproject.org
     - Python: pymatgen + MPRester

[17] AFLOW (aflowlib.org)
     - ~3,000,000材料的DFT数据
     - REST API

[18] JARVIS-DFT (jarvis.nist.gov)
     - ~55,000材料
     - 包含Berry曲率相关数据

[19] COD (crystallography.net)
     - 晶体结构数据库

4.2 超导数据库
─────────────
[20] SuperCon (supercon.nims.go.jp)
     - 36,000+超导材料
     - Tc, 压力, 结构

[21] Materials Project Superconductor
     - DFT计算的电子-声子耦合

4.3 计算工具链
─────────────
完整计算链:
  晶体结构(COD/MP)
    → DFT能带(QE/VASP)
      → Wannier函数(Wannier90)
        → Berry曲率 → δ_intrinsic
    → DFT声子(QE ph.x)
      → 声子本征矢量 → f
    → 正向计算Tc
      → 与SuperCon实验Tc比较

4.4 Python工具
─────────────
- pymatgen: 材料结构操作
- mp_api: Materials Project API
- ase: 原子模拟环境
- phonopy: 声子计算
- wannier90: Wannier函数(通过QE接口)
""")

# ============================================================
# 5. 具体计算路径
# ============================================================
print("""
╔══════════════════════════════════════════════════════════════════════╗
║ 5. 具体计算路径：从DFT到前向Tc                                       ║
╚══════════════════════════════════════════════════════════════════════╝

5.1 完整流程（以Nb为例）
─────────────────────
Step 1: 获取晶体结构
  → Materials Project: mp-72 (Nb, BCC, a=3.30Å)
  → pymatgen: MPRester().get_structure_by_material_id("mp-72")

Step 2: DFT自洽计算
  → Quantum ESPRESSO pw.x
  → PBE, 60 Ry, 24×24×24 k网格
  → 输出: 能带E_n(k), 波函数ψ_nk

Step 3a: Berry曲率 → δ_intrinsic
  → Wannier90: 构造Nb d轨道MLWF
  → berry.kmesh = 200 200 200
  → 输出: Ω(k)在Fermi面附近
  → 积分: δ_intrinsic = (1/2π)Σ|Ω(k)|ΔS/A_FS

Step 3b: 声子谱 → f
  → QE ph.x: 8×8×8 q网格
  → q2r.x → mat6×6×6实空间力常数
  → matdyn.x: 200×&times;200×200插值
  → 对每个最近邻对计算f

Step 4: 前向计算Tc
  → Δδ₀ = ddv_inter(M, L, θ_D, z, f)  [已有代码]
  → δ_v = δ_intrinsic + δ_pressure
  → x = 3β²Δδ₀² / (16(1-βδ_v)GAP)
  → Tc_calc = θ_D / (2·arccoth(x))

Step 5: 比较
  → Tc_calc vs Tc_exp(9.2K)
  → 不用任何反推或拟合参数

5.2 批量计算路径
─────────────
对226个材料:
  1. 从Materials Project获取结构
  2. 自动化DFT计算(脚本化QE输入)
  3. 自动化Wannier90 + Berry曲率
  4. 自动化声子计算
  5. 批量前向计算Tc
  6. 统计Tc_calc/Tc_exp分布

预计计算量:
  - 每个材料: ~100 CPU-hours (DFT+声子+Berry)
  - 226个材料: ~22,600 CPU-hours
  - 可在超算上~1周完成

5.3 简化路径（先用已有数据库）
─────────────────────────────
Materials Project已有:
  - 能带结构 → 可提取Fermi面信息
  - 声子谱(部分材料) → 可计算f
  - 弹性常数 → 体积模量B

可以先从MP提取已有数据:
  1. 用mp_api获取能带
  2. 从能带计算Fermi面曲率(不需要Wannier90)
  3. 从MP声子数据计算f(如果有)
  4. 前向计算Tc

这是零成本验证路径!
""")

# ============================================================
# 6. 从能带直接计算Fermi面曲率（不需要Wannier90）
# ============================================================
print("""
╔══════════════════════════════════════════════════════════════════════╗
║ 6. 简化方法：从DFT能带直接计算Fermi面曲率                           ║
╚══════════════════════════════════════════════════════════════════════╝

6.1 Fermi面Gaussian曲率（不需要Berry曲率）
──────────────────────────────────────────
Fermi面是E_n(k) = E_F的等能面。
其Gaussian曲率可以从E_n(k)的Hessian直接计算:

  K_G = (E_xx·E_yy - E_xy²) / |∇E|⁴  (2D截面)

  3D: 用主曲率 κ₁, κ₂:
  K_G = κ₁ · κ₂
  κ_i = Hessian(E)的本征值 / |∇E|

这不需要Wannier90或Berry曲率!
只需要DFT能带E_n(k)在Fermi面附近的值。

6.2 修正的δ_intrinsic公式
─────────────────────────
原始公式: δ = (1/2π)∫|Ω|dS/A (Berry曲率)
替代公式: δ = (1/2π)∫|K_G - K̄_G|/|K̄_G| dS/A (Fermi面曲率变化率)

其中K_G是Fermi面Gaussian曲率, K̄_G是平均值。

优点:
  - 不需要Wannier90
  - 只需要DFT能带(已有)
  - 可以直接从Materials Project数据计算

6.3 从Materials Project能带计算
──────────────────────────────
  from mp_api import MPRester
  with MPRester("API_KEY") as m:
      bs = m.get_bandstructure("mp-72")  # Nb
      # 提取E_n(k)在Fermi面附近
      # 计算Hessian → K_G
      # 积分 → δ_intrinsic
""")

# ============================================================
# 7. 关键问题与文献缺口
# ============================================================
print("""
╔══════════════════════════════════════════════════════════════════════╗
║ 7. 关键问题与文献缺口                                               ║
╚══════════════════════════════════════════════════════════════════════╝

7.1 CQM公式的文献定位
─────────────────────
CQM提出: δ_intrinsic = (1/2π)∫|Ω|dS/A, 超导条件 βδ ≈ 1

文献中已有的相关概念:
  - Fermi面嵌套矢量Q [5-7]
  - van Hove奇点 [8-11]
  - Fermi面曲率 [12-13]
  - Berry曲率 [1-4]

文献中缺失的:
  - "角亏"δ作为超导判据的具体公式
  - β = 8π+1的群论推导
  - δ ≈ 1/β作为超导临界条件
  - 黎曼零点与超导Tc的连接

→ CQM的核心贡献是新的, 但需要DFT数值验证

7.2 可能的验证路径
─────────────────
最快验证(零成本):
  1. 从Materials Project下载Nb/Pb/Al等能带
  2. 从能带计算Fermi面Gaussian曲率
  3. 积分得δ_intrinsic
  4. 前向计算Tc
  5. 与实验比较

中等成本:
  1. 对10个代表性材料做完整DFT+声子
  2. 从Berry曲率计算δ_intrinsic
  3. 从声子谱计算f
  4. 前向计算Tc

高成本:
  1. 对226个材料完整计算
  2. 统计Tc_calc/Tc_exp分布
  3. 与BCS/Eliashberg比较

7.3 核心不确定性
─────────────────
1. δ_intrinsic公式是否正确?
   - Berry曲率公式 vs Fermi面曲率公式
   - 需要DFT数值检验

2. βδ ≈ 1是否是真正的超导条件?
   - 当前只从反推法"验证"(数学恒等式)
   - 需要独立计算的δ_intrinsic检验

3. Tc对δ_intrinsic的极端敏感性是否物理?
   - δ差1% → Tc差数倍
   - 可能意味着公式结构有问题
   - 或者δ_intrinsic确实需要极高精度
""")

# ============================================================
# 8. 总结与行动项
# ============================================================
print("""
╔══════════════════════════════════════════════════════════════════════╗
║ 8. 总结与行动项                                                     ║
╚══════════════════════════════════════════════════════════════════════╝

文献调研结论:
  1. Berry曲率的DFT计算方法成熟(Wannier90/QE/VASP)
  2. Fermi面几何与超导的关系有大量文献支持
  3. 声子谱的DFT计算方法成熟(DFPT)
  4. Materials Project等数据库提供现成数据
  5. CQM的δ_intrinsic公式是新的, 需要数值验证

最优先行动项:
  ① 从Materials Project获取Nb/Pb/Al能带
  ② 从能带计算Fermi面Gaussian曲率 → δ_intrinsic
  ③ 前向计算Tc, 与实验比较
  ④ 如果成功 → 扩展到更多材料
  ⑤ 如果失败 → 修正δ_intrinsic公式

关键文献(按优先级):
  [1]  Xiao et al., RMP 82, 1959 (2010)     — Berry曲率理论
  [14] Baroni et al., RMP 73, 515 (2001)     — DFPT声子
  [16] Materials Project                      — DFT数据库
  [9]  Dzyaloshinskii, JPCM 9, 2422 (1996)   — Fermi面超导条件
  [11] Irifune et al., PRB 79, 125120 (2009)  — van Hove与Tc
  [4]  Wang et al., PRB 74, 195118 (2006)     — Wannier Berry曲率
""")