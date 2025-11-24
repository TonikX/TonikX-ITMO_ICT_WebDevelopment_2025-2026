package io.github.artsobol.kurkod.security.error;

import io.github.artsobol.kurkod.common.error.ErrorDescriptor;
import lombok.AllArgsConstructor;
import lombok.Getter;
import org.springframework.http.HttpStatus;

@Getter
@AllArgsConstructor
public enum JwtError implements ErrorDescriptor {
    ERROR_DURING_JWT_PROCESSING("JWT-500", "jwt.error_during_processing", HttpStatus.INTERNAL_SERVER_ERROR),
    INVALID_TOKEN_SIGNATURE("JWT-401", "jwt.invalid_signature", HttpStatus.UNAUTHORIZED),
    TOKEN_EXPIRED("JWT-401", "jwt.token_expired", HttpStatus.UNAUTHORIZED),
    NOT_FOUND_REFRESH_TOKEN("JWT-404", "jwt.refresh_token_not_found", HttpStatus.NOT_FOUND),
    UNEXPECTED_ERROR_OCCURRED("JWT-500", "jwt.unexpected_error_occurred", HttpStatus.INTERNAL_SERVER_ERROR),
    ;

    private final String code;
    private final String messageKey;
    private final HttpStatus status;

    public String format(Object... args) {
        return String.format("[%s] %s", code, String.format(messageKey, args));
    }
}
