import time
import multiprocessing as mp
import requests

from parser import parse
from urls_25 import URLS_25
from output_format import format_record

OUT_FILE = "mp_results.txt"

def parse_and_save(url: str) -> str:
    r = requests.get(url, timeout=20, headers={"User-Agent": "Mozilla/5.0 (student parser)"})
    r.raise_for_status()
    data = parse(r.text)
    return format_record(url, data)

def worker(urls, queue: mp.Queue):
    for url in urls:
        try:
            text = parse_and_save(url)
            queue.put(text)
            print(f"[proc {mp.current_process().name}] prepared: {url}")
        except Exception as e:
            queue.put(f"URL: {url}\nERROR: {e}\n{'-'*60}\n")

def writer(queue: mp.Queue, out_file: str):
    with open(out_file, "w", encoding="utf-8") as f:
        while True:
            item = queue.get()
            if item is None:  # sentinel
                break
            f.write(item)
            f.flush()

def chunk_list(items, chunks: int):
    chunks = max(1, chunks)
    size = (len(items) + chunks - 1) // chunks
    return [items[i:i+size] for i in range(0, len(items), size)]

def main():
    urls = URLS_25[:25]
    num_procs = min(5, mp.cpu_count())
    parts = chunk_list(urls, num_procs)

    queue = mp.Queue()
    w = mp.Process(target=writer, args=(queue, OUT_FILE))
    w.start()

    t0 = time.perf_counter()
    procs = [mp.Process(target=worker, args=(part, queue)) for part in parts]
    for p in procs: p.start()
    for p in procs: p.join()

    queue.put(None)  # stop writer
    w.join()
    t1 = time.perf_counter()

    print(f"[multiprocessing->file] procs={num_procs} time={t1 - t0:.6f}s output={OUT_FILE}")

if __name__ == "__main__":
    main()