# CQM 理论动画：代码组件库规划（双轨管线 v0.1）

> **定位**：动画生产的技术规划，不是理论文档；不新增、不修改理论主张。
> **目标**：让 CQM 的每个核心意象都能用同一套组件在快轨（SVG／Three.js／Manim）与精轨（Blender／UE5）中复用，做到可编辑、可复现、可逐帧检查。
> **原则**：代码优先、单一数据源、状态感知、科学准确优先于视觉炫技。
> **v0.2 增补**：依据《全理论内容地图 v1.0》与 6:30 全理论分镜，新增 `OntologyField`、`DecoherenceFork`、`CartanLattice`、`TcCurve`、`NumberSpectrum`、`CosmologyBoundary`；P0 仍为 8 个，新增组件按 P1 起步。

---

## 1. 总体架构

```text
cqm-animation/                    # 建议独立仓库，避免污染理论仓库
├─ data/
│  ├─ claims.yaml                 # 主张—出处—状态台账
│  ├─ tokens.json                 # 颜色、字体、间距、缓动
│  └─ scenes/
│     ├─ 00_cold_open.yaml
│     ├─ 01_problem.yaml
│     └─ ...
├─ packages/
│  ├─ core/                       # 类型、schema、时间轴、状态校验
│  ├─ svg/                        # Track A：React + SVG 组件
│  ├─ three/                      # Track A：Three.js／R3F 组件
│  ├─ blender/                    # Track B：Blender Python／Geometry Nodes
│  ├─ render/                     # Remotion／Playwright／FFmpeg 渲染
│  ├─ audio/                      # TTS、音效、波形对齐
│  └─ qa/                         # 主张校验、逐帧检查、色盲模拟
├─ scenes/                        # 每个镜头的 React／Blender 场景入口
├─ prompts/                       # Claude 生成脚本、组件、字幕的提示词与版本
└─ renders/                       # 输出（不入库）
```

**单一数据源**：`claims.yaml` ＋ `scenes/*.yaml` ＋ `tokens.json`。所有轨道都从这三类文件读取，不允许在组件里硬编码主张、出处或状态。

---

## 2. 数据模型

```ts
export type ClaimStatus = "gold" | "cyan" | "amber" | "white" | "purple";
export type ClaimScope = "main" | "short" | "interactive" | "internal";

export interface Claim {
  id: string;              // C01
  text: string;            // 主张原文
  source: string;          // 文档路径
  section?: string;        // 章节
  status: ClaimStatus;     // 状态
  scope: ClaimScope;       // 主片／短片／交互／内部
  canSayProven: boolean;   // 是否允许在宣传中说“已证”
}

export interface Shot {
  id: string;              // S16
  start: number;           // 秒
  end: number;             // 秒
  act: string;
  track: "A" | "B" | "H";
  scope: ClaimScope;       // 主片／短片／交互
  components: string[];    // 组件名
  narration: string;
  captions: { zh: string; en?: string };
  formula?: string;        // 深度层公式，可空
  claimIds: string[];      // 绑定主张
}

export interface Scene {
  id: string;
  title: string;
  shots: Shot[];
}
```

**镜头 YAML 示例**：

```yaml
id: S16
start: 193
end: 208
act: "4 引力"
track: B
components: [Simplex4D, DeficitWedge, ClockField]
narration: "质量让角亏出现——不是力，而是几何的凹凸。"
captions:
  zh: "质量让角亏出现——不是力，而是几何的凹凸。"
  en: "Mass creates a deficit angle — not a force, but a dent in geometry."
formula: "\\delta_v"
claimIds: [C05]
```

---

## 3. 组件清单

| 组件 | 用途 | 关键 props／状态 | 轨道实现 | 优先级 |
|:---|:---|:---|:---|:---|
| `NodeGraph` | 节点—连线网络、生长、同步态 | `nodes`、`edges`、`growth`、`lockState`、`highlight` | SVG／R3F／Blender | P0 |
| `PhaseRing` | 相位环、锁定、脉冲 | `phase`、`locked`、`frequency`、`pulse` | SVG／R3F／Blender | P0 |
| `Simplex4D` | 4-单纯形晶格、变形、角亏 | `vertices`、`edges`、`faces`、`delta`、`deform` | Blender（主）／R3F（预演） | P0 |
| `LayerStack` | 前时空／FG／GR 层级片 | `layers`、`active`、`opacity`、`transition` | SVG／R3F／Blender | P0 |
| `StatusBadge` | 状态徽章与图例 | `status`、`label`、`position` | SVG／HTML | P0 |
| `FormulaCard` | LaTeX 公式浮层 | `latex`、`reveal`、`position` | SVG／Manim／HTML | P0 |
| `CameraRig` | 连续变焦、推拉、转场 | `keyframes`、`easing`、`target` | R3F／Blender | P0 |
| `CaptionSystem` | 双语字幕、安全区 | `zh`、`en`、`safeArea` | HTML／Blender 合成 | P0 |
| `CouplingManifold` | 耦合空间流形、坐标移动 | `points`、`trajectory`、`field`、`glyph` | R3F／Blender | P1 |
| `LightCone` | 光锥、光线偏折 | `origin`、`aperture`、`bend`、`rays` | R3F／Blender | P1 |
| `Spectrum` | 本征值谱、能级、占位 | `values`、`levels`、`occupancy` | SVG／Manim／Blender | P1 |
| `MemoryEcho` | 脉冲余迹、局部窗口 | `pulse`、`decay`、`window` | SVG／R3F | P1 |
| `PhaseLattice` | 超导相位晶格、新旧层嵌套 | `grid`、`oldLayer`、`newLayer`、`lockState` | R3F／Blender | P1 |
| `SpinNetwork` | 自旋网络彩色面片、穿行镜头 | `edges`、`faces`、`spin`、`excitation` | R3F／Blender | P1 |
| `KuramotoPhase` | 相位轮、序参量、锁定瞬间 | `phases`、`coupling`、`orderParam`、`locked` | SVG／R3F | P1 |
| `CFTVertex` | OPE 顶点、共形自举 | `operators`、`ope`、`bootstrap` | SVG／R3F | P2 |
| `LanglandsSpectrum` | 自守谱、相变弧线 | `spectrum`、`arcs`、`criticalLine` | SVG／Manim | P2 |
| `MaterialDesignerUI` | 材料设计器参数与判定流水线 | `elements`、`cartan`、`score`、`candidates` | SVG／HTML | P2 |
| `OntologyField` | 物质先在、再生产、层级非还原的抽象场 | `texture`、`repetition`、`layers`、`relationMode` | R3F／Blender | P1 |
| `DecoherenceFork` | 三类退相干、四层筛选、唯一性 | `branches`、`mechanism`、`stage`、`uniqueness` | SVG／R3F | P1 |
| `CartanLattice` | $A_4$ 嘉当矩阵、$\mathrm{SU}(5)$ 重组底图 | `matrix`、`nodes`、`recombination`、`highlight` | SVG／R3F／Blender | P1 |
| `TcCurve` | 电阻骤降、$T_c$ 曲线、赝能隙 | `temperature`、`resistance`、`tc`、`pseudogap` | SVG／Manim | P1 |
| `Braid` | 三大支柱编绳 | `strands`、`twist`、`colors` | SVG／R3F | P1 |
| `GapMap` | 缺口编号地图 | `gaps`、`positions`、`highlight` | SVG | P1 |
| `NumberSpectrum` | 黎曼零点、临界线（仅短片） | `zeros`、`criticalLine`、`highlight` | SVG／Manim | P2 |
| `CosmologyBoundary` | 反物质引力实验边界（仅短片） | `experiments`、`bounds`、`labels` | SVG | P2 |
| `CodeStream` | Lean 代码流 | `lines`、`highlight`、`speed` | SVG／HTML | P2 |

**MVP 只做 8 个 P0 组件**：`NodeGraph`、`PhaseRing`、`Simplex4D`、`LayerStack`、`StatusBadge`、`FormulaCard`、`CameraRig`、`CaptionSystem`。P1／P2 在分镜锁定后再做，避免过度工程。v0.2 的第六幕依赖 `DecoherenceFork`、`CartanLattice`、`TcCurve`，这三个 P1 应优先于其他 P1。

### 幕—组件映射

| 幕 | 主组件 | 备注 |
|:---|:---|:---|
| 1 本体论 | `OntologyField`、`LayerStack`、`NodeGraph` | 关系先于实体 |
| 2 耦合空间 | `CouplingManifold`、`PhaseRing`、`LayerStack` | 常数坐标化 |
| 3 同步 | `PhaseRing`、`Waveform`、`LayerStack` | 锁定事件 |
| 4 退相干 | `DecoherenceFork`、`LightCone`、`MemoryEcho` | 三类／四层 |
| 5 引力 | `Simplex4D`、`ClockField`、`LightCone`、`LayerStack` | 角亏／固有时 |
| 6 物质与超导 | `Spectrum`、`CartanLattice`、`PhaseLattice`、`TcCurve`、`OntologyField` | 谱／重组／$T_c$ |
| 7 方法与边界 | `Braid`、`CodeStream`、`GapMap`、`StatusBadge` | 三大支柱／Lean／缺口 |
| 8 收束 | `CosmicPullback`、`CaptionSystem` | 拉远 |

---

## 4. 视觉 tokens

```json
{
  "color": {
    "bg": "#070A12",
    "relation": "#35E0FF",
    "coupling": "#F5C542",
    "decoherence": "#FF4FD8",
    "properTime": "#8A7CFF",
    "statusGold": "#F5C542",
    "statusCyan": "#35E0FF",
    "statusAmber": "#FFB020",
    "statusWhite": "#F2F5FA",
    "statusPurple": "#B98CFF"
  },
  "font": {
    "title": "Noto Sans SC",
    "body": "Noto Sans SC",
    "latin": "Inter",
    "mono": "JetBrains Mono"
  },
  "motion": {
    "ease": "cubic-bezier(0.22, 1, 0.36, 1)",
    "phaseLockMs": 600,
    "layerTransitionMs": 1200,
    "cameraMoveMs": 2000
  }
}
```

**规则**：状态色只用于徽章与图例，不用于主视觉；主视觉只用关系青、耦合金、退相干品红、固有时紫。红色只用于错误提示，不进入理论画面。

---

## 5. 双轨实现

### 5.1 Track A：快轨（Claude／SVG／Three.js／Manim）

- **框架**：React ＋ TypeScript ＋ Vite；SVG 用 React 组件；3D 用 Three.js／R3F；时间轴用 GSAP 或 Remotion。
- **视频输出**：Remotion 组合 React 场景，`npx remotion render` 直接出 MP4；Three.js 用 `@remotion/three`；纯 SVG 用 Playwright 逐帧截图 ＋ FFmpeg。
- **数学动画**：Manim 负责公式、矩阵、谱线；输出透明背景序列，合成进主片。
- **优点**：改字、改数、改时间只改 YAML；适合预演、章节短片、竖屏剪辑、交互地图。

### 5.2 Track B：精轨（Blender／UE5）

- **Blender 4.x**：Python API ＋ Geometry Nodes 生成节点网络、4-单纯形、角亏楔形、光锥；Cycles 渲染 EXR／PNG 序列。
- **UE5（可选）**：Niagara 做粒子与脉冲，Lumen 做体积光；适合实时预演与高质量镜头。
- **后期**：DaVinci Resolve Studio 剪辑、调色、合成；Fusion／Nuke 做深度合成。
- **优点**：材质、灯光、景深、体积感；负责 S01、S15–S19、S24 等 hero 镜头。

### 5.3 混合规则

- 同一组件在 A／B 中使用**同名、同参数、同数据**；A 版是 animatic，B 版是最终渲染。
- 转场处用“同构替换”：A 的 SVG 网络在画面中心与 B 的 3D 网络对齐，再做连续变焦，避免硬切。
- 所有镜头先出 A 版 animatic，锁定节奏后再进 B 版，避免高成本返工。

---

### 5.4 视觉参考与借鉴

| 参考 | 可借鉴 | 边界 |
|:---|:---|:---|
| Quanta Magazine 解释片 | 一个隐喻讲一个机制；2D／3D 混合；克制配色 | 不把理论压成新闻式快剪 |
| AEI／Einstein-Online 自旋网络动画 | 面片颜色表示面积／自旋；“空间只在被激发处出现”；穿行镜头 | 不把自旋网络等同于 CQM 前时空 |
| Regge calculus 可视化 | 4-单纯形 5 顶点、10 边、10 三角形、5 四面体；分片平坦 | 不把 Regge 骨架说成已严格由 LQG 导出 |
| Kuramoto 同步可视化 | 相位色轮、序参量 $r$、锁定瞬间 | 不把 CQM 同步简化成 Kuramoto 方程 |
| Manim／3Blue1Brown | 公式逐行出现、几何直觉 | 公式只进深度层 |
| Claude Motion／纯代码动画 | 代码驱动、可编辑、逐帧 QA | 不用于最终 hero 镜头 |

参考链接：
- [Quanta：Feynman diagrams](https://www.quantamagazine.org/videos/71618/)
- [Quanta：universal pattern](https://www.quantamagazine.org/the-universal-pattern-popping-up-in-math-physics-and-biology-20180823)
- [AEI：quantum gravity animation](https://www.aei.mpg.de/185045/quantum-gravity)
- [Einstein-Online：spin networks](https://www.einstein-online.info/en/spotlight/spin_networks/)
- [Regge calculus: 4-simplex model](https://arxiv.org/html/gr-qc/9706034v2)
- [Kuramoto model visualization](https://blogs.mathworks.com/cleve/2019/08/26/kuramoto-model-of-synchronized-oscillators/)
- [单一抽象层级＋一次放大](https://domer.io/blog/educational-video-protein-synthesis-workflow)

---

## 6. 渲染与 QA 管线

```text
YAML 场景 → 组件渲染（A/B）→ 帧序列 → 合成 → 调色 → 字幕 → 交付
                ↓
            QA：主张校验／状态校验／逐帧抽检／色盲模拟
```

| 检查 | 工具 | 规则 |
|:---|:---|:---|
| 主张完整性 | `packages/qa/claims-lint` | 每个镜头必须有 `claimIds`；每条主张必须有出处与状态 |
| 状态措辞 | 同上 | 琥珀主张的旁白不得出现“已证／证明／确定” |
| 文字溢出 | Playwright ＋ bounding box | 字幕、公式、标签不得越出安全区 |
| 逐帧抽检 | FFmpeg ＋ 像素差 | 每 1 秒抽帧；检查遮挡、穿模、闪烁 |
| 色盲友好 | 色盲模拟 | 关键信息不能只靠颜色区分，必须配形状或文字 |
| 输出规范 | FFmpeg／DaVinci | 4K／24fps；H.265 交付；ProRes 422 HQ 存档 |

---

## 7. Claude 协作方式

| 环节 | Claude 负责 | 人工负责 |
|:---|:---|:---|
| 分镜 | 从文档生成 YAML 场景草案、旁白变体 | 理论作者确认主张与状态 |
| 组件 | 生成 React／Three.js／Blender Python 脚手架 | 技术美术审核代码与性能 |
| 字幕 | 中英翻译、时间轴初稿 | 术语统一与语义校对 |
| QA | 生成检查脚本、汇总抽帧问题 | 最终视觉与科学签字 |

**规则**：Claude 生成的代码必须经过 review 才能进入渲染；提示词与版本存入 `prompts/`，保证可复现。

---

## 8. 里程碑

| 阶段 | 交付 | 完成判据 |
|:---|:---|:---|
| M0 | `claims.yaml`、`tokens.json`、场景 schema | 33 个镜头全部绑定主张、状态与 scope |
| M1 | 8 个 P0 组件 MVP | A 版能连续播放 30 秒测试片段 |
| M2 | 全片 A 版 animatic | 6 分 30 秒节奏、旁白、字幕齐全 |
| M3 | B 版 hero 镜头 | S01、S03、S20–S25、S33 达到交付画质 |
| M4 | 10 支短片 ＋ 交互地图 | 组件复用率 ≥ 70% |
| M5 | QA 与交付 | 四道验收门全部通过 |

---

## 9. 风险与控制

| 风险 | 控制 |
|:---|:---|
| 组件过度设计 | 先做 8 个 P0；P1／P2 等分镜锁定后再做 |
| 浏览器性能不足 | 限制粒子数；用 LOD；3D 重镜头走 B 轨 |
| Blender API 脆弱 | 锁定 Blender 版本；组件带回归测试场景 |
| 科学准确性 | `claims.yaml` ＋ 作者逐镜签字；琥珀色措辞 lint |
| 范围蔓延 | 主片固定 390 秒（6 分 30 秒）；新想法进短片或交互地图 |
| AI 生成不可复现 | 提示词、模型版本、随机种子全部入库 |

---

## 10. 第一批任务

1. 建立 `claims.yaml`，把分镜脚本第 3 节的 12 条主张录入，并填写 `scope` 与 `canSayProven`。
2. 建立 `tokens.json`，锁定颜色、字体、缓动。
3. 实现 `NodeGraph`、`PhaseRing`、`StatusBadge` 三个组件，先做 S12–S14 的 30 秒测试。
4. 实现 `OntologyField` 与 `DecoherenceFork` 的 A 版原型，验证第一、四幕的抽象概念能否不用文字讲清。
5. 用 Remotion 输出第一版 MP4，跑通“YAML → 组件 → 帧 → 视频”的链路。
6. 用 Blender 做一个 4-单纯形测试镜头（S20），验证 A／B 组件的同名参数对齐。
