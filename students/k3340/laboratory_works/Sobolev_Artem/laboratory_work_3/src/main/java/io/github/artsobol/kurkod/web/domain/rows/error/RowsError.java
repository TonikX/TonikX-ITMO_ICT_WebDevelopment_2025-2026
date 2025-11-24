package io.github.artsobol.kurkod.web.domain.rows.error;

import io.github.artsobol.kurkod.common.error.ErrorDescriptor;
import lombok.AllArgsConstructor;
import lombok.Getter;
import org.springframework.http.HttpStatus;

@Getter
@AllArgsConstructor
public enum RowsError implements ErrorDescriptor {
    NOT_FOUND_BY_ID("RS-404", "rows.not_found_by_id", HttpStatus.NOT_FOUND),
    NOT_FOUND_BY_KEYS("RS-404", "rows.not_found_by_keys", HttpStatus.NOT_FOUND),
    ALREADY_EXISTS("RS-409", "rows.already_exists", HttpStatus.CONFLICT),
    ;

    private final String code;
    private final String messageKey;
    private final HttpStatus status;

    public String format(Object... args) {
        return String.format("[%s] %s", code, String.format(messageKey, args));
    }
}
