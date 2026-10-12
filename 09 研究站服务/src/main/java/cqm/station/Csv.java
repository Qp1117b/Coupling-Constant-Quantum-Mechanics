package cqm.station;

import java.io.BufferedReader;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

/**
 * 极简 CSV 读取（RFC4180 子集：引号字段、字段内逗号与换行、双引号转义）。
 * 只读，够用于本项目的结构化表。
 */
public final class Csv {

    private Csv() {
    }

    public static List<Map<String, String>> read(Path file) throws IOException {
        List<Map<String, String>> out = new ArrayList<>();
        if (!Files.isRegularFile(file)) {
            return out;
        }
        try (BufferedReader br = Files.newBufferedReader(file, StandardCharsets.UTF_8)) {
            List<String> header = parseLine(br);
            if (header == null || header.isEmpty()) {
                return out;
            }
            header.set(0, stripBom(header.get(0)));
            List<String> row;
            while ((row = parseLine(br)) != null) {
                if (row.isEmpty() || (row.size() == 1 && row.get(0).isBlank())) {
                    continue;
                }
                Map<String, String> m = new LinkedHashMap<>();
                for (int i = 0; i < header.size(); i++) {
                    m.put(header.get(i), i < row.size() ? row.get(i) : "");
                }
                out.add(m);
            }
        }
        return out;
    }

    public static List<String> readHeader(Path file) throws IOException {
        if (!Files.isRegularFile(file)) {
            return List.of();
        }
        try (BufferedReader br = Files.newBufferedReader(file, StandardCharsets.UTF_8)) {
            List<String> h = parseLine(br);
            if (h == null || h.isEmpty()) {
                return List.of();
            }
            h.set(0, stripBom(h.get(0)));
            return h;
        }
    }

    private static String stripBom(String s) {
        return s.startsWith("\uFEFF") ? s.substring(1) : s;
    }

    /** 读一行；支持引号内含逗号/换行。文件结束时返回 null。 */
    private static List<String> parseLine(BufferedReader br) throws IOException {
        List<String> fields = new ArrayList<>();
        StringBuilder sb = new StringBuilder();
        boolean inQuotes = false;
        boolean sawAny = false;
        int c;
        while ((c = br.read()) != -1) {
            sawAny = true;
            char ch = (char) c;
            if (inQuotes) {
                if (ch == '"') {
                    int n = br.read();
                    if (n == '"') {
                        sb.append('"');
                    } else {
                        inQuotes = false;
                        if (n != -1 && n != '\n' && n != '\r' && n != ',') {
                            sb.append((char) n);
                        } else if (n == ',') {
                            fields.add(sb.toString());
                            sb.setLength(0);
                        } else if (n == -1) {
                            break;
                        }
                    }
                } else {
                    sb.append(ch);
                }
            } else {
                if (ch == '"') {
                    inQuotes = true;
                } else if (ch == ',') {
                    fields.add(sb.toString());
                    sb.setLength(0);
                } else if (ch == '\n') {
                    fields.add(sb.toString());
                    return fields;
                } else if (ch == '\r') {
                    // 跳过，等 \n
                } else {
                    sb.append(ch);
                }
            }
        }
        if (!sawAny) {
            return null;
        }
        fields.add(sb.toString());
        return fields;
    }
}
