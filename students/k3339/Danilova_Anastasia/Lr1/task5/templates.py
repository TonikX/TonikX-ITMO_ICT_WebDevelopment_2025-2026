def get_body_template():
    return """<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <title>Academic Record</title>
  <style>
    body { font-family: Arial, sans-serif; padding: 20px; background:#f6f6f6; }
    .box { max-width:800px; margin:0 auto; background:#fff; padding:20px; border-radius:6px; box-shadow:0 2px 6px rgba(0,0,0,0.08); }
    table { width:100%; border-collapse:collapse; margin:15px 0; }
    th,td { padding:8px 10px; border:1px solid #ddd; text-align:left; }
    form div { margin:8px 0; }
    input[type=text], input[type=number] { padding:6px; width:200px; }
    button { padding:8px 12px; cursor:pointer; }
    .success { background:#e6ffed; padding:10px; border:1px solid #8fe3a7; margin:10px 0; }
    .error { background:#ffecec; padding:10px; border:1px solid #f5a6a6; margin:10px 0; }
  </style>
</head>
<body>
  <div class="box">
    {{content}}
  </div>
</body>
</html>
"""


def get_main_page(grades):
    if grades:
        rows = "".join(f"<tr><td>{k}</td><td>{v}</td></tr>" for k, v in grades.items())
        table = f"<h2>Current Grades</h2><table><tr><th>Discipline</th><th>Grade</th></tr>{rows}</table>"
    else:
        table = "<p>No grades yet.</p>"

    form = """
      <h2>Add / Update Grade</h2>
      <form method="POST">
        <div><label>Discipline: <input type="text" name="discipline" required></label></div>
        <div><label>Grade (1-5): <input type="number" name="grade" min="1" max="5" required></label></div>
        <div><button type="submit">Save</button></div>
      </form>
    """

    content = f"<h1>Academic Record</h1>{table}{form}"
    return get_body_template().replace("{{content}}", content)


def get_success_page(message):
    content = f"<h1>Academic Record</h1><div class='success'><strong>Success:</strong> {message}</div><p><a href='/'>Back</a></p>"
    return get_body_template().replace("{{content}}", content)


def get_error_page(message, code=400):
    content = f"<h1>Academic Record</h1><div class='error'><strong>Error {code}:</strong> {message}</div><p><a href='/'>Back</a></p>"
    return get_body_template().replace("{{content}}", content)
