# Build stage
FROM golang:1.25-alpine AS builder

WORKDIR /app

# Install build dependencies
RUN apk add --no-cache git

# Install swag for Swagger documentation generation
RUN go install github.com/swaggo/swag/cmd/swag@latest

# Copy go mod files
COPY go.mod go.sum ./
RUN go mod download

# Copy source code
COPY . .

# Generate Swagger documentation (ignore errors for now)
RUN swag init -g cmd/api/main.go -o docs/swagger --parseDependency --parseInternal || true
# Ensure swagger.json exists (create empty if generation failed)
RUN mkdir -p docs/swagger && ([ -f docs/swagger/swagger.json ] || echo '{}' > docs/swagger/swagger.json)

# Build the application
RUN CGO_ENABLED=0 GOOS=linux go build -a -installsuffix cgo -o /app/bin/api ./cmd/api

# Build the seed binary
RUN CGO_ENABLED=0 GOOS=linux go build -a -installsuffix cgo -o /app/bin/seed ./cmd/seed

# Final stage
FROM alpine:latest

WORKDIR /app

# Install ca-certificates and wget for health checks
RUN apk --no-cache add ca-certificates tzdata wget

# Copy the binaries from builder
COPY --from=builder /app/bin/api /app/api
COPY --from=builder /app/bin/seed /app/seed

# Copy migrations
COPY --from=builder /app/migrations /app/migrations

# Copy Swagger documentation for Swagger UI
RUN mkdir -p /app/docs/swagger
COPY --from=builder /app/docs/swagger/swagger.json /app/docs/swagger/swagger.json

# Expose port
EXPOSE 8080

# Run the application
CMD ["/app/api"]

