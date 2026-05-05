def format_record(url: str, data: dict) -> str:
    user_id = 1
    status = "ACTIVE"
    condition = "NEW"

    description = data.get("description") or "(no summary-text-container)"

    return (
        f"URL: {url}\n"
        f"book.user_id: {user_id}\n"
        f"book.title: {data.get('title')}\n"
        f"book.author: {data.get('author')}\n"
        f"book.status: {status}\n"
        f"book.condition: {condition}\n"
        f"book.description: {description}\n"
        f"{'-'*60}\n"
    )