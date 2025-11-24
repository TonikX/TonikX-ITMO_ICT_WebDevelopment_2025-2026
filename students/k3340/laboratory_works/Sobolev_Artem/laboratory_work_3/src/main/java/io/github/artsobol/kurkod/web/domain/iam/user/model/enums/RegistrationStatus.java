package io.github.artsobol.kurkod.web.domain.iam.user.model.enums;

import lombok.AccessLevel;
import lombok.NoArgsConstructor;

@NoArgsConstructor(access = AccessLevel.PRIVATE)
public enum RegistrationStatus {
    ACTIVE,
    INACTIVE,
    PENDING_CONFIRMATION
}
