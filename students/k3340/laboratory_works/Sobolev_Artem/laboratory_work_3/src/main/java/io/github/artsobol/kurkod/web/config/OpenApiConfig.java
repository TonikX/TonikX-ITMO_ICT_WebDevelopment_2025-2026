package io.github.artsobol.kurkod.web.config;

import io.swagger.v3.oas.annotations.OpenAPIDefinition;
import io.swagger.v3.oas.models.parameters.Parameter;
import io.swagger.v3.oas.annotations.enums.SecuritySchemeType;
import io.swagger.v3.oas.annotations.info.Info;
import io.swagger.v3.oas.annotations.security.SecurityRequirement;
import io.swagger.v3.oas.annotations.security.SecurityScheme;
import io.swagger.v3.oas.models.Components;
import io.swagger.v3.oas.models.OpenAPI;
import io.swagger.v3.oas.models.media.StringSchema;
import io.swagger.v3.oas.models.servers.Server;
import io.swagger.v3.oas.models.tags.Tag;
import org.springdoc.core.customizers.OpenApiCustomizer;
import org.springdoc.core.models.GroupedOpenApi;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.http.HttpHeaders;

import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;
import java.util.Objects;

@Configuration
@OpenAPIDefinition(info = @Info(title = "KurKod REST API", version = "1.0"),
                   security = {@SecurityRequirement(name = HttpHeaders.AUTHORIZATION)})
@SecurityScheme(name = HttpHeaders.AUTHORIZATION,
                type = SecuritySchemeType.HTTP,
                scheme = "bearer",
                bearerFormat = "JWT")
public class OpenApiConfig {

    @Value("${swagger.servers.first}") private String firstServer;

    @Bean
    public OpenAPI customOpenAPI() {
        return new OpenAPI().addServersItem(new Server().url("/")).components(new Components().addParameters(
                "Accept-Language",
                new Parameter().in("header")
                               .required(false)
                               .name("Accept-Language")
                               .schema(new StringSchema())
                               .description("Locale, e.g. ru or en")));
    }

    @Bean
    public OpenApiCustomizer acceptLanguageHeaderCustomizer() {
        return openApi -> {
            if (openApi.getPaths() == null) {
                return;
            }
            openApi.getPaths().values().forEach(pathItem -> pathItem.readOperations().forEach(operation -> {
                boolean alreadyPresent = operation.getParameters() != null && operation.getParameters()
                                                                                       .stream()
                                                                                       .anyMatch(p -> "Accept-Language".equals(
                                                                                               p.getName()) && "header".equalsIgnoreCase(
                                                                                               p.getIn()));
                if (!alreadyPresent) {
                    operation.addParametersItem(new Parameter().in("header")
                                                               .required(false)
                                                               .name("Accept-Language")
                                                               .schema(new StringSchema())
                                                               .description("Locale, e.g. ru or en"));
                }
            }));
        };
    }


    @Bean
    public OpenApiCustomizer sortTagsAlphabetically() {
        return openApi -> {
            if (openApi.getTags() != null) {
                openApi.setTags(openApi.getTags().stream().sorted(Comparator.comparing(Tag::getName)).toList());
            }
        };
    }

    @Bean
    public GroupedOpenApi publicApi() {
        return GroupedOpenApi.builder()
                             .group("kurkod")
                             .packagesToScan("io.github.artsobol.kurkod")
                             .addOpenApiCustomizer(serverCustomizer())
                             .addOpenApiCustomizer(sortTagsAlphabetically())
                             .addOpenApiCustomizer(acceptLanguageHeaderCustomizer())
                             .build();
    }

    @Bean
    public OpenApiCustomizer serverCustomizer() {
        return openApi -> {
            List<Server> servers = new ArrayList<>();
            if (Objects.nonNull(firstServer)) {
                servers.add(new Server().url(firstServer).description("API Server"));
            }
            openApi.setServers(servers);
        };
    }
}
