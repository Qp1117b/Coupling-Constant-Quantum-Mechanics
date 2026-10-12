package cqm.station;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;

/**
 * Lean 对接：模块/声明/源码/概念映射的只读查询。
 *
 * 边界：
 * - 模块清单、声明表、映射表都来自 04_Lean对接 下的构建产物（只读）；
 * - 不提供编译（lake build 已按裁定移除；本地可用 elan 工具链手工执行）。
 */
@RestController
@RequestMapping("/api/lean")
public class LeanController {

    private final StationProperties props;

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
}
