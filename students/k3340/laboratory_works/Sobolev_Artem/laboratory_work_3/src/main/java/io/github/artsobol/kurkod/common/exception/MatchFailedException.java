package io.github.artsobol.kurkod.common.exception;

import io.github.artsobol.kurkod.common.error.ErrorDescriptor;
import org.springframework.http.HttpStatus;

public class MatchFailedException extends BaseException {

    public MatchFailedException(String message) {
        super(message, HttpStatus.PRECONDITION_FAILED);
    }

    public MatchFailedException(ErrorDescriptor error, Object... args) {
        super(error.getCode(), error.getMessageKey(), args, error.getStatus());
    }
}
