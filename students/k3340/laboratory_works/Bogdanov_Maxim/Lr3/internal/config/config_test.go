package config

import (
	"os"
	"testing"
	"time"
)

func TestLoad_Defaults(t *testing.T) {
	clearEnv()
	cfg, err := Load()
	if err != nil {
		t.Fatalf("Load() failed: %v", err)
	}

	if cfg.App.Name != defaultAppName {
		t.Errorf("expected App.Name = %s, got %s", defaultAppName, cfg.App.Name)
	}
	if cfg.App.Env != defaultAppEnv {
		t.Errorf("expected App.Env = %s, got %s", defaultAppEnv, cfg.App.Env)
	}
	if cfg.Database.Host != defaultDBHost {
		t.Errorf("expected Database.Host = %s, got %s", defaultDBHost, cfg.Database.Host)
	}
	if cfg.Database.Port != defaultDBPort {
		t.Errorf("expected Database.Port = %d, got %d", defaultDBPort, cfg.Database.Port)
	}

	if len(cfg.CORS.AllowedOrigins) == 0 || cfg.CORS.AllowedOrigins[0] != "*" {
		t.Errorf("expected CORS.AllowedOrigins = [*], got %v", cfg.CORS.AllowedOrigins)
	}
	if len(cfg.CORS.AllowedMethods) == 0 {
		t.Error("expected CORS.AllowedMethods to be set")
	}
	if cfg.CORS.MaxAge != 300 {
		t.Errorf("expected CORS.MaxAge = 300, got %d", cfg.CORS.MaxAge)
	}
}

func TestLoad_FromEnv(t *testing.T) {
	clearEnv()
	_ = os.Setenv("APP_NAME", "test-app")
	_ = os.Setenv("DB_HOST", "test-host")
	_ = os.Setenv("DB_PORT", "5433")
	_ = os.Setenv("LOG_LEVEL", "debug")
	defer clearEnv()

	cfg, err := Load()
	if err != nil {
		t.Fatalf("Load() failed: %v", err)
	}

	if cfg.App.Name != "test-app" {
		t.Errorf("expected App.Name = test-app, got %s", cfg.App.Name)
	}
	if cfg.Database.Host != "test-host" {
		t.Errorf("expected Database.Host = test-host, got %s", cfg.Database.Host)
	}
	if cfg.Database.Port != 5433 {
		t.Errorf("expected Database.Port = 5433, got %d", cfg.Database.Port)
	}
	if cfg.Logging.Level != "debug" {
		t.Errorf("expected Logging.Level = debug, got %s", cfg.Logging.Level)
	}
}

func TestLoad_CORSFromEnv(t *testing.T) {
	clearEnv()
	_ = os.Setenv("CORS_ALLOWED_ORIGINS", "http://localhost:3000,http://localhost:3001")
	_ = os.Setenv("CORS_ALLOWED_METHODS", "GET,POST")
	_ = os.Setenv("CORS_ALLOW_CREDENTIALS", "true")
	_ = os.Setenv("CORS_MAX_AGE", "600")
	defer clearEnv()

	cfg, err := Load()
	if err != nil {
		t.Fatalf("Load() failed: %v", err)
	}

	if len(cfg.CORS.AllowedOrigins) != 2 {
		t.Errorf("expected 2 allowed origins, got %d", len(cfg.CORS.AllowedOrigins))
	}
	if cfg.CORS.AllowedOrigins[0] != "http://localhost:3000" {
		t.Errorf("expected first origin = http://localhost:3000, got %s", cfg.CORS.AllowedOrigins[0])
	}
	if len(cfg.CORS.AllowedMethods) != 2 {
		t.Errorf("expected 2 allowed methods, got %d", len(cfg.CORS.AllowedMethods))
	}
	if !cfg.CORS.AllowCredentials {
		t.Error("expected AllowCredentials = true")
	}
	if cfg.CORS.MaxAge != 600 {
		t.Errorf("expected MaxAge = 600, got %d", cfg.CORS.MaxAge)
	}
}

func TestLoad_InvalidInt(t *testing.T) {
	clearEnv()
	_ = os.Setenv("DB_PORT", "invalid")
	defer clearEnv()

	cfg, err := Load()
	if err != nil {
		t.Fatalf("Load() failed: %v", err)
	}

	if cfg.Database.Port != defaultDBPort {
		t.Errorf("expected Database.Port = %d (default), got %d", defaultDBPort, cfg.Database.Port)
	}
}

func TestLoad_InvalidBool(t *testing.T) {
	clearEnv()
	_ = os.Setenv("APP_DEBUG", "invalid")
	defer clearEnv()

	cfg, err := Load()
	if err != nil {
		t.Fatalf("Load() failed: %v", err)
	}

	if cfg.App.Debug != true {
		t.Errorf("expected App.Debug = true (default), got %v", cfg.App.Debug)
	}
}

func TestLoad_InvalidDuration(t *testing.T) {
	clearEnv()
	_ = os.Setenv("READ_TIMEOUT", "invalid")
	defer clearEnv()

	cfg, err := Load()
	if err != nil {
		t.Fatalf("Load() failed: %v", err)
	}

	expected := defaultHTTPReadTimeoutSec * time.Second
	if cfg.HTTP.ReadTimeout != expected {
		t.Errorf("expected HTTP.ReadTimeout = %v (default), got %v", expected, cfg.HTTP.ReadTimeout)
	}
}

func TestLoad_ValidDuration(t *testing.T) {
	clearEnv()
	_ = os.Setenv("READ_TIMEOUT", "30s")
	defer clearEnv()

	cfg, err := Load()
	if err != nil {
		t.Fatalf("Load() failed: %v", err)
	}

	expected := 30 * time.Second
	if cfg.HTTP.ReadTimeout != expected {
		t.Errorf("expected HTTP.ReadTimeout = %v, got %v", expected, cfg.HTTP.ReadTimeout)
	}
}

func TestValidate_RequiredFields(t *testing.T) {
	tests := []struct {
		name    string
		cfg     *Config
		wantErr bool
		errMsg  string
	}{
		{
			name: "valid config",
			cfg: &Config{
				Database: DatabaseConfig{
					Host:     "localhost",
					User:     "postgres",
					Password: "password",
					Name:     "test_db",
				},
				App: AppConfig{Env: "development"},
			},
			wantErr: false,
		},
		{
			name: "missing DB_HOST",
			cfg: &Config{
				Database: DatabaseConfig{
					User:     "postgres",
					Password: "password",
					Name:     "test_db",
				},
			},
			wantErr: true,
			errMsg:  "DB_HOST is required",
		},
		{
			name: "missing DB_USER",
			cfg: &Config{
				Database: DatabaseConfig{
					Host:     "localhost",
					Password: "password",
					Name:     "test_db",
				},
			},
			wantErr: true,
			errMsg:  "DB_USER is required",
		},
		{
			name: "missing DB_PASSWORD",
			cfg: &Config{
				Database: DatabaseConfig{
					Host: "localhost",
					User: "postgres",
					Name: "test_db",
				},
			},
			wantErr: true,
			errMsg:  "DB_PASSWORD is required",
		},
		{
			name: "missing DB_NAME",
			cfg: &Config{
				Database: DatabaseConfig{
					Host:     "localhost",
					User:     "postgres",
					Password: "password",
				},
			},
			wantErr: true,
			errMsg:  "DB_NAME is required",
		},
		{
			name: "production with default JWT secret",
			cfg: &Config{
				Database: DatabaseConfig{
					Host:     "localhost",
					User:     "postgres",
					Password: "password",
					Name:     "test_db",
				},
				App: AppConfig{Env: "production"},
				JWT: JWTConfig{Secret: defaultJWTSecret},
			},
			wantErr: true,
			errMsg:  "JWT_SECRET must be set",
		},
		{
			name: "production with empty JWT secret",
			cfg: &Config{
				Database: DatabaseConfig{
					Host:     "localhost",
					User:     "postgres",
					Password: "password",
					Name:     "test_db",
				},
				App: AppConfig{Env: "production"},
				JWT: JWTConfig{Secret: ""},
			},
			wantErr: true,
			errMsg:  "JWT_SECRET must be set",
		},
		{
			name: "production with custom JWT secret",
			cfg: &Config{
				Database: DatabaseConfig{
					Host:     "localhost",
					User:     "postgres",
					Password: "password",
					Name:     "test_db",
				},
				App: AppConfig{Env: "production"},
				JWT: JWTConfig{Secret: "custom-secret-key"},
			},
			wantErr: false,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			err := tt.cfg.validate()
			if tt.wantErr {
				if err == nil {
					t.Errorf("expected error, got nil")
				} else if !contains(err.Error(), tt.errMsg) {
					t.Errorf("expected error to contain '%s', got '%s'", tt.errMsg, err.Error())
				}
			} else {
				if err != nil {
					t.Errorf("unexpected error: %v", err)
				}
			}
		})
	}
}

func TestDSN(t *testing.T) {
	cfg := DatabaseConfig{
		Host:     "localhost",
		Port:     5432,
		User:     "postgres",
		Password: "password",
		Name:     "test_db",
		SSLMode:  "require",
	}

	dsn := cfg.DSN()
	expected := "host=localhost port=5432 user=postgres password=password dbname=test_db sslmode=require"

	if dsn != expected {
		t.Errorf("expected DSN = %s, got %s", expected, dsn)
	}
}

func clearEnv() {
	envVars := []string{
		"APP_NAME", "APP_ENV", "APP_DEBUG",
		"DB_HOST", "DB_PORT", "DB_USER", "DB_PASSWORD", "DB_NAME", "DB_SSLMODE",
		"DB_MAX_OPEN_CONNS", "DB_MAX_IDLE_CONNS", "DB_CONN_MAX_LIFETIME",
		"JWT_SECRET", "JWT_ACCESS_TOKEN_TTL", "JWT_REFRESH_TOKEN_TTL",
		"LOG_LEVEL", "LOG_FORMAT", "LOG_ADD_SOURCE",
		"HTTP_PORT", "HTTP_HOST", "READ_TIMEOUT", "WRITE_TIMEOUT", "IDLE_TIMEOUT",
		"CORS_ALLOWED_ORIGINS", "CORS_ALLOWED_METHODS", "CORS_ALLOWED_HEADERS",
		"CORS_EXPOSED_HEADERS", "CORS_ALLOW_CREDENTIALS", "CORS_MAX_AGE",
	}
	for _, key := range envVars {
		_ = os.Unsetenv(key)
	}
}

func contains(s, substr string) bool {
	return len(s) >= len(substr) && (s == substr || len(substr) == 0 || len(s) > len(substr) && (s[:len(substr)] == substr || s[len(s)-len(substr):] == substr || containsMiddle(s, substr)))
}

func containsMiddle(s, substr string) bool {
	for i := 0; i <= len(s)-len(substr); i++ {
		if s[i:i+len(substr)] == substr {
			return true
		}
	}
	return false
}
