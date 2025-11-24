package io.github.artsobol.kurkod.web.domain.diet.error;

import io.github.artsobol.kurkod.common.error.ErrorDescriptor;
import lombok.AllArgsConstructor;
import lombok.Getter;
import org.springframework.http.HttpStatus;

@Getter
@AllArgsConstructor
public enum DietError implements ErrorDescriptor {
    NOT_FOUND_BY_ID("DT-404", "diet.not_found_by_id", HttpStatus.NOT_FOUND),
    ALREADY_EXISTS("DT-409", "diet.already_exists", HttpStatus.CONFLICT),
    ;

    private final String code;
    private final String messageKey;
    private final HttpStatus status;

    public String format(Object... args) {
        return String.format("[%s] %s", code, String.format(messageKey, args));
    }
}