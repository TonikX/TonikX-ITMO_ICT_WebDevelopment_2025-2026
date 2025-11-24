package io.github.artsobol.kurkod.web.domain.refreshtoken.service.impl;

import io.github.artsobol.kurkod.common.util.UuidUtils;
import io.github.artsobol.kurkod.security.error.JwtError;
import io.github.artsobol.kurkod.web.domain.refreshtoken.model.entity.RefreshToken;
import io.github.artsobol.kurkod.web.domain.iam.user.model.entity.User;
import io.github.artsobol.kurkod.common.exception.NotFoundException;
import io.github.artsobol.kurkod.web.domain.refreshtoken.repository.RefreshTokenRepository;
import io.github.artsobol.kurkod.web.domain.refreshtoken.service.api.RefreshTokenService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

import java.time.OffsetDateTime;

@Slf4j
@Service
@RequiredArgsConstructor
public class RefreshTokenImpl implements RefreshTokenService {

    private final RefreshTokenRepository refreshTokenRepository;

    @Override
    public RefreshToken generateOrUpdateRefreshToken(User user) {
        return refreshTokenRepository.findByUserId(user.getId())
                .map(refreshToken -> {
                    refreshToken.setCreatedAt(OffsetDateTime.now());
                    refreshToken.setToken(UuidUtils.generateUuidWithoutDash());
                    return refreshTokenRepository.save(refreshToken);
                })
                .orElseGet(
                        () -> {
                            RefreshToken newToken = new RefreshToken();
                            newToken.setUser(user);
                            newToken.setCreatedAt(OffsetDateTime.now());
                            newToken.setToken(UuidUtils.generateUuidWithoutDash());
                            return refreshTokenRepository.save(newToken);
                        }
                );
    }

    @Override
    public RefreshToken validateAndRefreshToken(String requestRefreshToken) {
        RefreshToken refreshToken = refreshTokenRepository.findByToken(requestRefreshToken)
                .orElseThrow(
                        () -> new NotFoundException(JwtError.NOT_FOUND_REFRESH_TOKEN, requestRefreshToken)
                );

        refreshToken.setCreatedAt(OffsetDateTime.now());
        refreshToken.setToken(UuidUtils.generateUuidWithoutDash());
        return refreshTokenRepository.save(refreshToken);
    }
}
