package io.github.artsobol.kurkod.web.domain.iam.user.mapper;

import io.github.artsobol.kurkod.web.domain.iam.role.model.dto.RoleDTO;
import io.github.artsobol.kurkod.web.domain.iam.user.model.dto.UserDTO;
import io.github.artsobol.kurkod.web.domain.iam.user.model.dto.UserProfileDTO;
import io.github.artsobol.kurkod.web.domain.iam.role.model.entity.Role;
import io.github.artsobol.kurkod.web.domain.iam.user.model.entity.User;
import io.github.artsobol.kurkod.web.domain.iam.auth.model.request.RegistrationRequest;
import io.github.artsobol.kurkod.web.domain.iam.user.model.request.UserPatchRequest;
import io.github.artsobol.kurkod.web.domain.iam.user.model.request.UserPostRequest;
import io.github.artsobol.kurkod.web.domain.iam.user.model.request.UserPutRequest;
import org.mapstruct.Mapper;
import org.mapstruct.Mapping;
import org.mapstruct.MappingTarget;

import java.util.Collection;
import java.util.List;

@Mapper(componentModel = "spring")
public interface UserMapper {

    @Mapping(target = "roles", expression = "java(mapRoles(user.getRoles()))")
    UserDTO toDto(User user);

    User toEntity(UserPostRequest userPostRequest);

    void updateFully(@MappingTarget User user, UserPutRequest userPutRequest);

    void updatePartially(@MappingTarget User user, UserPatchRequest userPatchRequest);

    @Mapping(target = "roles", expression = "java(mapRoles(user.getRoles()))")
    @Mapping(target = "username", source = "user.username")
    @Mapping(target = "email", source = "user.email")
    @Mapping(target = "token", source = "token")
    @Mapping(target =  "refreshToken", source = "refreshToken")
    UserProfileDTO toUserProfileDto(User user, String token, String refreshToken);

    @Mapping(target = "password", ignore = true)
    @Mapping(target = "roles", ignore = true)
    @Mapping(target = "registrationStatus", expression = "java(RegistrationStatus.PENDING_CONFIRMATION)")
    User fromDto(RegistrationRequest registrationRequest);

    default List<RoleDTO> mapRoles(Collection<Role> roles) {
        return roles.stream()
                .map(role -> new RoleDTO(role.getId(), role.getName()))
                .toList();
    }
}
