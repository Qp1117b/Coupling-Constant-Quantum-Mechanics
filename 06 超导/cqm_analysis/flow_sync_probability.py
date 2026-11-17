# -*- coding: utf-8 -*-
"""节点固有时流速相等(某时刻所有 v_tau^(i) 相等)的几率（可复核）
====================================================================

同步态(字面): 所有节点固有时流速 v_tau^(i) 相等。亏角涨落 eps_i(t)=eps_i^0+Delta eps_i(t)
(Delta eps_0 声子零点涨落, 温度依赖 Delta eps(T)=Delta eps_0 sqrt(tanh(hbar Omega/2kT)), 式738)
使流速也涨落, 故流速相等是几率事件。

核心解析: v=sqrt(1-eps/2pi) 单调 => 所有 v 相等 <=> 所有 Delta eps_i 相等。

边界: 几率依赖涨落模型(正弦示例); 闭环反相抵消(和为0)≠各涨落相等, 不增加流速相等几率;
      和乐相位与流速涨落关系未建立; G10/G19 未闭合。
"""
import sys, math
import numpy as np
sys.stdout.reconfigure(encoding="utf-8")

rng = np.random.default_rng(20261117)
N = 4       # 节点数
M = 200000  # 采样时刻
eps0 = 1.0  # 背景亏角(示例)
tol = 1e-3


def v_of(deps):
    return np.sqrt(np.clip(1 - (eps0 + deps) / (2 * math.pi), 0, None))


def main():
    phi = rng.uniform(0, 2 * np.pi, N)
    t = rng.uniform(0, 2 * np.pi, M)
    print("=" * 66)
    print("[解析] v 单调 => 所有 v_tau^(i) 相等 <=> 所有 Delta eps_i(t) 相等")
    print("\n[几率 vs 涨落幅度 A] (相位独立随机, N=4, tol=1e-3):")
    for A in [0.5, 0.3, 0.1, 0.01, 0.001]:
        d = A * np.cos(t[:, None] + phi[None, :])
        V = v_of(d)
        sync = np.all(np.abs(V - V[:, :1]) < tol, axis=1)
        print(f"  A={A:6.3f}: 流速相等几率={sync.mean():.6f}")
    print("\n  A->0 (低温 Delta eps->0) => 几率->1")
    print("\n[闭环反馈] sum Delta eps=0(反相抵消)不使各 Delta eps 相等 => 不增加几率(和为0≠彼此相等)")
    print("\n" + "=" * 66)
    print("结论: 节点固有时流速相等的几率由亏角涨落幅度与相位关联决定(低温/长程关联提高);")
    print("  闭环反馈是必要条件(绕环单值), 非充分。边界: 正弦涨落模型示例; 和乐相位关系未建立; G10/G19 未闭合。")


if __name__ == "__main__":
    main()
