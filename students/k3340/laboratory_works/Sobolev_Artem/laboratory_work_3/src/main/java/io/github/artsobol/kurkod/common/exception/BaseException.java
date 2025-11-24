package io.github.artsobol.kurkod.common.exception;

import lombok.Getter;
import org.springframework.http.HttpStatus;

@Getter
public abstract class BaseException extends RuntimeException {

    private final String code;
    private final String messageKey;
    private final Object[] args;
    private final HttpStatus status;

    protected BaseException(String message, HttpStatus status) {
        super(message);
        this.status = status;
        this.code = null;
        this.messageKey = null;
        this.args = new Object[0];
    }

    protected BaseException(String code, String messageKey, Object[] args, HttpStatus status) {
        super(messageKey);
        this.code = code;
        this.messageKey = messageKey;
        this.args = args == null ? new Object[0] : args;
        this.status = status;
    }
}
