import SuperconductivityChain.Basic

/-!
# 链层缺口全登记（62 条）

本文件是 Lean 侧的缺口台账镜像，**不是**证明义务的替代品：

- `audit1`–`audit15` 对应推导链 `审-1`…`审-15`；
- `lin1`–`lin26` 对应 `临-1`…`临-26`；
- `chainA`–`chainF` 对应链外 A–F；
- `m1`–`m10` 对应 M1–M10；
- `e4 / a12 / w3 / g19 / g22` 对应五个结构前提。

所有条目状态均为未闭合；`gaps_length` 只校验“没有漏登记”，
不校验任何缺口已经解决。
-/

namespace CQM.SuperconductivityChain

/-- 链层 62 个缺口编号。 -/
inductive GapId
  | audit1 | audit2 | audit3 | audit4 | audit5
  | audit6 | audit7 | audit8 | audit9 | audit10
  | audit11 | audit12 | audit13 | audit14 | audit15
  | lin1 | lin2 | lin3 | lin4 | lin5 | lin6 | lin7 | lin8 | lin9 | lin10
  | lin11 | lin12 | lin13 | lin14 | lin15 | lin16 | lin17 | lin18 | lin19 | lin20
  | lin21 | lin22 | lin23 | lin24 | lin25 | lin26
  | chainA | chainB | chainC | chainD | chainE | chainF
  | m1 | m2 | m3 | m4 | m5 | m6 | m7 | m8 | m9 | m10
  | e4 | a12 | w3 | g19 | g22
  deriving DecidableEq, Repr

/-- 一条缺口：编号、所属环（`none` 表示目标区或链外）、性质、代码短名。 -/
structure Gap where
  id : GapId
  ring : Option RingIndex
  status : GapStatus
  short : String
  deriving Repr

/-- 62 条缺口全表。`ring = none` 仅用于目标区与链外，不表示“无位置”。 -/
def gaps : List Gap :=
  [ ⟨.audit1, some .r6, .structural, "H_to_C"⟩,
    ⟨.audit2, some .r9, .missingDefinition, "kappa_f"⟩,
    ⟨.audit3, some .r9, .missingDefinition, "sigma_sq"⟩,
    ⟨.audit4, some .r15, .structural, "p_loop_vs_p_pair"⟩,
    ⟨.audit5, some .r18, .structural, "two_upper_bounds"⟩,
    ⟨.audit6, some .r17, .structural, "p_pair_T_vs_p_t"⟩,
    ⟨.audit7, some .r11, .structural, "three_twos"⟩,
    ⟨.audit8, some .r22, .structural, "anchor_slope_only"⟩,
    ⟨.audit9, some .r14, .structural, "uniform_c_ij"⟩,
    ⟨.audit10, some .r4, .structural, "T_cutoff"⟩,
    ⟨.audit11, some .r19, .structural, "free_energy"⟩,
    ⟨.audit12, some .r22, .structural, "local_anchor_global_perc"⟩,
    ⟨.audit13, some .r5, .structural, "multi_connectivity"⟩,
    ⟨.audit14, none, .missingDefinition, "Gamma_first_principle"⟩,
    ⟨.audit15, some .r14, .structural, "log_vs_power"⟩,
    ⟨.lin1, some .r7, .missingDynamics, "epsilon_drive"⟩,
    ⟨.lin2, some .r16, .missingDefinition, "lambda_k_n"⟩,
    ⟨.lin3, some .r16, .missingDefinition, "N0_n"⟩,
    ⟨.lin4, some .r20, .structural, "limit_sufficiency"⟩,
    ⟨.lin5, some .r12, .structural, "high_mode_carrier"⟩,
    ⟨.lin6, some .r11, .structural, "n_vs_zeta"⟩,
    ⟨.lin7, some .r11, .structural, "electron_density_vs_pair_charge"⟩,
    ⟨.lin8, some .r26, .structural, "K_vs_prime_formula"⟩,
    ⟨.lin9, some .r21, .structural, "zero_ratio_irrational"⟩,
    ⟨.lin10, some .r13, .structural, "readout_equiv_circular"⟩,
    ⟨.lin11, some .r13, .structural, "sampling_self_average"⟩,
    ⟨.lin12, some .r14, .structural, "K_zero_t0"⟩,
    ⟨.lin13, some .r13, .structural, "boundary_pair_state"⟩,
    ⟨.lin14, some .r14, .structural, "frozen_prenight"⟩,
    ⟨.lin15, some .r14, .structural, "node_correspondence"⟩,
    ⟨.lin16, some .r22, .structural, "c_ij_physical"⟩,
    ⟨.lin17, some .r24, .structural, "c_ij_distribution"⟩,
    ⟨.lin18, some .r3, .missingDefinition, "d_epsilon_dP"⟩,
    ⟨.lin19, none, .missingDefinition, "Upsilon_B"⟩,
    ⟨.lin20, none, .missingDefinition, "stiffness_convergence"⟩,
    ⟨.lin21, some .r16, .missingDefinition, "n_eff_definition"⟩,
    ⟨.lin22, some .r27, .structural, "damping_unification"⟩,
    ⟨.lin23, some .r25, .structural, "total_effect_conservation"⟩,
    ⟨.lin24, some .r6, .structural, "pair_aggregate_normalization"⟩,
    ⟨.lin25, some .r17, .missingDynamics, "expansion_dynamics"⟩,
    ⟨.lin26, some .r13, .structural, "pair_operator_prime_realization"⟩,
    ⟨.chainA, none, .external, "mu_star"⟩,
    ⟨.chainB, none, .external, "electromagnetic_response"⟩,
    ⟨.chainC, none, .external, "d_wave"⟩,
    ⟨.chainD, none, .external, "band_DOS_DFT"⟩,
    ⟨.chainE, none, .external, "pseudogap"⟩,
    ⟨.chainF, none, .external, "transport"⟩,
    ⟨.m1, some .r14, .structural, "spectral_identity"⟩,
    ⟨.m2, some .r9, .structural, "pairing_channel_identity"⟩,
    ⟨.m3, some .r10, .structural, "DOS_identity"⟩,
    ⟨.m4, some .r10, .structural, "frequency_identity"⟩,
    ⟨.m5, some .r7, .missingDefinition, "f_explicit"⟩,
    ⟨.m6, some .r10, .structural, "bond_stiffness"⟩,
    ⟨.m7, some .r4, .structural, "non_gaussian_frustration"⟩,
    ⟨.m8, some .r15, .structural, "percolation_not_Tc"⟩,
    ⟨.m9, some .r22, .structural, "anchor_order_parameter"⟩,
    ⟨.m10, some .r25, .structural, "IK_mapping"⟩,
    ⟨.e4, some .r5, .structural, "DNR_algebraic_status"⟩,
    ⟨.a12, some .r8, .structural, "A12_from_Regge"⟩,
    ⟨.w3, some .r2, .missingDefinition, "L_eigenvalue_dimension"⟩,
    ⟨.g19, some .r6, .structural, "ratio_transfer_holonomy"⟩,
    ⟨.g22, some .r26, .structural, "automorphic_representation"⟩]

/-- 缺口总数严格为 62；仅校验登记完整性。 -/
theorem gaps_length : gaps.length = 62 := by
  decide

/-- 某环登记到的缺口（可能有空）。 -/
def gapsOfRing (r : RingIndex) : List GapId :=
  (gaps.filter (fun g => g.ring == some r)).map (fun g => g.id)

end CQM.SuperconductivityChain
