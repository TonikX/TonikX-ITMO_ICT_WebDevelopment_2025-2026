package io.github.artsobol.kurkod.web.domain.iam.admin.service.api;

import io.github.artsobol.kurkod.web.domain.iam.admin.model.dto.ChangeRoleRequest;
import io.github.artsobol.kurkod.web.domain.iam.user.model.dto.UserDTO;

public interface AdminUserService {

    UserDTO changeUserRole(Long userId, ChangeRoleRequest request, Long expectedVersion);

    UserDTO activateUser(Long userId, Long expectedVersion);

    UserDTO deactivateUser(Long userId, Long expectedVersion);
}
