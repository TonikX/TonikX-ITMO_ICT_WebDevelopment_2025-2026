import json

from request import *

class Lessons:

    def __init__(self):
        self.lessons = {}

    def set_grade(self, lesson: str, grade: int):
        self.lessons[lesson] = grade

    def get_grades_html(self) -> str:
        if len(self.lessons.keys()) == 0:
            return f'<h1>Пусто тута</h1>'
        out = ''
        for i in self.lessons.keys():
            out += f'<br>{i}: {self.lessons[i]}</br>'
        return out



def parse_set_grades_req(lessons: Lessons, req: Request) -> Response:
    if req.content is None or len(req.content) == 0:
        return Response(400, "empty content")

    try:
        json_data = json.loads(req.content)
        lessons.set_grade(json_data['lesson'], int(json_data['grade']))
    except json.decoder.JSONDecodeError:
        return Response(400, "invalid json")
    except KeyError:
        return Response(400, "invalid json")
    except ValueError:
        return Response(400, "invalid json")

    return Response(200, "OK")


def parse_get_grades_req(lessons: Lessons, req: Request) -> Response:
    return Response(200, "OK", body=lessons.get_grades_html())
