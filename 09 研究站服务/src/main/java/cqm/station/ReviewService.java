package cqm.station;

import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Service;
import org.springframework.web.server.ResponseStatusException;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.StandardCopyOption;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.concurrent.locks.ReentrantLock;

/**
 * 证据人工复核的写回服务。
 *
 * 目标文件 {@code 00_外部引用/复核结果.csv}，列固定为
 * {@code struct_id, verdict, reviewer, note, reviewed_at}（与 _build/check_provenance.py、
 * build_evidence.py 的期望一致：verdict ∈ approved|rejected|unsure；approved 必须有 reviewer）。
 *
 * 采用「读入 → 同 struct_id 覆盖或追加 → 原子落盘」而非盲目 append，
 * 避免同一条断言留下多条互相矛盾的判定（校验脚本按 struct_id 建映射，后写覆盖先写）。
 */
@Service
public class ReviewService {

    public static final String HEADER = "struct_id,verdict,reviewer,note,reviewed_at";
    private static final Set<String> VERDICTS = Set.of("approved", "rejected", "unsure");
    private static final DateTimeFormatter TS = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss");

    private final Path file;
    private final IndexService index;
    private final ReentrantLock lock = new ReentrantLock();

    public ReviewService(StationProperties props, IndexService index) {
        this.file = props.resolve(props.getReviewFile());
        this.index = index;
    }

    public Path file() {
        return file;
    }

    public List<Map<String, String>> list() {
        try {
            return Csv.read(file);
        } catch (IOException e) {
            return List.of();
        }
    }

    /** 统计：总数、各判定数、尚未复核的断言数。 */
    public Map<String, Object> stats() {
        List<Map<String, String>> rows = list();
        Map<String, Long> by = new LinkedHashMap<>();
        by.put("approved", 0L);
        by.put("rejected", 0L);
        by.put("unsure", 0L);
        for (var r : rows) {
            String v = r.getOrDefault("verdict", "");
            by.put(v, by.getOrDefault(v, 0L) + 1);
        }
        Set<String> reviewed = new java.util.HashSet<>();
        for (var r : rows) {
            String id = r.getOrDefault("struct_id", "").trim();
            if (!id.isBlank()) {
                reviewed.add(id);
            }
        }
        int total = index.evidence().size();
        int pending = 0;
        for (var e : index.evidence()) {
            if (!reviewed.contains(e.getOrDefault("struct_id", "").trim())) {
                pending++;
            }
        }
        Map<String, Object> out = new LinkedHashMap<>();
        out.put("file", file.toString());
        out.put("total", rows.size());
        out.put("byVerdict", by);
        out.put("assertions", total);
        out.put("pending", pending);
        out.put("reviewed", total - pending);
        return out;
    }

    /** 提交一条复核判定。 */
    public Map<String, Object> submit(String structId, String verdict, String reviewer, String note) {
        String id = structId == null ? "" : structId.trim();
        String v = verdict == null ? "" : verdict.trim();
        String who = reviewer == null ? "" : reviewer.trim();
        String nt = note == null ? "" : note.trim();
        if (id.isBlank()) {
            throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "struct_id 不能为空");
        }
        if (!VERDICTS.contains(v)) {
            throw new ResponseStatusException(HttpStatus.BAD_REQUEST,
                    "verdict 必须是 approved / rejected / unsure，当前为 " + v);
        }
        boolean known = index.evidence().stream()
                .anyMatch(e -> id.equals(e.getOrDefault("struct_id", "").trim()));
        if (!known) {
            throw new ResponseStatusException(HttpStatus.BAD_REQUEST,
                    "未知 struct_id：" + id + "（不存在于证据映射）");
        }
        if (v.equals("approved") && who.isBlank()) {
            throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "approved 必须填写复核人 reviewer");
        }
        lock.lock();
        try {
            List<Map<String, String>> rows = new ArrayList<>(list());
            Map<String, String> rec = new LinkedHashMap<>();
            rec.put("struct_id", id);
            rec.put("verdict", v);
            rec.put("reviewer", who);
            rec.put("note", nt.length() > 200 ? nt.substring(0, 200) : nt);
            rec.put("reviewed_at", TS.format(LocalDateTime.now()));
            boolean replaced = false;
            for (int i = 0; i < rows.size(); i++) {
                if (id.equals(rows.get(i).getOrDefault("struct_id", "").trim())) {
                    rows.set(i, rec);
                    replaced = true;
                    break;
                }
            }
            if (!replaced) {
                rows.add(rec);
            }
            atomicWrite(rows);
            Map<String, Object> out = new LinkedHashMap<>();
            out.put("ok", true);
            out.put("replaced", replaced);
            out.put("saved", rec);
            out.put("stats", stats());
            return out;
        } catch (IOException e) {
            throw new ResponseStatusException(HttpStatus.INTERNAL_SERVER_ERROR, "写回失败：" + e.getMessage());
        } finally {
            lock.unlock();
        }
    }

    private void atomicWrite(List<Map<String, String>> rows) throws IOException {
        Files.createDirectories(file.getParent());
        Path tmp = file.resolveSibling(file.getFileName() + ".tmp");
        StringBuilder sb = new StringBuilder();
        sb.append(HEADER).append("\r\n");
        for (var r : rows) {
            sb.append(cell(r.getOrDefault("struct_id", ""))).append(',')
                    .append(cell(r.getOrDefault("verdict", ""))).append(',')
                    .append(cell(r.getOrDefault("reviewer", ""))).append(',')
                    .append(cell(r.getOrDefault("note", ""))).append(',')
                    .append(cell(r.getOrDefault("reviewed_at", ""))).append("\r\n");
        }
        Files.writeString(tmp, sb.toString(), StandardCharsets.UTF_8);
        Files.move(tmp, file, StandardCopyOption.REPLACE_EXISTING);
    }

    private static String cell(String s) {
        if (s == null) {
            return "";
        }
        boolean need = s.contains(",") || s.contains("\"") || s.contains("\n") || s.contains("\r");
        String t = s.replace("\"", "\"\"");
        return need ? "\"" + t + "\"" : t;
    }
}
