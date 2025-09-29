package httpserver

import (
	"bufio"
	"errors"
	"strconv"
	"strings"
)

type Request struct {
	Method        string
	Path          string
	Proto         string
	Headers       map[string]string
	ContentLength int
	Body          []byte
}

func ReadRequest(br *bufio.Reader) (*Request, error) {
	start, hdrs, err := readStartLineAndHeaders(br)
	if err != nil {
		return nil, err
	}
	m, p, proto, err := parseStartLine(start)
	if err != nil {
		return nil, err
	}
	req := &Request{
		Method:  m,
		Path:    p,
		Proto:   proto,
		Headers: hdrs,
	}
	if cl, ok := hdrs["content-length"]; ok {
		n, err := strconv.Atoi(strings.TrimSpace(cl))
		if err != nil || n < 0 {
			return nil, errors.New("invalid content-length")
		}
		req.ContentLength = n
	}
	return req, nil
}

func readStartLineAndHeaders(br *bufio.Reader) (string, map[string]string, error) {
	total := 0
	line, err := br.ReadString('\n')
	if err != nil {
		return "", nil, err
	}
	total += len(line)
	line = strings.TrimRight(line, "\r\n")
	hdrs := map[string]string{}
	for {
		l, err := br.ReadString('\n')
		if err != nil {
			return "", nil, err
		}
		total += len(l)
		l = strings.TrimRight(l, "\r\n")
		if l == "" {
			break
		}
		if i := strings.IndexByte(l, ':'); i != -1 {
			k := strings.ToLower(strings.TrimSpace(l[:i]))
			v := strings.TrimSpace(l[i+1:])
			hdrs[k] = v
		}
	}
	return line, hdrs, nil
}

func parseStartLine(l string) (method, path, proto string, err error) {
	p := strings.Fields(l)
	if len(p) != 3 {
		return "", "", "", errors.New("bad request line")
	}
	return p[0], p[1], p[2], nil
}

func Header(req *Request, key string) string {
	return req.Headers[strings.ToLower(key)]
}

func IsContentType(req *Request, prefix string) bool {
	ct := strings.ToLower(Header(req, "content-type"))
	return strings.HasPrefix(ct, strings.ToLower(prefix))
}
