# 09 · 研究站服务（Spring Boot）

> CQM 研究站的**应用层**：一个本地 Spring Boot 服务，把静态阅读站、结构化数据、知识图谱、
> 证据复核收进同一个入口。默认挂载的静态站点是 **VitePress 版阅读站**
> （`08 理论组织和形式化框架/10_展示可视化/阅读站VitePress/.vitepress/dist`，生成器 **VitePress v1.6.4**），
> 本服务在其上叠加"实时"能力；Material 版阅读站（`.../10_展示可视化/阅读站/`）保留为 `file://` 离线副本。

## 一句话

`http://127.0.0.1:8080/` 就是理论阅读站；同一端口下 `/api/**` 提供实时 SPARQL、结构化检索、
条目查询与**证据复核写回**。

## 启动

双击 **`启动.bat`**（或命令行）：

```bat
cd "09 研究站服务"
mvn -s settings.xml package -DskipTests
java -jar target/cqm-station-1.0.0.jar --server.port=8080
```

> 已知边界：本机路径含中文与空格，`mvn spring-boot:run` fork 出的 JVM 会报
> `ClassNotFoundException: cqm.station.CqmStationApplication`（classpath 未正确带上 `target/classes`）。
> 因此**实际用 `java -jar` 启动**；`启动.bat` 仍保留 `spring-boot:run` 仅作备选。

- 端口默认 **8080**，改端口：`java -jar target/cqm-station-1.0.0.jar --server.port=8081`
  （或在 `src/main/resources/application.yml` 里改 `server.port`）。
- 首次启动会从阿里云镜像拉依赖（本机直连 Maven 中央仓库不通，镜像配置在 `settings.xml`）。
- 需要 JDK 17+（本机为 Microsoft OpenJDK 25，编译目标 21）。

## 能力

| 入口 | 说明 |
|:---|:---|
| `/` | 静态阅读站（**VitePress v1.6.4** 产物：顶部导航 + 左侧分组侧栏 + 右侧大纲、品牌靛蓝 `#3451b2`、首页 hero + 特性卡；含展开链、两册讲稿、四件内嵌可视化） |
| `/api` | 端点索引 |
| `/api/status` | 状态读数：概念 82 / 命题 63 / 论证 70 / 缺口 24 / 证据 215 / 链条步 131、三元组数、站点文件数、待复核数 |
| `/api/search?q=&type=&limit=` | 结构化检索：概念 / 命题 / 论证 / 缺口 / 符号 / 链条步；CJK 一元+二元 + 拉丁词打分，可按 `type` 过滤 |
| `/api/sparql?query=...` | **实时 SPARQL**（Apache Jena 内存模型载入 `知识图谱.ttl`，5,146 三元组）；默认只读，写操作返回 403 |
| `/api/concepts` `/api/concepts/{id}` | 概念列表 / 详情（定义、别名、**证据引文**、语义近邻） |
| `/api/props` `/api/gaps` | 命题表 / 缺口台账（状态、Lean 对应、分组） |
| `/api/evidence/{structId}` | 断言 → 证据（引文、字符区间、置信度） |
| `/api/chain` | 展开链 131 步（逐字，含出处与字符区间） |
| `/api/review` `POST /api/review` | 复核统计与记录；提交 `{"struct_id","verdict","reviewer","note"}`，verdict ∈ `approved/rejected/unsure`，`approved` 必须带复核人 |

## 与既有机制的关系

- **写回闭环**：`POST /api/review` 写入 `08 .../00_外部引用/复核结果.csv`
  （列 `struct_id,verdict,reviewer,note,reviewed_at`，与 `_build/check_provenance.py`、
  `build_evidence.py` 的期望一致）。提交后重跑 `build_evidence.py` 与
  `check_provenance.py`，`verified` 即按"approved 且有复核人"置真，检查项由 10 升到 13。
- **数据只读**：除复核写回外，服务**不修改**任何 `08` 下的文件；`知识图谱.ttl`、CSV 均在启动时载入内存。
- **单一源不变**：服务只是既有产物的读取层，不产生新的事实。
- **降级**：服务不在时，**Material 版阅读站**（`.../阅读站/`）仍可 `file://` 双击使用（检索台内嵌的 SPARQL 结果为构建期实跑值）。
  注意 **VitePress 产物默认用绝对路径（`base: '/'`），`file://` 直开会丢资源**，必须经 HTTP 提供——这正是本服务的默认挂载对象。

## 已知边界（如实登记）

- 检索为内存线性打分（321 条文档规模），未接专用检索引擎；规模增长后再评估。
- SPARQL 为内存模型，重启后回到文件状态；不做持久化写。
- 站点的"服务已连接"徽标为**软探测**：服务缺席时静默降级，不报错。
- VitePress 站的**交互增强已移植完成**（2026-10-13）：术语/缺口悬浮卡（138 张，含语义近邻）、四层深度滑杆、
  结构化高级检索、服务探测徽标。由 `public/cqm-enhance-vp.js`（VitePress 适配版）与
  `.vitepress/theme/index.js`（`enhanceApp` 内 `router.onAfterRouteChanged` 重跑增强并重排公式）提供。
  - 与 Material 版的差异：正文容器 `.vp-doc`（原 `article.md-content__inner`）、导航挂 `.VPNavBar`、
    快捷键 **`Ctrl/⌘+Shift+K`**（`Ctrl+K` 留给 VitePress 自带全文搜索）、检索框不再依赖 `.md-search__input`。
  - 已知要点：构建期给内容页套 `<div v-pre>` 会让标题变成孙节点，增强脚本用 `contentRoot()` 逐层下潜解决；
    滑杆行为经 `.workbuddy/tools/depth_sim_vp.py` 复核，L001 107 块 / L002 86 块，与 Material 版层级数一致。
- 未实现：多用户与权限（单作者项目不需要）、Lean 在线编译、生成模型接入（已裁定不采用）。

## 结构

```
09 研究站服务/
├── pom.xml                 # Spring Boot 3.3.5 + Jena ARQ 4.10（编译目标 Java 21）
├── settings.xml            # Maven 镜像（阿里云），启动脚本带 -s 使用
├── 启动.bat
└── src/main/
    ├── java/cqm/station/
    │   ├── CqmStationApplication.java
    │   ├── StationProperties.java     # 路径与开关配置
    │   ├── StationConfig.java         # 静态站点挂载（路径归一化）
    │   ├── HomeController.java        # / → /index.html 转发
    │   ├── Csv.java                   # RFC4180 子集读取
    │   ├── KgService.java             # Jena 内存模型 + SPARQL（只读守卫）
    │   ├── IndexService.java          # 结构化索引与检索
    │   ├── ReviewService.java         # 复核写回（同 struct_id 覆盖 + 原子落盘）
    │   └── ApiController.java         # /api/**
    └── resources/application.yml
```

## 验证

端到端验证脚本（27 项：静态站点 4 项、status 9 项、检索 2 项、SPARQL 3 项、条目 4 项、复核写回 5 项）：

```bash
python ".workbuddy/tools/verify_station.py"     # 需服务已启动
```

最近一次运行：**27/27 通过**（写回测试产生的 `复核结果.csv` 已在测试后清理）。
