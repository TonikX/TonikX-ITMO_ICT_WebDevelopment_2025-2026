package repository

import (
	"context"
	"database/sql"
	"time"

	"github.com/Masterminds/squirrel"
	"school-service/internal/domain"
	"school-service/internal/domain/clock"
	"school-service/internal/domain/repository"
)

var _ repository.RefreshTokenRepository = (*RefreshTokenRepository)(nil)

// RefreshTokenRepository реализация репозитория refresh токенов
type RefreshTokenRepository struct {
	db      *sql.DB
	builder squirrel.StatementBuilderType
	clock   clock.Clock
}

// NewRefreshTokenRepository создает новый репозиторий refresh токенов
func NewRefreshTokenRepository(db *sql.DB, clock clock.Clock) *RefreshTokenRepository {
	return &RefreshTokenRepository{
		db:      db,
		builder: squirrel.StatementBuilder.PlaceholderFormat(squirrel.Dollar),
		clock:   clock,
	}
}

// Create создает новый refresh токен
func (r *RefreshTokenRepository) Create(ctx context.Context, token *domain.RefreshToken) error {
	now := r.clock.Now()
	token.CreatedAt = now
	token.UpdatedAt = now

	query := r.builder.
		Insert("auth_refresh_tokens").
		Columns("user_id", "token_hash", "issued_at", "expires_at", "created_at", "updated_at").
		Values(
			token.UserID,
			token.TokenHash,
			token.IssuedAt,
			token.ExpiresAt,
			token.CreatedAt,
			token.UpdatedAt,
		).
		Suffix("RETURNING id")

	var id int
	err := query.RunWith(r.db).QueryRowContext(ctx).Scan(&id)
	if err != nil {
		return domain.NewError(domain.ErrorCodeInternal, err, "RefreshToken", "token_hash", token.TokenHash, "failed to create refresh token", nil)
	}

	token.SetID(id)
	return nil
}

// GetByTokenHash получает токен по хешу
func (r *RefreshTokenRepository) GetByTokenHash(ctx context.Context, tokenHash string) (*domain.RefreshToken, error) {
	query := r.builder.
		Select("id", "user_id", "token_hash", "issued_at", "expires_at", "revoked_at", "created_at", "updated_at").
		From("auth_refresh_tokens").
		Where(squirrel.Eq{"token_hash": tokenHash})

	var token domain.RefreshToken
	var revokedAt sql.NullTime

	err := query.RunWith(r.db).QueryRowContext(ctx).Scan(
		&token.ID,
		&token.UserID,
		&token.TokenHash,
		&token.IssuedAt,
		&token.ExpiresAt,
		&revokedAt,
		&token.CreatedAt,
		&token.UpdatedAt,
	)
	if err != nil {
		if err == sql.ErrNoRows {
			return nil, domain.NewNotFoundError("RefreshToken", "token_hash", tokenHash, "refresh token not found")
		}
		return nil, domain.NewError(domain.ErrorCodeInternal, err, "RefreshToken", "token_hash", tokenHash, "failed to get refresh token", nil)
	}

	if revokedAt.Valid {
		token.RevokedAt = &revokedAt.Time
	}

	return &token, nil
}

// GetByUserID получает все активные токены пользователя
func (r *RefreshTokenRepository) GetByUserID(ctx context.Context, userID int) ([]*domain.RefreshToken, error) {
	query := r.builder.
		Select("id", "user_id", "token_hash", "issued_at", "expires_at", "revoked_at", "created_at", "updated_at").
		From("auth_refresh_tokens").
		Where(squirrel.Eq{"user_id": userID}).
		OrderBy("created_at DESC")

	rows, err := query.RunWith(r.db).QueryContext(ctx)
	if err != nil {
		return nil, domain.NewError(domain.ErrorCodeInternal, err, "RefreshToken", "user_id", userID, "failed to get refresh tokens", nil)
	}
	defer rows.Close()

	var tokens []*domain.RefreshToken
	for rows.Next() {
		var token domain.RefreshToken
		var revokedAt sql.NullTime

		err := rows.Scan(
			&token.ID,
			&token.UserID,
			&token.TokenHash,
			&token.IssuedAt,
			&token.ExpiresAt,
			&revokedAt,
			&token.CreatedAt,
			&token.UpdatedAt,
		)
		if err != nil {
			return nil, domain.NewError(domain.ErrorCodeInternal, err, "RefreshToken", "user_id", userID, "failed to scan refresh token", nil)
		}

		if revokedAt.Valid {
			token.RevokedAt = &revokedAt.Time
		}

		tokens = append(tokens, &token)
	}

	if err = rows.Err(); err != nil {
		return nil, domain.NewError(domain.ErrorCodeInternal, err, "RefreshToken", "user_id", userID, "failed to iterate refresh tokens", nil)
	}

	return tokens, nil
}

// Revoke отзывает токен
func (r *RefreshTokenRepository) Revoke(ctx context.Context, tokenHash string) error {
	now := r.clock.Now()

	query := r.builder.
		Update("auth_refresh_tokens").
		Set("revoked_at", now).
		Set("updated_at", now).
		Where(squirrel.Eq{"token_hash": tokenHash}).
		Where(squirrel.Expr("revoked_at IS NULL"))

	result, err := query.RunWith(r.db).ExecContext(ctx)
	if err != nil {
		return domain.NewError(domain.ErrorCodeInternal, err, "RefreshToken", "token_hash", tokenHash, "failed to revoke refresh token", nil)
	}

	rowsAffected, err := result.RowsAffected()
	if err != nil {
		return domain.NewError(domain.ErrorCodeInternal, err, "RefreshToken", "token_hash", tokenHash, "failed to get rows affected", nil)
	}

	if rowsAffected == 0 {
		return domain.NewNotFoundError("RefreshToken", "token_hash", tokenHash, "refresh token not found")
	}

	return nil
}

// RevokeAllForUser отзывает все токены пользователя
func (r *RefreshTokenRepository) RevokeAllForUser(ctx context.Context, userID int) error {
	now := r.clock.Now()

	query := r.builder.
		Update("auth_refresh_tokens").
		Set("revoked_at", now).
		Set("updated_at", now).
		Where(squirrel.Eq{"user_id": userID}).
		Where(squirrel.Expr("revoked_at IS NULL"))

	_, err := query.RunWith(r.db).ExecContext(ctx)
	if err != nil {
		return domain.NewError(domain.ErrorCodeInternal, err, "RefreshToken", "user_id", userID, "failed to revoke all refresh tokens", nil)
	}

	return nil
}

// DeleteExpired удаляет истекшие токены
func (r *RefreshTokenRepository) DeleteExpired(ctx context.Context, before time.Time) error {
	query := r.builder.
		Delete("auth_refresh_tokens").
		Where(squirrel.Lt{"expires_at": before})

	_, err := query.RunWith(r.db).ExecContext(ctx)
	if err != nil {
		return domain.NewError(domain.ErrorCodeInternal, err, "RefreshToken", "", "", "failed to delete expired refresh tokens", nil)
	}

	return nil
}
