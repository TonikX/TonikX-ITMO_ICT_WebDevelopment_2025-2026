
class Response:
    def __init__(self, status, reason, headers=None, body=None):
        self.status = status
        self.reason = reason
        self.headers = headers
        self.body = body

    def __str__(self):
        return f"Response(status={self.status}, reason={self.reason}, body_length={len(self.body) if self.body else 0})"