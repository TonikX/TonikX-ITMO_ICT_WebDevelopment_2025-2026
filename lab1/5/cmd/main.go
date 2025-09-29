package main

import (
	"fmt"
	"grades/internal/api"
	"grades/internal/httpserver"
	"grades/internal/static"
	"grades/internal/storage"
)

func main() {
	cfg := httpserver.Config{
		Addr:      "127.0.0.1:8080",
		PublicDir: "public",
	}

	// Инициализируем хранилище
	if err := storage.Init("grades.json"); err != nil {
		fmt.Println("storage init error:", err)
		return
	}

	// Роутер: регистрируем обработчики API и статику
	r := httpserver.NewRouter()
	api.RegisterRoutes(r)
	static.Register(r, cfg.PublicDir)

	// Запускаем сервер
	if err := httpserver.ListenAndServe(cfg, r); err != nil {
		fmt.Println("server error:", err)
	}
}
