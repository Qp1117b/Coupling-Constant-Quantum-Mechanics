package cqm.station;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.servlet.config.annotation.ResourceHandlerRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;

import java.nio.file.Files;
import java.nio.file.Path;

/**
 * 静态站点挂载：把阅读站产物目录挂到 {@code /**}，使本服务成为唯一入口。
 * API 控制器（{@code /api/**}）优先级更高，不受影响。
 */
@Configuration
public class StationConfig {

    @Bean
    WebMvcConfigurer siteResourceConfig(StationProperties props) {
        Path site = props.resolve(props.getSiteDir()).toAbsolutePath().normalize();
        boolean ok = Files.isDirectory(site);
        return new WebMvcConfigurer() {
            @Override
            public void addResourceHandlers(ResourceHandlerRegistry registry) {
                if (!ok) {
                    System.err.println("[cqm] 阅读站目录不存在：" + site
                            + "（先运行 _build/build_reader_site.py 生成站点）");
                    return;
                }
                String location = site.toUri().toString();
                if (!location.endsWith("/")) {
                    location = location + "/";
                }
                registry.addResourceHandler("/**")
                        .addResourceLocations(location)
                        .setCachePeriod(0);
                System.out.println("[cqm] 静态阅读站已挂载：" + site);
            }
        };
    }
}
