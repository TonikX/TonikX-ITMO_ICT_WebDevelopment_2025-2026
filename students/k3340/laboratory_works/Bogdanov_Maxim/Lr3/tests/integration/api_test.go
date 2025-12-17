package integration

import (
	"bytes"
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"testing"

	"school-service/internal/config"
	httphandler "school-service/internal/delivery/http"
	"school-service/internal/infrastructure/clock"
	"school-service/internal/infrastructure/database"
	"school-service/internal/infrastructure/jwt"
	"school-service/internal/infrastructure/logger"
	"school-service/internal/infrastructure/password"
	"school-service/internal/infrastructure/repository"
	"school-service/internal/usecase"
)

func setupTestServer(t *testing.T) (*httptest.Server, func()) {
	cfg, err := config.Load()
	if err != nil {
		t.Fatalf("failed to load config: %v", err)
	}

	log := logger.New(cfg.Logging.Level, cfg.Logging.Format, cfg.Logging.AddSource)
	clock := clock.NewRealClock()

	db, err := database.New(cfg.Database, log)
	if err != nil {
		t.Fatalf("failed to connect to database: %v", err)
	}

	teacherRepo := repository.NewTeacherRepository(db.DB, clock)
	studentRepo := repository.NewStudentRepository(db.DB, clock)
	classRepo := repository.NewClassRepository(db.DB, clock)
	scheduleRepo := repository.NewScheduleRepository(db.DB, clock)
	gradeRepo := repository.NewGradeRepository(db.DB, clock)
	infoRepo := repository.NewInfoRepository(db.DB, clock)
	reportRepo := repository.NewReportRepository(db.DB, clock)
	userRepo := repository.NewUserRepository(db.DB, clock)
	refreshTokenRepo := repository.NewRefreshTokenRepository(db.DB, clock)

	passwordHasher := password.NewBcryptHasher(0)
	jwtService := jwt.NewJWTService(jwt.JWTConfig{
		AccessSecret:  cfg.JWT.Secret,
		RefreshSecret: cfg.JWT.Secret,
		AccessTTL:     cfg.JWT.AccessTokenTTL,
		RefreshTTL:    cfg.JWT.RefreshTokenTTL,
		Clock:         clock,
	})

	teacherUC := usecase.NewTeacherUseCase(teacherRepo, clock, log)
	studentUC := usecase.NewStudentUseCase(studentRepo, clock, log)
	classUC := usecase.NewClassUseCase(classRepo, clock, log)
	scheduleUC := usecase.NewScheduleUseCase(scheduleRepo, clock, log)
	gradeUC := usecase.NewGradeUseCase(gradeRepo, clock, log)
	infoUC := usecase.NewInfoUseCase(infoRepo, teacherRepo, log)
	reportUC := usecase.NewReportUseCase(reportRepo, teacherRepo, log)
	authUC := usecase.NewAuthUseCase(userRepo, refreshTokenRepo, passwordHasher, jwtService, clock, log, cfg.JWT.RefreshTokenTTL)

	router := httphandler.Router(cfg, db, clock, log, jwtService, teacherUC, studentUC, classUC, scheduleUC, gradeUC, infoUC, reportUC, authUC)

	server := httptest.NewServer(router)

	cleanup := func() {
		server.Close()
		db.Close()
	}

	return server, cleanup
}

type APIResponse struct {
	StatusCode int
	Body       map[string]interface{}
	Headers    http.Header
}

func makeRequest(method, url string, body interface{}, token string) (*APIResponse, error) {
	var reqBody []byte
	var err error

	if body != nil {
		reqBody, err = json.Marshal(body)
		if err != nil {
			return nil, err
		}
	}

	req, err := http.NewRequest(method, url, bytes.NewBuffer(reqBody))
	if err != nil {
		return nil, err
	}

	req.Header.Set("Content-Type", "application/json")
	if token != "" {
		req.Header.Set("Authorization", "Bearer "+token)
	}

	client := &http.Client{}
	resp, err := client.Do(req)
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()

	var respBody map[string]interface{}
	if resp.ContentLength > 0 {
		json.NewDecoder(resp.Body).Decode(&respBody)
	}

	return &APIResponse{
		StatusCode: resp.StatusCode,
		Body:       respBody,
		Headers:    resp.Header,
	}, nil
}

func TestAPI_HealthEndpoints(t *testing.T) {
	server, cleanup := setupTestServer(t)
	defer cleanup()

	tests := []struct {
		name           string
		endpoint       string
		expectedStatus int
	}{
		{"Health Check", "/health", http.StatusOK},
		{"Readiness Check", "/health/ready", http.StatusOK},
		{"Liveness Check", "/health/live", http.StatusOK},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			resp, err := makeRequest("GET", server.URL+tt.endpoint, nil, "")
			if err != nil {
				t.Fatalf("request failed: %v", err)
			}

			if resp.StatusCode != tt.expectedStatus {
				t.Errorf("expected status %d, got %d", tt.expectedStatus, resp.StatusCode)
			}
		})
	}
}

func TestAPI_AuthenticationFlow(t *testing.T) {
	server, cleanup := setupTestServer(t)
	defer cleanup()

	var accessToken string
	var refreshToken string

	t.Run("Register new user", func(t *testing.T) {
		registerBody := map[string]interface{}{
			"username": "testuser",
			"email":    "test@example.com",
			"password": "password123",
			"role":     "admin",
		}

		resp, err := makeRequest("POST", server.URL+"/api/v1/auth/register", registerBody, "")
		if err != nil {
			t.Fatalf("register request failed: %v", err)
		}

		if resp.StatusCode != http.StatusCreated {
			t.Errorf("expected status 201, got %d. Body: %v", resp.StatusCode, resp.Body)
		}

		if resp.Body["access_token"] == nil {
			t.Error("access_token not found in response")
		} else {
			accessToken = resp.Body["access_token"].(string)
		}

		if resp.Body["refresh_token"] == nil {
			t.Error("refresh_token not found in response")
		} else {
			refreshToken = resp.Body["refresh_token"].(string)
		}
	})

	t.Run("Login existing user", func(t *testing.T) {
		loginBody := map[string]interface{}{
			"username": "testuser",
			"password": "password123",
		}

		resp, err := makeRequest("POST", server.URL+"/api/v1/auth/login", loginBody, "")
		if err != nil {
			t.Fatalf("login request failed: %v", err)
		}

		if resp.StatusCode != http.StatusOK {
			t.Errorf("expected status 200, got %d. Body: %v", resp.StatusCode, resp.Body)
		}

		if resp.Body["access_token"] == nil {
			t.Error("access_token not found in response")
		}
	})

	t.Run("Refresh token", func(t *testing.T) {
		if refreshToken == "" {
			t.Skip("refresh token not available")
		}

		refreshBody := map[string]interface{}{
			"refresh_token": refreshToken,
		}

		resp, err := makeRequest("POST", server.URL+"/api/v1/auth/refresh", refreshBody, "")
		if err != nil {
			t.Fatalf("refresh request failed: %v", err)
		}

		if resp.StatusCode != http.StatusOK {
			t.Errorf("expected status 200, got %d. Body: %v", resp.StatusCode, resp.Body)
		}
	})

	t.Run("Logout", func(t *testing.T) {
		if refreshToken == "" {
			t.Skip("refresh token not available")
		}

		logoutBody := map[string]interface{}{
			"refresh_token": refreshToken,
		}

		resp, err := makeRequest("POST", server.URL+"/api/v1/auth/logout", logoutBody, "")
		if err != nil {
			t.Fatalf("logout request failed: %v", err)
		}

		if resp.StatusCode != http.StatusOK {
			t.Errorf("expected status 200, got %d. Body: %v", resp.StatusCode, resp.Body)
		}
	})
}

func TestAPI_ProtectedEndpoints(t *testing.T) {
	server, cleanup := setupTestServer(t)
	defer cleanup()

	var accessToken string

	t.Run("Register and get token", func(t *testing.T) {
		registerBody := map[string]interface{}{
			"username": "apiuser",
			"email":    "api@example.com",
			"password": "password123",
			"role":     "admin",
		}

		resp, err := makeRequest("POST", server.URL+"/api/v1/auth/register", registerBody, "")
		if err != nil {
			t.Fatalf("register failed: %v", err)
		}

		if resp.StatusCode == http.StatusCreated && resp.Body["access_token"] != nil {
			accessToken = resp.Body["access_token"].(string)
		}
	})

	if accessToken == "" {
		t.Fatal("failed to get access token")
	}

	t.Run("Access protected endpoint without token", func(t *testing.T) {
		resp, err := makeRequest("GET", server.URL+"/api/v1/teachers", nil, "")
		if err != nil {
			t.Fatalf("request failed: %v", err)
		}

		if resp.StatusCode != http.StatusUnauthorized {
			t.Errorf("expected 401, got %d", resp.StatusCode)
		}
	})

	t.Run("Access protected endpoint with token", func(t *testing.T) {
		resp, err := makeRequest("GET", server.URL+"/api/v1/teachers", nil, accessToken)
		if err != nil {
			t.Fatalf("request failed: %v", err)
		}

		if resp.StatusCode != http.StatusOK {
			t.Errorf("expected 200, got %d. Body: %v", resp.StatusCode, resp.Body)
		}
		_ = accessToken
	})
}

func TestAPI_CRUDOperations(t *testing.T) {
	server, cleanup := setupTestServer(t)
	defer cleanup()

	var accessToken string

	t.Run("Get access token", func(t *testing.T) {
		registerBody := map[string]interface{}{
			"username": "cruduser",
			"password": "password123",
			"role":     "admin",
		}

		resp, err := makeRequest("POST", server.URL+"/api/v1/auth/register", registerBody, "")
		if err == nil && resp.StatusCode == http.StatusCreated {
			if token, ok := resp.Body["access_token"].(string); ok {
				accessToken = token
			}
		}
	})

	if accessToken == "" {
		t.Fatal("failed to get access token")
	}

	t.Run("Create Teacher", func(t *testing.T) {
		teacherBody := map[string]interface{}{
			"first_name":  "John",
			"last_name":   "Doe",
			"middle_name": nil,
		}

		resp, err := makeRequest("POST", server.URL+"/api/v1/teachers", teacherBody, accessToken)
		if err != nil {
			t.Fatalf("create teacher failed: %v", err)
		}

		if resp.StatusCode != http.StatusCreated {
			t.Errorf("expected 201, got %d. Body: %v", resp.StatusCode, resp.Body)
		}
	})

	t.Run("List Teachers", func(t *testing.T) {
		resp, err := makeRequest("GET", server.URL+"/api/v1/teachers", nil, accessToken)
		if err != nil {
			t.Fatalf("list teachers failed: %v", err)
		}

		if resp.StatusCode != http.StatusOK {
			t.Errorf("expected 200, got %d. Body: %v", resp.StatusCode, resp.Body)
		}
	})
}

func TestAPI_ValidationErrors(t *testing.T) {
	server, cleanup := setupTestServer(t)
	defer cleanup()

	var accessToken string

	t.Run("Get access token", func(t *testing.T) {
		registerBody := map[string]interface{}{
			"username": "validuser",
			"password": "password123",
			"role":     "admin",
		}

		resp, err := makeRequest("POST", server.URL+"/api/v1/auth/register", registerBody, "")
		if err == nil && resp.StatusCode == http.StatusCreated {
			if token, ok := resp.Body["access_token"].(string); ok {
				accessToken = token
			}
		}
	})

	t.Run("Create teacher with invalid data", func(t *testing.T) {
		invalidBody := map[string]interface{}{
			"first_name": "",
			"last_name":  "",
		}

		resp, err := makeRequest("POST", server.URL+"/api/v1/teachers", invalidBody, accessToken)
		if err != nil {
			t.Fatalf("request failed: %v", err)
		}

		if resp.StatusCode != http.StatusBadRequest {
			t.Errorf("expected 400, got %d", resp.StatusCode)
		}
	})

	t.Run("Get non-existent resource", func(t *testing.T) {
		if accessToken == "" {
			t.Skip("access token not available")
		}
		resp, err := makeRequest("GET", server.URL+"/api/v1/teachers/99999", nil, accessToken)
		if err != nil {
			t.Fatalf("request failed: %v", err)
		}

		if resp.StatusCode != http.StatusNotFound {
			t.Errorf("expected 404, got %d", resp.StatusCode)
		}
	})
}
