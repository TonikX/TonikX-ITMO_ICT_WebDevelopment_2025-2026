.PHONY: help build run test test-unit test-integration test-e2e lint fmt vet clean docker-up docker-down docker-logs migrate-up migrate-down coverage mocks ci check

# Variables
APP_NAME=school-service
DOCKER_COMPOSE=docker-compose
GO=go
GOLANGCI_LINT=golangci-lint

help: ## Show this help message
	@echo Usage: make [target]
	@echo Available targets:
	@echo   help              Show this help message
	@echo   build             Build the application
	@echo   run               Run the application
	@echo   test              Run all tests
	@echo   test-unit         Run unit tests only
	@echo   test-integration  Run integration tests
	@echo   test-e2e          Run E2E tests
	@echo   lint              Run linter
	@echo   lint-fix          Run linter fix
	@echo   fmt               Format code
	@echo   vet               Run go vet
	@echo   clean             Clean build artifacts
	@echo   docker-up         Start Docker containers
	@echo   docker-down       Stop Docker containers
	@echo   docker-logs       Show Docker logs
	@echo   migrate-up        Run database migrations up
	@echo   migrate-down      Rollback database migrations
	@echo   coverage          Generate coverage report
	@echo   mocks             Generate mocks
	@echo   ci                Run CI pipeline: lint, vet, test
	@echo   check             Run all checks: fmt, lint, vet, test

build: ## Build the application
	@echo Building $(APP_NAME)...
	$(GO) build -o bin/$(APP_NAME) ./cmd/api
	@echo Build complete!

run: ## Run the application
	@echo Running $(APP_NAME)...
	$(GO) run ./cmd/api

test: ## Run all tests
	@echo Running all tests...
	$(GO) test -v -race -coverprofile=coverage.out ./...
	@echo Tests complete!

test-unit: ## Run unit tests only
	@echo Running unit tests...
	$(GO) test -v -short -race ./internal/usecase/... ./internal/domain/...
	@echo Unit tests complete!

test-integration: ## Run integration tests
	@echo Running integration tests...
	$(GO) test -v -race -tags=integration ./internal/infrastructure/...
	@echo Integration tests complete!

test-e2e: ## Run E2E tests
	@echo Running E2E tests...
	$(GO) test -v -race -tags=e2e ./tests/e2e/...
	@echo E2E tests complete!

lint: ## Run linter
	@echo Running linter...
	$(GOLANGCI_LINT) run
	@echo Linting complete!

lint-fix: ## Run linter fix
	@echo Running linter fix...
	$(GOLANGCI_LINT) run --fix
	@echo Linting fix complete!

fmt: ## Format code
	@echo Formatting code...
	$(GO) fmt ./...
	@echo Formatting complete!

vet: ## Run go vet
	@echo Running go vet...
	$(GO) vet ./...
	@echo Vet complete!

clean: ## Clean build artifacts
	@echo Cleaning...
ifeq ($(OS),Windows_NT)
	if exist bin rmdir /s /q bin
	if exist coverage.out del /f coverage.out
	if exist coverage.html del /f coverage.html
else
	rm -rf bin/
	rm -f coverage.out coverage.html
endif
	$(GO) clean -cache -testcache
	@echo Clean complete!

docker-up: ## Start Docker containers
	@echo Starting Docker containers...
	$(DOCKER_COMPOSE) up -d
	@echo Docker containers started!

docker-down: ## Stop Docker containers
	@echo Stopping Docker containers...
	$(DOCKER_COMPOSE) down
	@echo Docker containers stopped!

docker-logs: ## Show Docker logs
	$(DOCKER_COMPOSE) logs -f

migrate-up: ## Run database migrations up
	@echo Running migrations up...
	migrate -path ./migrations -database "postgres://postgres:postgres@localhost:5432/school_db?sslmode=disable" up
	@echo Migrations complete!

migrate-down: ## Rollback database migrations
	@echo Rolling back migrations...
	migrate -path ./migrations -database "postgres://postgres:postgres@localhost:5432/school_db?sslmode=disable" down 1
	@echo Rollback complete!

coverage: test ## Generate coverage report
	@echo Generating coverage report...
	$(GO) tool cover -html=coverage.out -o coverage.html
	@echo Coverage report generated: coverage.html

mocks: ## Generate mocks
	@echo Generating mocks...
ifeq ($(OS),Windows_NT)
	@where mockgen >nul 2>&1 && (mockgen -source=internal/domain/repository/teacher.go -destination=internal/infrastructure/repository/mocks/teacher_repository_mock.go -package=mocks && echo Mocks generated!) || echo mockgen not found. Install with: go install go.uber.org/mock/mockgen@latest
else
	@if command -v mockgen > /dev/null; then \
		mockgen -source=internal/domain/repository/teacher.go -destination=internal/infrastructure/repository/mocks/teacher_repository_mock.go -package=mocks; \
		echo Mocks generated!; \
	else \
		echo mockgen not found. Install with: go install go.uber.org/mock/mockgen@latest; \
	fi
endif

ci: lint vet test ## Run CI pipeline (lint, vet, test)
	@echo CI pipeline complete!

swagger: ## Generate Swagger documentation
	@echo Generating Swagger docs...
	swag init -g cmd/api/main.go -o docs/swagger --parseDependency --parseInternal
	@echo Swagger docs generated!

check: fmt lint vet test ## Run all checks (fmt, lint, vet, test)
	@echo All checks complete!

