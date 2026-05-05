import re
from bs4 import BeautifulSoup

def _clean_spaces(s: str) -> str:
    return " ".join(s.split()).strip()

def clean_author(author_raw: str) -> str:
    s = _clean_spaces(author_raw)

    s = re.sub(r"\b\d{3,4}\s*[-–]\s*\d{2,4}\b", "", s)
    s = re.sub(r"\b\d+\b", "", s)

    parts = [p.strip() for p in s.split(",") if p.strip()]
    if len(parts) >= 2:
        last, first = parts[0], parts[1]
        full = f"{first} {last}"
    else:
        full = parts[0] if parts else "Unknown"

    full = _clean_spaces(full)
    return full if full else "Unknown"

def split_title_and_author(text: str):
    t = _clean_spaces(text)

    m = re.match(r"^(?P<title>.+?)\s+by\s+(?P<author>.+)$", t, flags=re.IGNORECASE)
    if not m:
        return t, None

    title = _clean_spaces(m.group("title"))
    author = _clean_spaces(m.group("author"))
    return title, author

def parse(html: str) -> dict:
    soup = BeautifulSoup(html, "lxml")

    # page title
    page_title = "(no title)"
    if soup.title and soup.title.string:
        page_title = _clean_spaces(soup.title.string)

    # 1) get header title text
    header_text = None
    h1 = soup.select_one('h1[itemprop="name"]') or soup.select_one("h1")
    if h1 and h1.get_text(strip=True):
        header_text = _clean_spaces(h1.get_text(" ", strip=True))

    # fallback title from <title>
    if not header_text:
        header_text = page_title.replace(" | Project Gutenberg", "").strip()

    # split "Title by Author" if present in header
    book_title, author_from_header = split_title_and_author(header_text)

    # 2) try to parse author from dedicated author fields (more reliable)
    author_raw = None
    a = soup.select_one('[itemprop="creator"]')
    if a and a.get_text(strip=True):
        author_raw = _clean_spaces(a.get_text(" ", strip=True))

    if not author_raw:
        for row in soup.select("table.bibrec tr"):
            th = row.find("th")
            td = row.find("td")
            if th and td and _clean_spaces(th.get_text()) == "Author":
                author_raw = _clean_spaces(td.get_text(" ", strip=True))
                break

    # choose author: dedicated field first, else header "by ..." part, else Unknown
    if author_raw:
        author = clean_author(author_raw)
    elif author_from_header:
        author = clean_author(author_from_header)
    else:
        author = "Unknown"

    # summary: class, not id
    summary_div = soup.select_one("div.summary-text-container")
    summary = None
    if summary_div:
        # 1) Try common readmore text targets first (site can vary)
        preferred = summary_div.select_one(
            ".readmore-text, .readmore-content, .readmore__content, [data-readmore-content]"
        )
        target = preferred or summary_div

        summary = _clean_spaces(target.get_text(" ", strip=True))

        # 2) Cleanup UI words if they appear in text
        summary = re.sub(r"\bRead more\b", "", summary, flags=re.IGNORECASE).strip()

        if not summary:
            summary = None

    return {
        "page_title": page_title[:500],
        "title": book_title[:200],
        "author": author[:100],
        "description": (summary[:5000] if summary else None),
    }