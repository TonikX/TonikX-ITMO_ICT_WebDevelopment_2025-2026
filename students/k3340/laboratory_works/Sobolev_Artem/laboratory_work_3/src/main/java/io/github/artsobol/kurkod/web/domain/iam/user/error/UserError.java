package io.github.artsobol.kurkod.web.domain.iam.user.error;

import io.github.artsobol.kurkod.common.error.ErrorDescriptor;
import lombok.AllArgsConstructor;
import lombok.Getter;
import org.springframework.http.HttpStatus;

@Getter
@AllArgsConstructor
public enum UserError implements ErrorDescriptor {
    NOT_FOUND_BY_ID("USR-404", "user.not_found_by_id", HttpStatus.NOT_FOUND),
    NOT_FOUND_BY_USERNAME("USR-404", "user.not_found_by_username", HttpStatus.NOT_FOUND),
    NOT_FOUND_BY_EMAIL("USR-404", "user.not_found_by_email", HttpStatus.NOT_FOUND),
    WITH_USERNAME_ALREADY_EXISTS("USR-409", "user.with_username_already_exists", HttpStatus.CONFLICT),
    WITH_EMAIL_ALREADY_EXISTS("USR-409","user.with_email_already_exists", HttpStatus.CONFLICT),
    HAVE_NO_ACCESS("USR-403", "user.no_have_access", HttpStatus.FORBIDDEN),
    ;

    private final String code;
    private final String messageKey;
    private final HttpStatus status;

    public String format(Object... args) {
        return String.format("[%s] %s", code, String.format(messageKey, args));
    }
}
