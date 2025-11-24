package io.github.artsobol.kurkod.security.validation;

import io.github.artsobol.kurkod.web.domain.iam.auth.error.AuthError;
import io.github.artsobol.kurkod.web.domain.iam.user.error.UserError;
import io.github.artsobol.kurkod.common.exception.DataExistException;
import io.github.artsobol.kurkod.common.exception.InvalidPasswordException;
import io.github.artsobol.kurkod.web.domain.iam.user.repository.UserRepository;
import io.github.artsobol.kurkod.common.util.PasswordUtils;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Component;


@Component
@RequiredArgsConstructor
public class AccessValidator {

    private final UserRepository userRepository;

    public void validateNewUser(String username, String email, String password, String confirmPassword) {
        userRepository.findByUsernameAndIsActiveTrue(username).ifPresent(u -> {
            throw new DataExistException(UserError.WITH_USERNAME_ALREADY_EXISTS, username);
        });

        userRepository.findByEmailAndIsActiveTrue(email).ifPresent(u -> {
            throw new DataExistException(UserError.WITH_EMAIL_ALREADY_EXISTS, email);
        });

        if(!password.equals(confirmPassword)) {
            throw new InvalidPasswordException(AuthError.MISMATCH_PASSWORDS, confirmPassword);
        }

        if (PasswordUtils.isNotValidPassword(password) ) {
            throw new InvalidPasswordException(AuthError.INVALID_PASSWORD, password);
        }
    }
}
