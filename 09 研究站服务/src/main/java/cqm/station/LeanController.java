package cqm.station;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.io.BufferedReader;
import java.io.File;
import java.io.InputStreamReader;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.atomic.AtomicBoolean;

/**
 * Lean 对接：模块/声明/源码/概念映射的只读查询，以及 lake build 的触发与状态查询。
 *
 * 边界：
 * - 模块清单、声明表、映射表都来自 04_Lean对接 下的构建产物（只读）；
 * - 编译只运行 lake build（产出 .olean，不改动任何 .lean 源文件），
 *   同一时刻仅允许一个构建，输出截断保存，可随时轮询进度。
 */
@RestController
@RequestMapping("/api/lean")
public class LeanController {

    private final StationProperties props;
    private final AtomicBoolean building = new AtomicBoolean(false);
    private volatile String buildStatus = "idle";
    private volatile String buildLog = "";
    private volatile long buildStartMs = 0L;
    private volatile long buildEndMs = 0L;

    public LeanController(StationProperties props) {
        this.props = props;
    }

    private Path leanDir() {
        return props.resolve("08 理论组织和形式化框架/04_Lean对接");
    }

    private Path srcDir() {
        String cfg = props.getLean().getDir();
        return (cfg == null || cfg.isBlank())
                ? leanDir().resolve("Lean源码")
                : props.resolve(cfg);
    }

    /** 模块清单（含 theorem/def/axiom/structure 等计数）。 */
    @GetMapping("/modules")
    public List<Map<String, String>> modules() throws Exception {
        return Csv.read(leanDir().resolve("Lean结构提取/模块清单.csv"));
    }

    /** 全部声明，可按 module / kind 过滤（kind: def/theorem/lemma/axiom/class/structure/inductive/abbrev）。 */
    @GetMapping("/decls")
    public List<Map<String, String>> decls(@RequestParam(required = false) String module,
                                           @RequestParam(required = false) String kind) throws Exception {
        List<Map<String, String>> rows = Csv.read(leanDir().resolve("Lean结构提取/declarations.csv"));
        List<Map<String, String>> out = new ArrayList<>();
        for (Map<String, String> r : rows) {
            if (module != null && !module.isBlank() && !module.equals(r.get("module"))) {
                continue;
            }
            if (kind != null && !kind.isBlank() && !kind.equals(r.get("kind"))) {
                continue;
            }
            out.add(r);
        }
        return out;
    }

    /** 概念/命题/缺口 ↔ Lean 符号映射（人工整理的 25 条）。 */
    @GetMapping("/mapping")
    public List<Map<String, String>> mapping() throws Exception {
        return Csv.read(leanDir().resolve("Lean↔概念映射.csv"));
    }

    /** Lean 源码文本。file 相对 Lean源码/，禁止 .. 越界。 */
    @GetMapping(value = "/source", produces = "text/plain;charset=UTF-8")
    public String source(@RequestParam String file) throws Exception {
        Path base = srcDir().toAbsolutePath().normalize();
        Path target = base.resolve(file).normalize();
        if (!target.startsWith(base) || !Files.isRegularFile(target)) {
            return "无效路径或文件不存在: " + file;
        }
        return Files.readString(target, StandardCharsets.UTF_8);
    }

    /** 触发 lake build（异步；同一时刻仅一个；可配 lean.build-enabled 关闭）。 */
    @PostMapping("/build")
    public Map<String, Object> build() {
        Map<String, Object> out = new LinkedHashMap<>();
        if (!props.getLean().isBuildEnabled()) {
            out.put("status", "disabled");
            out.put("message", "编译功能未启用（cqm.lean.build-enabled=false）");
            return out;
        }
        String lake = props.getLean().getLakeExe();
        if (lake == null || lake.isBlank() || !new File(lake).isFile()) {
            out.put("status", "unavailable");
            out.put("message", "lake 可执行文件未配置或不存在: " + lake);
            return out;
        }
        if (!building.compareAndSet(false, true)) {
            out.put("status", "already_running");
            return out;
        }
        buildStatus = "running";
        buildLog = "";
        buildStartMs = System.currentTimeMillis();
        buildEndMs = 0L;
        Thread th = new Thread(() -> {
            try {
                ProcessBuilder pb = new ProcessBuilder(lake, "build");
                pb.directory(srcDir().toFile());
                pb.redirectErrorStream(true);
                Process p = pb.start();
                StringBuilder sb = new StringBuilder();
                try (BufferedReader br = new BufferedReader(
                        new InputStreamReader(p.getInputStream(), StandardCharsets.UTF_8))) {
                    String line;
                    while ((line = br.readLine()) != null) {
                        if (sb.length() < 200_000) {
                            sb.append(line).append('\n');
                            buildLog = sb.toString();
                        }
                    }
                }
                int code = p.waitFor(15, TimeUnit.MINUTES) ? p.exitValue() : -1;
                if (code == -1) {
                    p.destroyForcibly();
                    sb.append("\n[超时] 超过 15 分钟，已终止");
                }
                buildStatus = code == 0 ? "done" : "error";
                buildLog = sb + (code == 0 ? "" : "\n[exit " + code + "]");
            } catch (Exception e) {
                buildStatus = "error";
                buildLog += "\n[exception] " + e;
            } finally {
                buildEndMs = System.currentTimeMillis();
                building.set(false);
            }
        }, "lake-build");
        th.setDaemon(true);
        th.start();
        out.put("status", "started");
        return out;
    }

    /** 编译状态与输出尾部（前端轮询）。 */
    @GetMapping("/build")
    public Map<String, Object> buildStatus() {
        Map<String, Object> out = new LinkedHashMap<>();
        out.put("status", buildStatus);
        out.put("running", building.get());
        out.put("startedAt", buildStartMs);
        out.put("endAt", buildEndMs);
        long now = buildEndMs == 0 ? System.currentTimeMillis() : buildEndMs;
        out.put("elapsedSec", buildStartMs == 0 ? 0 : Math.max(0, (now - buildStartMs) / 1000));
        String log = buildLog;
        if (log.length() > 20_000) {
            log = "…（已截断，仅显示尾部）\n" + log.substring(log.length() - 20_000);
        }
        out.put("log", log);
        return out;
    }
}
