package io.github.artsobol.kurkod.common.error;

import org.springframework.http.HttpStatus;

public interface ErrorDescriptor {
    String getCode();
    String getMessageKey();
    HttpStatus getStatus();
}
