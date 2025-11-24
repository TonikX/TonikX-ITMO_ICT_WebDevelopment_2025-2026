package io.github.artsobol.kurkod.web.domain.iam.user.model.dto;

import io.github.artsobol.kurkod.web.domain.iam.role.model.dto.RoleDTO;
import io.github.artsobol.kurkod.web.domain.iam.userrole.model.entity.UserRole;
import io.github.artsobol.kurkod.web.domain.iam.user.model.enums.RegistrationStatus;

import java.time.OffsetDateTime;
import java.util.List;

public record UserDTO(
        Long id,
        String username,
        String email,
        UserRole role,
        RegistrationStatus registrationStatus,
        List<RoleDTO> roles,
        OffsetDateTime createdAt,
        OffsetDateTime updatedAt,
        Long version
) {
};
