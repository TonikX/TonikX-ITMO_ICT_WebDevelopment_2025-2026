"""Запускает все три подхода подряд и печатает таблицу времён."""
import threading_sum
import multiprocessing_sum
import async_sum
import asyncio


def main() -> None:
    t_total, t_time = threading_sum.run()
    m_total, m_time = multiprocessing_sum.run()
    a_total, a_time = asyncio.run(async_sum.main())

    print()
    print(f"{'approach':<18}{'sum':<25}{'time, s':>10}")
    print("-" * 55)
    for name, total, elapsed in (
        ("threading", t_total, t_time),
        ("multiprocessing", m_total, m_time),
        ("async", a_total, a_time),
    ):
        print(f"{name:<18}{total:<25}{elapsed:>10.3f}")


if __name__ == "__main__":
    main()
