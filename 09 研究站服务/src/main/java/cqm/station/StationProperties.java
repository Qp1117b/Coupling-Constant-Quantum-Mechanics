package cqm.station;

import org.springframework.boot.context.properties.ConfigurationProperties;

import java.nio.file.Path;
import java.nio.file.Paths;

/**
 * 站点与数据路径配置。所有相对路径基于 {@code cqm.root}（默认上一级＝仓库根）。
 */
@ConfigurationProperties(prefix = "cqm")
public class StationProperties {

    /** 项目根（相对当前工作目录）。 */
    private String root = "..";
    /** 阅读站产物目录（静态站点根）。 */
    private String siteDir = "08 理论组织和形式化框架/10_展示可视化/阅读站";
    /** 知识图谱 TTL。 */
    private String kgFile = "08 理论组织和形式化框架/03_超图与理论图/知识图谱.ttl";
    /** 结构化数据目录（源 CSV）。 */
    private String dataDir = "08 理论组织和形式化框架/01_结构化数据";
    /** 桥接与翻译目录（符号对照表、语义近邻）。 */
    private String bridgeDir = "08 理论组织和形式化框架/09_桥接与翻译";
    /** 证据映射 CSV。 */
    private String evidenceFile = "08 理论组织和形式化框架/00_外部引用/证据映射.csv";
    /** 人工复核结果 CSV（写回目标）。 */
    private String reviewFile = "08 理论组织和形式化框架/00_外部引用/复核结果.csv";
    /** 阅读站前端数据（含展开链步）。 */
    private String chainFile = "08 理论组织和形式化框架/10_展示可视化/阅读站/assets/cqm-glossary.js";

    private final Sparql sparql = new Sparql();
    private final Rebuild rebuild = new Rebuild();
    private final Lean lean = new Lean();

    public Path resolve(String rel) {
        return Paths.get(root, rel);
    }

    public String getRoot() { return root; }
    public void setRoot(String root) { this.root = root; }
    public String getSiteDir() { return siteDir; }
    public void setSiteDir(String siteDir) { this.siteDir = siteDir; }
    public String getKgFile() { return kgFile; }
    public void setKgFile(String kgFile) { this.kgFile = kgFile; }
    public String getDataDir() { return dataDir; }
    public void setDataDir(String dataDir) { this.dataDir = dataDir; }
    public String getBridgeDir() { return bridgeDir; }
    public void setBridgeDir(String bridgeDir) { this.bridgeDir = bridgeDir; }
    public String getEvidenceFile() { return evidenceFile; }
    public void setEvidenceFile(String evidenceFile) { this.evidenceFile = evidenceFile; }
    public String getReviewFile() { return reviewFile; }
    public void setReviewFile(String reviewFile) { this.reviewFile = reviewFile; }
    public String getChainFile() { return chainFile; }
    public void setChainFile(String chainFile) { this.chainFile = chainFile; }
    public Sparql getSparql() { return sparql; }
    public Rebuild getRebuild() { return rebuild; }
    public Lean getLean() { return lean; }

    public static class Sparql {
        /** 是否允许写操作（INSERT/DELETE/UPDATE/LOAD/CLEAR/DROP）。 */
        private boolean allowUpdate = false;

        public boolean isAllowUpdate() { return allowUpdate; }
        public void setAllowUpdate(boolean allowUpdate) { this.allowUpdate = allowUpdate; }
    }

    public static class Rebuild {
        /** 是否允许 POST /api/rebuild 触发阅读站重建。 */
        private boolean enabled = false;

        public boolean isEnabled() { return enabled; }
        public void setEnabled(boolean enabled) { this.enabled = enabled; }
    }

    public static class Lean {
        /** lake 可执行文件绝对路径（编译用；留空或不存在则编译接口返回不可用）。 */
        private String lakeExe = "";
        /** Lean 源码目录（相对 root）。 */
        private String dir = "08 理论组织和形式化框架/04_Lean对接/Lean源码";
        /** 是否允许 POST /api/lean/build 触发 lake build。 */
        private boolean buildEnabled = true;

        public String getLakeExe() { return lakeExe; }
        public void setLakeExe(String lakeExe) { this.lakeExe = lakeExe; }
        public String getDir() { return dir; }
        public void setDir(String dir) { this.dir = dir; }
        public boolean isBuildEnabled() { return buildEnabled; }
        public void setBuildEnabled(boolean buildEnabled) { this.buildEnabled = buildEnabled; }
    }
}
