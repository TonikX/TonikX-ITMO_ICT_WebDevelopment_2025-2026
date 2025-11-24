package io.github.artsobol.kurkod.common.exception;

import io.github.artsobol.kurkod.common.error.ErrorDescriptor;
import org.springframework.http.HttpStatus;

public class MissingIfMatchException extends BaseException {

    public MissingIfMatchException(String message) {
        super(message, HttpStatus.PRECONDITION_REQUIRED);
    }

    public MissingIfMatchException(ErrorDescriptor error, Object... args) {
        super(error.getCode(), error.getMessageKey(), args, error.getStatus());
    }
}
