package io.github.artsobol.kurkod.web.controller.iam;

import io.github.artsobol.kurkod.common.constants.ApiLogMessage;
import io.github.artsobol.kurkod.common.util.EtagUtils;
import io.github.artsobol.kurkod.common.util.LogUtils;
import io.github.artsobol.kurkod.web.domain.iam.admin.model.dto.ChangeRoleRequest;
import io.github.artsobol.kurkod.web.domain.iam.admin.service.api.AdminUserService;
import io.github.artsobol.kurkod.web.domain.iam.user.model.dto.UserDTO;
import io.github.artsobol.kurkod.web.response.IamResponse;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.Parameter;
import io.swagger.v3.oas.annotations.enums.ParameterIn;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@Slf4j
@RestController
@RequiredArgsConstructor
@RequestMapping(value = "/api/v1/admin/users/{id}", produces = MediaType.APPLICATION_JSON_VALUE)
@Tag(name = "Admin Users", description = "Administrative user management operations")
public class AdminUserController {

    private final AdminUserService userService;

    @Operation(summary = "Change user role",
               description = "Updates the role of a specific user. Requires ETag for optimistic locking.")
    @PatchMapping("/role")
    public ResponseEntity<IamResponse<UserDTO>> changeRole(
            @Parameter(description = "User identifier", example = "10") @PathVariable(name = "id") Long userId,

            @Valid @RequestBody ChangeRoleRequest request,

            @Parameter(name = "If-Match",
                       in = ParameterIn.HEADER,
                       required = true,
                       description = "ETag of the resource") @RequestHeader(value = "If-Match") String ifMatch) {
        log.info(ApiLogMessage.NAME_OF_CURRENT_METHOD.getValue(), LogUtils.getMethodName());
        long expected = EtagUtils.parseIfMatch(ifMatch);
        UserDTO response = userService.changeUserRole(userId, request, expected);

        return ResponseEntity.ok()
                             .eTag(EtagUtils.toEtag(response.version()))
                             .body(IamResponse.createSuccessful(response));
    }

    @Operation(summary = "Activate user", description = "Sets user status to ACTIVE. Requires ETag.")
    @PostMapping("/activate")
    public ResponseEntity<IamResponse<UserDTO>> activateUser(
            @Parameter(description = "User identifier", example = "10") @PathVariable(name = "id") Long userId,

            @Parameter(name = "If-Match",
                       in = ParameterIn.HEADER,
                       required = true,
                       description = "ETag of the resource") @RequestHeader(value = "If-Match") String ifMatch) {
        log.info(ApiLogMessage.NAME_OF_CURRENT_METHOD.getValue(), LogUtils.getMethodName());
        long expected = EtagUtils.parseIfMatch(ifMatch);
        UserDTO response = userService.activateUser(userId, expected);

        return ResponseEntity.ok()
                             .eTag(EtagUtils.toEtag(response.version()))
                             .body(IamResponse.createSuccessful(response));
    }

    @Operation(summary = "Deactivate user", description = "Sets user status to INACTIVE. Requires ETag.")
    @PostMapping("/deactivate")
    public ResponseEntity<IamResponse<UserDTO>> deactivateUser(
            @Parameter(description = "User identifier", example = "10") @PathVariable(name = "id") Long userId,

            @Parameter(name = "If-Match",
                       in = ParameterIn.HEADER,
                       required = true,
                       description = "ETag of the resource") @RequestHeader(value = "If-Match") String ifMatch) {
        log.info(ApiLogMessage.NAME_OF_CURRENT_METHOD.getValue(), LogUtils.getMethodName());
        long expected = EtagUtils.parseIfMatch(ifMatch);
        UserDTO response = userService.deactivateUser(userId, expected);

        return ResponseEntity.ok()
                             .eTag(EtagUtils.toEtag(response.version()))
                             .body(IamResponse.createSuccessful(response));
    }
}
