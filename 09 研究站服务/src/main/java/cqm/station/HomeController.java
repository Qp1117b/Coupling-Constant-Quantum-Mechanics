package cqm.station;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;

/**
 * 欢迎页转发：自定义静态资源位置不会像 Boot 默认静态目录那样把 {@code /} 映射到 {@code index.html}，
 * 这里显式转发，使 {@code http://127.0.0.1:8080/} 直接落在阅读站首页。
 */
@Controller
public class HomeController {

    @GetMapping("/")
    public String home() {
        return "forward:/index.html";
    }
}
