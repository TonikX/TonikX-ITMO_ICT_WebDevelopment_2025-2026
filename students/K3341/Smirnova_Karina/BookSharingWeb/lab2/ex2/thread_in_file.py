import time
import threading
import requests

from parser import parse
from urls_25 import URLS_25
from output_format import format_record

OUT_FILE = "thread_results.txt"
file_lock = threading.Lock()

def parse_and_save(url: str) -> None:
    r = requests.get(url, timeout=20, headers={"User-Agent": "Mozilla/5.0 (student parser)"})
    r.raise_for_status()
    data = parse(r.text)

    text = format_record(url, data)
    with file_lock:
        with open(OUT_FILE, "a", encoding="utf-8") as f:
            f.write(text)

    print(f"[thread] saved: {url} -> {data['title']}")

def worker(urls):
    for url in urls:
        try:
            parse_and_save(url)
        except Exception as e:
            print(f"[thread][error] {url}: {e}")

def chunk_list(items, chunks: int):
    chunks = max(1, chunks)
    size = (len(items) + chunks - 1) // chunks
    return [items[i:i+size] for i in range(0, len(items), size)]

def main():
    # clear output
    open(OUT_FILE, "w", encoding="utf-8").close()

    urls = URLS_25[:25]
    num_threads = 5
    parts = chunk_list(urls, num_threads)

    threads = [threading.Thread(target=worker, args=(part,)) for part in parts]

    t0 = time.perf_counter()
    for t in threads: t.start()
    for t in threads: t.join()
    t1 = time.perf_counter()

    print(f"[threading->file] threads={num_threads} time={t1 - t0:.6f}s output={OUT_FILE}")

if __name__ == "__main__":
    main()