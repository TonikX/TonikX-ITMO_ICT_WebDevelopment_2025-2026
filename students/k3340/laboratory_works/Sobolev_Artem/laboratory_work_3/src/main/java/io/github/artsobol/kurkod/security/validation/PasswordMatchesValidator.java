package io.github.artsobol.kurkod.security.validation;

import io.github.artsobol.kurkod.web.domain.iam.auth.model.request.RegistrationRequest;
import io.github.artsobol.kurkod.common.validation.PasswordMatches;
import jakarta.validation.ConstraintValidator;
import jakarta.validation.ConstraintValidatorContext;

public class PasswordMatchesValidator implements ConstraintValidator<PasswordMatches, RegistrationRequest> {
    @Override
    public boolean isValid(RegistrationRequest registrationRequest, ConstraintValidatorContext constraintValidatorContext) {
        return registrationRequest.getPassword().equals(registrationRequest.getConfirmPassword());
    }
}
