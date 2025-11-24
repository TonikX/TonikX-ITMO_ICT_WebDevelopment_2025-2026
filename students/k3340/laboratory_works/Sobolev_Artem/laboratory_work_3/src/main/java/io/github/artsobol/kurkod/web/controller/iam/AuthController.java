package io.github.artsobol.kurkod.web.controller.iam;

import io.github.artsobol.kurkod.common.constants.ApiLogMessage;
import io.github.artsobol.kurkod.common.util.LogUtils;
import io.github.artsobol.kurkod.web.cookie.CookieFactory;
import io.github.artsobol.kurkod.web.domain.iam.auth.model.request.LoginRequest;
import io.github.artsobol.kurkod.web.domain.iam.user.model.dto.UserProfileDTO;
import io.github.artsobol.kurkod.web.domain.iam.auth.model.request.RegistrationRequest;
import io.github.artsobol.kurkod.web.response.IamResponse;
import io.github.artsobol.kurkod.web.domain.auth.service.api.AuthService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.servlet.http.Cookie;
import jakarta.servlet.http.HttpServletResponse;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@Slf4j
@RestController
@RequiredArgsConstructor
@RequestMapping(value = "/auth", produces = MediaType.APPLICATION_JSON_VALUE)
@Tag(name = "Authentication", description = "Authentication operations")
public class AuthController {

    private final AuthService authService;

    @Operation(summary = "Authenticate user",
               description = "Authenticates the user using email and password. Returns an access token and sets it in a cookie.")
    @PostMapping(value = "/login", consumes = MediaType.APPLICATION_JSON_VALUE)
    public ResponseEntity<IamResponse<UserProfileDTO>> login(
            @RequestBody @Valid LoginRequest loginRequest,
            HttpServletResponse response) {
        log.trace(ApiLogMessage.NAME_OF_CURRENT_METHOD.getValue(), LogUtils.getMethodName());

        IamResponse<UserProfileDTO> result = authService.login(loginRequest);

        Cookie authorizationCookie = CookieFactory.createAuthCookie(result.getPayload().getToken());
        response.addCookie(authorizationCookie);

        return ResponseEntity.ok(result);
    }

    @Operation(summary = "Refresh access token",
               description = "Generates a new access token using a valid refresh token. The new token is also set in a cookie.")
    @GetMapping("/refresh/token")
    public ResponseEntity<IamResponse<UserProfileDTO>> refreshToken(
            @RequestParam(name = "token") String refreshToken,
            HttpServletResponse response) {
        log.trace(ApiLogMessage.NAME_OF_CURRENT_METHOD.getValue(), LogUtils.getMethodName());

        IamResponse<UserProfileDTO> result = authService.refreshAccessToken(refreshToken);
        Cookie authorizationCookie = CookieFactory.createAuthCookie(result.getPayload().getToken());
        response.addCookie(authorizationCookie);
        return ResponseEntity.ok(result);
    }

    @Operation(summary = "Register new user",
               description = "Registers a new user account and immediately returns an access token set in a cookie.")
    @PostMapping(value = "/register", consumes = MediaType.APPLICATION_JSON_VALUE)
    public ResponseEntity<IamResponse<UserProfileDTO>> register(
            @RequestBody @Valid RegistrationRequest registrationRequest,
            HttpServletResponse response) {
        log.trace(ApiLogMessage.NAME_OF_CURRENT_METHOD.getValue(), LogUtils.getMethodName());

        IamResponse<UserProfileDTO> result = authService.registerUser(registrationRequest);
        Cookie authorizationCookie = CookieFactory.createAuthCookie(result.getPayload().getToken());
        response.addCookie(authorizationCookie);
        return ResponseEntity.ok(result);
    }
}
