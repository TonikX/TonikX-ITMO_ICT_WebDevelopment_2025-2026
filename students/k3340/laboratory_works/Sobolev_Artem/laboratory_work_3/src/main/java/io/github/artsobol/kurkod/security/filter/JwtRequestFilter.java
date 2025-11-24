package io.github.artsobol.kurkod.security.filter;

import io.github.artsobol.kurkod.security.error.JwtError;
import io.github.artsobol.kurkod.security.jwt.JwtTokenProvider;
import io.jsonwebtoken.ExpiredJwtException;
import io.jsonwebtoken.MalformedJwtException;
import io.jsonwebtoken.SignatureException;
import jakarta.servlet.FilterChain;
import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import jakarta.validation.constraints.NotNull;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.HttpStatus;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.authority.SimpleGrantedAuthority;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.stereotype.Component;
import org.springframework.web.filter.OncePerRequestFilter;

import java.io.IOException;
import java.util.List;
import java.util.Optional;
import java.util.stream.Collectors;
@Slf4j
@Component
@RequiredArgsConstructor
public class JwtRequestFilter extends OncePerRequestFilter {
    private static final String AUTHORIZATION_HEADER = "Authorization";
    private static final String BEARER_PREFIX = "Bearer ";
    private static final String LOGIN_PATH = "/auth/login";
    private static final String REGISTER_PATH = "/auth/register";

    private final JwtTokenProvider jwtTokenProvider;

    @Override
    protected void doFilterInternal(
            @NotNull HttpServletRequest request,
            @NotNull HttpServletResponse response,
            @NotNull FilterChain filterChain)
            throws ServletException, IOException {

        Optional<String> authHeader = Optional.ofNullable(request.getHeader(AUTHORIZATION_HEADER));
        String requestURI = request.getRequestURI();

        if (authHeader.isPresent() && authHeader.get().startsWith(BEARER_PREFIX)) {
            String jwt = authHeader.get().substring(BEARER_PREFIX.length());
            try {
                if (!jwtTokenProvider.validateToken(jwt)) {
                    throw new ExpiredJwtException(null, null, JwtError.TOKEN_EXPIRED.format());
                }

                Optional<String> emailOpt = Optional.ofNullable(jwtTokenProvider.getUsername(jwt));
                Optional<String> userIdOpt = Optional.ofNullable(jwtTokenProvider.getUserId(jwt));

                if (emailOpt.isPresent() && userIdOpt.isPresent()) {
                    if (SecurityContextHolder.getContext().getAuthentication() == null) {
                        List<SimpleGrantedAuthority> authorities = jwtTokenProvider.getRoles(jwt).stream()
                                .map(SimpleGrantedAuthority::new)
                                .collect(Collectors.toList());

                        UsernamePasswordAuthenticationToken authenticationToken = new UsernamePasswordAuthenticationToken(
                                emailOpt.get(),
                                jwt,
                                authorities
                        );
                        SecurityContextHolder.getContext().setAuthentication(authenticationToken);
                    }
                }

            } catch (ExpiredJwtException e) {
                handleTokenExpiration(requestURI, jwt, response);
                return;
            } catch (SignatureException | MalformedJwtException e) {
                handleSignatureException(response);
                return;
            } catch (Exception e) {
                handleUnexpectedException(response, e);
                return;
            }
        }
        filterChain.doFilter(request, response);
    }

    private void handleTokenExpiration(String requestURI, String jwt, HttpServletResponse response) throws IOException {
        if (isAuthEndpoint(requestURI)) {
            String refreshedToken = jwtTokenProvider.refreshToken(jwt);
            response.setHeader(AUTHORIZATION_HEADER, BEARER_PREFIX + refreshedToken);
        } else {
            sendErrorResponse(response, HttpStatus.UNAUTHORIZED, JwtError.TOKEN_EXPIRED.format());
        }
    }

    private void handleSignatureException(HttpServletResponse response) throws IOException {
        sendErrorResponse(response, HttpStatus.UNAUTHORIZED, JwtError.INVALID_TOKEN_SIGNATURE.format());
    }

    private void handleUnexpectedException(HttpServletResponse response, Exception e) throws IOException {
        log.error(JwtError.ERROR_DURING_JWT_PROCESSING.format(), e);
        sendErrorResponse(response, HttpStatus.INTERNAL_SERVER_ERROR, JwtError.UNEXPECTED_ERROR_OCCURRED.format());
    }

    private void sendErrorResponse(HttpServletResponse response, HttpStatus status, String message) throws IOException {
        response.setStatus(status.value());
        response.getWriter().write(message);
    }

    private boolean isAuthEndpoint(String uri) {
        return uri.equals(LOGIN_PATH) || uri.equals(REGISTER_PATH);
    }
}