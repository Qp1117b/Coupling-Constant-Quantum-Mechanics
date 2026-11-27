# a_gate.ps1 —— 环 15 A 闸固化（第 174 轮建，第 185 轮起含 LockStiff）
# 用途：每次新增/修改环 15 引理后一键重放"出 olean → 只 import Spec → axioms → 类型对齐 → token 卫生"。
# 不通过（任一模块非零退出、出现 sorryAx / 自造 axiom、类型不对齐、token 命中）则 exit 1。
# 用法：pwsh -File .\a_gate.ps1   （工作目录会自动切到本脚本所在目录）
# 说明：仅覆盖环 15 的四十六模块（v12 起 Bridge 撤销、由 LockStiff 接替；v13 加 LockT；v14 加 LockThr；v15 加 LockR；v16 加 LockPhi；v17 加 LockW；v18 加 LockS；v19 加 LockWStr；v20 加 LockTStrict；v21 加 LockTChan；v22 加 LockTDom；v23 加 LockWD；v24 加 LockIbp；v25 加 LockWD2；v26 加 LockWD3；v27 加 LockWD4；v28 加 LockUnary；v29 加 LockDeficit；v30 加 LockLambda；v31 加 LockDeficitMono；v32 加 LockGapDeriv；v33 加 LockTail；v34 加 LockTailRatio；v35 加 LockSecant；v36 加 LockNearZero；v37 加 LockZeroExists；v38 加 LockZeroUnique；v39 加 LockRatioForm；v40 加 LockDeficitUb；v41 加 LockTanhTools；v42 加 LockTanhQuintic；v43 加 LockDeficitSq；v44 加 LockTanhSeptic；v45 加 LockTanhSepticUb；v46 加 LockWGapSeptic）；全目录尚未纳入，故不能据此宣称"全目录 A 闸通过"。

$ErrorActionPreference = "Continue"
$LeanExe = "D:\DevTools\.elan\toolchains\leanprover--lean4---v4.29.1\bin\lean.exe"
$Root    = "D:\WorkSpace\物理\CQMFormal\08 理论组织和形式化框架\04_Lean对接\Lean源码"
$Py      = "C:\Users\13649\AppData\Local\Doubao\User Data\sandbox_runtime\bases\fa694f517e5995233c80a9a8db5212c2\python\python.exe"

Set-Location -LiteralPath $PSScriptRoot

$lp = "$Root\.lake\build\lib\lean"
foreach ($p in Get-ChildItem -LiteralPath "$Root\.lake\packages" -Force -ErrorAction SilentlyContinue) {
    $lp += ";$($p.FullName)\.lake\build\lib\lean"
}
$env:LEAN_PATH = $lp + ";$PSScriptRoot\olean_tmp"

if (-not (Test-Path -LiteralPath ".\olean_tmp")) { New-Item -ItemType Directory -Path ".\olean_tmp" | Out-Null }

$fail = @()

# ---- 1. 出 olean（Spec 先，证明模块只 import Spec）----
$mods = @("Ring15Spec", "Ring15LockMult", "Ring15LockLayer", "Ring15LockMono", "Ring15LockCorr", "Ring15LockCorrGen", "Ring15LockCorrNear", "Ring15LockScale", "Ring15LockProbability", "Ring15LockNonlin", "Ring15LockRatio", "Ring15LockStiff", "Ring15LockT", "Ring15LockThr", "Ring15LockR", "Ring15LockPhi", "Ring15LockW", "Ring15LockS", "Ring15LockWStr", "Ring15LockTStrict", "Ring15LockTChan", "Ring15LockTDom", "Ring15LockWD", "Ring15LockIbp", "Ring15LockWD2", "Ring15LockWD3", "Ring15LockWD4", "Ring15LockUnary", "Ring15LockDeficit", "Ring15LockLambda", "Ring15LockDeficitMono", "Ring15LockGapDeriv", "Ring15LockTail", "Ring15LockTailRatio", "Ring15LockSecant", "Ring15LockNearZero", "Ring15LockZeroExists", "Ring15LockZeroUnique", "Ring15LockRatioForm", "Ring15LockDeficitUb", "Ring15LockTanhTools", "Ring15LockTanhQuintic", "Ring15LockDeficitSq", "Ring15LockTanhSeptic", "Ring15LockTanhSepticUb", "Ring15LockWGapSeptic")
foreach ($m in $mods) {
    & $LeanExe -o ".\olean_tmp\$m.olean" ".\$m.lean" > ".\_gate_compile.out" 2>&1
    if ($LASTEXITCODE -ne 0) { $fail += "compile:$m" ; Write-Output "[FAIL] compile $m"; Get-Content ".\_gate_compile.out" | Select-Object -First 25 }
    else { Write-Output "[ ok ] compile $m" }
}
if ($fail.Count -gt 0) { Write-Output "A 闸 FAIL（编译）"; exit 1 }

# ---- 2. axioms + 类型对齐 ----
$check = @(
    "import Ring15Spec",
    "import Ring15LockMult",
    "import Ring15LockLayer",
    "import Ring15LockMono",
    "import Ring15LockCorr",
    "import Ring15LockCorrGen",
    "import Ring15LockCorrNear",
    "import Ring15LockScale",
    "import Ring15LockProbability",
    "import Ring15LockNonlin",
    "import Ring15LockRatio",
    "import Ring15LockStiff",
    "import Ring15LockT",
    "import Ring15LockThr",
    "import Ring15LockR",
    "import Ring15LockPhi",
    "import Ring15LockW",
    "import Ring15LockS",
    "import Ring15LockWStr",
    "import Ring15LockTStrict",
    "import Ring15LockTChan",
    "import Ring15LockTDom",
    "import Ring15LockWD",
    "import Ring15LockIbp",
    "import Ring15LockWD2",
    "import Ring15LockWD3",
    "import Ring15LockWD4",
    "import Ring15LockUnary",
    "import Ring15LockDeficit",
    "import Ring15LockLambda",
    "import Ring15LockDeficitMono",
    "import Ring15LockGapDeriv",
    "import Ring15LockTail",
    "import Ring15LockTailRatio",
    "import Ring15LockSecant",
    "import Ring15LockNearZero",
    "import Ring15LockZeroExists",
    "import Ring15LockZeroUnique",
    "import Ring15LockRatioForm",
    "import Ring15LockDeficitUb",
    "import Ring15LockTanhTools",
    "import Ring15LockTanhQuintic",
    "import Ring15LockDeficitSq",
"import Ring15LockTanhSeptic",
"import Ring15LockTanhSepticUb",
"import Ring15LockWGapSeptic",
    "#print axioms CQM.Ring15.LockMult.targetProp",
    "#print axioms CQM.Ring15.LockMult.mLock_eq_one",
    "#print axioms CQM.Ring15.LockMult.lockMult_eq_one_iff",
    "#print axioms CQM.Ring15.LockLayer.targetPropLayer",
    "#print axioms CQM.Ring15.LockLayer.cond_eq_pLock",
    "#print axioms CQM.Ring15.LockMono.targetPropFugMono",
    "#print axioms CQM.Ring15.LockMono.targetPropSyncMono",
    "#print axioms CQM.Ring15.LockCorr.targetPropAdjCorr",
    "#print axioms CQM.Ring15.LockCorrGen.targetPropAdjCorrGen",
    "#print axioms CQM.Ring15.LockCorrNear.targetPropAdjCorrNear",
    "#print axioms CQM.Ring15.LockScale.targetPropAdjCorrScale",
    "#print axioms CQM.Ring15.LockProbability.targetPropLock",
    "#print axioms CQM.Ring15.LockProbability.rpow_m2",
    "#print axioms CQM.Ring15.LockNonlin.targetPropLockLamDeriv",
    "#print axioms CQM.Ring15.LockNonlin.targetPropLockLamAnti",
    "#print axioms CQM.Ring15.LockNonlin.targetPropLockLamExp",
    "#print axioms CQM.Ring15.LockRatio.targetPropLockRatio",
    "#print axioms CQM.Ring15.LockStiff.targetPropFugStiff",
    "#print axioms CQM.Ring15.LockStiff.targetPropFugBound",
    "#print axioms CQM.Ring15.LockStiff.targetPropUpsLower",
    "#print axioms CQM.Ring15.LockT.targetPropTEffMMono",
    "#print axioms CQM.Ring15.LockT.targetPropTEffMGeOne",
    "#check (CQM.Ring15.LockMult.targetProp : CQM.Ring15.Spec.TargetProp)",
    "#check (CQM.Ring15.LockLayer.targetPropLayer : CQM.Ring15.Spec.TargetPropLayer)",
    "#check (CQM.Ring15.LockMono.targetPropFugMono : CQM.Ring15.Spec.TargetPropFugMono)",
    "#check (CQM.Ring15.LockMono.targetPropSyncMono : CQM.Ring15.Spec.TargetPropSyncMono)",
    "#check (CQM.Ring15.LockCorr.targetPropAdjCorr : CQM.Ring15.Spec.TargetPropAdjCorr)",
    "#check (CQM.Ring15.LockCorrGen.targetPropAdjCorrGen : CQM.Ring15.Spec.TargetPropAdjCorrGen)",
    "#check (CQM.Ring15.LockCorrNear.targetPropAdjCorrNear : CQM.Ring15.Spec.TargetPropAdjCorrNear)",
    "#check (CQM.Ring15.LockScale.targetPropAdjCorrScale : CQM.Ring15.Spec.TargetPropAdjCorrScale)",
    "#check (CQM.Ring15.LockProbability.targetPropLock : CQM.Ring15.Spec.TargetPropLock)",
    "#check (CQM.Ring15.LockNonlin.targetPropLockLamDeriv : CQM.Ring15.Spec.TargetPropLockLamDeriv)",
    "#check (CQM.Ring15.LockNonlin.targetPropLockLamAnti : CQM.Ring15.Spec.TargetPropLockLamAnti)",
    "#check (CQM.Ring15.LockRatio.targetPropLockRatio : CQM.Ring15.Spec.TargetPropLockRatio)",
    "#check (CQM.Ring15.LockStiff.targetPropFugStiff : CQM.Ring15.Spec.TargetPropFugStiff)",
    "#check (CQM.Ring15.LockStiff.targetPropFugBound : CQM.Ring15.Spec.TargetPropFugBound)",
    "#check (CQM.Ring15.LockStiff.targetPropUpsLower : CQM.Ring15.Spec.TargetPropUpsLower)",
    "#check (CQM.Ring15.LockT.targetPropTEffMMono : CQM.Ring15.Spec.TargetPropTEffMMono)",
    "#check (CQM.Ring15.LockT.targetPropTEffMGeOne : CQM.Ring15.Spec.TargetPropTEffMGeOne)",
    "#print axioms CQM.Ring15.LockThr.targetPropThrLog",
    "#print axioms CQM.Ring15.LockThr.targetPropThrRpow",
    "#check (CQM.Ring15.LockThr.targetPropThrLog : CQM.Ring15.Spec.TargetPropThrLog)",
    "#check (CQM.Ring15.LockThr.targetPropThrRpow : CQM.Ring15.Spec.TargetPropThrRpow)",
    "#print axioms CQM.Ring15.LockR.targetPropROfEps",
    "#print axioms CQM.Ring15.LockR.targetPropSFail",
    "#check (CQM.Ring15.LockR.targetPropROfEps : CQM.Ring15.Spec.TargetPropROfEps)",
    "#check (CQM.Ring15.LockR.targetPropSFail : CQM.Ring15.Spec.TargetPropSFail)",
    "#print axioms CQM.Ring15.LockPhi.targetPropPhiMono",
    "#print axioms CQM.Ring15.LockPhi.targetPropPhiBktVal",
    "#print axioms CQM.Ring15.LockPhi.targetPropPhiMinEq",
    "#print axioms CQM.Ring15.LockPhi.targetPropPhiConflict",
    "#check (CQM.Ring15.LockPhi.targetPropPhiMono : CQM.Ring15.Spec.TargetPropPhiMono)",
    "#check (CQM.Ring15.LockPhi.targetPropPhiBktVal : CQM.Ring15.Spec.TargetPropPhiBktVal)",
    "#check (CQM.Ring15.LockPhi.targetPropPhiMinEq : CQM.Ring15.Spec.TargetPropPhiMinEq)",
    "#check (CQM.Ring15.LockPhi.targetPropPhiConflict : CQM.Ring15.Spec.TargetPropPhiConflict)",
    "#print axioms CQM.Ring15.LockW.targetPropWGapPos",
    "#print axioms CQM.Ring15.LockW.targetPropWGapAnti",
    "#print axioms CQM.Ring15.LockW.targetPropWGapLeOne",
    "#check (CQM.Ring15.LockW.targetPropWGapPos : CQM.Ring15.Spec.TargetPropWGapPos)",
    "#check (CQM.Ring15.LockW.targetPropWGapAnti : CQM.Ring15.Spec.TargetPropWGapAnti)",
    "#check (CQM.Ring15.LockW.targetPropWGapLeOne : CQM.Ring15.Spec.TargetPropWGapLeOne)",
    "#print axioms CQM.Ring15.LockS.targetPropSolSurj",
    "#print axioms CQM.Ring15.LockS.targetPropSolNeg",
    "#check (CQM.Ring15.LockS.targetPropSolSurj : CQM.Ring15.Spec.TargetPropSolSurj)",
    "#check (CQM.Ring15.LockS.targetPropSolNeg : CQM.Ring15.Spec.TargetPropSolNeg)",
    "#print axioms CQM.Ring15.LockWStr.targetPropWGapStrictAnti",
    "#check (CQM.Ring15.LockWStr.targetPropWGapStrictAnti : CQM.Ring15.Spec.TargetPropWGapStrictAnti)",
    "#print axioms CQM.Ring15.LockTStrict.targetPropKStrictAnti",
    "#print axioms CQM.Ring15.LockTStrict.targetPropYStrictMono",
    "#print axioms CQM.Ring15.LockTStrict.targetPropTStrictMono",
    "#check (CQM.Ring15.LockTStrict.targetPropKStrictAnti : CQM.Ring15.Spec.TargetPropKStrictAnti)",
    "#check (CQM.Ring15.LockTStrict.targetPropYStrictMono : CQM.Ring15.Spec.TargetPropYStrictMono)",
    "#check (CQM.Ring15.LockTStrict.targetPropTStrictMono : CQM.Ring15.Spec.TargetPropTStrictMono)",
    "#print axioms CQM.Ring15.LockTChan.targetPropTEffMPMono",
    "#print axioms CQM.Ring15.LockTChan.targetPropTChanSplit",
    "#check (CQM.Ring15.LockTChan.targetPropTEffMPMono : CQM.Ring15.Spec.TargetPropTEffMPMono)",
    "#check (CQM.Ring15.LockTChan.targetPropTChanSplit : CQM.Ring15.Spec.TargetPropTChanSplit)",
    "#print axioms CQM.Ring15.LockTDom.targetPropTChanDominate",
    "#print axioms CQM.Ring15.LockTDom.targetPropTChanCriterion",
    "#check (CQM.Ring15.LockTDom.targetPropTChanDominate : CQM.Ring15.Spec.TargetPropTChanDominate)",
    "#check (CQM.Ring15.LockTDom.targetPropTChanCriterion : CQM.Ring15.Spec.TargetPropTChanCriterion)",
    "#print axioms CQM.Ring15.LockWD.targetPropWGapDeriv",
    "#print axioms CQM.Ring15.LockWD.targetPropWGapDerivNeg",
    "#check (CQM.Ring15.LockWD.targetPropWGapDeriv : CQM.Ring15.Spec.TargetPropWGapDeriv)",
    "#check (CQM.Ring15.LockWD.targetPropWGapDerivNeg : CQM.Ring15.Spec.TargetPropWGapDerivNeg)",
    "#print axioms CQM.Ring15.LockIbp.targetPropWGapIbp",
    "#print axioms CQM.Ring15.LockIbp.targetPropShapeSplit",
    "#print axioms CQM.Ring15.LockIbp.targetPropShapeEnd",
    "#print axioms CQM.Ring15.LockIbp.targetPropShapeEndGt",
    "#check (CQM.Ring15.LockIbp.targetPropWGapIbp : CQM.Ring15.Spec.TargetPropWGapIbp)",
    "#check (CQM.Ring15.LockIbp.targetPropShapeSplit : CQM.Ring15.Spec.TargetPropShapeSplit)",
    "#check (CQM.Ring15.LockIbp.targetPropShapeEnd : CQM.Ring15.Spec.TargetPropShapeEnd)",
    "#check (CQM.Ring15.LockIbp.targetPropShapeEndGt : CQM.Ring15.Spec.TargetPropShapeEndGt)",
    "#print axioms CQM.Ring15.LockWD2.targetPropWGapDeriv2",
    "#print axioms CQM.Ring15.LockWD2.targetPropShapeDeriv",
    "#check (CQM.Ring15.LockWD2.targetPropWGapDeriv2 : CQM.Ring15.Spec.TargetPropWGapDeriv2)",
    "#check (CQM.Ring15.LockWD2.targetPropShapeDeriv : CQM.Ring15.Spec.TargetPropShapeDeriv)",
    "#print axioms CQM.Ring15.LockWD3.targetPropWGapDeriv2Alt",
    "#print axioms CQM.Ring15.LockWD3.targetPropWGapDeriv2Pos",
    "#print axioms CQM.Ring15.LockWD3.targetPropShapeDerivSign",
    "#check (CQM.Ring15.LockWD3.targetPropWGapDeriv2Alt : CQM.Ring15.Spec.TargetPropWGapDeriv2Alt)",
    "#check (CQM.Ring15.LockWD3.targetPropWGapDeriv2Pos : CQM.Ring15.Spec.TargetPropWGapDeriv2Pos)",
    "#check (CQM.Ring15.LockWD3.targetPropShapeDerivSign : CQM.Ring15.Spec.TargetPropShapeDerivSign)",
    "#print axioms CQM.Ring15.LockWD4.targetPropShapeSignRatio",
    "#print axioms CQM.Ring15.LockWD4.targetPropShapeNegOfRatioGeOne",
    "#check (CQM.Ring15.LockWD4.targetPropShapeSignRatio : CQM.Ring15.Spec.TargetPropShapeSignRatio)",
    "#check (CQM.Ring15.LockWD4.targetPropShapeNegOfRatioGeOne : CQM.Ring15.Spec.TargetPropShapeNegOfRatioGeOne)",
    "#print axioms CQM.Ring15.LockUnary.targetPropRatioPhiForm",
    "#print axioms CQM.Ring15.LockUnary.targetPropShapeSignUnary",
    "#check (CQM.Ring15.LockUnary.targetPropRatioPhiForm : CQM.Ring15.Spec.TargetPropRatioPhiForm)",
    "#check (CQM.Ring15.LockUnary.targetPropShapeSignUnary : CQM.Ring15.Spec.TargetPropShapeSignUnary)",
    "#print axioms CQM.Ring15.LockDeficit.targetPropRatioBracketLow",
    "#print axioms CQM.Ring15.LockDeficit.targetPropRatioBracketHigh",
    "#print axioms CQM.Ring15.LockDeficit.targetPropLambdaForm",
    "#print axioms CQM.Ring15.LockDeficit.targetPropShapeSignDeficit",
    "#check (CQM.Ring15.LockDeficit.targetPropRatioBracketLow : CQM.Ring15.Spec.TargetPropRatioBracketLow)",
    "#check (CQM.Ring15.LockDeficit.targetPropRatioBracketHigh : CQM.Ring15.Spec.TargetPropRatioBracketHigh)",
    "#check (CQM.Ring15.LockDeficit.targetPropLambdaForm : CQM.Ring15.Spec.TargetPropLambdaForm)",
    "#check (CQM.Ring15.LockDeficit.targetPropShapeSignDeficit : CQM.Ring15.Spec.TargetPropShapeSignDeficit)",
    "#print axioms CQM.Ring15.LockLambda.targetPropDeficitRatioMono",
    "#print axioms CQM.Ring15.LockLambda.targetPropLambdaStrictMono",
    "#print axioms CQM.Ring15.LockLambda.targetPropLambdaBounds",
    "#print axioms CQM.Ring15.LockDeficitMono.targetPropDeficitDeriv",
    "#print axioms CQM.Ring15.LockDeficitMono.targetPropDeficitDerivPos",
    "#print axioms CQM.Ring15.LockDeficitMono.targetPropDeficitStrictMono",
    "#print axioms CQM.Ring15.LockDeficitMono.targetPropDeficitRatioStrictMonoT",
    "#print axioms CQM.Ring15.LockGapDeriv.targetPropLambdaDeriv",
    "#print axioms CQM.Ring15.LockGapDeriv.targetPropRatioFunDeriv",
    "#print axioms CQM.Ring15.LockGapDeriv.targetPropCriterionGapDeriv",
    "#check (CQM.Ring15.LockLambda.targetPropDeficitRatioMono : CQM.Ring15.Spec.TargetPropDeficitRatioMono)",
    "#check (CQM.Ring15.LockLambda.targetPropLambdaStrictMono : CQM.Ring15.Spec.TargetPropLambdaStrictMono)",
    "#check (CQM.Ring15.LockLambda.targetPropLambdaBounds : CQM.Ring15.Spec.TargetPropLambdaBounds)",
    "#check (CQM.Ring15.LockDeficitMono.targetPropDeficitDeriv : CQM.Ring15.Spec.TargetPropDeficitDeriv)",
    "#check (CQM.Ring15.LockDeficitMono.targetPropDeficitDerivPos : CQM.Ring15.Spec.TargetPropDeficitDerivPos)",
    "#check (CQM.Ring15.LockDeficitMono.targetPropDeficitStrictMono : CQM.Ring15.Spec.TargetPropDeficitStrictMono)",
    "#check (CQM.Ring15.LockDeficitMono.targetPropDeficitRatioStrictMonoT : CQM.Ring15.Spec.TargetPropDeficitRatioStrictMonoT)"
    "#check (CQM.Ring15.LockGapDeriv.targetPropLambdaDeriv : CQM.Ring15.Spec.TargetPropLambdaDeriv)",
    "#check (CQM.Ring15.LockGapDeriv.targetPropRatioFunDeriv : CQM.Ring15.Spec.TargetPropRatioFunDeriv)",
    "#check (CQM.Ring15.LockGapDeriv.targetPropCriterionGapDeriv : CQM.Ring15.Spec.TargetPropCriterionGapDeriv)",
    "#print axioms CQM.Ring15.LockTail.targetPropSinhOneLt",
    "#print axioms CQM.Ring15.LockTail.targetPropLambdaOne",
    "#print axioms CQM.Ring15.LockTail.targetPropLambdaTailGt",
    "#check (CQM.Ring15.LockTail.targetPropSinhOneLt : CQM.Ring15.Spec.TargetPropSinhOneLt)",
    "#check (CQM.Ring15.LockTail.targetPropLambdaOne : CQM.Ring15.Spec.TargetPropLambdaOne)",
    "#check (CQM.Ring15.LockTail.targetPropLambdaTailGt : CQM.Ring15.Spec.TargetPropLambdaTailGt)"
    "#print axioms CQM.Ring15.LockTailRatio.targetPropRatioLeOfLeThird",
    "#print axioms CQM.Ring15.LockTailRatio.targetPropGapNegOfDeficitLeThird",
    "#check (CQM.Ring15.LockTailRatio.targetPropRatioLeOfLeThird : CQM.Ring15.Spec.TargetPropRatioLeOfLeThird)",
    "#check (CQM.Ring15.LockTailRatio.targetPropGapNegOfDeficitLeThird : CQM.Ring15.Spec.TargetPropGapNegOfDeficitLeThird)"
    "#print axioms CQM.Ring15.LockSecant.targetPropTanhSecant",
    "#print axioms CQM.Ring15.LockSecant.targetPropDeficitLeThird",
    "#print axioms CQM.Ring15.LockSecant.targetPropGapNegTail",
    "#check (CQM.Ring15.LockSecant.targetPropTanhSecant : CQM.Ring15.Spec.TargetPropTanhSecant)",
    "#check (CQM.Ring15.LockSecant.targetPropDeficitLeThird : CQM.Ring15.Spec.TargetPropDeficitLeThird)",
    "#check (CQM.Ring15.LockSecant.targetPropGapNegTail : CQM.Ring15.Spec.TargetPropGapNegTail)",
    "#print axioms CQM.Ring15.LockNearZero.targetPropDeficitGeSq",
    "#print axioms CQM.Ring15.LockNearZero.targetPropLambdaLeSq",
    "#print axioms CQM.Ring15.LockNearZero.targetPropGapPosNearZero",
    "#check (CQM.Ring15.LockNearZero.targetPropDeficitGeSq : CQM.Ring15.Spec.TargetPropDeficitGeSq)",
    "#check (CQM.Ring15.LockNearZero.targetPropLambdaLeSq : CQM.Ring15.Spec.TargetPropLambdaLeSq)",
    "#check (CQM.Ring15.LockNearZero.targetPropGapPosNearZero : CQM.Ring15.Spec.TargetPropGapPosNearZero)",
    "#print axioms CQM.Ring15.LockZeroExists.targetPropGapZeroExists",
    "#check (CQM.Ring15.LockZeroExists.targetPropGapZeroExists : CQM.Ring15.Spec.TargetPropGapZeroExists)",
    "#print axioms CQM.Ring15.LockZeroUnique.targetPropGapZeroUniqueOfRatioMono",
    "#check (CQM.Ring15.LockZeroUnique.targetPropGapZeroUniqueOfRatioMono : CQM.Ring15.Spec.TargetPropGapZeroUniqueOfRatioMono)",
    "#print axioms CQM.Ring15.LockRatioForm.targetPropDeficitRatioPos",
    "#print axioms CQM.Ring15.LockRatioForm.targetPropRatioOverLambdaPos",
    "#check (CQM.Ring15.LockRatioForm.targetPropDeficitRatioPos : CQM.Ring15.Spec.TargetPropDeficitRatioPos)",
    "#print axioms CQM.Ring15.LockDeficitUb.targetPropDeficitDerivAlt",
    "#print axioms CQM.Ring15.LockDeficitUb.targetPropDeficitDerivLtTwoDelta",
    "#print axioms CQM.Ring15.LockDeficitUb.targetPropDeficitDerivLtTwoThird",
    "#check (CQM.Ring15.LockDeficitUb.targetPropDeficitDerivAlt : CQM.Ring15.Spec.TargetPropDeficitDerivAlt)",
    "#check (CQM.Ring15.LockDeficitUb.targetPropDeficitDerivLtTwoDelta : CQM.Ring15.Spec.TargetPropDeficitDerivLtTwoDelta)",
    "#check (CQM.Ring15.LockDeficitUb.targetPropDeficitDerivLtTwoThird : CQM.Ring15.Spec.TargetPropDeficitDerivLtTwoThird)",
    "#check (CQM.Ring15.LockRatioForm.targetPropRatioOverLambdaPos : CQM.Ring15.Spec.TargetPropRatioOverLambdaPos)",
    "#print axioms CQM.Ring15.LockTanhTools.continuous_tanh",
    "#print axioms CQM.Ring15.LockTanhTools.cont_sechSq",
    "#print axioms CQM.Ring15.LockTanhTools.sechSq_pos",
    "#print axioms CQM.Ring15.LockTanhTools.sechSq_le_one",
    "#print axioms CQM.Ring15.LockTanhTools.tanhHasDerivAt",
    "#print axioms CQM.Ring15.LockTanhTools.sechSq_eq_one_sub_tanh_sq",
    "#print axioms CQM.Ring15.LockTanhTools.tanh_pos_of_pos",
    "#print axioms CQM.Ring15.LockTanhTools.tanhLtSelf",
    "#print axioms CQM.Ring15.LockTanhTools.targetPropTanhCubic",
    "#check (CQM.Ring15.LockTanhTools.targetPropTanhCubic : CQM.Ring15.Spec.TargetPropTanhCubic)",
    "#print axioms CQM.Ring15.LockTanhQuintic.tanhQuintic",
    "#print axioms CQM.Ring15.LockTanhQuintic.targetPropTanhQuintic",
    "#check (CQM.Ring15.LockTanhQuintic.targetPropTanhQuintic : CQM.Ring15.Spec.TargetPropTanhQuintic)",
    "#print axioms CQM.Ring15.LockDeficitSq.deficitLeThirdSubSq",
    "#print axioms CQM.Ring15.LockDeficitSq.targetPropDeficitLeThirdSubSq",
    "#check (CQM.Ring15.LockDeficitSq.targetPropDeficitLeThirdSubSq : CQM.Ring15.Spec.TargetPropDeficitLeThirdSubSq)
#print axioms CQM.Ring15.LockTanhSeptic.tanhSepticLower
#print axioms CQM.Ring15.LockTanhSeptic.targetPropTanhSepticLower
#check (CQM.Ring15.LockTanhSeptic.targetPropTanhSepticLower : CQM.Ring15.Spec.TargetPropTanhSepticLower)
#print axioms CQM.Ring15.LockTanhSepticUb.tanhSepticUpper
#print axioms CQM.Ring15.LockTanhSepticUb.targetPropTanhSeptic
#check (CQM.Ring15.LockTanhSepticUb.targetPropTanhSeptic : CQM.Ring15.Spec.TargetPropTanhSeptic)",
    "#print axioms CQM.Ring15.LockWGapSeptic.wGapLowerBound",
    "#print axioms CQM.Ring15.LockWGapSeptic.targetPropWGapUpperBound",
    "#check (CQM.Ring15.LockWGapSeptic.targetPropWGapUpperBound : CQM.Ring15.Spec.TargetPropWGapUpperBound)"
) -join "`n"
$checkFile = ".\_a_gate_check.lean"
Set-Content -LiteralPath $checkFile -Value $check -Encoding UTF8
& $LeanExe $checkFile > ".\_a_gate_out.txt" 2>&1
# 215 修：Lean 的 #print axioms 在 80 列处折行（续行以空格开头），
# 原逐行解析会把折行条目整条丢掉（静默漏检）。先把续行拼回单行。
$outRaw = ((Get-Content ".\_a_gate_out.txt") -join "`n") -replace "`n ", ""
$out = $outRaw -split "`n"
if ($LASTEXITCODE -ne 0) { $fail += "axioms-run"; Write-Output "[FAIL] axioms/type 检查执行失败"; $out }
Remove-Item -LiteralPath $checkFile -Force

$allowed = @("propext", "Classical.choice", "Quot.sound")
foreach ($line in $out) {
    $s = "$line"
    if ($s -match "depends on axioms: \[(.*)\]") {
        $names = $Matches[1] -split "," | ForEach-Object { $_.Trim() }
        $bad = $names | Where-Object { $allowed -notcontains $_ }
        if ($bad) { $fail += "axiom:$s"; Write-Output "[FAIL] 非白名单公理：$s" }
        else { Write-Output "[ ok ] axioms: $($Matches[1])" }
    }
    elseif ($s -match "^\S+ : ") { Write-Output "[ ok ] type: $s" }
    elseif ($s -match "sorryAx") { $fail += "sorryAx"; Write-Output "[FAIL] 命中 sorryAx" }
    elseif ($s -match "error") { $fail += "lean-error"; Write-Output "[FAIL] $s" }
    }

# ---- 3. token 卫生（去注释后扫描）----
$scan = @'
import pathlib, re, sys, json
root = pathlib.Path(".")
files = sorted(root.glob("*.lean"))
pat = re.compile(r"\b(sorry|admit|native_decide|unsafe|axiom)\b")
hits = []
for f in files:
    if f.name.startswith("_"):
        continue
    t = f.read_text(encoding="utf-8", errors="ignore")
    t = re.sub(r"/-.*?-/", "", t, flags=re.S)
    t = re.sub(r"--[^\n]*", "", t)
    for i, line in enumerate(t.splitlines(), 1):
        if pat.search(line):
            hits.append(f"{f.name}:{i}:{line.strip()}")
print(json.dumps({"files": len(files), "hits": hits}, ensure_ascii=False))
sys.exit(1 if hits else 0)
'@
$scanFile = ".\_a_gate_scan.py"
Set-Content -LiteralPath $scanFile -Value $scan -Encoding UTF8
& $Py $scanFile > ".\_a_gate_scan.txt" 2>&1
$scanOut = Get-Content ".\_a_gate_scan.txt"
$scanCode = $LASTEXITCODE
Remove-Item -LiteralPath $scanFile -Force
Write-Output "token: $scanOut"
if ($scanCode -ne 0) { $fail += "token" }

# ---- 汇总 ----
if ($fail.Count -gt 0) {
    Write-Output ""
    Write-Output "A 闸 FAIL（限环 15）：$($fail -join ', ')"
    exit 1
}
Write-Output ""
Write-Output "A 闸 PASS（限环 15 四十六模块 v46：编译 + axioms 白名单 + 类型对齐 + token 卫生）"
exit 0





