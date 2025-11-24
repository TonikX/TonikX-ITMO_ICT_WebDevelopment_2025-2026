package io.github.artsobol.kurkod.web.domain.iam.auth.error;

import io.github.artsobol.kurkod.common.error.ErrorDescriptor;
import lombok.AllArgsConstructor;
import lombok.Getter;
import org.springframework.http.HttpStatus;

@Getter
@AllArgsConstructor
public enum AuthError implements ErrorDescriptor {
    AUTHENTICATION_FAILED_FOR_USER("AUTH-401", "auth.authentication_failed_for_user", HttpStatus.UNAUTHORIZED),
    INVALID_USER_OR_PASSWORD("AUTH-401", "auth.invalid_user_or_password", HttpStatus.UNAUTHORIZED),
    INVALID_USER_REGISTRATION_STATUS("AUTH-400", "auth.invalid_registration_status", HttpStatus.BAD_REQUEST),
    CONFIRM_YOUR_EMAIL("AUTH-403-01", "auth.confirm_your_email", HttpStatus.FORBIDDEN),
    EMAIL_VERIFICATION_TOKEN_NOT_FOUND("AUTH-404", "auth.email_verification_token_not_found", HttpStatus.NOT_FOUND),
    CONFIRMATION_LINK_EXPIRED("AUTH-410", "auth.confirmation_link_expired", HttpStatus.GONE),
    MISMATCH_PASSWORDS("AUTH-400", "auth.mismatch_passwords", HttpStatus.BAD_REQUEST),
    INVALID_PASSWORD("AUTH-400", "auth.invalid_password", HttpStatus.BAD_REQUEST);

    private final String code;
    private final String messageKey;
    private final HttpStatus status;

    public String format(Object... args) {
        return String.format("[%s] %s", code, String.format(messageKey, args));
    }
}
