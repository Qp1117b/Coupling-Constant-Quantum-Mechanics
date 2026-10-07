# -*- coding: utf-8 -*-
"""
G_N 结构因果模型：敏感性 / 反事实分解（对接 DoWhy / statsmodels）。
G_N = (ℏc/m_p²)·I·λ_c·☯²·𝔠₁·exp(-2/☯)·(1+κ☯)
未安装 dowhy 时，直接运行本文件的解析弹性即可。

依赖（可选）：pip install dowhy pandas
"""
import json, os, math

TAIJI = 0.02309570897
LAM_C = 1.316022911308
I_DYN = 5/3
KAPPA = (31 + TAIJI)/30

def log_gn_factors(I, lam, taiji, c1, kappa, mp, hbarC=1.0):
    return (math.log(hbarC) - 2*math.log(mp) + math.log(I) + math.log(lam)
            + 2*math.log(taiji) + math.log(c1) - 2/taiji + math.log(1 + kappa*taiji))

def elasticities():
    return {
        "I": 1.0, "lambda_c": 1.0, "c_1": 1.0, "m_p": -2.0,
        "kappa": (KAPPA*TAIJI)/(1+KAPPA*TAIJI),
        "taiji": 2 + 2/TAIJI + (KAPPA*TAIJI)/(1+KAPPA*TAIJI),
    }

def counterfactual(taiji_new):
    """仅改 ☯，其余因子固定，返回 ln G_N 的相对变化。"""
    base = log_gn_factors(I_DYN, LAM_C, TAIJI, 1.0, KAPPA, 1.0)
    cf = log_gn_factors(I_DYN, LAM_C, taiji_new, 1.0, (31+taiji_new)/30, 1.0)
    return cf - base

if __name__ == "__main__":
    print("elasticities:", json.dumps(elasticities(), ensure_ascii=False, indent=2))
    print("dlnGN for taiji +1%:", round(counterfactual(TAIJI*1.01), 4))
    # DoWhy（若已安装）：以解析弹性作为结构假设的检验
    try:
        import dowhy  # noqa
        print("dowhy available: 可据 GN_causal_dag.json 构造 CausalModel 做识别与反驳")
    except ImportError:
        print("dowhy 未安装：pip install dowhy 后可构造识别/反驳检验")
