# seed_factory.py
from __future__ import annotations

import sys
import time
from datetime import date, datetime, timedelta
from decimal import Decimal
from typing import Any, Dict, List, Optional, Tuple

import requests

BASE_URL = "http://127.0.0.1:8000"
TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwiaWF0IjoxNzY1ODQwNTM0LCJleHAiOjE3NjU4NDQxMzQsInJvbGUiOiJlbXBsb3llZSIsInVzZXJuYW1lIjoibmlraXRhIn0.NjpBRsaEgmzn6cJbb-zLFPOh2Py0HZZQNIS0XWvYUQ8"

# -----------------------------
# HTTP helpers (only Authorization header as you requested)
# -----------------------------
SESSION = requests.Session()
SESSION.headers.update({"Authorization": f"Bearer {TOKEN}"})


def _url(path: str) -> str:
    if not path.startswith("/"):
        path = "/" + path
    return BASE_URL + path


def http_get(path: str, params: Optional[dict] = None) -> Any:
    r = SESSION.get(_url(path), params=params, timeout=30)
    if r.status_code >= 400:
        raise RuntimeError(f"GET {path} failed: {r.status_code} {r.text}")
    return r.json()


def http_post(path: str, json: dict) -> Any:
    r = SESSION.post(_url(path), json=json, timeout=30)
    if r.status_code == 409:
        return {"__conflict__": True, "status_code": 409, "text": r.text}
    if r.status_code >= 400:
        raise RuntimeError(f"POST {path} failed: {r.status_code} {r.text}")
    return r.json()


def http_put(path: str, json: dict) -> Any:
    r = SESSION.put(_url(path), json=json, timeout=30)
    if r.status_code == 409:
        return {"__conflict__": True, "status_code": 409, "text": r.text}
    if r.status_code >= 400:
        raise RuntimeError(f"PUT {path} failed: {r.status_code} {r.text}")
    return r.json()


def http_patch(path: str, json: dict) -> Any:
    r = SESSION.patch(_url(path), json=json, timeout=30)
    if r.status_code == 409:
        return {"__conflict__": True, "status_code": 409, "text": r.text}
    if r.status_code >= 400:
        raise RuntimeError(f"PATCH {path} failed: {r.status_code} {r.text}")
    return r.json()


# -----------------------------
# List helpers (fetch all with pagination)
# -----------------------------
def list_all(path: str, *, base_params: Optional[dict] = None, limit: int = 500) -> List[dict]:
    out: List[dict] = []
    skip = 0
    base_params = dict(base_params or {})
    while True:
        params = dict(base_params)
        params.update({"skip": skip, "limit": limit})
        chunk = http_get(path, params=params)
        if not isinstance(chunk, list):
            raise RuntimeError(f"Expected list from GET {path}, got: {type(chunk)}")
        out.extend(chunk)
        if len(chunk) < limit:
            break
        skip += limit
    return out


# -----------------------------
# Domain create-or-get helpers
# -----------------------------
def ensure_diets(target: List[Dict[str, Any]]) -> Dict[int, dict]:
    """
    target items: {"diet_no": int, "content": str}
    returns: dict diet_no -> diet object
    """
    existing = list_all("/diets", base_params={})
    by_no = {d["diet_no"]: d for d in existing}

    for d in target:
        if d["diet_no"] in by_no:
            continue
        res = http_post("/diets", json=d)
        if res.get("__conflict__"):
            # someone already created it between list and post; refresh later
            pass
        else:
            by_no[res["diet_no"]] = res

    # refresh (safe)
    existing = list_all("/diets", base_params={})
    return {d["diet_no"]: d for d in existing}


def ensure_workshops(target: List[Dict[str, Any]]) -> Dict[int, dict]:
    """
    target items: {"workshop_no": int, "name": Optional[str]}
    returns: dict workshop_no -> workshop object
    """
    existing = list_all("/workshops", base_params={})
    by_no = {w["workshop_no"]: w for w in existing}

    for w in target:
        if w["workshop_no"] in by_no:
            continue
        res = http_post("/workshops", json=w)
        if not res.get("__conflict__"):
            by_no[res["workshop_no"]] = res

    existing = list_all("/workshops", base_params={})
    return {w["workshop_no"]: w for w in existing}


def ensure_cages_for_workshops(
    workshops_by_no: Dict[int, dict],
    cages_per_workshop: int,
    rows: int,
) -> Dict[Tuple[int, int, int], dict]:
    """
    Create cages with deterministic pattern:
    row_no in [1..rows], cage_no increments per row.
    workshop_id comes from workshops_by_no.
    Returns: (workshop_id,row_no,cage_no) -> cage object
    """
    existing = list_all("/cages", base_params={})
    by_key = {(c["workshop_id"], c["row_no"], c["cage_no"]): c for c in existing}

    for ws_no, ws in workshops_by_no.items():
        wid = ws["workshop_id"]
        per_row = max(1, cages_per_workshop // rows)
        extra = cages_per_workshop - per_row * rows

        cage_no_counter = 1
        for row_no in range(1, rows + 1):
            n = per_row + (1 if row_no <= extra else 0)
            for _ in range(n):
                key = (wid, row_no, cage_no_counter)
                cage_no_counter += 1
                if key in by_key:
                    continue
                payload = {"workshop_id": wid, "row_no": row_no, "cage_no": key[2]}
                res = http_post("/cages", json=payload)
                if not res.get("__conflict__"):
                    by_key[key] = res

    existing = list_all("/cages", base_params={})
    return {(c["workshop_id"], c["row_no"], c["cage_no"]): c for c in existing}


def ensure_breeds(target: List[Dict[str, Any]]) -> Dict[str, dict]:
    """
    target items: {"name": str, "avg_eggs_per_month": int, "avg_weight_kg": Decimal/str/float, "recommended_diet_no": int}
    returns: dict name -> breed object
    """
    existing = list_all("/breeds", base_params={})
    by_name = {b["name"]: b for b in existing}

    for b in target:
        if b["name"] in by_name:
            continue
        # ensure Decimal-safe JSON
        payload = dict(b)
        payload["avg_weight_kg"] = str(payload["avg_weight_kg"])
        res = http_post("/breeds", json=payload)
        if not res.get("__conflict__"):
            by_name[res["name"]] = res

    existing = list_all("/breeds", base_params={})
    return {b["name"]: b for b in existing}


def ensure_breed_season_diets(breeds_by_name: Dict[str, dict], diets_by_no: Dict[int, dict]) -> None:
    # deterministic mapping
    seasons = ["winter", "spring", "summer", "autumn"]
    breed_names = sorted(breeds_by_name.keys())
    diet_nos = sorted(diets_by_no.keys())

    for i, bname in enumerate(breed_names):
        bid = breeds_by_name[bname]["breed_id"]
        # rotate diets across seasons
        for j, season in enumerate(seasons):
            diet_no = diet_nos[(i + j) % len(diet_nos)]
            diet_id = diets_by_no[diet_no]["diet_id"]
            http_put(f"/breeds/{bid}/diets/{season}", json={"diet_id": diet_id})


def ensure_employees(target: List[Dict[str, Any]]) -> Dict[str, dict]:
    """
    Idempotency key: passport (since list_employees supports passport filter)
    returns passport -> employee object
    """
    existing = list_all("/employees", base_params={})
    by_passport = {e["passport"]: e for e in existing}

    for e in target:
        if e["passport"] in by_passport:
            continue
        payload = dict(e)
        payload["salary"] = str(payload["salary"])
        res = http_post("/employees", json=payload)
        if not res.get("__conflict__"):
            by_passport[res["passport"]] = res

    existing = list_all("/employees", base_params={})
    return {e["passport"]: e for e in existing}


def ensure_employee_assignments(
    employees: List[dict],
    cages: List[dict],
    assigned_from: date,
    active_fraction: float = 0.7,
) -> None:
    """
    Deterministic assignments:
    - assign employees to cages in round-robin
    - some active (assigned_to=None), some closed
    Idempotent by checking existing /employee-cages for exact (employee_id,cage_id,assigned_from).
    """
    # fetch all existing assignments once
    existing = list_all("/employee-cages", base_params={})
    existing_keys = {(a["employee_id"], a["cage_id"], a["assigned_from"]): a for a in existing}

    n_emp = len(employees)
    for idx, cage in enumerate(cages):
        emp = employees[idx % n_emp]
        key = (emp["employee_id"], cage["cage_id"], assigned_from.isoformat())
        if key in existing_keys:
            continue

        # deterministic: first X% active
        make_active = (idx / max(1, len(cages))) < active_fraction
        payload = {
            "employee_id": emp["employee_id"],
            "cage_id": cage["cage_id"],
            "assigned_from": assigned_from.isoformat(),
            "assigned_to": None if make_active else (assigned_from + timedelta(days=14)).isoformat(),
        }
        http_post("/employee-cages", json=payload)


def ensure_chickens(
    breeds_by_name: Dict[str, dict],
    cages_by_key: Dict[Tuple[int, int, int], dict],
    chickens_per_cage_target: int,
) -> List[dict]:
    """
    Idempotency strategy:
    - For each cage, we check current count of chickens in that cage via /chickens?cage_id=...
    - Create only missing up to chickens_per_cage_target
    - Breed distribution is deterministic and stable
    Returns the full list of chickens after seeding.
    """
    breed_list = [breeds_by_name[name] for name in sorted(breeds_by_name.keys())]
    cages = list(cages_by_key.values())
    cages.sort(key=lambda c: (c["workshop_id"], c["row_no"], c["cage_no"]))

    for i, cage in enumerate(cages):
        cage_id = cage["cage_id"]
        current = list_all("/chickens", base_params={"cage_id": cage_id})
        missing = max(0, chickens_per_cage_target - len(current))
        if missing == 0:
            continue

        # deterministic distribution by cage index
        for j in range(missing):
            breed = breed_list[(i + j) % len(breed_list)]

            # deterministic but varied numbers
            weight = Decimal(str(1.6 + ((i + j) % 10) * 0.08))  # ~1.6..2.32
            age = 4 + ((i + j) % 12)                            # 4..15 months
            eggs = int(breed["avg_eggs_per_month"]) + (((i + j) % 7) - 3)  # around avg

            payload = {
                "breed_id": breed["breed_id"],
                "cage_id": cage_id,
                "weight_kg": str(weight),
                "age_months": age,
                "eggs_per_month": max(0, eggs),
            }
            http_post("/chickens", json=payload)

    return list_all("/chickens", base_params={})


def ensure_moves(chickens: List[dict], cages: List[dict], moves_target: int) -> None:
    existing = list_all("/chicken-moves", base_params={"newest_first": False})
    existing_reasons = {m.get("reason") for m in existing if m.get("reason")}

    cages_sorted = sorted(cages, key=lambda c: c["cage_id"])
    chickens_sorted = sorted(chickens, key=lambda c: c["chicken_id"])

    now = datetime.now()
    start = now - timedelta(days=30)
    step = timedelta(hours=12)

    created = 0
    k = 0

    while created < moves_target and k < moves_target * 20:
        reason = f"seed:v1:move:{created+1:02d}"
        if reason in existing_reasons:
            created += 1
            continue

        ch = chickens_sorted[k % len(chickens_sorted)]
        current_cage_id = ch["cage_id"]

        # выбираем клетку детерминированно, но НЕ текущую
        idx = (k * 3 + 7) % len(cages_sorted)
        to_cage = cages_sorted[idx]
        if to_cage["cage_id"] == current_cage_id:
            to_cage = cages_sorted[(idx + 1) % len(cages_sorted)]

        payload = {
            "chicken_id": ch["chicken_id"],
            "from_cage_id": None,  # сервис сам проверит текущую
            "to_cage_id": to_cage["cage_id"],
            "moved_at": (start + step * k).replace(microsecond=0).isoformat(),
            "reason": reason,
        }

        res = http_post(f"/chickens/{ch['chicken_id']}/move", json=payload)
        if not res.get("__conflict__"):
            existing_reasons.add(reason)

        created += 1
        k += 1


# -----------------------------
# Main seed plan
# -----------------------------
def main() -> int:
    # 1) Diets (needed for breeds + season diets)
    diet_targets = [
        {"diet_no": 1, "content": "Standard balanced feed: grain 60%, protein 25%, minerals 10%, vitamins 5%"},
        {"diet_no": 2, "content": "High-protein feed: grain 45%, protein 40%, minerals 10%, vitamins 5%"},
        {"diet_no": 3, "content": "Winter feed: grain 55%, protein 25%, minerals 15%, vitamins 5%"},
        {"diet_no": 4, "content": "Summer feed: grain 65%, protein 20%, minerals 10%, vitamins 5%"},
    ]
    diets_by_no = ensure_diets(diet_targets)
    print(f"[OK] diets: {len(diets_by_no)}")

    # 2) Workshops
    workshop_targets = [
        {"workshop_no": 1, "name": "Цех №1"},
        {"workshop_no": 2, "name": "Цех №2"},
        {"workshop_no": 3, "name": "Цех №3"},
    ]
    workshops_by_no = ensure_workshops(workshop_targets)
    print(f"[OK] workshops: {len(workshops_by_no)}")

    # 3) Cages
    cages_by_key = ensure_cages_for_workshops(
        workshops_by_no=workshops_by_no,
        cages_per_workshop=12,  # сам решил: 12 клеток на цех
        rows=3,                 # 3 ряда
    )
    cages = list(cages_by_key.values())
    print(f"[OK] cages: {len(cages)}")

    # 4) Breeds
    breed_targets = [
        {"name": "Lohmann Brown", "avg_eggs_per_month": 26, "avg_weight_kg": Decimal("2.0"), "recommended_diet_no": 1},
        {"name": "Hy-Line W-36",  "avg_eggs_per_month": 28, "avg_weight_kg": Decimal("1.8"), "recommended_diet_no": 2},
        {"name": "Isa Brown",     "avg_eggs_per_month": 25, "avg_weight_kg": Decimal("2.1"), "recommended_diet_no": 1},
        {"name": "Rhode Island",  "avg_eggs_per_month": 22, "avg_weight_kg": Decimal("2.4"), "recommended_diet_no": 3},
    ]
    breeds_by_name = ensure_breeds(breed_targets)
    print(f"[OK] breeds: {len(breeds_by_name)}")

    # 5) BreedDietSeason (upsert) — безопасно хоть 100 раз
    ensure_breed_season_diets(breeds_by_name, diets_by_no)
    print("[OK] breed season diets upserted")

    # 6) Chickens
    chickens = ensure_chickens(
        breeds_by_name=breeds_by_name,
        cages_by_key=cages_by_key,
        chickens_per_cage_target=10,  # сам решил: 10 кур в клетке
    )
    print(f"[OK] chickens total: {len(chickens)}")

    # 7) Employees
    employee_targets = [
        {"passport": "SEED-PAS-0001", "salary": Decimal("65000"), "contract_no": "SEED-CTR-0001", "fire_date": None, "fire_reason": None},
        {"passport": "SEED-PAS-0002", "salary": Decimal("62000"), "contract_no": "SEED-CTR-0002", "fire_date": None, "fire_reason": None},
        {"passport": "SEED-PAS-0003", "salary": Decimal("68000"), "contract_no": "SEED-CTR-0003", "fire_date": None, "fire_reason": None},
        {"passport": "SEED-PAS-0004", "salary": Decimal("60000"), "contract_no": "SEED-CTR-0004", "fire_date": None, "fire_reason": None},
        {"passport": "SEED-PAS-0005", "salary": Decimal("70000"), "contract_no": "SEED-CTR-0005", "fire_date": None, "fire_reason": None},
    ]
    employees_by_passport = ensure_employees(employee_targets)
    employees = [employees_by_passport[p] for p in sorted(employees_by_passport.keys())]
    print(f"[OK] employees: {len(employees)}")

    # 8) Assign employees to cages
    # assigned_from = first day of previous month (deterministic for reporting timeframe idea)
    today = date.today()
    first_of_this_month = today.replace(day=1)
    prev_month_last_day = first_of_this_month - timedelta(days=1)
    assigned_from = prev_month_last_day.replace(day=1)

    ensure_employee_assignments(
        employees=employees,
        cages=cages,
        assigned_from=assigned_from,
        active_fraction=0.75,
    )
    print("[OK] employee assignments ensured")

    # 9) Moves (a couple dozens)
    ensure_moves(chickens=chickens, cages=cages, moves_target=30)
    print("[OK] moves ensured (30, idempotent by reason tag)")

    print("\nDONE ✅ You can now build the monthly report queries over workshops/breeds.")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\nInterrupted.")
        sys.exit(130)
