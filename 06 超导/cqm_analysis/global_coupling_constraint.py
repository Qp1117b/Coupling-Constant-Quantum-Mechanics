# -*- coding: utf-8 -*-
"""
全局耦合约束: u_G 与每个节点固有时流速都不对易 + U(1)//Z_n 群论（可复核）
==========================================================================

用户要求: 全局耦合常数是全局节点约束(与群论有关, U(1)耦合常数涨落/子群涨落),
          必须保证它与【每一个节点】的固有时流速不对易。

权威口径:
  - 单节点胚 [u_i, p_u,j]=i δ_ij, p_u,i=v_tau,i/☯ (04前沿 §6.3, 构造假设待E4)
  - 全局 u_G=(1/N) sum u_i (对数耦合的几何平均)
  - DNR: [u_G, sum v_tau]=i☯; 逐节点下界按 1/sqrt(N) 减弱, 集体不衰减(§6.3 line120/307)
  - 群论: U(1)//Z_n 商群(n偶, 泡利统计), n=2 α->4α, Δu_2=ln4 (规范重组文档 line49)

代数推导(纯代数恒等式, 仅用对易子线性性, 无需数值表示):
  [u_G, v_tau,j] = (☯/N) sum_k [u_k, p_u,j] = i☯/N  (∀j, 仅k=j项非零)
  sum_j [u_G, v_tau,j] = i☯  (回到 DNR)
  N=1 退化为 [u,p_u]=i☯ (框架既有单节点口径)

群论意义: u_G 是全局 U(1) 耦合涨落生成元; 它与每个局域 v_tau,j 不对易 =>
  全局约束不能约化为局域量, 每个节点都"感知"全局耦合涨落。
  U(1)//Z_n 子群涨落 Δu_n=2ln n 是 u_G 谱上的跃迁; n=2 库珀对。

边界(如实): DNR 是【构造假设待E4】; u_G/u_i 正则共轭、不能从 v_tau 取对数得 α。
"""
import math
import sympy as sp

XIS_VAL = 0.02309570897  # README 权威值

def main():
    N, XI = sp.symbols('N Xi', positive=True)
    per_node = sp.I * XI / N
    collective = sp.simplify(N * per_node)

    print("=" * 68)
    print("[代数] 单节点胚 [u_i,p_j]=i d_ij; v_j=Xi p_j; u_G=(1/N)sum u_k")
    print("  [u_G, v_j] = (Xi/N) sum_k [u_k,p_j] = i Xi/N   (每个节点 j 非零)")
    print("  sum_j [u_G,v_j] =", collective, "= i Xi  <- 回到 DNR")
    print("  N=1 ->", sp.simplify(per_node.subs(N,1)), "(框架既有单节点口径)")
    print()
    print("  逐节点对易子 i Xi/N; 不确定下界 Delta u_G Delta v_j >= Xi/(2N)")
    print("  集体下界 Delta u_G Delta(sum v) >= Xi/2 (N-independent)")
    print()
    print("  N      逐节点系数 (Xi/N)   逐节点下界 Xi/(2N)")
    for NV in (1, 2, 4, 10, 100):
        print("  %3d      %.6f            %.6f" % (NV, 1.0/NV, XIS_VAL/(2*NV)))

    print("\n" + "=" * 68)
    print("[群论] U(1)//Z_n 子群涨落 (全局U(1)耦合常数谱上的跃迁):")
    for n in (2, 4, 6):
        print("  n=%d: du_n=2ln n=%.4f, alpha->%d*alpha (Z_%d商, n偶)" %
              (n, math.log(n*n), n*n, n))
    print()
    print("=" * 68)
    print("结论: u_G 与每个节点 v_tau,j 都不对易(i Xi/N), 求和回 DNR(i Xi);")
    print("  逐节点 1/N 减弱(下界 1/sqrt N), 集体不衰减 = 全局 U(1) 约束")
    print("  与每个局域流速生成元不对易; U(1)//Z_n 是 u_G 谱上的子群跃迁。")
    print("边界: DNR 构造假设待E4; u=ln g 与 p_u=v_tau/Xi 共轭, 不从 v_tau 取对数得 alpha。")

if __name__ == "__main__":
    main()
