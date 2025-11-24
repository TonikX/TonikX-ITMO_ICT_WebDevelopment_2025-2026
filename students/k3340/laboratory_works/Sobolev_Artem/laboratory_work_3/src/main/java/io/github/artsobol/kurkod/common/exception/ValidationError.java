package io.github.artsobol.kurkod.common.exception;

import io.github.artsobol.kurkod.common.error.ErrorDescriptor;
import org.springframework.http.HttpStatus;

public class ValidationError extends BaseException{

    public ValidationError(String message) {
        super(message, HttpStatus.BAD_REQUEST);
    }

    public ValidationError(ErrorDescriptor error, Object... args) {
        super(error.getCode(), error.getMessageKey(), args, error.getStatus());
    }
}
