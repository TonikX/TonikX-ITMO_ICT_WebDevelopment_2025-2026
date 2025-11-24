package io.github.artsobol.kurkod.web.domain.cage.error;

import io.github.artsobol.kurkod.common.error.ErrorDescriptor;
import lombok.AllArgsConstructor;
import lombok.Getter;
import org.springframework.http.HttpStatus;


@AllArgsConstructor
@Getter
public enum CageError implements ErrorDescriptor {
    NOT_FOUND_BY_KEYS("CG-404", "cage.not_found_by_keys", HttpStatus.NOT_FOUND),
    ALREADY_EXISTS("CG-409", "cage.already_exists", HttpStatus.CONFLICT),
    NOT_FOUND_BY_ID("CG-404", "cage.not_found_by_id", HttpStatus.NOT_FOUND),
    ;

    private final String code;
    private final String messageKey;
    private final HttpStatus status;

    public String format(Object... args) {
        return String.format("[%s] %s", code, String.format(messageKey, args));
    }
}
