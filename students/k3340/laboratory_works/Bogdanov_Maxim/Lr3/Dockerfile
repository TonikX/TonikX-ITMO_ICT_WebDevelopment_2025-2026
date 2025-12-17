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

# Generate Swagger documentation
RUN swag init -g cmd/api/main.go -o docs/swagger --parseDependency --parseInternal

# Build the application
RUN CGO_ENABLED=0 GOOS=linux go build -a -installsuffix cgo -o /app/bin/api ./cmd/api

# Final stage
FROM alpine:latest

WORKDIR /app

# Install ca-certificates and wget for health checks
RUN apk --no-cache add ca-certificates tzdata wget

# Copy the binary from builder
COPY --from=builder /app/bin/api /app/api

# Copy migrations
COPY --from=builder /app/migrations /app/migrations

# Copy Swagger documentation for Swagger UI
COPY --from=builder /app/docs/swagger /app/docs/swagger

# Expose port
EXPOSE 8080

# Run the application
CMD ["/app/api"]

