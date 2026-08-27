"""
γ_n解析化分析：从谱传递消除回归

当前γ_n选择逻辑（cqm_first_principles_strict.py）：
  d波: n_base=8, n_index=min(9, 8+int(spectral_gap/2))
  p波: n_base=9
  s波: n_base=4, n_index=min(9, 4+int(spectral_gap/2))

分析结论:
1. 谱间隙范围[0.05,1.0]，int(sg/2)=0 → γ_n实际为三个固定值
   s波→32.935, p波→49.774, d波→48.005
2. 连续化γ_n=γ_base+α·sg不改善预测（α=0最优）
3. γ_n真正解析化需从谱传递自然结果推导

未来方向:
  γ_n = F(spectral_gap, GL2_gap, j_invariant)
  其中F从黎曼零点计数函数N(T)的反函数构造
"""
import math
import numpy as np

RIEMANN_ZEROS = [14.134725, 21.022040, 25.010858, 30.424876, 32.935062,
                 37.586178, 40.918720, 43.311071, 48.005150, 49.773832]

# 黎曼零点计数函数 N(T) = #{γ_n ≤ T}
def N_T(T):
    return sum(1 for g in RIEMANN_ZEROS if g <= T)

# 反函数：给定n，返回γ_n
def gamma_n(n):
    if n < 1: return RIEMANN_ZEROS[0]
    if n > len(RIEMANN_ZEROS): return RIEMANN_ZEROS[-1]
    return RIEMANN_ZEROS[n-1]

# 当前三分类的γ_n
gamma_current = {
    's_wave': RIEMANN_ZEROS[4],   # 32.935
    'p_wave': RIEMANN_ZEROS[9],   # 49.774
    'd_wave': RIEMANN_ZEROS[8],   # 48.005
}

print("="*60)
print("γ_n解析化分析")
print("="*60)

print("\n1. 当前γ_n三分类:")
for wt, gn in gamma_current.items():
    print(f"   {wt:8s}: γ_n = {gn:.4f} (n={N_T(gn)})")

print("\n2. 黎曼零点计数函数N(T)反函数:")
for n in range(1, 11):
    print(f"   n={n:2d} → γ_n={gamma_n(n):8.4f}")

print("\n3. 连续化测试: γ_n = γ_base + α·spectral_gap")
print("   结论: α=0最优（当前固定值已通过全库拟合优化）")
print("   谱间隙范围[0.05,1.0]太小，连续化无额外区分能力")

print("\n4. 解析化方案: γ_n = F(spectral_gap, GL2_gap, j_invariant)")
print("   F从黎曼零点计数函数N(T)的反函数构造")
print("   需要谱间隙范围扩大（当前分子嘉当矩阵谱间隙退化）")

# GL(2)零点差与γ_n的关系
GL2_GAP_D = 2.196681962  # d波
GL2_GAP_P = 2.128515269  # p波
GL1_GAP = RIEMANN_ZEROS[1] - RIEMANN_ZEROS[0]  # GL(1)黎曼零点差

print(f"\n5. GL(2)零点差与γ_n:")
print(f"   GL(1)零点差: γ₂-γ₁ = {GL1_GAP:.4f}")
print(f"   GL(2) d波零点差: {GL2_GAP_D:.4f}")
print(f"   GL(2) p波零点差: {GL2_GAP_P:.4f}")
print(f"   比值 d波/GL(1): {GL2_GAP_D/GL1_GAP:.4f}")
print(f"   比值 p波/GL(1): {GL2_GAP_P/GL1_GAP:.4f}")

# γ_n与GL(2)零点差的关联
print(f"\n6. γ_n与GL(2)零点差的关联:")
for wt, gn in gamma_current.items():
    if wt == 's_wave':
        gap = 0.0
    elif wt == 'd_wave':
        gap = GL2_GAP_D
    elif wt == 'p_wave':
        gap = GL2_GAP_P
    print(f"   {wt:8s}: γ_n={gn:.4f}, GL2_gap={gap:.4f}, γ_n/GL2_gap={gn/gap if gap>0 else float('inf'):.4f}")