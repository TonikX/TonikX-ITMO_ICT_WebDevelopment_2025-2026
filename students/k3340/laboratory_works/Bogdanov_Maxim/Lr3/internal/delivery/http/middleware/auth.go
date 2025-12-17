package middleware

import (
	"context"
	"encoding/json"
	"net/http"
	"strings"

	"school-service/internal/ctx"
	"school-service/internal/domain"
)

func AuthMiddleware(jwtService domain.JWTService) func(http.Handler) http.Handler {
	return func(next http.Handler) http.Handler {
		return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
			authHeader := r.Header.Get("Authorization")
			if authHeader == "" {
				writeAuthError(w, http.StatusUnauthorized, "authorization header is required")
				return
			}

			parts := strings.Split(authHeader, " ")
			if len(parts) != 2 || parts[0] != "Bearer" {
				writeAuthError(w, http.StatusUnauthorized, "invalid authorization header format")
				return
			}

			tokenString := parts[1]
			claims, err := jwtService.ValidateAccessToken(tokenString)
			if err != nil {
				writeAuthError(w, http.StatusUnauthorized, "invalid or expired token")
				return
			}

			reqCtx := context.WithValue(r.Context(), ctx.UserIDKey, claims.UserID)
			reqCtx = context.WithValue(reqCtx, ctx.UsernameKey, claims.Username)
			reqCtx = context.WithValue(reqCtx, ctx.UserRoleKey, claims.Role)

			next.ServeHTTP(w, r.WithContext(reqCtx))
		})
	}
}

func RequireRole(allowedRoles ...domain.UserRole) func(http.Handler) http.Handler {
	return func(next http.Handler) http.Handler {
		return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
			role, ok := r.Context().Value(ctx.UserRoleKey).(domain.UserRole)
			if !ok {
				writeAuthError(w, http.StatusUnauthorized, "user role not found in context")
				return
			}

			allowed := false
			for _, allowedRole := range allowedRoles {
				if role == allowedRole {
					allowed = true
					break
				}
			}

			if !allowed {
				writeAuthError(w, http.StatusForbidden, "insufficient permissions")
				return
			}

			next.ServeHTTP(w, r)
		})
	}
}

func writeAuthError(w http.ResponseWriter, statusCode int, message string) {
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(statusCode)
	response := map[string]string{
		"error": message,
	}
	_ = json.NewEncoder(w).Encode(response)
}
