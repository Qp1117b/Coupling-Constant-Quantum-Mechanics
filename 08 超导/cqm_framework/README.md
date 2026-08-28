# CQM 超导计算框架

## 架构

```
cqm_framework/
├── atom_db.py # 共享原子数据库（82个元素，被41个脚本引用）
├── constants.py # 物理常数与CQM理论常数
├── cqm_pure_v7.py # CQM纯理论计算核心（v7）
└── README.md # 本文件
```

> **注**：Tc预测脚本位于 `08 超导/cqm_analysis/` 目录下（`cqm_first_principles_strict.py` 纯第一性预测）。本目录仅保留核心常数定义和纯理论计算模块。

## 自由能模型 F_n(T) [核心突破]

```
F_n(T) = E_regge(n) + E_gauge(n) + E_cond(n, T) - T · S_n(T)
```

| 分量 | 公式 | 物理来源 |
|:-----|:-----|:---------|
| 角亏能 | E_regge = θ_D·λ·δ_v²·n²/(2π)² | Regge作用量 → Ricci曲率 |
| 规范场能 | E_gauge = θ_D·(n-1)²/(4π²) | U(1)动量量子化 k=2πn/L |
| 凝聚能 | E_cond = -θ_D·λ·Δ_n²/(2·V_n) | 序参量凝聚 |
| 熵 | S_n = λ·ln(n)·(1+1/2n²)·coth(θ_D/2T) | Z_n简并 × Bose统计 |

**Tc由自由能交叉决定**: F_{n1}(Tc) = F_{n2}(Tc) → 数值求解

## Tc估算方法

| 方法 | 适用 | 公式 |
|:-----|:-----|:-----|
| free_energy_cross | CQM核心 | F_n1(Tc)=F_n2(Tc) |
| bcs_cqm | BCS-CQM修正 | Tc=ℏΩ₀/(2kB·arctanh[y²]) |
| mcmillan | 常规强耦合 | Tc=(ω_log/1.2)·exp[...] |
| allen_dynes | 强耦合修正 | McMillan × f1 × f2 |

## 流水线

```
材料结构 → 角亏δ_v → 自由能F_n(T) → Tc求解 → 超导分类 → 报告
```

## 使用

```python
from cqm_framework.constants import *
from cqm_framework.cqm_pure_v7 import *

# 自由能计算和Tc预测见 cqm_analysis/cqm_first_principles_strict.py
```

## 验证结果（226个超导材料数据库）

| 关联 | 系数 | 意义 |
|:-----|:-----|:-----|
| r(δ_v, Tc) | +0.901 | 角亏与Tc高度正相关 |
| r(Δδ_0, Tc) | +0.841 | 涨落与Tc正相关 |
| r(θ_D, Tc) | -0.164 | 声子频率弱相关 |
| r(λ, Tc) | -0.042 | 电声耦合弱相关 |

## 已知限制

1. 自由能公式已建立纯第一性前向预测框架（LOOCV中位76.6%）
2. 化合物德拜温度取元素近似值，需DFT精确计算
3. K_0^cat含电子结构细节，纯材料参数不足，需DFT数据