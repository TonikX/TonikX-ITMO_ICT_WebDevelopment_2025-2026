package io.github.artsobol.kurkod.web.controller.iam;

import io.github.artsobol.kurkod.common.constants.ApiLogMessage;
import io.github.artsobol.kurkod.common.util.EtagUtils;
import io.github.artsobol.kurkod.common.util.LocationUtils;
import io.github.artsobol.kurkod.common.util.LogUtils;
import io.github.artsobol.kurkod.web.domain.iam.user.model.dto.UserDTO;
import io.github.artsobol.kurkod.web.domain.iam.user.model.request.UserPatchRequest;
import io.github.artsobol.kurkod.web.domain.iam.user.model.request.UserPostRequest;
import io.github.artsobol.kurkod.web.domain.iam.user.model.request.UserPutRequest;
import io.github.artsobol.kurkod.web.response.IamResponse;
import io.github.artsobol.kurkod.web.domain.iam.user.service.api.UserService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.Parameter;
import io.swagger.v3.oas.annotations.enums.ParameterIn;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.*;

@RestController
@Slf4j
@Validated
@RequiredArgsConstructor
@RequestMapping(value = "/api/v1/users", produces = MediaType.APPLICATION_JSON_VALUE)
@Tag(name = "Users", description = "User operations")
public class UserController {

    private final UserService userService;

    @Operation(summary = "Get user by ID", description = "Returns user information by unique identifier.")
    @GetMapping("/id/{userId}")
    public ResponseEntity<IamResponse<UserDTO>> getById(
            @Parameter(description = "User identifier", example = "5") @PathVariable(name = "userId") Long userId) {
        log.trace(ApiLogMessage.NAME_OF_CURRENT_METHOD.getValue(), LogUtils.getMethodName());
        UserDTO response = userService.getById(userId);
        return ResponseEntity.status(HttpStatus.OK)
                             .eTag(EtagUtils.toEtag(response.version()))
                             .body(IamResponse.createSuccessful(response));
    }

    @Operation(summary = "Get user by username", description = "Returns user information by username.")
    @GetMapping("/username/{username}")
    public ResponseEntity<IamResponse<UserDTO>> getByUsername(
            @Parameter(description = "Username of the user", example = "John") @PathVariable(name = "username") String username) {
        log.trace(ApiLogMessage.NAME_OF_CURRENT_METHOD.getValue(), LogUtils.getMethodName());
        UserDTO response = userService.getByUsername(username);
        return ResponseEntity.status(HttpStatus.OK)
                             .eTag(EtagUtils.toEtag(response.version()))
                             .body(IamResponse.createSuccessful(response));
    }

    @Operation(summary = "Create a new user", description = "Creates a new user account.")
    @PostMapping(consumes = MediaType.APPLICATION_JSON_VALUE)
    public ResponseEntity<IamResponse<UserDTO>> create(@RequestBody @Valid UserPostRequest userPostRequest) {
        log.trace(ApiLogMessage.NAME_OF_CURRENT_METHOD.getValue(), LogUtils.getMethodName());
        UserDTO response = userService.create(userPostRequest);
        return ResponseEntity.created(LocationUtils.buildLocation("api/v1/users/id/{id}", response.id()))
                             .eTag(EtagUtils.toEtag(response.version()))
                             .body(IamResponse.createSuccessful(response));
    }

    @Operation(summary = "Partially update user", description = "Applies a partial update to the user account.")
    @PatchMapping(value = "/{userId}", consumes = MediaType.APPLICATION_JSON_VALUE)
    public ResponseEntity<IamResponse<UserDTO>> updatePartiallyUser(
            @Parameter(description = "User identifier", example = "5") @PathVariable(name = "userId") Long userId,
            @RequestBody @Valid UserPatchRequest request,
            @Parameter(name = "If-Match",
                       in = ParameterIn.HEADER,
                       required = true,
                       description = "ETag of the resource") @RequestHeader(value = "If-Match") String ifMatch) {
        log.trace(ApiLogMessage.NAME_OF_CURRENT_METHOD.getValue(), LogUtils.getMethodName());
        long expected = EtagUtils.parseIfMatch(ifMatch);
        UserDTO response = userService.update(userId, request, expected);
        return ResponseEntity.status(HttpStatus.OK)
                             .eTag(EtagUtils.toEtag(response.version()))
                             .body(IamResponse.createSuccessful(response));
    }

    @Operation(summary = "Fully update user", description = "Fully replaces user data by ID.")
    @PutMapping(value = "/{userId}", consumes = MediaType.APPLICATION_JSON_VALUE)
    public ResponseEntity<IamResponse<UserDTO>> updateFullyUser(
            @Parameter(description = "User identifier", example = "5") @PathVariable(name = "userId") Long userId,
            @RequestBody @Valid UserPutRequest request,
            @Parameter(name = "If-Match",
                       in = ParameterIn.HEADER,
                       required = true,
                       description = "ETag of the resource") @RequestHeader(value = "If-Match") String ifMatch) {
        log.trace(ApiLogMessage.NAME_OF_CURRENT_METHOD.getValue(), LogUtils.getMethodName());
        long expected = EtagUtils.parseIfMatch(ifMatch);
        UserDTO response = userService.replace(userId, request, expected);
        return ResponseEntity.status(HttpStatus.OK)
                             .eTag(EtagUtils.toEtag(response.version()))
                             .body(IamResponse.createSuccessful(response));
    }

    @Operation(summary = "Delete user", description = "Deletes the user account by ID.")
    @DeleteMapping("/{userId}")
    public ResponseEntity<Void> deleteById(
            @Parameter(description = "User identifier", example = "5") @PathVariable(name = "userId") Long userId,
            @Parameter(name = "If-Match",
                       in = ParameterIn.HEADER,
                       required = true,
                       description = "ETag of the resource") @RequestHeader(value = "If-Match") String ifMatch) {
        log.trace(ApiLogMessage.NAME_OF_CURRENT_METHOD.getValue(), LogUtils.getMethodName());
        long expected = EtagUtils.parseIfMatch(ifMatch);
        userService.deleteById(userId, expected);
        return ResponseEntity.noContent().build();
    }
}
