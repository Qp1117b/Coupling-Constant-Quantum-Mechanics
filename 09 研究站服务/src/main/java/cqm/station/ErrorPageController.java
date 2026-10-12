package cqm.station;

import org.springframework.boot.web.servlet.error.ErrorController;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;

import jakarta.servlet.http.HttpServletRequest;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;

/**
 * 把错误页接到阅读站的 404.html（VitePress 产物，自带返回首页的跳转与站内样式），
 * 替代默认的白板错误页。仅 404 走阅读站页面；其余状态维持空响应由容器处理。
 */
@Controller
public class ErrorPageController implements ErrorController {

    private final StationProperties props;

    public ErrorPageController(StationProperties props) {
        this.props = props;
    }

    @RequestMapping("/error")
    public ResponseEntity<String> error(HttpServletRequest request) {
        Object statusObj = request.getAttribute("jakarta.servlet.error.status_code");
        int status = statusObj instanceof Integer ? (Integer) statusObj : 500;
        if (status == 404) {
            Path p = props.resolve(props.getSiteDir()).resolve("404.html");
            if (Files.isRegularFile(p)) {
                try {
                    String html = Files.readString(p, StandardCharsets.UTF_8);
                    return ResponseEntity.status(HttpStatus.NOT_FOUND)
                            .contentType(MediaType.TEXT_HTML)
                            .body(html);
                } catch (Exception ignored) {
                    // 读不到就落到下面的空响应
                }
            }
        }
        return ResponseEntity.status(HttpStatus.resolve(status) == null
                ? HttpStatus.INTERNAL_SERVER_ERROR : HttpStatus.resolve(status)).build();
    }
}
