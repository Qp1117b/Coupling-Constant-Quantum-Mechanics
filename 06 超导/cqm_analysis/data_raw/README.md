# cqm_analysis 数据与脚本资产清单

> 这些是**可复用资产**，供 CQM 超导第一性计算循环反复使用，不要删除。

## 数据

| 文件 | 内容 | 来源 |
|:---|:---|:---|
| `3DSC_MP.csv` | 5773 条超导材料：化学式、Tc、空间群、晶系、晶格常数 a/b/c、晶胞体积、nsites、密度、形成能、元素组成、structure id | 3DSC, Nature Sci Data 2023, doi:10.1038/s41597-023-02721-y, CC BY 4.0 |
| `cifs/*.cif` | 按需下载的晶体结构文件（含原子分数坐标+对称操作），用于配位几何/键角/亏角计算 | aimat-lab/3DSC GitHub, raw CIF |

## 脚本（可复用工具）

| 脚本 | 用途 | 用法 |
|:---|:---|:---|
| `../first_principles_tc.py` | 第一性端到端标度律 $T_c\propto\sqrt{F_{\rm struct}}$（θ_D 消去，零材料拟合参数） | `python ../first_principles_tc.py` |
| `../same_structure_analysis.py` | 同结构不同 Tc 分析（证伪结构决定论，中位 2.12×） | `python ../same_structure_analysis.py` |
| `../download_cifs.py` | 按需下载 CIF，断点续传 | `python ../download_cifs.py --class Cuprate --max 20` / `--ids mp-xxx` / `--all` |
| `../lattice_regge_model.py` | 一般 3D 晶格几何剖分建模：Delaunay 四面体化→二面角→亏角→cot 权重拉普拉斯（＝Regge 二阶变分矩阵／图拉普拉斯），验证对称/零行和/半正定/单一零模 | `python ../lattice_regge_model.py`（含 BCC-Nb/FCC-Al/HCP-Tc）|
| `../vtau_coupling_chain.py` | 声子→亏角→参考标定固有时流速→DNR→全局耦合常数关系链：验证参考点 v_tau=1、A12=0、C_ij 反对称、alpha→n²alpha 跃迁 | `python ../vtau_coupling_chain.py`（含 BCC-Nb/FCC-Al/HCP-Tc）|
| `../chain_1d_flow.py` | 一维开链固有时流速序列：参考节点 v_o（变量），沿相邻节点用边亏角(曲率载体)经 LQG 接口 v=√(1-y/2π) **乘积关系**（非加和）递推，验证比值关系/无阻挫 | `python ../chain_1d_flow.py`（含 BCC-Nb/FCC-Al）|
| `../global_coupling_constraint.py` | 全局耦合约束的代数验证：u_G 与每个节点流速都不对易 [u_G,v_j]=i☯/N、附加假设下求和得 i☯、U(1)//Z_n 子群跃迁 | `python ../global_coupling_constraint.py` |
| `../ring_1d_flow.py` | 一维闭环节点链：首尾相接节点环 + 乘积递推 v_(k+1)=v_k√(1-ε/2π)，绕环 v_o'=prod(r)·v_o，反馈约束 prod r=1 自然推出 | `python ../ring_1d_flow.py` |
| `../flow_sync_probability.py` | 节点固有时流速相等(某时刻所有 v 相等)的几率：v 单调⇒相等⇔各亏角涨落相等；几率随涨落幅度减小(低温)升高 | `python ../flow_sync_probability.py` |
| `../sync_phase_transition.py` | 稳定固有时流速同步=相变：Kuramoto 型序参量 R 随耦合从无序→锁定，临界 K_c≈1.8（外部对照模型） | `python ../sync_phase_transition.py` |

## 复用场景

- 研究"同结构不同掺杂→Tc"：`cifs/` 已含 mp-22719 之外的 mp-1198030(B/C 掺杂)、mp-510668(As/F 掺杂)、mp-1229011(Ag/Se/Sn 掺杂)全系列；
- 计算配位多面体几何：用 pymatgen `Structure.from_file(cif)` → `get_neighbors` → 键角/立体角；
- 扩大样本：`download_cifs.py --all`（约 5773 个，较慢）或按类别筛选。

> 注：曾尝试的"键角方差直接当内禀亏角代理"方法无效（各类无区分度，因理想八面体本身含 90°/180° 角），该方法脚本已删除；但原始 CIF 数据保留，可用于正确的球面亏角/CSM 畸变计算。
