# CQM 超导计算框架

## 架构

```
cqm_framework/
├── constants.py          # 物理常数与CQM理论常数
├── lattice.py            # 晶格结构 → Regge角亏计算
├── free_energy.py        # 可计算自由能 F_n(T) 模型 [核心]
├── tc_estimator.py       # Tc估算器（多方法集成）
├── pipeline.py           # 完整流水线
├── validate.py           # 全量验证与报告
├── framework_report.json # 验证报告
└── materials/
    └── known_sc.py       # 已知超导体数据库
```

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
from pipeline import CQMPipeline
from free_energy import MaterialParameters

pipe = CQMPipeline()
params = MaterialParameters(theta_D=275, lambda_epc=0.98, delta_v=0.01, delta_delta_0=0.15)
result = pipe.run("Nb", params, tc_experimental=9.25)
print(result.classification)
```

## 验证结果（68条已知超导体）

| 关联 | 系数 | 意义 |
|:-----|:-----|:-----|
| r(δ_v, Tc) | +0.901 | 角亏与Tc高度正相关 |
| r(Δδ_0, Tc) | +0.841 | 涨落与Tc正相关 |
| r(θ_D, Tc) | -0.164 | 声子频率弱相关 |
| r(λ, Tc) | -0.042 | 电声耦合弱相关 |

## 已知限制

1. 自由能交叉Tc偏高，需校准凝聚能/熵的相对权重
2. 化合物德拜温度取元素近似值，需DFT精确计算
3. 角亏从家族特征估算，有3D坐标时可精确计算