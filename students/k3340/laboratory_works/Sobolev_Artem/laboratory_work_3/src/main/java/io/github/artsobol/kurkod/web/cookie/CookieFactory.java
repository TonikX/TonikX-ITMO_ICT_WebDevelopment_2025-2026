package io.github.artsobol.kurkod.web.cookie;

import jakarta.servlet.http.Cookie;
import org.springframework.http.HttpHeaders;

public final class CookieFactory {

    private CookieFactory() {}

    public static Cookie createAuthCookie(String value) {
        Cookie authorizationCookie = new Cookie(HttpHeaders.AUTHORIZATION, value);
        authorizationCookie.setHttpOnly(true);
        authorizationCookie.setSecure(true);
        authorizationCookie.setPath("/");
        authorizationCookie.setMaxAge(300);
        return authorizationCookie;
    }
}
