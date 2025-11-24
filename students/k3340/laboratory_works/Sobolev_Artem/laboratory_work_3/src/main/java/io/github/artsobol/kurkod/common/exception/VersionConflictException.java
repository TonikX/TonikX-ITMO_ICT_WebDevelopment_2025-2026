package io.github.artsobol.kurkod.common.exception;

import io.github.artsobol.kurkod.common.error.ErrorDescriptor;
import org.springframework.http.HttpStatus;

public class VersionConflictException extends BaseException {

    public VersionConflictException(String message) {
        super(message, HttpStatus.CONFLICT);
    }

    public VersionConflictException(ErrorDescriptor error, Object... args) {
        super(error.getCode(), error.getMessageKey(), args, error.getStatus());
    }
}
