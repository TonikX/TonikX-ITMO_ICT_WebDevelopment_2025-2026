package storage

import (
	"encoding/json"
	"os"
	"sync"
	"time"
)

type SubjectRecord struct {
	Grades  []int  `json:"grades"`
	Updated string `json:"updated"`
}

var (
	dbPath  string
	mu      sync.Mutex
	journal map[string]SubjectRecord
)

func Init(path string) error {
	dbPath = path
	journal = map[string]SubjectRecord{}
	_ = load()
	return nil
}

func load() error {
	mu.Lock()
	defer mu.Unlock()
	f, err := os.Open(dbPath)
	if err != nil {
		if os.IsNotExist(err) {
			journal = map[string]SubjectRecord{}
			return nil
		}
		return err
	}
	defer f.Close()
	var m map[string]SubjectRecord
	if err := json.NewDecoder(f).Decode(&m); err != nil {
		journal = map[string]SubjectRecord{}
		return nil
	}
	journal = m
	return nil
}

func saveLocked() error {
	tmp := dbPath + ".tmp"
	b, _ := json.MarshalIndent(journal, "", "  ")
	if err := os.WriteFile(tmp, b, 0o644); err != nil {
		return err
	}
	return os.Rename(tmp, dbPath)
}

func AddGrade(subject string, grade int) error {
	mu.Lock()
	defer mu.Unlock()
	rec := journal[subject]
	rec.Grades = append(rec.Grades, grade)
	rec.Updated = time.Now().Format(time.RFC3339)
	journal[subject] = rec
	return saveLocked()
}

func Snapshot() map[string]SubjectRecord {
	mu.Lock()
	defer mu.Unlock()
	out := make(map[string]SubjectRecord, len(journal))
	for k, v := range journal {
		cp := make([]int, len(v.Grades))
		copy(cp, v.Grades)
		out[k] = SubjectRecord{Grades: cp, Updated: v.Updated}
	}
	return out
}
