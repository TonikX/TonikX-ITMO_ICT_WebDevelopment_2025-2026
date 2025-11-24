import json
from typing import Dict
from request import Request, Response

class Lessons:
    def __init__(self, persist_file: str = None):  # Fixed: __init__ instead of init
        self.lessons: Dict[str, int] = {}
        self.persist_file = persist_file
        if self.persist_file:
            try:
                with open(self.persist_file, "r") as f:
                    self.lessons = json.load(f)
            except Exception:
                self.lessons = {}

    def set_grade(self, lesson: str, grade: int):
        self.lessons[lesson] = grade
        if self.persist_file:
            with open(self.persist_file, "w") as f:
                json.dump(self.lessons, f)

    def get_grades_html(self) -> str:
        if not self.lessons:
            return "<h1>No grades yet</h1>"
        out = "<ul>"
        for k, v in self.lessons.items():
            out += f"<li>{k}: {v}</li>"
        out += "</ul>"
        return out

def parse_set_grades_req(lessons: Lessons, req: Request) -> Response:
    if not req.content:
        return Response(400, "Bad Request", body="empty content")
    try:
        j = json.loads(req.content)
        lessons.set_grade(j["lesson"], int(j["grade"]))
        return Response(200, "OK", body="OK")
    except Exception as e:
        return Response(400, "Bad Request", body=f"invalid json: {e}")

def parse_get_grades_req(lessons: Lessons, req: Request) -> Response:
    return Response(200, "OK", body=lessons.get_grades_html())