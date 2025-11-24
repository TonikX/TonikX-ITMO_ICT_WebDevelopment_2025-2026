package io.github.artsobol.kurkod.common.exception;

import io.github.artsobol.kurkod.common.error.ErrorDescriptor;
import org.springframework.http.HttpStatus;

/**
 * Thrown when an authentication attempt fails due to an invalid password.
 */
public class InvalidPasswordException extends BaseException{

    public InvalidPasswordException(String message) {
        super(message, HttpStatus.UNAUTHORIZED);
    }

    public InvalidPasswordException(ErrorDescriptor error, Object... args) {
        super(error.getCode(), error.getMessageKey(), args, error.getStatus());
    }
}
