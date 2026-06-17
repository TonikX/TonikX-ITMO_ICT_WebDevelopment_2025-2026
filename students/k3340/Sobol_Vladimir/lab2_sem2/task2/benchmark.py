"""Запускает все три парсера подряд и печатает сравнительную таблицу."""
import asyncio

import threading_parser
import multiprocessing_parser
import async_parser


def main() -> None:
    t_time = threading_parser.run()
    m_time = multiprocessing_parser.run()
    a_time = asyncio.run(async_parser.main())

    print()
    print(f"{'approach':<18}{'time, s':>10}")
    print("-" * 30)
    for name, elapsed in (("threading", t_time), ("multiprocessing", m_time), ("async", a_time)):
        print(f"{name:<18}{elapsed:>10.3f}")


if __name__ == "__main__":
    main()
