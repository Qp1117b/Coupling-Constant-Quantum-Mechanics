package cqm.station;

import com.fasterxml.jackson.databind.node.ArrayNode;
import com.fasterxml.jackson.databind.node.JsonNodeFactory;
import com.fasterxml.jackson.databind.node.ObjectNode;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.time.Instant;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

/**
 * 对外 REST API。所有路径挂在 {@code /api} 下；静态站点由 StationConfig 挂载到根路径。
 */
@RestController
@RequestMapping("/api")
public class ApiController {

    private final IndexService index;
    private final KgService kg;
    private final ReviewService review;
    private final StationProperties props;

    public ApiController(IndexService index, KgService kg, ReviewService review, StationProperties props) {
        this.index = index;
        this.kg = kg;
        this.review = review;
        this.props = props;
    }

    /** 端点索引：便于发现可用 API。 */
    @GetMapping
    public Map<String, Object> apiIndex() {
        Map<String, Object> out = new LinkedHashMap<>();
        out.put("service", "CQM 研究站服务");
        out.put("endpoints", List.of(
                "GET  /api/status                 状态读数（计数/三元组/站点）",
                "GET  /api/search?q=&type=&limit= 结构化检索（概念/命题/缺口/符号/链条步）",
                "GET  /api/sparql?query=...       实时 SPARQL（默认只读）",
                "GET  /api/concepts               概念列表",
                "GET  /api/concepts/{id}          概念详情（定义/别名/证据引文/语义近邻）",
                "GET  /api/props                  命题列表",
                "GET  /api/gaps                   缺口台账（状态/Lean/分组）",
                "GET  /api/evidence/{structId}    断言证据（引文/字符区间/置信度）",
                "GET  /api/chain                  展开链步（131 步，逐字）",
                "GET  /api/review                 复核统计与记录",
                "POST /api/review                 提交复核（struct_id/verdict/reviewer/note）"));
        return out;
    }

    @GetMapping("/status")
    public Map<String, Object> status() throws IOException {
        Path site = props.resolve(props.getSiteDir());
        long htmlFiles = 0;
        long indexBytes = 0;
        if (Files.isDirectory(site)) {
            try (var s = Files.walk(site)) {
                List<Path> html = s.filter(p -> p.toString().endsWith(".html")).toList();
                htmlFiles = html.size();
                Path idx = site.resolve("index.html");
                if (Files.isRegularFile(idx)) {
                    indexBytes = Files.size(idx);
                }
            }
        }
        Map<String, Object> counts = new LinkedHashMap<>();
        counts.put("concepts", index.concepts().size());
        counts.put("propositions", index.props().size());
        counts.put("arguments", index.args().size());
        counts.put("gaps", index.gapCount());
        counts.put("symbols", index.symbols().size());
        counts.put("evidence", index.evidence().size());
        counts.put("verified", 0);
        counts.put("chainSteps", index.chain().size());
        counts.put("indexDocs", index.size());
        for (var e : index.evidence()) {
            if ("True".equalsIgnoreCase(e.getOrDefault("verified", ""))) {
                counts.put("verified", ((Number) counts.get("verified")).intValue() + 1);
            }
        }
        Map<String, Object> out = new LinkedHashMap<>();
        out.put("service", "CQM 研究站服务");
        out.put("version", "1.0.0");
        out.put("time", Instant.now().toString());
        out.put("counts", counts);
        out.put("kg", Map.of("triples", kg.triples()));
        out.put("site", Map.of("dir", site.toAbsolutePath().toString(), "htmlFiles", htmlFiles, "indexBytes", indexBytes));
        out.put("sparql", Map.of("allowUpdate", props.getSparql().isAllowUpdate()));
        out.put("review", review.stats());
        return out;
    }

    @GetMapping("/search")
    public Map<String, Object> search(@RequestParam String q,
                                      @RequestParam(required = false) String type,
                                      @RequestParam(defaultValue = "20") int limit) {
        var hits = index.search(q, type, Math.max(1, Math.min(limit, 200)));
        Map<String, Object> out = new LinkedHashMap<>();
        out.put("query", q);
        out.put("type", type == null ? "" : type);
        out.put("total", hits.size());
        ArrayNode arr = new ObjectNode(JsonNodeFactory.instance).arrayNode();
        for (var h : hits) {
            ObjectNode n = arr.addObject();
            n.put("id", h.id()).put("type", h.type()).put("title", h.title())
                    .put("snippet", h.snippet()).put("url", h.url()).put("score", h.score());
        }
        out.put("hits", arr);
        return out;
    }

    @GetMapping(value = "/sparql", produces = MediaType.APPLICATION_JSON_VALUE)
    public ObjectNode sparqlGet(@RequestParam String query) {
        return kg.query(query, props.getSparql().isAllowUpdate());
    }

    @PostMapping(value = "/sparql", consumes = MediaType.APPLICATION_FORM_URLENCODED_VALUE,
            produces = MediaType.APPLICATION_JSON_VALUE)
    public ObjectNode sparqlPost(@RequestParam String query) {
        return kg.query(query, props.getSparql().isAllowUpdate());
    }

    @GetMapping("/concepts")
    public Map<String, Object> concepts() {
        return Map.of("total", index.concepts().size(), "items", index.concepts());
    }

    @GetMapping("/concepts/{id}")
    public ResponseEntity<?> concept(@PathVariable String id) {
        var c = index.concepts().stream()
                .filter(r -> id.equalsIgnoreCase(r.getOrDefault("concept_id", ""))).findFirst();
        if (c.isEmpty()) {
            return ResponseEntity.notFound().build();
        }
        var row = c.get();
        Map<String, Object> out = new LinkedHashMap<>(row);
        out.put("evidence", index.evidence().stream()
                .filter(e -> id.equalsIgnoreCase(e.getOrDefault("struct_id", ""))).toList());
        var nb = index.neighbors().stream()
                .filter(r -> id.equalsIgnoreCase(r.getOrDefault("concept_id", ""))).findFirst();
        nb.ifPresent(r -> out.put("semanticNeighbors", r.getOrDefault("neighbors", "")));
        return ResponseEntity.ok(out);
    }

    @GetMapping("/props")
    public Map<String, Object> props() {
        return Map.of("total", index.props().size(), "items", index.props());
    }

    @GetMapping("/gaps")
    public Map<String, Object> gaps() {
        return Map.of("total", index.gaps().size(), "items", index.gaps());
    }

    @GetMapping("/evidence/{structId}")
    public ResponseEntity<?> evidence(@PathVariable String structId) {
        var rows = index.evidence().stream()
                .filter(e -> structId.equalsIgnoreCase(e.getOrDefault("struct_id", ""))).toList();
        if (rows.isEmpty()) {
            return ResponseEntity.notFound().build();
        }
        return ResponseEntity.ok(Map.of("structId", structId, "total", rows.size(), "items", rows));
    }

    @GetMapping("/chain")
    public Map<String, Object> chain() {
        return Map.of("total", index.chain().size(), "items", index.chain());
    }

    @GetMapping("/review")
    public Map<String, Object> reviewGet() {
        Map<String, Object> out = new LinkedHashMap<>();
        out.put("stats", review.stats());
        out.put("items", review.list());
        return out;
    }

    @PostMapping(value = "/review", consumes = MediaType.APPLICATION_JSON_VALUE)
    public Map<String, Object> reviewPost(@RequestBody Map<String, Object> body) {
        return review.submit(
                String.valueOf(body.getOrDefault("struct_id", "")),
                String.valueOf(body.getOrDefault("verdict", "")),
                String.valueOf(body.getOrDefault("reviewer", "")),
                String.valueOf(body.getOrDefault("note", "")));
    }
}
