package password

import (
	"errors"
	"testing"

	"school-service/internal/domain"
)

func TestBcryptHasher_Hash(t *testing.T) {
	hasher := NewBcryptHasher(0)

	tests := []struct {
		name     string
		password string
		wantErr  bool
	}{
		{
			name:     "successful hash",
			password: "password123",
			wantErr:  false,
		},
		{
			name:     "empty password",
			password: "",
			wantErr:  false,
		},
		{
			name:     "long password",
			password: "very_long_password_that_exceeds_normal_length_requirements_123456789",
			wantErr:  false,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			hash, err := hasher.Hash(tt.password)

			if tt.wantErr {
				if err == nil {
					t.Error("expected error, got nil")
				}
				return
			}

			if err != nil {
				t.Fatalf("unexpected error: %v", err)
			}

			if hash == "" {
				t.Error("expected non-empty hash")
			}

			if hash == tt.password {
				t.Error("expected hash to be different from password")
			}
		})
	}
}

func TestBcryptHasher_Verify(t *testing.T) {
	hasher := NewBcryptHasher(0)

	tests := []struct {
		name           string
		password       string
		hashedPassword string
		wantErr        bool
	}{
		{
			name:           "successful verification",
			password:       "password123",
			hashedPassword: "",
			wantErr:        false,
		},
		{
			name:           "wrong password",
			password:       "wrongpassword",
			hashedPassword: "",
			wantErr:        true,
		},
		{
			name:           "empty password",
			password:       "",
			hashedPassword: "",
			wantErr:        false,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			hashedPassword := tt.hashedPassword
			if hashedPassword == "" {
				var err error
				hashedPassword, err = hasher.Hash(tt.password)
				if err != nil {
					t.Fatalf("failed to hash password: %v", err)
				}
			}

			if tt.name == "wrong password" {
				hashedPassword, _ = hasher.Hash("correctpassword")
			}

			err := hasher.Verify(hashedPassword, tt.password)

			if tt.wantErr {
				if err == nil {
					t.Error("expected error, got nil")
				}
				var domainErr *domain.Error
				if !errors.As(err, &domainErr) {
					t.Error("expected domain error")
				}
				return
			}

			if err != nil {
				t.Fatalf("unexpected error: %v", err)
			}
		})
	}
}

func TestBcryptHasher_HashConsistency(t *testing.T) {
	hasher := NewBcryptHasher(0)
	password := "test_password_123"

	hash1, err1 := hasher.Hash(password)
	if err1 != nil {
		t.Fatalf("failed to hash: %v", err1)
	}

	hash2, err2 := hasher.Hash(password)
	if err2 != nil {
		t.Fatalf("failed to hash: %v", err2)
	}

	if hash1 == hash2 {
		t.Error("bcrypt should generate different hashes for same password (salt)")
	}

	err1 = hasher.Verify(hash1, password)
	if err1 != nil {
		t.Errorf("failed to verify hash1: %v", err1)
	}

	err2 = hasher.Verify(hash2, password)
	if err2 != nil {
		t.Errorf("failed to verify hash2: %v", err2)
	}
}
