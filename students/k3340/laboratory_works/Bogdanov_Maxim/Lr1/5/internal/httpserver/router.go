package httpserver

import (
	"net"
	"strings"
)

type Handler func(net.Conn, *Request) bool

type Router struct {
	get  map[string]Handler
	post map[string]Handler
	any  []Handler
}

func NewRouter() *Router {
	return &Router{
		get:  map[string]Handler{},
		post: map[string]Handler{},
	}
}

func (r *Router) GET(path string, h Handler)  { r.get[path] = h }
func (r *Router) POST(path string, h Handler) { r.post[path] = h }
func (r *Router) Use(h Handler)               { r.any = append(r.any, h) }

func (r *Router) Serve(c net.Conn, req *Request) bool {
	switch req.Method {
	case "GET":
		if h, ok := r.get[req.Path]; ok && h(c, req) {
			return true
		}
	case "POST":
		if h, ok := r.post[req.Path]; ok && h(c, req) {
			return true
		}
	}
	// маршруты с префиксами (например, /assets/)
	for path, h := range r.get {
		if strings.HasSuffix(path, "*") && strings.HasPrefix(req.Path, strings.TrimSuffix(path, "*")) && req.Method == "GET" {
			if h(c, req) {
				return true
			}
		}
	}

	for _, h := range r.any {
		if h(c, req) {
			return true
		}
	}
	return false
}
