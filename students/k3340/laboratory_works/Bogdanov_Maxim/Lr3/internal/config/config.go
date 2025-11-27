package config

import (
	"fmt"
	"os"
	"strconv"
	"time"
)

const (
	defaultAppName              = "school-service"
	defaultAppEnv               = "development"
	defaultDBHost               = "localhost"
	defaultDBPort               = 5432
	defaultDBUser               = "postgres"
	defaultDBPassword           = "postgres"
	defaultDBName               = "school_db"
	defaultDBSSLMode            = "disable"
	defaultDBMaxOpenConns       = 25
	defaultDBMaxIdleConns       = 5
	defaultDBConnMaxLifetimeMin = 5
	defaultJWTSecret            = "your-secret-key-change-in-production"
	defaultJWTAccessTokenTTLMin = 15
	defaultJWTRefreshTokenTTLHr = 168
	defaultLogLevel             = "info"
	defaultLogFormat            = "json"
	defaultHTTPPort             = 8080
	defaultHTTPHost             = "0.0.0.0"
	defaultHTTPReadTimeoutSec   = 15
	defaultHTTPWriteTimeoutSec  = 15
	defaultHTTPIdleTimeoutSec   = 60
)

// Config содержит всю конфигурацию приложения
type Config struct {
	App      AppConfig
	Database DatabaseConfig
	JWT      JWTConfig
	Logging  LoggingConfig
	HTTP     HTTPConfig
}

// AppConfig содержит конфигурацию уровня приложения
type AppConfig struct {
	Name  string
	Env   string
	Debug bool
}

// DatabaseConfig содержит конфигурацию базы данных
type DatabaseConfig struct {
	Host            string
	Port            int
	User            string
	Password        string
	Name            string
	SSLMode         string
	MaxOpenConns    int
	MaxIdleConns    int
	ConnMaxLifetime time.Duration
}

// DSN возвращает строку подключения к базе данных
func (d DatabaseConfig) DSN() string {
	return fmt.Sprintf("host=%s port=%d user=%s password=%s dbname=%s sslmode=%s",
		d.Host, d.Port, d.User, d.Password, d.Name, d.SSLMode)
}

// JWTConfig содержит конфигурацию JWT
type JWTConfig struct {
	Secret          string
	AccessTokenTTL  time.Duration
	RefreshTokenTTL time.Duration
}

// LoggingConfig содержит конфигурацию логирования
type LoggingConfig struct {
	Level  string
	Format string
}

// HTTPConfig содержит конфигурацию HTTP сервера
type HTTPConfig struct {
	Port         int
	Host         string
	ReadTimeout  time.Duration
	WriteTimeout time.Duration
	IdleTimeout  time.Duration
}

// Load загружает конфигурацию из переменных окружения
func Load() (*Config, error) {
	cfg := &Config{
		App: AppConfig{
			Name:  getEnv("APP_NAME", defaultAppName),
			Env:   getEnv("APP_ENV", defaultAppEnv),
			Debug: getEnvBool("APP_DEBUG", true),
		},
		Database: DatabaseConfig{
			Host:            getEnv("DB_HOST", defaultDBHost),
			Port:            getEnvInt("DB_PORT", defaultDBPort),
			User:            getEnv("DB_USER", defaultDBUser),
			Password:        getEnv("DB_PASSWORD", defaultDBPassword),
			Name:            getEnv("DB_NAME", defaultDBName),
			SSLMode:         getEnv("DB_SSLMODE", defaultDBSSLMode),
			MaxOpenConns:    getEnvInt("DB_MAX_OPEN_CONNS", defaultDBMaxOpenConns),
			MaxIdleConns:    getEnvInt("DB_MAX_IDLE_CONNS", defaultDBMaxIdleConns),
			ConnMaxLifetime: getEnvDuration("DB_CONN_MAX_LIFETIME", defaultDBConnMaxLifetimeMin*time.Minute),
		},
		JWT: JWTConfig{
			Secret:          getEnv("JWT_SECRET", defaultJWTSecret),
			AccessTokenTTL:  getEnvDuration("JWT_ACCESS_TOKEN_TTL", defaultJWTAccessTokenTTLMin*time.Minute),
			RefreshTokenTTL: getEnvDuration("JWT_REFRESH_TOKEN_TTL", defaultJWTRefreshTokenTTLHr*time.Hour),
		},
		Logging: LoggingConfig{
			Level:  getEnv("LOG_LEVEL", defaultLogLevel),
			Format: getEnv("LOG_FORMAT", defaultLogFormat),
		},
		HTTP: HTTPConfig{
			Port:         getEnvInt("HTTP_PORT", defaultHTTPPort),
			Host:         getEnv("HTTP_HOST", defaultHTTPHost),
			ReadTimeout:  getEnvDuration("READ_TIMEOUT", defaultHTTPReadTimeoutSec*time.Second),
			WriteTimeout: getEnvDuration("WRITE_TIMEOUT", defaultHTTPWriteTimeoutSec*time.Second),
			IdleTimeout:  getEnvDuration("IDLE_TIMEOUT", defaultHTTPIdleTimeoutSec*time.Second),
		},
	}

	if err := cfg.validate(); err != nil {
		return nil, fmt.Errorf("config validation failed: %w", err)
	}

	return cfg, nil
}

// validate валидирует конфигурацию
func (c *Config) validate() error {
	if c.Database.Host == "" {
		return fmt.Errorf("DB_HOST is required")
	}
	if c.Database.User == "" {
		return fmt.Errorf("DB_USER is required")
	}
	if c.Database.Password == "" {
		return fmt.Errorf("DB_PASSWORD is required")
	}
	if c.Database.Name == "" {
		return fmt.Errorf("DB_NAME is required")
	}
	if c.App.Env == "production" && (c.JWT.Secret == "" || c.JWT.Secret == defaultJWTSecret) {
		return fmt.Errorf("JWT_SECRET must be set to a secure value in production")
	}
	return nil
}

func getEnv(key, defaultValue string) string {
	if value := os.Getenv(key); value != "" {
		return value
	}
	return defaultValue
}

func getEnvInt(key string, defaultValue int) int {
	if value := os.Getenv(key); value != "" {
		if intValue, err := strconv.Atoi(value); err == nil {
			return intValue
		}
	}
	return defaultValue
}

func getEnvBool(key string, defaultValue bool) bool {
	if value := os.Getenv(key); value != "" {
		if boolValue, err := strconv.ParseBool(value); err == nil {
			return boolValue
		}
	}
	return defaultValue
}

func getEnvDuration(key string, defaultValue time.Duration) time.Duration {
	if value := os.Getenv(key); value != "" {
		if duration, err := time.ParseDuration(value); err == nil {
			return duration
		}
	}
	return defaultValue
}
