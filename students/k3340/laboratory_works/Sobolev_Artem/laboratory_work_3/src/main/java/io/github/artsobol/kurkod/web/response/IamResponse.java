package io.github.artsobol.kurkod.web.response;

import io.github.artsobol.kurkod.security.jwt.constants.JWTApiMesage;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;
import org.apache.commons.lang3.StringUtils;

@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
public class IamResponse<P>{

    private String message;
    private P payload;
    private boolean success;

    public static<P> IamResponse<P> createSuccessful(P payload) {
        return new IamResponse<>(StringUtils.EMPTY, payload, true);
    }

    public static<P> IamResponse<P> createSuccessfulWithNewToken(P payload) {
        return new IamResponse<>(JWTApiMesage.TOKEN_CREATED_OR_UPDATED.getMessage(), payload, true);
    }
}
