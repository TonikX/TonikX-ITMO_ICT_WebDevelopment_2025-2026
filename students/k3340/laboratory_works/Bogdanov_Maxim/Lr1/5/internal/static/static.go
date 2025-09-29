package static

import (
	"os"
	"path/filepath"
	"strings"

	"grades/internal/httpserver"
	"net"
)

var mimeByExt = map[string]string{
	".html": "text/html; charset=utf-8",
	".css":  "text/css; charset=utf-8",
	".js":   "application/javascript; charset=utf-8",
	".json": "application/json; charset=utf-8",
	".txt":  "text/plain; charset=utf-8",
}

func Register(r *httpserver.Router, publicDir string) {
	// index
	r.GET("/", func(c net.Conn, req *httpserver.Request) bool {
		return serve(c, publicDir, "/index.html")
	})
	r.GET("/index.html", func(c net.Conn, req *httpserver.Request) bool {
		return serve(c, publicDir, "/index.html")
	})
	// ассеты
	r.GET("/assets/*", func(c net.Conn, req *httpserver.Request) bool {
		return serve(c, publicDir, req.Path)
	})
}

func serve(c net.Conn, publicDir, rel string) bool {
	clean := filepath.Clean(rel)
	if clean == "/" {
		clean = "/index.html"
	}
	fpath := filepath.Join(publicDir, clean)
	// защита от выхода за public
	if !strings.HasPrefix(filepath.Clean(fpath), filepath.Clean(publicDir)+string(filepath.Separator)) &&
		filepath.Clean(fpath) != filepath.Clean(filepath.Join(publicDir, "index.html")) {
		return false
	}
	data, err := os.ReadFile(fpath)
	if err != nil {
		return false
	}
	ct := mimeByExt[strings.ToLower(filepath.Ext(fpath))]
	if ct == "" {
		ct = "application/octet-stream"
	}
	httpserver.WriteBytes(c, httpserver.StatusOK, ct, data)
	return true
}
