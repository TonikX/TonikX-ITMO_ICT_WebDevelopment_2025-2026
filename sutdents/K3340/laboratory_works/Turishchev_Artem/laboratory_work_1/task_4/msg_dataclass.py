import json
from dataclasses import dataclass, asdict

@dataclass
class Message:
    type: str = ""
    msg: str = ""
    author: str = "self"

    def __str__(self):
        return json.dumps(asdict(self))
    
    @classmethod
    def parse_msg(cls, msg):
        msg = json.loads(msg)
        return cls(**msg)