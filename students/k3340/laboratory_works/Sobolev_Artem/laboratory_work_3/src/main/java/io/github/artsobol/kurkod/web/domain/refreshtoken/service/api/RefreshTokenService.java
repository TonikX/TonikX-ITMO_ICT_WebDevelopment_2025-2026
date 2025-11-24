package io.github.artsobol.kurkod.web.domain.refreshtoken.service.api;

import io.github.artsobol.kurkod.web.domain.refreshtoken.model.entity.RefreshToken;
import io.github.artsobol.kurkod.web.domain.iam.user.model.entity.User;

public interface RefreshTokenService {

    RefreshToken generateOrUpdateRefreshToken(User user);

    RefreshToken validateAndRefreshToken(String refreshToken);
}
