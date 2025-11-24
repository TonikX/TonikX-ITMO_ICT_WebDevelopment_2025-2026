package io.github.artsobol.kurkod.security.facade;

import io.github.artsobol.kurkod.security.jwt.JwtTokenProvider;
import lombok.RequiredArgsConstructor;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.stereotype.Component;

@Component
@RequiredArgsConstructor
public class SecurityContextFacade {

    private final JwtTokenProvider jwtTokenProvider;;

    public Authentication getAuthentication(){
        return SecurityContextHolder.getContext().getAuthentication();
    }

    public String getCurrentUsername(){
        Authentication authentication = getAuthentication();
        return (authentication == null) ? null : authentication.getName();
    }

    public Long getCurrentUserId(){
        Authentication authentication = getAuthentication();
        if (authentication == null || authentication.getCredentials() == null) {
            return null;
        }
        String token = authentication.getCredentials().toString();
        return Long.parseLong(jwtTokenProvider.getUserId(token));
    }
}
