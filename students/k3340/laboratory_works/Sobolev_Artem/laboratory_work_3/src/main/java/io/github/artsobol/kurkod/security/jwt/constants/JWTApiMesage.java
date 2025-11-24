package io.github.artsobol.kurkod.security.jwt.constants;

import lombok.AccessLevel;
import lombok.AllArgsConstructor;
import lombok.Getter;

@Getter
@AllArgsConstructor(access = AccessLevel.PRIVATE)
public enum JWTApiMesage {
    TOKEN_CREATED_OR_UPDATED("User's token has been created or updated"),
    ;

    private final String message;
}
