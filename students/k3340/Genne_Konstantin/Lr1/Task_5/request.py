from functools import lru_cache
from urllib.parse import parse_qs, urlparse


class Request:
    def __init__(self, method, target, version, headers, rfile):
        self.method = method
        self.target = target
        self.version = version
        self.headers = headers
        self.rfile = rfile

    @property
    def path(self):
        return self.url.path
    
    @property
    @lru_cache(maxsize=None)
    def query(self):
        return parse_qs(self.url.query)
    
    @property
    @lru_cache(maxsize=None)
    def url(self):
        return urlparse(self.target)
    

    @property
    def body(self):
        try:
            size = self.headers.get('Content-Length')
            if not size:
                return {}
        
            content_length = int(size)
            if content_length == 0:
                return {}
            
            raw_body = self.rfile.read(content_length)
            if not raw_body:
                return {}
            
            body_str = raw_body.decode('utf-8')
            return parse_qs(body_str)
        
        except (ValueError, UnicodeDecodeError, Exception) as e:
            print(f"Error parsing request body: {e}")
        return {}