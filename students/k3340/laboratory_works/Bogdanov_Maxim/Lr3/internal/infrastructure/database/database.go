package database

import (
	"context"
	"database/sql"
	"fmt"

	_ "github.com/lib/pq"
	"school-service/internal/config"
	"school-service/internal/domain/health"
	"school-service/internal/domain/logger"
)

var _ health.HealthChecker = (*DB)(nil)

// DB обертка над sql.DB
type DB struct {
	*sql.DB
	logger logger.Logger
}

// New создает новое подключение к БД
func New(cfg config.DatabaseConfig, log logger.Logger) (*DB, error) {
	db, err := sql.Open("postgres", cfg.DSN())
	if err != nil {
		return nil, fmt.Errorf("failed to open database: %w", err)
	}

	db.SetMaxOpenConns(cfg.MaxOpenConns)
	db.SetMaxIdleConns(cfg.MaxIdleConns)
	db.SetConnMaxLifetime(cfg.ConnMaxLifetime)
	db.SetConnMaxIdleTime(cfg.ConnMaxIdleTime)

	ctx, cancel := context.WithTimeout(context.Background(), cfg.PingTimeout)
	defer cancel()

	if err := db.PingContext(ctx); err != nil {
		_ = db.Close()
		return nil, fmt.Errorf("failed to ping database: %w", err)
	}

	log.Info("Database connection established",
		"host", cfg.Host,
		"port", cfg.Port,
		"database", cfg.Name,
		"max_open_conns", cfg.MaxOpenConns,
		"max_idle_conns", cfg.MaxIdleConns,
		"conn_max_lifetime", cfg.ConnMaxLifetime,
		"conn_max_idle_time", cfg.ConnMaxIdleTime,
		"ping_timeout", cfg.PingTimeout,
	)

	return &DB{
		DB:     db,
		logger: log,
	}, nil
}

// Close закрывает подключение к БД
func (d *DB) Close() error {
	if d.DB != nil {
		d.logger.Info("Closing database connection")
		return d.DB.Close()
	}
	return nil
}

// Health проверяет доступность БД
func (d *DB) Health(ctx context.Context) error {
	if err := d.PingContext(ctx); err != nil {
		d.logger.WithError(err).Error("Database health check failed")
		return fmt.Errorf("database ping failed: %w", err)
	}
	return nil
}
