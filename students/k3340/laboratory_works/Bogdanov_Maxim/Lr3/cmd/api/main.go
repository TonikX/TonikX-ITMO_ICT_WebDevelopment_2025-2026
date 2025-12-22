// @title           School Management Service API
// @version         1.0
// @description     API для управления школьной системой

// @host      localhost:8080
// @BasePath  /api/v1

// @securityDefinitions.apikey BearerAuth
// @in header
// @name Authorization
// @description Type "Bearer" followed by a space and JWT token.

package main

import (
	"context"
	"errors"
	"fmt"
	"net/http"
	"os"
	"os/signal"
	"syscall"
	"time"

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

func main() {
	cfg, err := config.Load()
	if err != nil {
		panic(fmt.Sprintf("failed to load config: %v", err))
	}

	log := logger.New(cfg.Logging.Level, cfg.Logging.Format, cfg.Logging.AddSource)
	log.Info("Starting application", "name", cfg.App.Name, "env", cfg.App.Env)

	appClock := clock.NewRealClock()

	// Подключение к БД
	db, err := database.New(cfg.Database, log)
	if err != nil {
		log.Error("Failed to connect to database", "error", err)
		panic(fmt.Sprintf("failed to connect to database: %v", err))
	}
	defer func(db *database.DB) {
		_ = db.Close()
	}(db)

	// Инициализация репозиториев
	teacherRepo := repository.NewTeacherRepository(db.DB, appClock)
	studentRepo := repository.NewStudentRepository(db.DB, appClock)
	classRepo := repository.NewClassRepository(db.DB, appClock)
	scheduleRepo := repository.NewScheduleRepository(db.DB, appClock)
	gradeRepo := repository.NewGradeRepository(db.DB, appClock)
	infoRepo := repository.NewInfoRepository(db.DB, appClock)
	reportRepo := repository.NewReportRepository(db.DB, appClock)
	userRepo := repository.NewUserRepository(db.DB, appClock)
	refreshTokenRepo := repository.NewRefreshTokenRepository(db.DB, appClock)
	referenceRepo := repository.NewReferenceRepository(db.DB)

	passwordHasher := password.NewBcryptHasher(0)
	jwtService := jwt.NewJWTService(jwt.JWTConfig{
		AccessSecret:  cfg.JWT.Secret,
		RefreshSecret: cfg.JWT.Secret,
		AccessTTL:     cfg.JWT.AccessTokenTTL,
		RefreshTTL:    cfg.JWT.RefreshTokenTTL,
		Clock:         appClock,
	})

	teacherUC := usecase.NewTeacherUseCase(teacherRepo, appClock, log)
	studentUC := usecase.NewStudentUseCase(studentRepo, appClock, log)
	classUC := usecase.NewClassUseCase(classRepo, appClock, log)
	scheduleUC := usecase.NewScheduleUseCase(scheduleRepo, appClock, log)
	gradeUC := usecase.NewGradeUseCase(gradeRepo, appClock, log)
	infoUC := usecase.NewInfoUseCase(infoRepo, teacherRepo, log)
	reportUC := usecase.NewReportUseCase(reportRepo, teacherRepo, log)
	authUC := usecase.NewAuthUseCase(userRepo, refreshTokenRepo, passwordHasher, jwtService, appClock, log, cfg.JWT.RefreshTokenTTL)
	referenceUC := usecase.NewReferenceUseCase(referenceRepo)

	// Настройка HTTP роутера
	router := httphandler.Router(cfg, db, appClock, log, jwtService, teacherUC, studentUC, classUC, scheduleUC, gradeUC, infoUC, reportUC, authUC, referenceUC)

	// Запуск HTTP сервера
	addr := fmt.Sprintf("%s:%d", cfg.HTTP.Host, cfg.HTTP.Port)
	srv := &http.Server{
		Addr:         addr,
		Handler:      router,
		ReadTimeout:  cfg.HTTP.ReadTimeout,
		WriteTimeout: cfg.HTTP.WriteTimeout,
		IdleTimeout:  cfg.HTTP.IdleTimeout,
	}

	go func() {
		log.Info("Starting HTTP server", "address", addr)
		if err := srv.ListenAndServe(); err != nil && !errors.Is(err, http.ErrServerClosed) {
			log.Error("HTTP server error", "error", err)
			panic(fmt.Sprintf("HTTP server error: %v", err))
		}
	}()

	// Graceful shutdown
	quit := make(chan os.Signal, 1)
	signal.Notify(quit, syscall.SIGINT, syscall.SIGTERM)
	<-quit

	log.Info("Shutting down server...")

	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()

	if err := srv.Shutdown(ctx); err != nil {
		log.Error("Server forced to shutdown", "error", err)
	}

	log.Info("Server stopped")
}
