\\ =====================================================================
\\ CQM 工作包1：CM 椭圆曲线 L-函数非平凡零点谱的精确计算
\\ 运行环境：PARI/GP 2.17.x (可在 WSL/Debian 上通过 `apt install pari-gp` 获得)
\\ 运行方法：gp -q < 本文件
\\ 用途：为非常规 d/p 波超导的 GL(2) 零点差 gamma2^f - gamma1^f 提供
\\       权威算术精确值，替代早期文档中的启发式数值（0.367 / 0.346）。
\\ =====================================================================
default(realprecision, 40);

\\ ---- E1: y^2 = x^3 - x  (d 波配对对称，CM 由 Z[i] 实现，导子 N=32) ----
E1 = ellinit([0,0,0,-1,0]);
print("E1  y^2 = x^3 - x");
print("    导子           = ", ellconductor(E1));
print("    root number    = ", ellrootno(E1));
print("    解析秩/an 秩    = ", ellanalyticrank(E1));
print("    L(1)/Omega     = ", ellL1(E1, 0));
z1 = lfunzeros(E1, 25);
print("    前三个非平凡零点虚部 = ", z1[1], " | ", z1[2], " | ", z1[3]);
print("    gamma1^f       = ", z1[1]);
print("    gamma2^f       = ", z1[2]);
print("    DLG = gamma2^f - gamma1^f = ", z1[2] - z1[1]);
print(" ");

\\ ---- E2: y^2 = x^3 - 1  (p 波配对对称，CM 由 Z[omega] 实现，导子 N=27) ----
E2 = ellinit([0,0,0,0,-1]);
print("E2  y^2 = x^3 - 1");
print("    导子           = ", ellconductor(E2));
print("    root number    = ", ellrootno(E2));
print("    解析秩/an 秩    = ", ellanalyticrank(E2));
print("    L(1)/Omega     = ", ellL1(E2, 0));
z2 = lfunzeros(E2, 25);
print("    前三个非平凡零点虚部 = ", z2[1], " | ", z2[2], " | ", z2[3]);
print("    gamma1^f       = ", z2[1]);
print("    gamma2^f       = ", z2[2]);
print("    DLG = gamma2^f - gamma1^f = ", z2[2] - z2[1]);
print(" ");

\\ ---- 对照：GL(1) 黎曼 xi 函数零点差（用于 GL(2)/GL(1) 比值） ----
g1 = lfunzeros("zeta", 22);
print("GL(1) zeta  gamma1   = ", g1[1]);
print("GL(1) zeta  gamma2   = ", g1[2]);
print("GL(1) zeta  DLG      = ", g1[2] - g1[1]);
print("GL(1) zeta  DLG 差异对照   = ", g1[2] - g1[1], "  (文献值 6.887314497...)");
quit();