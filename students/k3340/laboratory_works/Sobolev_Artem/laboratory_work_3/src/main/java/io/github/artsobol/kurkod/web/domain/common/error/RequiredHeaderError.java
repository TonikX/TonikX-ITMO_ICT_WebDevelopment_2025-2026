package io.github.artsobol.kurkod.web.domain.common.error;

import io.github.artsobol.kurkod.common.error.ErrorDescriptor;
import lombok.AllArgsConstructor;
import lombok.Getter;
import org.springframework.http.HttpStatus;

@Getter
@AllArgsConstructor
public enum RequiredHeaderError implements ErrorDescriptor {
    IF_MATCH("IFM-428", "error.header.if_match.missing", HttpStatus.PRECONDITION_REQUIRED),
    MATCH_FAILED("IFM-412", "error.version_not_equals", HttpStatus.PRECONDITION_FAILED),
    MATCH_INVALID("IFM-400", "error.header.match_invalid", HttpStatus.BAD_REQUEST),
    ;

    private final String code;
    private final String messageKey;
    private final HttpStatus status;

    public String format(Object... args) {
        return String.format("[%s] %s", code, String.format(messageKey, args));
    }
}
