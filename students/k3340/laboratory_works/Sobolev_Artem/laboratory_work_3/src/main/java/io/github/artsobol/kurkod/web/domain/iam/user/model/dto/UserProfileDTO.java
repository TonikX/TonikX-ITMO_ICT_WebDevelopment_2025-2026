package io.github.artsobol.kurkod.web.domain.iam.user.model.dto;

import io.github.artsobol.kurkod.web.domain.iam.role.model.dto.RoleDTO;
import io.github.artsobol.kurkod.web.domain.iam.user.model.enums.RegistrationStatus;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;

import java.time.LocalDateTime;
import java.time.OffsetDateTime;
import java.util.List;

@Data
@Builder
@AllArgsConstructor
public class UserProfileDTO {

    private Integer id;
    private String username;
    private String email;

    private RegistrationStatus registrationStatus;
    private OffsetDateTime lastLogin;

    private String token;
    private String refreshToken;
    private List<RoleDTO> roles;
}
