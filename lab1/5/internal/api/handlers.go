package api

import (
	"encoding/json"
	"grades/internal/httpserver"
	"grades/internal/storage"
	"grades/internal/util"
	"net"
	"net/url"
)

func RegisterRoutes(r *httpserver.Router) {
	r.GET("/api/grades", getGrades)
	r.POST("/api/grades", postGrades)
}

func getGrades(c net.Conn, req *httpserver.Request) bool {
	data := storage.Snapshot()
	httpserver.WriteJSON(c, httpserver.StatusOK, httpserver.H{"data": data})
	return true
}

func postGrades(c net.Conn, req *httpserver.Request) bool {
	ctype := httpserver.Header(req, "content-type")
	var subject, gradeStr string

	switch {
	case util.HasPrefixFold(ctype, "application/json"):
		var in struct {
			Subject string `json:"subject"`
			Grade   any    `json:"grade"`
		}
		if err := json.Unmarshal(req.Body, &in); err != nil {
			httpserver.WriteJSON(c, httpserver.StatusBadRequest, httpserver.H{"error": "некорректный JSON"})
			return true
		}
		subject = in.Subject
		switch v := in.Grade.(type) {
		case float64:
			gradeStr = util.Itoa(int(v))
		case string:
			gradeStr = v
		default:
			gradeStr = util.Sprint(v)
		}
	case util.HasPrefixFold(ctype, "application/x-www-form-urlencoded"):
		vals, err := url.ParseQuery(string(req.Body))
		if err != nil {
			httpserver.WriteJSON(c, httpserver.StatusBadRequest, httpserver.H{"error": "некорректная форма"})
			return true
		}
		subject = vals.Get("subject")
		gradeStr = vals.Get("grade")
	default:
		httpserver.WriteJSON(c, httpserver.StatusUnsupportedMedia, httpserver.H{"error": "поддерживаются JSON и x-www-form-urlencoded"})
		return true
	}

	// Валидация
	subj, err := util.ValidateSubject(subject)
	if err != nil {
		httpserver.WriteJSON(c, httpserver.StatusBadRequest, httpserver.H{"error": err.Error()})
		return true
	}
	grade, err := util.ValidateGrade(gradeStr)
	if err != nil {
		httpserver.WriteJSON(c, httpserver.StatusBadRequest, httpserver.H{"error": err.Error()})
		return true
	}

	if err := storage.AddGrade(subj, grade); err != nil {
		httpserver.WriteJSON(c, httpserver.StatusInternalServerError, httpserver.H{"error": "не удалось сохранить"})
		return true
	}

	httpserver.WriteJSON(c, httpserver.StatusCreated, httpserver.H{"ok": true, "message": "оценка добавлена"})
	return true
}
