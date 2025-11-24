package io.github.artsobol.kurkod.web.domain.iam.admin.service.impl;

import io.github.artsobol.kurkod.common.constants.ApiLogMessage;
import io.github.artsobol.kurkod.common.exception.NotFoundException;
import io.github.artsobol.kurkod.common.logging.LogHelper;
import io.github.artsobol.kurkod.common.util.VersionUtils;
import io.github.artsobol.kurkod.security.facade.SecurityContextFacade;
import io.github.artsobol.kurkod.web.domain.iam.admin.model.dto.ChangeRoleRequest;
import io.github.artsobol.kurkod.web.domain.iam.admin.service.api.AdminUserService;
import io.github.artsobol.kurkod.web.domain.iam.role.error.RoleError;
import io.github.artsobol.kurkod.web.domain.iam.role.model.entity.Role;
import io.github.artsobol.kurkod.web.domain.iam.role.repository.RoleRepository;
import io.github.artsobol.kurkod.web.domain.iam.user.error.UserError;
import io.github.artsobol.kurkod.web.domain.iam.user.mapper.UserMapper;
import io.github.artsobol.kurkod.web.domain.iam.user.model.dto.UserDTO;
import io.github.artsobol.kurkod.web.domain.iam.user.model.entity.User;
import io.github.artsobol.kurkod.web.domain.iam.user.model.enums.RegistrationStatus;
import io.github.artsobol.kurkod.web.domain.iam.user.model.enums.SystemRole;
import io.github.artsobol.kurkod.web.domain.iam.user.repository.UserRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.HashSet;
import java.util.Set;

@Slf4j
@Service
@Transactional
@PreAuthorize("hasAnyAuthority('ADMIN', 'SUPER_ADMIN')")
@RequiredArgsConstructor
public class AdminUserServiceImpl implements AdminUserService {

    private final UserRepository userRepository;
    private final RoleRepository roleRepository;
    private final UserMapper userMapper;
    private final SecurityContextFacade securityContextFacade;

    private String getCurrentUsername() {
        return securityContextFacade.getCurrentUsername();
    }

    @Override
    public UserDTO changeUserRole(Long userId, ChangeRoleRequest request, Long expectedVersion) {
        VersionUtils.checkVersion(expectedVersion, getUserById(userId).getVersion());
        User user = getUserById(userId);
        Role role = getRoleBySystemRole(request.role());

        Set<Role> roles = new HashSet<>();
        roles.add(role);
        user.setRoles(roles);

        log.info(ApiLogMessage.UPDATE_ENTITY.getValue(), getCurrentUsername(), LogHelper.getEntityName(User.class), userId);
        return userMapper.toDto(userRepository.save(user));
    }

    @Override
    public UserDTO activateUser(Long userId, Long expectedVersion) {
        VersionUtils.checkVersion(expectedVersion, getUserById(userId).getVersion());
        User user = changeStatus(getUserById(userId), RegistrationStatus.ACTIVE);
        log.info(ApiLogMessage.UPDATE_ENTITY.getValue(), getCurrentUsername(), LogHelper.getEntityName(User.class), userId);
        return userMapper.toDto(user);
    }

    @Override
    public UserDTO deactivateUser(Long userId, Long expectedVersion) {
        VersionUtils.checkVersion(expectedVersion, getUserById(userId).getVersion());
        User user = changeStatus(getUserById(userId), RegistrationStatus.INACTIVE);
        log.info(ApiLogMessage.UPDATE_ENTITY.getValue(), getCurrentUsername(), LogHelper.getEntityName(User.class), userId);
        return userMapper.toDto(user);
    }

    protected User changeStatus(User user, RegistrationStatus status) {
        user.setRegistrationStatus(status);
        return userRepository.save(user);
    }

    protected User getUserById(Long id) {
        return userRepository.findByIdAndIsActiveTrue(id)
                             .orElseThrow(() -> new NotFoundException(UserError.NOT_FOUND_BY_ID, id));
    }

    protected Role getRoleBySystemRole(SystemRole role) {
        return roleRepository.findByUserSystemRole(role)
                .orElseThrow(() -> new NotFoundException(RoleError.NOT_FOUND_BY_SYSTEM_NAME, role.name()));
    }
}
