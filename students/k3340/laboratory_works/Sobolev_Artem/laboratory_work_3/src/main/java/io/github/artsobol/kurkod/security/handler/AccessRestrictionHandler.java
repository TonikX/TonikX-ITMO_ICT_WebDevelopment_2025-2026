package io.github.artsobol.kurkod.security.handler;

import com.fasterxml.jackson.databind.ObjectMapper;
import io.github.artsobol.kurkod.web.domain.iam.user.error.UserError;
import io.github.artsobol.kurkod.web.response.IamError;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import lombok.RequiredArgsConstructor;
import lombok.SneakyThrows;
import org.springframework.context.MessageSource;
import org.springframework.context.i18n.LocaleContextHolder;
import org.springframework.security.access.AccessDeniedException;
import org.springframework.security.web.access.AccessDeniedHandler;
import org.springframework.stereotype.Component;

import java.util.Locale;

@Component
@RequiredArgsConstructor
public class AccessRestrictionHandler implements AccessDeniedHandler {

    private final ObjectMapper objectMapper;
    private final MessageSource messageSource;

    @Override
    @SneakyThrows
    public void handle(HttpServletRequest request,
                       HttpServletResponse response,
                       AccessDeniedException accessDeniedException) {

        var errorDef = UserError.HAVE_NO_ACCESS;

        Locale locale = LocaleContextHolder.getLocale();
        String message = messageSource.getMessage(
                errorDef.getMessageKey(),
                null,
                locale
                                                 );

        IamError body = IamError.createError(
                errorDef.getStatus(),
                errorDef.getCode(),
                message,
                request.getRequestURI()
                                            );

        response.setStatus(errorDef.getStatus().value());
        response.setContentType("application/json");
        response.setCharacterEncoding("UTF-8");

        response.getWriter().write(objectMapper.writeValueAsString(body));
    }
}

