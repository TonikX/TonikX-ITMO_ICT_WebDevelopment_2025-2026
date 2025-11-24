package io.github.artsobol.kurkod.web.domain.dismissal.error;

import io.github.artsobol.kurkod.common.error.ErrorDescriptor;
import lombok.AllArgsConstructor;
import lombok.Getter;
import org.springframework.http.HttpStatus;

@Getter
@AllArgsConstructor
public enum DismissalError implements ErrorDescriptor {
    NOT_FOUND_BY_WORKER_AND_DISMISSED("DE-404", "dismissal.not_found_by_worker_and_dismissed", HttpStatus.NOT_FOUND),
    NOT_FOUND_BY_WORKER_ID("DE-404", "dismissal.not_found_by_worker_id", HttpStatus.NOT_FOUND),
    ;

    private final String code;
    private final String messageKey;
    private final HttpStatus status;

    public String format(Object... args) {
        return String.format("[%s] %s", code, String.format(messageKey, args));
    }
}