# -*- coding: utf-8 -*-
"""
Lin-5: weight normalization for high modes (structural, NOT closing status).
CQM 12.A3: Phi_n/Phi_2 = 1/k for n=2k. ALL modes -> sum 1/k DIVERGES.
Finite participation ratio n_eff (Lin-21) -> finite K -> w_k=(1/k)/H_K.
Experiment Ge PRX2024: charge-2e dominant (low T), 4e/6e weaker (higher T).
Panels: A harmonic series divergence; B normalized weights for K=3,5,10;
C first-mode weight vs K; D system-size/participation bound.
"""
import csv, math, os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_PNG = os.path.join(HERE, "临5_权重归一与发散.png")
OUT_CSV = os.path.join(HERE, "临5_权重归一与发散.csv")

def H(K): return sum(1.0 / j for j in range(1, K + 1))

def main():
    rows = []
    print("Lin-5: high-mode weight normalization (structural)")
    print("A harmonic series H_K = sum_{k=1}^K 1/k (diverges as ln K)")
    Ks = [1, 2, 3, 5, 10, 100, 1000, 10000]
    for K in Ks:
        hk = H(K)
        print(f"  K={K:>6}: H_K={hk:.4f}  (ln K={math.log(K) if K>0 else 0:.4f})")
        rows.append(("harmonic", K, hk, math.log(K) if K > 0 else 0))
    print("  => H_K unbounded -> cannot normalize over infinite modes -> finite K required")

    # B normalized weights
    print("\nB normalized weights w_k=(1/k)/H_K:")
    for K in (3, 5, 10):
        hk = H(K)
        ws = [1.0 / k / hk for k in range(1, K + 1)]
        print(f"  K={K}: w_1={ws[0]:.4f}, sum={sum(ws):.6f}, weights={[round(w,3) for w in ws]}")
        for k, w in enumerate(ws, 1):
            rows.append(("weights", K, k, w))

    # C first-mode dominance
    print("\nC first-mode weight w_1 = 1/H_K decreases with K:")
    K_range = np.arange(1, 51)
    w1s = [1.0 / H(int(K)) for K in K_range]
    for K in (3, 5, 10, 50):
        print(f"  K={K}: w_1={1.0/H(K):.4f} (higher modes total {1-1.0/H(K):.4f})")
    for K, w in zip(K_range, w1s):
        rows.append(("w1", K, w, 0))

    # D experiment: charge-2e/4e/6e (Ge PRX2024) -- qualitative weight ordering
    print("\nD experiment (Ge PRX2024, CsV3Sb5): 2e dominant at low T; 4e,6e appear at higher T")
    print("  => w(n=2) > w(n=4) > w(n=6): consistent with 1/k decreasing (k=n/2)")
    for n in (2, 4, 6):
        k = n // 2
        w = (1.0 / k) / H(3)
        print(f"  n={n} (k={k}): model weight {w:.3f}")
        rows.append(("exp_weight", n, w, 0))

    with open(OUT_CSV, "w", newline="", encoding="utf-8-sig") as fh:
        wr = csv.writer(fh); wr.writerow(["kind", "x", "y", "z"])
        wr.writerows(rows)

    fig, ax = plt.subplots(2, 2, figsize=(13.4, 9.6))
    # A divergence
    Kp = np.arange(1, 2001)
    ax[0, 0].plot(Kp, [H(int(K)) for K in Kp], lw=2.2, color="tab:red", label=r"$H_K$")
    ax[0, 0].plot(Kp, np.log(Kp), "--", lw=1.4, color="gray", label=r"$\ln K$")
    ax[0, 0].set_xlabel("K (number of modes)"); ax[0, 0].set_ylabel(r"$\sum 1/k$")
    ax[0, 0].set_title("A  harmonic divergence -> finite cutoff required")
    ax[0, 0].legend(fontsize=8); ax[0, 0].grid(alpha=0.3)

    # B normalized weights
    for K, color in ((3, "tab:blue"), (5, "tab:orange"), (10, "tab:green")):
        ks = np.arange(1, K + 1)
        ax[0, 1].bar(ks + (0.15 if K==3 else (-0.15 if K==5 else 0)), [1.0/k/H(K) for k in ks],
                     width=0.28, alpha=0.7, label=f"K={K}")
    ax[0, 1].set_xlabel("k (mode index, n=2k)"); ax[0, 1].set_ylabel(r"$w_k$")
    ax[0, 1].set_title("B  normalized weights (sum=1)"); ax[0, 1].legend(fontsize=8)
    ax[0, 1].grid(alpha=0.3, axis="y")

    # C first-mode dominance
    ax[1, 0].plot(K_range, w1s, "o-", lw=2, color="tab:purple", ms=4)
    ax[1, 0].set_xlabel("K"); ax[1, 0].set_ylabel(r"$w_1=1/H_K$")
    ax[1, 0].set_title("C  first-mode dominance decreases with K")
    ax[1, 0].grid(alpha=0.3)

    # D experiment weight ordering
    ns = [2, 4, 6]
    ax[1, 1].bar([f"n={n}" for n in ns], [(1.0/(n//2))/H(3) for n in ns],
                 color=["tab:blue", "tab:orange", "tab:green"], alpha=0.85)
    ax[1, 1].set_ylabel("model weight (relative)")
    ax[1, 1].set_title("D  2e>4e>6e: Ge PRX2024 vs 1/k ordering")
    ax[1, 1].grid(alpha=0.3, axis="y")

    fig.tight_layout(); fig.savefig(OUT_PNG, dpi=150); plt.close(fig)
    print("\nsaved:", OUT_PNG, OUT_CSV)
    print("NOTE: Lin-5 structural ONLY; status NOT changed; n_eff material value external.")

if __name__ == "__main__":
    main()
