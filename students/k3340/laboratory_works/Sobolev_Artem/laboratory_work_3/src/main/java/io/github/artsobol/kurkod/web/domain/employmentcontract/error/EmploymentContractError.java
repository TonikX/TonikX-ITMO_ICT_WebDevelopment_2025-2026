package io.github.artsobol.kurkod.web.domain.employmentcontract.error;

import io.github.artsobol.kurkod.common.error.ErrorDescriptor;
import lombok.AllArgsConstructor;
import lombok.Getter;
import org.springframework.http.HttpStatus;

@Getter
@AllArgsConstructor
public enum EmploymentContractError implements ErrorDescriptor {
    NOT_FOUND_BY_WORKER_ID("EMP-404", "employmentContract.not_found_by_worker_id", HttpStatus.NOT_FOUND),
    ;

    private final String code;
    private final String messageKey;
    private final HttpStatus status;

    public String format(Object... args) {
        return String.format("[%s] %s", code, String.format(messageKey, args));
    }
}
