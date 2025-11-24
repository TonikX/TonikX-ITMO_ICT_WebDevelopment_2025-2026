package io.github.artsobol.kurkod.common.exception;

import io.github.artsobol.kurkod.common.error.ErrorDescriptor;
import org.springframework.http.HttpStatus;

public class InvalidIfMatchException extends BaseException {

    public InvalidIfMatchException(String message) {
        super(message, HttpStatus.BAD_REQUEST);
    }

    public InvalidIfMatchException(ErrorDescriptor error, Object... args) {
        super(error.getCode(), error.getMessageKey(), args, error.getStatus());
    }
}
