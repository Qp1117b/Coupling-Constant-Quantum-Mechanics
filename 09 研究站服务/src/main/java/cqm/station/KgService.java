package cqm.station;

import com.fasterxml.jackson.databind.node.ArrayNode;
import com.fasterxml.jackson.databind.node.ObjectNode;
import org.apache.jena.query.Query;
import org.apache.jena.query.QueryExecution;
import org.apache.jena.query.QueryExecutionFactory;
import org.apache.jena.query.QueryFactory;
import org.apache.jena.query.ResultSet;
import org.apache.jena.rdf.model.Model;
import org.apache.jena.rdf.model.ModelFactory;
import org.apache.jena.rdf.model.Statement;
import org.apache.jena.rdf.model.StmtIterator;
import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Service;
import org.springframework.web.server.ResponseStatusException;

import java.io.InputStream;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;
import java.util.Locale;

/**
 * 知识图谱：把 {@code 知识图谱.ttl} 载入内存模型，提供 SPARQL 查询。
 * 数据量 5,567 三元组，内存模型足够；查询为只读（可配置放开写操作）。
 */
@Service
public class KgService {

    private static final List<String> WRITE_KEYWORDS = List.of(
            "INSERT", "DELETE", "UPDATE", "LOAD", "CLEAR", "DROP", "COPY", "MOVE", "ADD", "CREATE");

    private final Model model;
    private final int triples;

    public KgService(StationProperties props) {
        Path ttl = props.resolve(props.getKgFile());
        this.model = ModelFactory.createDefaultModel();
        if (Files.isRegularFile(ttl)) {
            try (InputStream in = Files.newInputStream(ttl)) {
                model.read(in, null, "TTL");
            } catch (Exception e) {
                System.err.println("[cqm] 知识图谱载入失败：" + e.getMessage());
            }
        } else {
            System.err.println("[cqm] 知识图谱文件不存在：" + ttl.toAbsolutePath());
        }
        this.triples = (int) model.size();
    }

    public int triples() {
        return triples;
    }

    public long classes() {
        return model.listStatements(null, org.apache.jena.vocabulary.RDF.type,
                org.apache.jena.vocabulary.OWL.Class).toList().size();
    }

    public boolean isReadOnly(String q) {
        String up = q.toUpperCase(Locale.ROOT);
        return WRITE_KEYWORDS.stream().noneMatch(up::contains);
    }

    /** 执行 SPARQL，返回统一 JSON 结构。 */
    public ObjectNode query(String q, boolean allowUpdate) {
        if (q == null || q.isBlank()) {
            throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "缺少 query 参数");
        }
        if (!allowUpdate && !isReadOnly(q)) {
            throw new ResponseStatusException(HttpStatus.FORBIDDEN,
                    "当前为只读模式：拒绝写操作（INSERT/DELETE/UPDATE/LOAD/CLEAR/DROP）");
        }
        Query parsed;
        try {
            parsed = QueryFactory.create(q);
        } catch (Exception e) {
            throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "SPARQL 解析失败：" + e.getMessage());
        }
        ObjectNode out = new ObjectNode(com.fasterxml.jackson.databind.node.JsonNodeFactory.instance);
        try (QueryExecution qe = QueryExecutionFactory.create(parsed, model)) {
            if (parsed.isAskType()) {
                out.put("type", "ask").put("boolean", qe.execAsk());
                return out;
            }
            if (parsed.isConstructType() || parsed.isDescribeType()) {
                Model m = qe.execConstruct();
                ArrayNode arr = out.put("type", "graph").putArray("triples");
                for (StmtIterator it = m.listStatements(); it.hasNext(); ) {
                    Statement s = it.next();
                    ObjectNode t = arr.addObject();
                    t.put("s", s.getSubject().toString());
                    t.put("p", s.getPredicate().toString());
                    t.put("o", s.getObject().toString());
                }
                out.put("count", arr.size());
                return out;
            }
            ResultSet rs = qe.execSelect();
            List<String> vars = rs.getResultVars();
            ArrayNode head = out.put("type", "select").putArray("head");
            vars.forEach(head::add);
            ArrayNode rows = out.putArray("rows");
            int n = 0;
            while (rs.hasNext()) {
                org.apache.jena.query.QuerySolution sol = rs.nextSolution();
                ObjectNode row = rows.addObject();
                for (String v : vars) {
                    org.apache.jena.rdf.model.RDFNode node = sol.get(v);
                    row.put(v, node == null ? "" : node.toString());
                }
                n++;
            }
            out.put("count", n);
            return out;
        } catch (ResponseStatusException e) {
            throw e;
        } catch (Exception e) {
            throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "查询执行失败：" + e.getMessage());
        }
    }

    /** 供检索用的简短三元组抽样（不对外暴露全量，避免 JSON 过大）。 */
    public List<String> sample(int n) {
        List<String> out = new ArrayList<>();
        for (StmtIterator it = model.listStatements(); it.hasNext() && out.size() < n; ) {
            Statement s = it.next();
            out.add(s.getSubject() + " " + s.getPredicate() + " " + s.getObject());
        }
        return out;
    }
}
