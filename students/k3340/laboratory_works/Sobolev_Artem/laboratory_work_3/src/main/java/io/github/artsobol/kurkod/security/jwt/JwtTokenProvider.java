package io.github.artsobol.kurkod.security.jwt;

import io.github.artsobol.kurkod.web.domain.iam.role.model.entity.Role;
import io.github.artsobol.kurkod.web.domain.iam.user.model.entity.User;
import io.github.artsobol.kurkod.security.jwt.constants.JWTConstants;
import io.jsonwebtoken.*;
import io.jsonwebtoken.io.Decoders;
import io.jsonwebtoken.security.Keys;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.lang.NonNull;
import org.springframework.stereotype.Component;

import javax.crypto.SecretKey;
import java.time.LocalDateTime;
import java.util.stream.Collectors;

import java.util.Date;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

@Slf4j
@Component
public class JwtTokenProvider {
    private final SecretKey secretKey;
    private final Long jwtValidityInMilliseconds;

    public JwtTokenProvider(@Value("${jwt.secret}") String secret,
                            @Value("${jwt.expiration:3600000}") long jwtValidityInMilliseconds) {
        this.secretKey = getKey(secret);
        this.jwtValidityInMilliseconds = jwtValidityInMilliseconds;
    }

    public String generateToken(@NonNull User user) {
        Map<String, Object> claims = new HashMap<>();
        claims.put(JWTConstants.USER_ID, user.getId());
        claims.put(JWTConstants.USERNAME, user.getUsername());
        claims.put(JWTConstants.USER_EMAIL, user.getEmail());
        claims.put(JWTConstants.USER_REGISTRATION_STATUS, user.getRegistrationStatus().name());
        claims.put(JWTConstants.LAST_UPDATE, LocalDateTime.now().toString());

        List<String> rolesList = user.getRoles().stream()
                .map(Role::getName)
                .collect(Collectors.toList());
        claims.put(JWTConstants.ROLE, rolesList);

        return createToken(claims, user.getEmail());
    }

    public String refreshToken(String token) {
        Claims claims = getAllClaimsFromToken(token);
        return createToken(claims, claims.getSubject());
    }

    public boolean validateToken(String token) {
        try {
            Jws<Claims> claims = Jwts.parserBuilder()
                    .setSigningKey(secretKey)
                    .build()
                    .parseClaimsJws(token);
            return !claims.getBody().getExpiration().before(new Date());
        } catch (JwtException | IllegalArgumentException e) {
            return false;
        }
    }

    public String getUsername(String token) {
        Claims claims = getAllClaimsFromToken(token);
        return claims.get(JWTConstants.USERNAME, String.class);
    }

    public String getUserId(String token) {
        Claims claims = getAllClaimsFromToken(token);
        return String.valueOf(claims.get(JWTConstants.USER_ID));
    }

    public List<String> getRoles(String token) {
        return getAllClaimsFromToken(token).get(JWTConstants.ROLE, List.class);
    }

    private Claims getAllClaimsFromToken(String token) {
        try {
            return Jwts.parserBuilder()
                    .setSigningKey(secretKey)
                    .build()
                    .parseClaimsJws(token)
                    .getBody();
        } catch (ExpiredJwtException e) {
            return e.getClaims();
        }
    }

    private SecretKey getKey(String secretKey64) {
        byte[] decode64 = Decoders.BASE64.decode(secretKey64);
        return Keys.hmacShaKeyFor(decode64);
    }

    private String createToken(Map<String, Object> claims, String subject) {
        return Jwts.builder()
                .setClaims(claims)
                .setSubject(subject)
                .setIssuedAt(new Date())
                .setExpiration(new Date(System.currentTimeMillis() + jwtValidityInMilliseconds))
                .signWith(secretKey, SignatureAlgorithm.HS512)
                .compact();
    }
}