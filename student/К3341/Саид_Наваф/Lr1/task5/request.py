from dataclasses import dataclass
from typing import Dict, Optional

@dataclass
class Request:
    method: str
    url: str
    http_version: str
    params: Dict[str, str]
    headers: Dict[str, str]
    content: Optional[str]

@dataclass
class Response:
    status: int
    reason: str
    http_version: str = "HTTP/1.1"
    headers: Dict[str, str] = None
    body: str = ""