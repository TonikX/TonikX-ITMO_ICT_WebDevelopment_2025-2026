from dataclasses import dataclass

from typing_extensions import Dict, Optional


@dataclass
class Request:
    method: str
    url: str
    http_version: str
    params: dict
    headers: Dict[str, str]
    content: Optional[str]


@dataclass
class Response:
    status: int
    reason: str
    http_version: str = 'HTTP/1.1'
    body: str = ''
