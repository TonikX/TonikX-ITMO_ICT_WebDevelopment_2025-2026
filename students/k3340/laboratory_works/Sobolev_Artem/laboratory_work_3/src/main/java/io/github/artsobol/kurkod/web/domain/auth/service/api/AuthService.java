package io.github.artsobol.kurkod.web.domain.auth.service.api;

import io.github.artsobol.kurkod.web.domain.iam.auth.model.request.LoginRequest;
import io.github.artsobol.kurkod.web.domain.iam.user.model.dto.UserProfileDTO;
import io.github.artsobol.kurkod.web.domain.iam.auth.model.request.RegistrationRequest;
import io.github.artsobol.kurkod.web.response.IamResponse;

public interface AuthService {

    IamResponse<UserProfileDTO> login(LoginRequest request);

    IamResponse<UserProfileDTO> refreshAccessToken(String refreshToken);

    IamResponse<UserProfileDTO> registerUser(RegistrationRequest registrationRequest);
}
