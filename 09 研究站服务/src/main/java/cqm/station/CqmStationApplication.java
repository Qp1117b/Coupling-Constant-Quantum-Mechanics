package cqm.station;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.context.properties.EnableConfigurationProperties;

@SpringBootApplication
@EnableConfigurationProperties(StationProperties.class)
public class CqmStationApplication {

    public static void main(String[] args) {
        SpringApplication.run(CqmStationApplication.class, args);
    }
}
