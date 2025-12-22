package repository

import (
	"context"
	"database/sql"

	"github.com/Masterminds/squirrel"
	"school-service/internal/domain"
	"school-service/internal/domain/clock"
	"school-service/internal/domain/repository"
)

var _ repository.UserRepository = (*UserRepository)(nil)

// UserRepository реализация репозитория пользователей
type UserRepository struct {
	db      *sql.DB
	builder squirrel.StatementBuilderType
	clock   clock.Clock
}

// NewUserRepository создает новый репозиторий пользователей
func NewUserRepository(db *sql.DB, clock clock.Clock) *UserRepository {
	return &UserRepository{
		db:      db,
		builder: squirrel.StatementBuilder.PlaceholderFormat(squirrel.Dollar),
		clock:   clock,
	}
}

// Create создает нового пользователя
func (r *UserRepository) Create(ctx context.Context, user *domain.User) error {
	now := r.clock.Now()
	user.CreatedAt = now
	user.UpdatedAt = now

	query := r.builder.
		Insert("auth_users").
		Columns("username", "email", "password_hash", "role", "teacher_id", "is_active", "created_at", "updated_at").
		Values(
			user.Username,
			user.Email,
			user.PasswordHash,
			user.Role.String(),
			user.TeacherID,
			user.IsActive,
			user.CreatedAt,
			user.UpdatedAt,
		).
		Suffix("RETURNING id")

	var id int
	err := query.RunWith(r.db).QueryRowContext(ctx).Scan(&id)
	if err != nil {
		return domain.NewAlreadyExistsError("User", "username", user.Username, "user with this username already exists")
	}

	user.SetID(id)
	return nil
}

// GetByID получает пользователя по ID
func (r *UserRepository) GetByID(ctx context.Context, id int) (*domain.User, error) {
	query := r.builder.
		Select("id", "username", "email", "password_hash", "role", "teacher_id", "is_active", "created_at", "updated_at", "deleted_at").
		From("auth_users").
		Where(squirrel.Eq{"id": id}).
		Where(squirrel.Expr("deleted_at IS NULL"))

	var user domain.User
	var email sql.NullString
	var teacherID sql.NullInt64
	var deletedAt sql.NullTime

	err := query.RunWith(r.db).QueryRowContext(ctx).Scan(
		&user.ID,
		&user.Username,
		&email,
		&user.PasswordHash,
		&user.Role,
		&teacherID,
		&user.IsActive,
		&user.CreatedAt,
		&user.UpdatedAt,
		&deletedAt,
	)
	if err != nil {
		if err == sql.ErrNoRows {
			return nil, domain.NewNotFoundError("User", "id", id, "user not found")
		}
		return nil, domain.NewError(domain.ErrorCodeInternal, err, "User", "id", id, "failed to get user", nil)
	}

	if email.Valid {
		user.Email = &email.String
	}
	if teacherID.Valid {
		id := int(teacherID.Int64)
		user.TeacherID = &id
	}
	if deletedAt.Valid {
		user.DeletedAt = &deletedAt.Time
	}

	return &user, nil
}

// GetByUsername получает пользователя по username
func (r *UserRepository) GetByUsername(ctx context.Context, username string) (*domain.User, error) {
	query := r.builder.
		Select("id", "username", "email", "password_hash", "role", "teacher_id", "is_active", "created_at", "updated_at", "deleted_at").
		From("auth_users").
		Where(squirrel.Eq{"username": username}).
		Where(squirrel.Expr("deleted_at IS NULL")).
		Where(squirrel.Eq{"is_active": true})

	var user domain.User
	var email sql.NullString
	var teacherID sql.NullInt64
	var deletedAt sql.NullTime

	err := query.RunWith(r.db).QueryRowContext(ctx).Scan(
		&user.ID,
		&user.Username,
		&email,
		&user.PasswordHash,
		&user.Role,
		&teacherID,
		&user.IsActive,
		&user.CreatedAt,
		&user.UpdatedAt,
		&deletedAt,
	)
	if err != nil {
		if err == sql.ErrNoRows {
			return nil, domain.NewNotFoundError("User", "username", username, "user not found")
		}
		return nil, domain.NewError(domain.ErrorCodeInternal, err, "User", "username", username, "failed to get user", nil)
	}

	if email.Valid {
		user.Email = &email.String
	}
	if teacherID.Valid {
		id := int(teacherID.Int64)
		user.TeacherID = &id
	}
	if deletedAt.Valid {
		user.DeletedAt = &deletedAt.Time
	}

	return &user, nil
}

// GetByEmail получает пользователя по email
func (r *UserRepository) GetByEmail(ctx context.Context, email string) (*domain.User, error) {
	query := r.builder.
		Select("id", "username", "email", "password_hash", "role", "teacher_id", "is_active", "created_at", "updated_at", "deleted_at").
		From("auth_users").
		Where(squirrel.Eq{"email": email}).
		Where(squirrel.Expr("deleted_at IS NULL")).
		Where(squirrel.Eq{"is_active": true})

	var user domain.User
	var emailVal sql.NullString
	var teacherID sql.NullInt64
	var deletedAt sql.NullTime

	err := query.RunWith(r.db).QueryRowContext(ctx).Scan(
		&user.ID,
		&user.Username,
		&emailVal,
		&user.PasswordHash,
		&user.Role,
		&teacherID,
		&user.IsActive,
		&user.CreatedAt,
		&user.UpdatedAt,
		&deletedAt,
	)
	if err != nil {
		if err == sql.ErrNoRows {
			return nil, domain.NewNotFoundError("User", "email", email, "user not found")
		}
		return nil, domain.NewError(domain.ErrorCodeInternal, err, "User", "email", email, "failed to get user", nil)
	}

	if emailVal.Valid {
		user.Email = &emailVal.String
	}
	if teacherID.Valid {
		id := int(teacherID.Int64)
		user.TeacherID = &id
	}
	if deletedAt.Valid {
		user.DeletedAt = &deletedAt.Time
	}

	return &user, nil
}

// Update обновляет пользователя
func (r *UserRepository) Update(ctx context.Context, user *domain.User) error {
	now := r.clock.Now()
	user.UpdatedAt = now

	query := r.builder.
		Update("auth_users").
		Set("username", user.Username).
		Set("email", user.Email).
		Set("password_hash", user.PasswordHash).
		Set("role", user.Role.String()).
		Set("teacher_id", user.TeacherID).
		Set("is_active", user.IsActive).
		Set("updated_at", user.UpdatedAt).
		Where(squirrel.Eq{"id": user.ID}).
		Where(squirrel.Expr("deleted_at IS NULL"))

	result, err := query.RunWith(r.db).ExecContext(ctx)
	if err != nil {
		return domain.NewError(domain.ErrorCodeInternal, err, "User", "id", user.ID, "failed to update user", nil)
	}

	rowsAffected, err := result.RowsAffected()
	if err != nil {
		return domain.NewError(domain.ErrorCodeInternal, err, "User", "id", user.ID, "failed to get rows affected", nil)
	}

	if rowsAffected == 0 {
		return domain.NewNotFoundError("User", "id", user.ID, "user not found")
	}

	return nil
}

// Delete выполняет soft delete пользователя
func (r *UserRepository) Delete(ctx context.Context, id int) error {
	now := r.clock.Now()

	query := r.builder.
		Update("auth_users").
		Set("deleted_at", now).
		Set("updated_at", now).
		Where(squirrel.Eq{"id": id}).
		Where(squirrel.Expr("deleted_at IS NULL"))

	result, err := query.RunWith(r.db).ExecContext(ctx)
	if err != nil {
		return domain.NewError(domain.ErrorCodeInternal, err, "User", "id", id, "failed to delete user", nil)
	}

	rowsAffected, err := result.RowsAffected()
	if err != nil {
		return domain.NewError(domain.ErrorCodeInternal, err, "User", "id", id, "failed to get rows affected", nil)
	}

	if rowsAffected == 0 {
		return domain.NewNotFoundError("User", "id", id, "user not found")
	}

	return nil
}
