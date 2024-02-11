package com.cookbuddy.data;

import java.io.FileInputStream;
import java.io.IOException;
import java.util.Properties;
import javax.sql.DataSource;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.jdbc.core.namedparam.NamedParameterJdbcTemplate;
import org.springframework.jdbc.datasource.DataSourceTransactionManager;
import org.springframework.jdbc.datasource.DriverManagerDataSource;

@Configuration
public class JdbcControl {

    @Bean
    public DataSource dataSource() {
        DriverManagerDataSource dataSource = new DriverManagerDataSource();
        String driverClassName = getPropertiesValue("jdbc.driverClassName");
        String jdbcUrl = getPropertiesValue("jdbc.url");
        String username = getPropertiesValue("jdbc.username");
        String password = getPropertiesValue("jdbc.password");
        dataSource.setDriverClassName(driverClassName);
        dataSource.setUrl(jdbcUrl);
        dataSource.setUsername(username);
        dataSource.setPassword(password);
        return dataSource;
    }

    @Bean
    public NamedParameterJdbcTemplate namedParameterJdbcTemplate() {
        NamedParameterJdbcTemplate retBean = new NamedParameterJdbcTemplate(dataSource());
        return retBean;
    }

    @Bean
    public DataSourceTransactionManager txnManager() {
        DataSourceTransactionManager txnManager = new DataSourceTransactionManager(dataSource());
        return txnManager;
    }

    public static String getPropertiesValue(String propName) {
        try {
            Properties properties = new Properties();
            String rootPath = Thread.currentThread().getContextClassLoader().getResource("").getPath();
            String appConfigPath = rootPath + "META-INF/project.dev.extension.properties";
            properties.load(new FileInputStream(appConfigPath));
            String propertyName = properties.getProperty(propName);
            return propertyName;
        } catch (IOException e) {
            e.printStackTrace();

        }
        return "";
    }

}
