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


def get_add_grade_form_html() -> str:
        return """
<html>
    <head>
        <meta charset="utf-8">
        <title>Add Lesson Grade</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    </head>
    <body class="p-4">
        <div class="container">
            <h1 class="mb-3">Add Lesson and Grade</h1>
            <form method="post" action="/add" class="row g-3">
                <div class="col-md-8">
                    <label class="form-label">Lesson</label>
                    <input name="lesson" class="form-control" required />
                </div>
                <div class="col-md-4">
                    <label class="form-label">Grade</label>
                    <input name="grade" type="number" min="0" max="100" class="form-control" required />
                </div>
                <div class="col-12">
                    <button class="btn btn-primary">Submit</button>
                    <a href="/grades" class="btn btn-secondary ms-2">View Grades</a>
                </div>
            </form>
        </div>
    </body>
</html>
"""


def parse_set_grades_form(lessons: Lessons, req: Request) -> Response:
        # Expecting form-encoded body like: lesson=Math&grade=95
        if not req.content:
                return Response(400, "Bad Request", body="empty content")
        try:
                pairs = {}
                for part in req.content.split("&"):
                        if "=" in part:
                                k, v = part.split("=", 1)
                                # Basic URL decode for + and %20
                                k = k.replace("+", " ")
                                v = v.replace("+", " ")
                                pairs[k] = v
                lesson = pairs.get("lesson")
                grade = pairs.get("grade")
                if lesson is None or grade is None:
                        return Response(400, "Bad Request", body="missing fields")
                lessons.set_grade(lesson, int(grade))
                # Redirect back to form or grades page
                return Response(303, "See Other", headers={"Location": "/grades"}, body="")
        except Exception as e:
                return Response(400, "Bad Request", body=f"invalid form data: {e}")