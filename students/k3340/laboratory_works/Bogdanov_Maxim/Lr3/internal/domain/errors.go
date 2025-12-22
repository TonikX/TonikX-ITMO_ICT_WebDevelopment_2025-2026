package domain

import (
	"errors"
	"fmt"
)

type ErrorCode string

const (
	ErrorCodeNotFound      ErrorCode = "NOT_FOUND"
	ErrorCodeAlreadyExists ErrorCode = "ALREADY_EXISTS"
	ErrorCodeValidation    ErrorCode = "VALIDATION_ERROR"
	ErrorCodeDeleted       ErrorCode = "RESOURCE_DELETED"
	ErrorCodeInternal      ErrorCode = "INTERNAL_ERROR"
)

var (
	// ErrNotFound возвращается, когда запрашиваемый ресурс не найден
	ErrNotFound = errors.New("resource not found")

	// ErrAlreadyExists возвращается, когда пытаемся создать ресурс, который уже существует
	ErrAlreadyExists = errors.New("resource already exists")

	// ErrValidation возвращается при ошибках валидации данных
	ErrValidation = errors.New("validation error")

	// ErrDeleted возвращается, когда пытаемся работать с удаленной сущностью (soft delete)
	ErrDeleted = errors.New("resource is deleted")
)

// Error представляет доменную ошибку с контекстом
type Error struct {
	Code       ErrorCode
	BaseErr    error
	Entity     string
	Field      string
	Value      any
	Reason     string
	Additional map[string]any
}

// Error реализует интерфейс error
func (e *Error) Error() string {
	base := "domain error"
	if e.BaseErr != nil {
		base = e.BaseErr.Error()
	}

	switch {
	case e.Entity != "" && e.Field != "":
		return fmt.Sprintf("%s: entity=%s field=%s: %s (value=%v)", base, e.Entity, e.Field, e.Reason, e.Value)
	case e.Entity != "":
		return fmt.Sprintf("%s: entity=%s: %s", base, e.Entity, e.Reason)
	case e.Field != "":
		return fmt.Sprintf("%s: field=%s: %s (value=%v)", base, e.Field, e.Reason, e.Value)
	default:
		return fmt.Sprintf("%s: %s", base, e.Reason)
	}
}

// Unwrap возвращает базовую ошибку
func (e *Error) Unwrap() error {
	return e.BaseErr
}

// newError создает новую доменную ошибку
func newError(code ErrorCode, baseErr error, entity, field string, value any, reason string) *Error {
	return &Error{
		Code:    code,
		BaseErr: baseErr,
		Entity:  entity,
		Field:   field,
		Value:   value,
		Reason:  reason,
	}
}

// newErrorWithAdditional создает новую доменную ошибку с дополнительными данными
func newErrorWithAdditional(code ErrorCode, baseErr error, entity, field string, value any, reason string, additional map[string]any) *Error {
	return &Error{
		Code:       code,
		BaseErr:    baseErr,
		Entity:     entity,
		Field:      field,
		Value:      value,
		Reason:     reason,
		Additional: additional,
	}
}

// NewValidationError создает новую ошибку валидации
func NewValidationError(entity, field string, value any, reason string) *Error {
	return newError(ErrorCodeValidation, ErrValidation, entity, field, value, reason)
}

// NewNotFoundError создает новую ошибку "не найдено"
func NewNotFoundError(entity, field string, value any, reason string) *Error {
	return newError(ErrorCodeNotFound, ErrNotFound, entity, field, value, reason)
}

// NewAlreadyExistsError создает новую ошибку "уже существует"
func NewAlreadyExistsError(entity, field string, value any, reason string) *Error {
	return newError(ErrorCodeAlreadyExists, ErrAlreadyExists, entity, field, value, reason)
}

// NewDeletedError создает новую ошибку "ресурс удален"
func NewDeletedError(entity, field string, value any, reason string) *Error {
	return newError(ErrorCodeDeleted, ErrDeleted, entity, field, value, reason)
}

// NewError создает новую доменную ошибку (для внутренних ошибок)
func NewError(code ErrorCode, baseErr error, entity, field string, value any, reason string, additional map[string]any) *Error {
	if additional != nil {
		return newErrorWithAdditional(code, baseErr, entity, field, value, reason, additional)
	}
	return newError(code, baseErr, entity, field, value, reason)
}

// IsNotFound проверяет, является ли ошибка ошибкой "не найдено"
func IsNotFound(err error) bool {
	var domainErr *Error
	if errors.As(err, &domainErr) {
		return domainErr.Code == ErrorCodeNotFound
	}
	return false
}
