import Mathlib.Analysis.Calculus.Deriv.Basic
import Mathlib.Analysis.Calculus.Deriv.Comp
import Mathlib.Analysis.Calculus.Deriv.Mul
import Mathlib.Analysis.Calculus.Deriv.Pow
import Mathlib.Analysis.SpecialFunctions.Pow.Real
import Mathlib.Analysis.SpecialFunctions.Pow.Deriv
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Positivity

/-!
# 环 19：$\sigma_c$ 相界反解与 $\Phi(T)$ 形状的代数骨架（第 154 轮）

只承载链内代数、序与链式法则，不引入分布函数具体形式、不证明外部普适指数：
1. `phi_boundary`：$\Phi(p_*)=\kappa$（相界反解的恒等式）；
2. `phi_pc_zero`：$\Phi(p_c)=0$；
3. `old_calibration_contradicts_bkt`：旧定标 $\Upsilon(T_c)=0$ 与 BKT 下界矛盾；
4. `x_from_calibration`：$x(T)=x_c w_c/w(T)$；
5. `p_of_w_strictMono`：$p(y)=1-F(a/y)$ 在正半轴严格增；
6. `stiffness_split`、`G_one`：$\Upsilon(T)/\Upsilon(0)=w\Phi/\Phi_0$ 的代数；
7. `B_pos`：低温放大系数 $B>0$；
8. `G_deriv_one`：$G'(1)=1+B$（链式法则）。

无 `axiom`／`sorry`／`admit`／`native_decide`／`unsafe`。
-/

namespace CQM.PercolationStiffnessShape

noncomputable section

/-- **相界恒等式**。若 $p_*=p_c+(1-p_c)\kappa^{1/t_\Upsilon}$，则 $\Phi(p_*)=\kappa$。 -/
theorem phi_boundary {pc kap tU : ℝ} (hpc : pc < 1) (hk : 0 < kap) (ht : 0 < tU) :
    ((pc + (1 - pc) * kap ^ (tU⁻¹) - pc) / (1 - pc)) ^ tU = kap := by
  have hden : 1 - pc ≠ 0 := ne_of_gt (sub_pos.mpr hpc)
  have hq : (pc + (1 - pc) * kap ^ (tU⁻¹) - pc) / (1 - pc) = kap ^ (tU⁻¹) := by
    field_simp [hden]
    ring
  rw [hq]
  exact Real.rpow_inv_rpow (le_of_lt hk) (ne_of_gt ht)

/-- **阈值归零**。$\Phi(p_c)=0$。 -/
theorem phi_pc_zero {pc t : ℝ} (hpc : pc < 1) (ht : 0 < t) :
    ((pc - pc) / (1 - pc)) ^ t = 0 := by
  have hden : 1 - pc ≠ 0 := ne_of_gt (sub_pos.mpr hpc)
  have h : (pc - pc) / (1 - pc) = 0 := by
    field_simp [hden]
    ring
  rw [h]
  exact Real.zero_rpow (ne_of_gt ht)

/-- **旧定标与 BKT 下界矛盾**。旧口径给 $\Upsilon(T_c)=0$，BKT 给 $\Upsilon(T_c)=\frac{2}{\pi}k_BT_c>0$。 -/
theorem old_calibration_contradicts_bkt {Tc U : ℝ} (hTc : 0 < Tc)
    (hUbkt : U = (2 / Real.pi) * Tc) (hU0 : U = 0) : False := by
  have hpos : 0 < U := by
    rw [hUbkt]
    positivity
  linarith

/-- **标度传递**。$\sigma_c^2=x_cZw_c/\nu$ ⇒ $x(T)=\nu\sigma_c^2/(Zw)=x_cw_c/w$。 -/
theorem x_from_calibration {nu Z wv wc sig2 xc : ℝ}
    (hnu : nu ≠ 0) (hZ : Z ≠ 0) (hw : wv ≠ 0)
    (hsig : sig2 = xc * Z * wc / nu) :
    nu * sig2 / (Z * wv) = xc * wc / wv := by
  rw [hsig]
  field_simp [hnu, hZ, hw]

/-- **配对随 $w$ 严格增**。若 $F$ 严格增，则 $y\mapsto1-F(a/y)$ 在 $y>0$ 严格增。 -/
theorem p_of_w_strictMono {a : ℝ} (ha : 0 < a) {F : ℝ → ℝ} (hF : StrictMono F) :
    StrictMonoOn (fun y : ℝ => 1 - F (a / y)) (Set.Ioi 0) := by
  intro x hx y hy hxy
  have h1 : 1 / y < 1 / x := one_div_lt_one_div_of_lt hx hxy
  have h2 : a * (1 / y) < a * (1 / x) := mul_lt_mul_of_pos_left h1 ha
  have hdiv : a / y < a / x := by
    convert h2 using 1 <;> ring
  have hFlt := hF hdiv
  linarith

/-- **刚度读数分裂**。$\Upsilon(T)/\Upsilon(0)=w\cdot\Phi/\Phi_0$（$\Upsilon_0\ne0$）。 -/
theorem stiffness_split {U0 wv phiv phi0 : ℝ} (hU0 : U0 ≠ 0) :
    (U0 * wv * phiv) / (U0 * phi0) = wv * (phiv / phi0) := by
  field_simp [hU0]

/-- **归一化**。$G(1)=1$。 -/
theorem G_one {phi0 : ℝ} (hphi0 : phi0 ≠ 0) : (1 : ℝ) * phi0 / phi0 = 1 := by
  field_simp [hphi0]

/-- **渗流放大系数为正**。$B=t_\Upsilon h f/(p-p_c)>0$。 -/
theorem B_pos {tU h f p pc : ℝ} (ht : 0 < tU) (hh : 0 < h) (hf : 0 < f)
    (hp : pc < p) : 0 < tU * (h * f) / (p - pc) := by
  have hn : 0 < p - pc := sub_pos.mpr hp
  exact div_pos (mul_pos ht (mul_pos hh hf)) hn

/-- **低温系数（链式法则）**。设 $q(y)=\frac{(1-p_c)-F(a/y)}{1-p_c}$，
$G(y)=y\,q(y)^{t}/q(1)^{t}$，则 $G'(1)=1+t\,F'(a)\,a/((1-p_c)-F(a))$。 -/
theorem G_deriv_one {a pc t : ℝ} (hpc : pc < 1)
    {F F' : ℝ → ℝ} (hF : ∀ z, HasDerivAt F (F' z) z)
    (hFa : pc < 1 - F a) :
    HasDerivAt
      (fun y : ℝ => y * (((1 - pc) - F (a / y)) / (1 - pc)) ^ t /
        (((1 - pc) - F a) / (1 - pc)) ^ t)
      (1 + t * (F' a * a) / ((1 - pc) - F a)) 1 := by
  have hdenpos : 0 < 1 - pc := by linarith
  have hden : 1 - pc ≠ 0 := ne_of_gt hdenpos
  have hnumpos : 0 < (1 - pc) - F a := by linarith
  have hq1pos : 0 < ((1 - pc) - F a) / (1 - pc) := div_pos hnumpos hdenpos
  have hq1ne : ((1 - pc) - F a) / (1 - pc) ≠ 0 := ne_of_gt hq1pos
  have hq1ne' : ((1 - pc) - F (a / 1)) / (1 - pc) ≠ 0 := by simpa using hq1ne
  have hdiv : HasDerivAt (fun y : ℝ => a / y) (-a) 1 := by
    simpa using (hasDerivAt_const (1 : ℝ) a).div (hasDerivAt_id (1 : ℝ)) one_ne_zero
  have hFcomp : HasDerivAt (fun y : ℝ => F (a / y)) (F' a * (-a)) 1 := by
    simpa using (hF (a / 1)).comp 1 hdiv
  have hnum : HasDerivAt (fun y : ℝ => (1 - pc) - F (a / y)) (F' a * a) 1 := by
    convert (hasDerivAt_const (1 : ℝ) (1 - pc)).sub hFcomp using 1
    ring
  have hq : HasDerivAt (fun y : ℝ => ((1 - pc) - F (a / y)) / (1 - pc))
      ((F' a * a) / (1 - pc)) 1 := hnum.div_const (1 - pc)
  have hpow := hq.rpow_const (p := t) (Or.inl hq1ne')
  have hpow' : HasDerivAt (fun y : ℝ => (((1 - pc) - F (a / y)) / (1 - pc)) ^ t)
      ((F' a * a / (1 - pc)) * t *
        ((((1 - pc) - F a) / (1 - pc)) ^ t / (((1 - pc) - F a) / (1 - pc)))) 1 := by
    convert hpow using 1
    · simp only [div_one]
      rw [Real.rpow_sub hq1pos t 1, Real.rpow_one]
  have hprod := (hasDerivAt_id (1 : ℝ)).mul hpow'
  have hres := hprod.div_const ((((1 - pc) - F a) / (1 - pc)) ^ t)
  convert hres using 1
  simp only [id_eq]
  field_simp [hq1ne, hden]

end
end CQM.PercolationStiffnessShape
