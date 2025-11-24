package io.github.artsobol.kurkod.common.exception;

import io.github.artsobol.kurkod.common.error.ErrorDescriptor;

public final class Exceptions {
    private Exceptions() {}

    public static BaseException of(ErrorDescriptor e, Object... args) {
        return new BaseException(e.getCode(), e.getMessageKey(), args, e.getStatus()) {};
    }
}
