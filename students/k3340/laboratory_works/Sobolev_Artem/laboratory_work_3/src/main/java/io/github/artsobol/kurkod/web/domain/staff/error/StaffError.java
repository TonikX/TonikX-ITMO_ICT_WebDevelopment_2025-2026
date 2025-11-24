package io.github.artsobol.kurkod.web.domain.staff.error;

import io.github.artsobol.kurkod.common.error.ErrorDescriptor;
import lombok.AllArgsConstructor;
import lombok.Getter;
import org.springframework.http.HttpStatus;

@Getter
@AllArgsConstructor
public enum StaffError implements ErrorDescriptor {
    NOT_FOUND_BY_ID("STAFF-404", "staff.not_found_by_id", HttpStatus.NOT_FOUND),
    ALREADY_EXISTS("STAFF-409", "staff.already_exists", HttpStatus.CONFLICT),
    ;

    private final String code;
    private final String messageKey;
    private final HttpStatus status;

    public String format(Object... args) {
        return String.format("[%s] %s", code, String.format(messageKey, args));
    }
}
