# -*- coding: utf-8 -*-
"""
稳定固有时流速同步 = 相变：Kuramoto 型序参量 R 随耦合强度的同步转变（可复核）
==================================================================================

对照骨架（06 超导 §11.6.1 的 Kuramoto 型共振传播、CNST §5 相变=同步再锁定）：
  - 节点 i 的亏角涨落相位 theta_i（Delta eps_i(t) 的相位）
  - 序参量 R = |(1/N) sum exp(i theta_i)| : R~0 相位无序, R~1 相位锁定(稳定同步)
  - 耦合 K ~ 亏角涨落相位关联长度 / 低温程度（Delta eps 小、热噪声弱 => K 大）
  - 相变: K 过临界值 K_c 后 R 从无序升到有序锁定（稳定同步 = 相变）

外部对照（Kuramoto 标准模型，仅对照不引入作 CQM 结论）。
边界: K 的 CQM 微观定义(相位关联长度/Delta eps 定量关系)未建立(骨架 §686 定性);
      K_c 与 T_c 的定量映射待推; 和乐相位与流速涨落关系未建立; G10/G19 未闭合。
"""
import sys
import numpy as np
sys.stdout.reconfigure(encoding="utf-8")

rng = np.random.default_rng(20261117)
N = 64  # 节点数


def kuramoto_R(K, omega_spread=1.0, steps=8000, dt=0.01):
    """Kuramoto 平均场: dtheta_i = omega_i + (K/N) sum_j sin(theta_j - theta_i)"""
    omega = rng.normal(0, omega_spread, N)
    theta = rng.uniform(0, 2 * np.pi, N)
    for _ in range(steps):
        d = theta[None, :] - theta[:, None]
        coupling = (K / N) * np.sin(d).sum(axis=1)
        theta = np.mod(theta + dt * (omega + coupling), 2 * np.pi)
    return float(np.abs(np.exp(1j * theta).mean()))


def main():
    Ks = np.linspace(0, 3, 16)
    Rs = [kuramoto_R(K) for K in Ks]
    print("=" * 68)
    print("[Kuramoto 序参量 R vs 耦合 K]  K ~ 相位关联长度/低温程度")
    print("  R~0: 相位无序(流速仅几率性瞬时相等); R~1: 相位锁定(稳定同步=相变)")
    for K, R in zip(Ks, Rs):
        print(f"  K={K:4.2f}: R={R:.3f} {'#' * int(R * 40)}")
    Kc = None
    for i in range(len(Rs)):
        if Rs[i] > 0.5 and all(r > 0.4 for r in Rs[i:]):
            Kc = Ks[i]; break
    print(f"\n  相变临界 K_c ≈ {Kc} (R 首次持续 >0.5)")
    print("  有限 N=64 转变渐进; 热力学极限 N->inf 才尖锐(Kuramoto 标准结果)")
    print("\n" + "=" * 68)
    print("对应骨架: K 增大(相位关联/低温) => 锚点出现(T=T_c) => 锚点锁定稳定平台(T<T_c)")
    print("  = 稳定固有时流速同步 = 相变; 热噪声破坏相位关联 => 同步瓦解(§686/§807)为逆过程。")
    print("边界: Kuramoto 外部对照; K 微观定义/K_c-T_c 映射待推; 和乐相位关系未建立; G10/G19 未闭合。")


if __name__ == "__main__":
    main()
