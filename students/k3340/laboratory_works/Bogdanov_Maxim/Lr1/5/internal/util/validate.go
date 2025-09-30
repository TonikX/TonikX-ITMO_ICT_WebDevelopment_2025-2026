package util

import (
	"errors"
	"fmt"
	"strconv"
	"strings"
	"unicode/utf8"
)

func ValidateSubject(s string) (string, error) {
	s = strings.TrimSpace(s)
	if s == "" {
		return "", errors.New("дисциплина не должна быть пустой")
	}
	if utf8.RuneCountInString(s) > 100 {
		return "", errors.New("слишком длинное название (макс 100)")
	}
	return s, nil
}

func ValidateGrade(s string) (int, error) {
	g, err := strconv.Atoi(strings.TrimSpace(s))
	if err != nil {
		return 0, errors.New("оценка должна быть числом")
	}
	if g < 2 || g > 5 {
		return 0, errors.New("оценка должна быть в диапазоне 2–5")
	}
	return g, nil
}

func HasPrefixFold(s, prefix string) bool {
	return strings.HasPrefix(strings.ToLower(s), strings.ToLower(prefix))
}
func Itoa(i int) string   { return strconv.Itoa(i) }
func Sprint(v any) string { return fmt.Sprint(v) }
