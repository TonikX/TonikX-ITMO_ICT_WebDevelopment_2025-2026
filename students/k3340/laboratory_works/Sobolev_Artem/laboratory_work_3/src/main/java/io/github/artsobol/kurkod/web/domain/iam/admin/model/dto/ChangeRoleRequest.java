package io.github.artsobol.kurkod.web.domain.iam.admin.model.dto;

import io.github.artsobol.kurkod.web.domain.iam.user.model.enums.SystemRole;

public record ChangeRoleRequest(SystemRole role) {
}
