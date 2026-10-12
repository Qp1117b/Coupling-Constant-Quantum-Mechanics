package cqm.station;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.stereotype.Service;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;
import java.util.Locale;
import java.util.Map;

/**
 * 结构化检索：把概念/命题/缺口/符号/文档/展开链步载入内存，提供 CJK 一元+二元 + 拉丁词的
 * 轻量打分检索（与阅读站前端同思路，服务端可编程访问）。
 */
@Service
public class IndexService {

    public record Doc(String id, String type, String title, String body, String url, String haystack) {
    }

    public record Hit(String id, String type, String title, String snippet, String url, double score) {
    }

    private final List<Doc> docs = new ArrayList<>();
    private final List<Map<String, String>> concepts = new ArrayList<>();
    private final List<Map<String, String>> gaps = new ArrayList<>();
    private final List<Map<String, String>> args = new ArrayList<>();
    private final List<Map<String, String>> props = new ArrayList<>();
    private final List<Map<String, String>> symbols = new ArrayList<>();
    private final List<Map<String, String>> evidence = new ArrayList<>();
    private final List<Map<String, String>> neighbors = new ArrayList<>();
    private final List<JsonNode> chain = new ArrayList<>();
    private final ObjectMapper mapper = new ObjectMapper();

    public IndexService(StationProperties props) {
        Path data = props.resolve(props.getDataDir());
        Path bridge = props.resolve(props.getBridgeDir());
        try {
            loadConcepts(data, props);
            loadProps(data);
            loadGaps(data);
            loadArgs(data);
            loadSymbols(bridge);
            loadNeighbors(bridge);
            loadEvidence(props);
            loadChain(props);
        } catch (IOException e) {
            System.err.println("[cqm] 结构化数据载入失败：" + e.getMessage());
        }
    }

    private void loadConcepts(Path data, StationProperties props) throws IOException {
        concepts.addAll(Csv.read(data.resolve("概念表.csv")));
        for (var r : concepts) {
            String id = r.getOrDefault("concept_id", "");
            String name = r.getOrDefault("name", "");
            if (name.isBlank()) {
                continue;
            }
            String url = docUrl(r.getOrDefault("source_doc", ""));
            docs.add(new Doc(id, "概念", name, r.getOrDefault("definition", ""), url,
                    (name + " " + id + " " + r.getOrDefault("definition", "") + " "
                            + r.getOrDefault("synonyms", "") + " " + r.getOrDefault("type", "")).toLowerCase(Locale.ROOT)));
        }
    }

    private void loadProps(Path data) throws IOException {
        props.addAll(Csv.read(data.resolve("命题表.csv")));
        for (var r : props) {
            String id = r.getOrDefault("prop_id", "");
            docs.add(new Doc(id, r.getOrDefault("type", "命题"), id, r.getOrDefault("statement", ""), "",
                    (id + " " + r.getOrDefault("statement", "") + " " + r.getOrDefault("status", "")).toLowerCase(Locale.ROOT)));
        }
    }

    private void loadGaps(Path data) throws IOException {
        gaps.addAll(Csv.read(data.resolve("缺口编号对照.csv")));
        for (var r : gaps) {
            String code = r.getOrDefault("gap_code", "");
            if (code.isBlank()) {
                continue;
            }
            docs.add(new Doc(r.getOrDefault("prop_id", ""), "缺口", "缺口 " + code,
                    r.getOrDefault("desc_closure", ""), "",
                    (code + " " + r.getOrDefault("prop_id", "") + " " + r.getOrDefault("desc_closure", "")
                            + " " + r.getOrDefault("status_closure", "")).toLowerCase(Locale.ROOT)));
        }
    }

    private void loadArgs(Path data) throws IOException {
        args.addAll(Csv.read(data.resolve("论证表.csv")));
        for (var r : args) {
            String id = r.getOrDefault("arg_id", "");
            if (id.isBlank()) {
                continue;
            }
            docs.add(new Doc(id, "论证", id, r.getOrDefault("conclusion", ""), "",
                    (id + " " + r.getOrDefault("conclusion", "") + " " + r.getOrDefault("premises", "")
                            + " " + r.getOrDefault("type", "")).toLowerCase(Locale.ROOT)));
        }
    }

    private void loadSymbols(Path bridge) throws IOException {
        symbols.addAll(Csv.read(bridge.resolve("符号对照表.csv")));
        for (var r : symbols) {
            String sym = r.getOrDefault("symbol", "");
            if (sym.isBlank()) {
                continue;
            }
            docs.add(new Doc(sym, "符号", sym + "　" + r.getOrDefault("name", ""),
                    String.join("；", r.getOrDefault("value_or_note", ""), r.getOrDefault("kind", "")), "",
                    (sym + " " + r.getOrDefault("name", "") + " " + r.getOrDefault("latex", "") + " "
                            + r.getOrDefault("value_or_note", "")).toLowerCase(Locale.ROOT)));
        }
    }

    private void loadEvidence(StationProperties props) throws IOException {
        evidence.addAll(Csv.read(props.resolve(props.getEvidenceFile())));
    }

    private void loadNeighbors(Path bridge) throws IOException {
        Path near = bridge.getParent().resolve("05_机器学习数据准备/嵌入就绪/语义近邻.csv");
        neighbors.addAll(Csv.read(near));
    }

    private void loadChain(StationProperties props) throws IOException {
        Path f = props.resolve(props.getChainFile());
        if (!Files.isRegularFile(f)) {
            return;
        }
        String txt = Files.readString(f);
        int a = txt.indexOf('{');
        int b = txt.lastIndexOf('}');
        if (a < 0 || b <= a) {
            return;
        }
        JsonNode root = mapper.readTree(txt.substring(a, b + 1));
        JsonNode arr = root.path("chain");
        for (JsonNode n : arr) {
            chain.add(n);
            String text = n.path("text").asText("");
            docs.add(new Doc("S%03d".formatted(n.path("n").asInt()), "链条步",
                    "S%03d".formatted(n.path("n").asInt()), text, "",
                    (text + " " + n.path("doc").asText("") + " 展开链 讲稿").toLowerCase(Locale.ROOT)));
        }
    }

    private String docUrl(String sid) {
        if (sid == null || sid.isBlank()) {
            return "";
        }
        return "#doc-" + sid;
    }

    public List<Map<String, String>> concepts() { return concepts; }

    public List<Map<String, String>> gaps() { return gaps; }

    public List<Map<String, String>> args() { return args; }

    /** 有效缺口数（gap_code 非空；缺口编号对照表含 8 条 id 前缀冲突登记行）。 */
    public int gapCount() {
        int n = 0;
        for (var r : gaps) {
            if (!r.getOrDefault("gap_code", "").isBlank()) {
                n++;
            }
        }
        return n;
    }

    public List<Map<String, String>> props() { return props; }

    public List<Map<String, String>> symbols() { return symbols; }

    public List<Map<String, String>> evidence() { return evidence; }

    public List<Map<String, String>> neighbors() { return neighbors; }

    public List<JsonNode> chain() { return chain; }

    public int size() { return docs.size(); }

    public List<Doc> docsOfType(String type) {
        List<Doc> out = new ArrayList<>();
        for (Doc d : docs) {
            if (type == null || type.isBlank() || d.type().equals(type)) {
                out.add(d);
            }
        }
        return out;
    }

    /** CJK 一元+二元 + 拉丁词切分。 */
    public static List<String> tokens(String q) {
        List<String> out = new ArrayList<>();
        String s = q.toLowerCase(Locale.ROOT).replaceAll("\\s+", "");
        var re = java.util.regex.Pattern.compile("[a-z0-9_.\\-]+|[\\u4e00-\\u9fff]+");
        var m = re.matcher(s);
        while (m.find()) {
            String t = m.group();
            if (t.codePoints().allMatch(Character::isIdeographic)) {
                out.add(t);
                for (int i = 0; i < t.length() - 1; i++) {
                    out.add(t.substring(i, i + 2));
                }
            } else {
                out.add(t);
            }
        }
        return out;
    }

    public List<Hit> search(String q, String type, int limit) {
        List<String> toks = tokens(q);
        List<Hit> hits = new ArrayList<>();
        for (Doc d : docs) {
            if (type != null && !type.isBlank() && !d.type().equals(type)) {
                continue;
            }
            String hay = (d.title() + " " + d.haystack()).toLowerCase(Locale.ROOT);
            double score = 0;
            int hit = 0;
            for (String t : toks) {
                if (hay.contains(t)) {
                    hit++;
                    score += 1 + t.length() * 0.6;
                } else if (t.length() > 2 && hay.contains(t.substring(0, 2))) {
                    score += 0.25;
                }
            }
            if (hit == 0) {
                continue;
            }
            if (hay.startsWith(toks.isEmpty() ? "" : toks.get(0))) {
                score += 2;
            }
            if (d.type().equals("概念")) {
                score += 1.2;
            }
            if (d.type().equals("缺口")) {
                score += 0.8;
            }
            score *= (1 + (double) hit / toks.size());
            String body = d.body();
            String snippet = body.length() > 220 ? body.substring(0, 220) + "…" : body;
            hits.add(new Hit(d.id(), d.type(), d.title(), snippet, d.url(), Math.round(score * 100.0) / 100.0));
        }
        hits.sort((a, b) -> Double.compare(b.score(), a.score()));
        return hits.subList(0, Math.min(limit, hits.size()));
    }
}
