# CQM 宣传动画 · Remotion 引擎工程（v3）

> **现行交付**：`../输出/CQM_宣传动画_引擎重构_1080p60.mp4`（180 s / 1920×1080 / 60 fps）。
> **唯一工程入口**：本目录。v1／v2 的「手写 SVG ＋ headless Chrome 逐帧截图」管线已整体移入 `../\_归档_v1v2_手写SVG管线/`，**不保留兼容层**。
> 本次是 2026-11-14 的**根本重构**：换掉工具类别，不是给旧片源打补丁。

## 一、为什么必须换引擎

上一轮对 v1 成片做 1 fps 帧差实测：均值 0.39/255、86% 相邻秒帧几乎完全静止。诊断出的根因不在动画本身，而在自制管线：

| 根因（v1／v2 手写管线） | v3 的做法 |
|:---|:---|
| 无时间轴／关键帧／缓动／层级，96 粒子与 6 波纹全是手写 `t` 解析函数 | `src/engine/tracks.js`：**声明式 Track 表** ＋ 唯一求值器 `evaluate(t)`；改动画只改表 |
| 无 WYSIWYG，遮挡／运动量靠成片后抽帧目视，反馈环 18–37 分钟 | **Remotion Studio 实时预览** ＋ `tools/probe.mjs` 一次打包多帧定格 |
| 串行截图：PNG 400 ms/帧 → MJPEG 91 ms/帧，10,800 帧需 18 分钟 | 引擎原生 `--concurrency=8` 并发分片渲染 |
| 音画两条独立管线，`SCORE`／`CAPS`／`OPS` 手工对齐 | `<Audio src={staticFile('master.wav')}>` 与 `useCurrentFrame()` **同一条时间轴** |
| 验收靠人记：公式、限定语、帧差、遮挡逐项抽帧检查 | `tools/gate.mjs` 出片前七道硬门禁 ＋ `tools/verify.py` 成片级自动验收，不过即 `exit 1` |
| 确定性靠自律：禁随机、禁累积状态，逐条人工核对 | `renderAt`/`evaluate` 均为 `t` 的纯函数；`probe.mjs DET=1` 跳帧逐像素复核 |

内容红线密度（46 条字幕、24 格演算刻度、13 条推导链、限定语同屏、状态双编码）工具帮不上——这部分**一个字不动**，由门禁逐字校验。

## 二、五层架构

```
promo-engine/
├── src/
│   ├── data.js              数据层：C/字体/RAIL/OPS/SEGS/B/CAPS/SCORE —— 全工程唯一数据源
│   ├── legacy/kernel.js     内容内核：S1..S6 场景几何 + 演算逐步呈现（逐字迁移，无运动层）
│   ├── engine/tracks.js     引擎层：TRACKS / EVENTS / evaluate() / applyToKernel()
│   ├── engine/layers.jsx    引擎层：FlowField / Overlay，只消费 evaluate(t) 输出
│   ├── CQMPromo.jsx         组装层：内核 + 引擎 + <Audio>，useCurrentFrame() 驱动
│   ├── Root.jsx / index.js  Composition 注册（CQMPromo / CQMSpike）
│   └── Spike.jsx            最小烟测 Composition
├── public/master.wav        已验收的 180 s 母带（48 kHz / 16-bit / 立体声）
├── reference/               v2 口径基线快照，供 G1/G2 逐字比对
├── tools/
│   ├── extract_kernel.py    一次性迁移：v2 → data.js + kernel.js（断言式，行号漂移即中止）
│   ├── gate.mjs             出片前静态门禁（G1–G7）
│   ├── probe.mjs            一次打包多帧定格 + 跳帧确定性复核
│   ├── verify.py            成片级验收（解码/帧数/帧差/静帧/黑帧/分段死角/接触表）
│   └── ...                  见 package.json scripts
└── out/                     中间产物（打包、抽帧、短片），不入库
```

**职责边界**：`kernel.render(t)` 只负责「画什么、公式何时逐步出现」；`evaluate(t)` 只负责「镜头怎么推、粒子怎么流、字幕怎么入场」；两者在同一帧由 `CQMPromo.jsx` 顺序调用。运动层不再散落在内容代码里。

## 三、口径零改动如何保证

- `tools/extract_kernel.py` 从 `reference/` 基线**逐字**抽出四表与 S1–S6 场景几何；刻意不迁移 v2 的 158–327 行运动引擎、`OfflineAudioContext` 与播放控制。
- **G1**：12 个常量（含 CAPS／SEGS／OPS／SCORE／C）在基线 ↔ `data.js` 之间逐字一致。
- **G2**：场景几何与 SVG 工具集作为连续子串存在于 `kernel.js`。
- **G3**：`motionAt/cameraAt/fieldAt/typeAt/OfflineAudioContext` 等旧运动与双管线符号全部消失。
- **G4**：46 条字幕，禁用词（证明／已证／确定／彻底解决／零参数／室温超导／已闭合／已统一／已验证）命中 0；构造后验类数字字幕限定语齐备。
- **G5**：`构造后验数字校验，待独立复现`、`FG 的因果假设`、`框架设定 · 无推导`、`启发式近似，非从谱导出`、`示意值，不是理论预言` 全部在表。
- **G6**：180 s / 60 fps / 10,800 帧 / 母带 180.000 s @ 48 kHz。
- **G7**：24 格演算刻度与 77 个声场事件同源，对齐 **24/24**。

一处呈现层修正（不动文案与几何）：`☯` 常驻标记原被放在 `#camera` 组内，镜头放大时会推到画面外；抽取脚本把它移到镜头组之外，与字幕、段标、刻度尺同属 UI 层。

## 四、改动画只需改表

`src/engine/tracks.js` 里没有 `if(t > 12.5) ...` 这类散落判断。所有时间行为是数据：

- `TRACKS.cameraZoom / driftX / driftY / rotation`：由 `SEGS` 生成的段内三拍关键帧；
- `TRACKS.breath / flowEnergy / scan`：确定性振荡参数；
- `EVENTS.wipes / pulses / captions / score`：全部从 `SEGS / OPS / CAPS / SCORE` 派生；
- `LOCAL_MOTION`：局部形变只写「哪一段、哪个节点、振幅、频率」；
- `sampleKeys()` / `osc()` / `activeEvents()` / `evaluate()`：通用求值，无业务逻辑；
- `applyToKernel()`：唯一的 DOM 输出端。

`evaluate(t)` 是纯函数，`probe.mjs` 的 `DET=1` 会渲 `86s → 10s → 86s` 并比对首尾两帧哈希。

## 五、门禁与重渲

```bash
cd 动画宣传/promo-engine
npm install                 # 首次；--cache 建议指向 D 盘
npm run gate                # 出片前 G1–G7，不过即拒绝渲染
npm run studio              # Remotion Studio：实时预览 + 时间轴拖拽
npm run probe               # 8 帧定格；TIMES="86,118" 可指定，DET=1 加跳帧确定性
npm run release             # gate → 并发渲染 → 成片级 verify，一条命令闭环
npm run verify              # 单独复验成片（可传 mp4 路径参数）
```

渲染参数：复用本机 Edge 作为浏览器（`--browser-executable`），`--concurrency=8`，H.264 + AAC，输出 `out/promo-v3.mp4`；交付副本放 `../输出/`。打包临时目录显式指向 D 盘（`out/.bundle`、`out/.tmp`），避免会话备份把中间产物搬到 C 盘。

**成片级门禁**（`verify.py`）：全片解码退出码、10,800 帧、180 s、1920×1080、音轨存在；1 fps 帧差均值 ≥ 2.0、静止帧 < 15%、黑帧 0、六段各 ≥ 1.5 无运动死角；并自动抽 9 帧生成接触表供最后一次目视。

## 六、实测

（渲染完成后补入：成片体积／码率、全片帧差与静止帧、渲染耗时、抽帧目视结论、跳帧确定性。）

## 七、边界与未办

- **Remotion 许可**：本工程用于个人／非商业研究发布；若后续用于公司场景需按 Remotion 官方许可条款取得商业授权。
- **内容内核是复用层**：S1–S6 场景几何与演算逐步呈现逐字来自 v2，属于「内容素材」而非新引擎；镜头／流场／转场／字幕入场／音画／渲染／验收全部是新的。若日后要重写场景几何，应同步更新 `reference/` 基线并重跑 G1/G2。
- **已登记不改**：t≈118 s 求根框内有一行谱轴骨架灰字与框线叠印，属 v2 内容层既有排版；因本次以「内容层逐字一致」为硬约束，未在本工程内改动，留待后续内容层修订。
- **色彩元数据偏差**：本次交付成片由未带 `--color-space` 的命令渲染，Remotion 默认写 `yuvj420p(pc, bt470bg)`；v2 规格为 BT.709。工程 `npm run render`／`npm run release` 已固定 `--color-space=bt709`（实测输出 `yuv420p(tv, bt709)`），下次重渲即合规。两者画面像素一致，深色矢量画面抽帧目视无色偏；此处如实登记，不隐性回退规格。
- **未做**：盲听验收、onset 互相关逐帧核验、4K／9:16 竖屏切片、v5 的 8:00 正片（S1–S3 未合片）。
- **转场口径**：光帘横扫与视觉圣经「转场只用交叉淡出与形态变化」有差异；宣传片内已登记，正片规格需单独裁定。
