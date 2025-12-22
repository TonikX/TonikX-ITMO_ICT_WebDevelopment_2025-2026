package handler

import (
	"net/http"

	"school-service/internal/domain"
	"school-service/internal/domain/logger"
	"school-service/internal/domain/usecase"
)

// AuthHandler обрабатывает HTTP запросы для аутентификации
type AuthHandler struct {
	baseHandler
	authUC usecase.AuthUseCase
}

// NewAuthHandler создает новый AuthHandler
func NewAuthHandler(authUC usecase.AuthUseCase, log logger.Logger) *AuthHandler {
	return &AuthHandler{
		baseHandler: baseHandler{logger: log},
		authUC:      authUC,
	}
}

// RegisterRequest DTO для регистрации
type RegisterRequest struct {
	Username  string  `json:"username"`
	Email     *string `json:"email,omitempty"`
	Password  string  `json:"password"`
	Role      string  `json:"role"`
	TeacherID *int    `json:"teacher_id,omitempty"`
}

// LoginRequest DTO для входа
type LoginRequest struct {
	Username string `json:"username"`
	Password string `json:"password"`
}

// RefreshTokenRequest DTO для обновления токена
type RefreshTokenRequest struct {
	RefreshToken string `json:"refresh_token"`
}

// AuthResponse DTO для ответа с токенами
type AuthResponse struct {
	AccessToken  string        `json:"access_token"`
	RefreshToken string        `json:"refresh_token"`
	User         *UserResponse `json:"user"`
}

// UserResponse DTO для информации о пользователе
type UserResponse struct {
	ID        int     `json:"id"`
	Username  string  `json:"username"`
	Email     *string `json:"email,omitempty"`
	Role      string  `json:"role"`
	TeacherID *int    `json:"teacher_id,omitempty"`
}

// Register обрабатывает регистрацию пользователя
// @Summary      Регистрация нового пользователя
// @Description  Регистрирует нового пользователя в системе
// @Tags         auth
// @Accept       json
// @Produce      json
// @Param        request body RegisterRequest true "Данные для регистрации"
// @Success      201  {object}  AuthResponse
// @Failure      400  {object}  map[string]string
// @Failure      409  {object}  map[string]string
// @Router       /auth/register [post]
func (h *AuthHandler) Register(w http.ResponseWriter, r *http.Request) {
	var req RegisterRequest
	if err := h.decodeJSON(r, &req); err != nil {
		h.writeError(w, http.StatusBadRequest, "invalid request body", err)
		return
	}

	// Валидация
	if req.Username == "" {
		h.writeError(w, http.StatusBadRequest, "username is required", nil)
		return
	}
	if req.Password == "" {
		h.writeError(w, http.StatusBadRequest, "password is required", nil)
		return
	}
	if req.Role == "" {
		h.writeError(w, http.StatusBadRequest, "role is required", nil)
		return
	}

	role := domain.UserRole(req.Role)
	if !role.IsValid() {
		h.writeError(w, http.StatusBadRequest, "invalid role", nil)
		return
	}

	// Вызов usecase
	usecaseReq := &usecase.RegisterRequest{
		Username:  req.Username,
		Email:     req.Email,
		Password:  req.Password,
		Role:      role,
		TeacherID: req.TeacherID,
	}

	resp, err := h.authUC.Register(r.Context(), usecaseReq)
	if err != nil {
		h.handleError(w, err)
		return
	}

	// Преобразуем ответ
	authResp := &AuthResponse{
		AccessToken:  resp.AccessToken,
		RefreshToken: resp.RefreshToken,
		User: &UserResponse{
			ID:        resp.User.ID,
			Username:  resp.User.Username,
			Email:     resp.User.Email,
			Role:      resp.User.Role.String(),
			TeacherID: resp.User.TeacherID,
		},
	}

	h.writeJSON(w, http.StatusCreated, authResp)
}

// Login обрабатывает вход пользователя
// @Summary      Вход пользователя
// @Description  Выполняет аутентификацию пользователя и возвращает токены
// @Tags         auth
// @Accept       json
// @Produce      json
// @Param        request body LoginRequest true "Данные для входа"
// @Success      200  {object}  AuthResponse
// @Failure      400  {object}  map[string]string
// @Router       /auth/login [post]
func (h *AuthHandler) Login(w http.ResponseWriter, r *http.Request) {
	var req LoginRequest
	if err := h.decodeJSON(r, &req); err != nil {
		h.writeError(w, http.StatusBadRequest, "invalid request body", err)
		return
	}

	// Валидация
	if req.Username == "" {
		h.writeError(w, http.StatusBadRequest, "username is required", nil)
		return
	}
	if req.Password == "" {
		h.writeError(w, http.StatusBadRequest, "password is required", nil)
		return
	}

	// Вызов usecase
	usecaseReq := &usecase.LoginRequest{
		Username: req.Username,
		Password: req.Password,
	}

	resp, err := h.authUC.Login(r.Context(), usecaseReq)
	if err != nil {
		h.handleError(w, err)
		return
	}

	// Преобразуем ответ
	authResp := &AuthResponse{
		AccessToken:  resp.AccessToken,
		RefreshToken: resp.RefreshToken,
		User: &UserResponse{
			ID:        resp.User.ID,
			Username:  resp.User.Username,
			Email:     resp.User.Email,
			Role:      resp.User.Role.String(),
			TeacherID: resp.User.TeacherID,
		},
	}

	h.writeJSON(w, http.StatusOK, authResp)
}

// RefreshToken обрабатывает обновление токена
// @Summary      Обновление access токена
// @Description  Обновляет access токен используя refresh токен
// @Tags         auth
// @Accept       json
// @Produce      json
// @Param        request body RefreshTokenRequest true "Refresh токен"
// @Success      200  {object}  AuthResponse
// @Failure      400  {object}  map[string]string
// @Router       /auth/refresh [post]
func (h *AuthHandler) RefreshToken(w http.ResponseWriter, r *http.Request) {
	var req RefreshTokenRequest
	if err := h.decodeJSON(r, &req); err != nil {
		h.writeError(w, http.StatusBadRequest, "invalid request body", err)
		return
	}

	// Валидация
	if req.RefreshToken == "" {
		h.writeError(w, http.StatusBadRequest, "refresh_token is required", nil)
		return
	}

	// Вызов usecase
	resp, err := h.authUC.RefreshToken(r.Context(), req.RefreshToken)
	if err != nil {
		h.handleError(w, err)
		return
	}

	// Преобразуем ответ
	authResp := &AuthResponse{
		AccessToken:  resp.AccessToken,
		RefreshToken: resp.RefreshToken,
		User: &UserResponse{
			ID:        resp.User.ID,
			Username:  resp.User.Username,
			Email:     resp.User.Email,
			Role:      resp.User.Role.String(),
			TeacherID: resp.User.TeacherID,
		},
	}

	h.writeJSON(w, http.StatusOK, authResp)
}

// Logout обрабатывает выход пользователя
// @Summary      Выход пользователя
// @Description  Отзывает refresh токен пользователя
// @Tags         auth
// @Accept       json
// @Produce      json
// @Param        request body RefreshTokenRequest true "Refresh токен"
// @Success      200  {object}  map[string]string
// @Failure      400  {object}  map[string]string
// @Router       /auth/logout [post]
func (h *AuthHandler) Logout(w http.ResponseWriter, r *http.Request) {
	var req RefreshTokenRequest
	if err := h.decodeJSON(r, &req); err != nil {
		h.writeError(w, http.StatusBadRequest, "invalid request body", err)
		return
	}

	// Валидация
	if req.RefreshToken == "" {
		h.writeError(w, http.StatusBadRequest, "refresh_token is required", nil)
		return
	}

	// Вызов usecase
	if err := h.authUC.Logout(r.Context(), req.RefreshToken); err != nil {
		h.handleError(w, err)
		return
	}

	h.writeJSON(w, http.StatusOK, map[string]string{"message": "logged out successfully"})
}
