"""Check declared nonsecret QA ledger data; do not acquire evidence or certify PASS."""
from __future__ import annotations

import json
import sys
from decimal import Decimal, ROUND_HALF_UP
from typing import Any


class LedgerError(ValueError):
    pass


STATES = {
    "AVAILABLE_UNCHECKED", "VERIFIED", "MISSING_RECOVERABLE",
    "NEEDS_AUTHORIZATION", "EXHAUSTED", "N/A",
}


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise LedgerError("duplicate JSON key")
        result[key] = value
    return result


def reject_constant(value):
    raise LedgerError("nonfinite JSON constant")


def obj(value: Any) -> dict:
    if not isinstance(value, dict):
        raise LedgerError("expected object")
    return value


def text(value: Any) -> str:
    if not isinstance(value, str) or not value.strip():
        raise LedgerError("expected nonempty string")
    return value


def flag(value: Any) -> bool:
    if type(value) is not bool:
        raise LedgerError("expected boolean")
    return value


def rows(value: Any) -> list:
    if not isinstance(value, list):
        raise LedgerError("expected list")
    return value


def ratio(numerator: int, denominator: int) -> str:
    if denominator == 0:
        return f"N/A（{numerator}/0）"
    percentage = (Decimal(numerator) * 100 / Decimal(denominator)).quantize(
        Decimal("0.01"), rounding=ROUND_HALF_UP,
    )
    label = format(percentage, "f").rstrip("0").rstrip(".")
    return f"{label}%（{numerator}/{denominator}）"


def identities(value: Any, *, current: bool = False) -> dict:
    result = {}
    for row in rows(value):
        row = obj(row)
        key = text(row.get("key"))
        if key in result:
            raise LedgerError("duplicate scoring key")
        if row.get("kind") not in {"criterion", "check"}:
            raise LedgerError("invalid scoring kind")
        text(row.get("source_ref"))
        flag(row.get("verified"))
        if current:
            if "inherits" not in row:
                raise LedgerError("current identity needs explicit inherits")
            if row["inherits"] is not None:
                text(row["inherits"])
        result[key] = row
    return result


def check_ledger(data: Any) -> dict:
    data = obj(data)
    if type(data.get("schema_version")) is not int or data["schema_version"] != 1:
        raise LedgerError("unsupported schema_version")
    if not {"baseline", "current", "fixes", "requirements"} <= data.keys():
        raise LedgerError("missing ledger field")
    baseline = data["baseline"]
    original = None
    meta = None
    if baseline is not None:
        baseline = obj(baseline)
        for field in ("id", "scope", "source_ref", "captured_at"):
            text(baseline.get(field))
        if baseline.get("origin") not in {"original", "handoff"}:
            raise LedgerError("invalid baseline origin")
        verified = flag(baseline.get("verified"))
        original = identities(baseline.get("identities"))
        baseline_known = verified and all(row["verified"] for row in original.values())
        meta = {field: baseline[field] for field in ("id", "origin", "scope")}
    else:
        baseline_known = False

    current = None if data["current"] is None else identities(data["current"], current=True)
    retained = set()
    if original is not None and current is not None:
        for row in current.values():
            inherited = row["inherits"]
            if inherited is None:
                continue
            if inherited not in original or inherited in retained:
                raise LedgerError("invalid or reused inherited identity")
            if original[inherited]["kind"] != row["kind"]:
                raise LedgerError("inherited kind differs")
            retained.add(inherited)

    fixes_known = data["fixes"] is not None
    count_f = 0
    if fixes_known:
        roots = set()
        for row in rows(data["fixes"]):
            row = obj(row)
            root = text(row.get("root_id"))
            if root in roots:
                raise LedgerError("duplicate root issue; merge before counting")
            roots.add(root)
            baseline_root = flag(row.get("baseline_root"))
            fixed = flag(row.get("fixed"))
            verified = flag(row.get("verified"))
            if row.get("freshness") not in {"FRESH", "STALE", "UNVERIFIED"}:
                raise LedgerError("invalid fix freshness")
            if fixed and verified:
                text(row.get("evidence_ref"))
            if baseline_root and fixed and verified and row["freshness"] == "FRESH":
                count_f += 1

    missing = []
    requirement_ids = set()
    for requirement in rows(data["requirements"]):
        requirement = obj(requirement)
        identity = text(requirement.get("id"))
        if identity in requirement_ids:
            raise LedgerError("duplicate requirement ID")
        requirement_ids.add(identity)
        required = flag(requirement.get("required"))
        state = requirement.get("state")
        if state not in STATES:
            raise LedgerError("invalid acquisition state")
        for field in ("kind", "scope"):
            text(requirement.get(field))
        if state == "VERIFIED":
            text(requirement.get("actual_ref"))
            text(requirement.get("source_authority"))
        elif state == "N/A":
            text(requirement.get("reason"))
        else:
            actions = rows(requirement.get("acquisition_actions"))
            for action in actions:
                text(action)
            text(requirement.get("remaining_gap"))
            text(requirement.get("owner"))
            if state == "EXHAUSTED" and not actions:
                raise LedgerError("EXHAUSTED needs checked acquisition actions")
        if required and state not in {"VERIFIED", "N/A"}:
            missing.append({"id": identity, "state": state})

    result = {
        "status": "VALID_DECLARATION",
        "certifies_acceptance": False,
        "baseline": meta,
        "metric_label": "接手阶段指标" if meta and meta["origin"] == "handoff" else "原题累计指标",
        "R0": None, "T0": None, "N0": None,
        "F": count_f if fixes_known else None,
        "AR": None, "AT": None, "A": None, "DR": None, "DT": None,
        "error_rate": "N/A：可信基线或根因台账缺失",
        "omission_rate": "N/A：可信基线或当前身份台账缺失",
        "missing_required": missing,
        "checklist_ready": not missing,
    }
    if baseline_known:
        r0 = sum(row["kind"] == "criterion" for row in original.values())
        t0 = len(original) - r0
        n0 = r0 + t0
        result.update(R0=r0, T0=t0, N0=n0)
        if fixes_known:
            result["error_rate"] = ratio(count_f, n0)
        if current is not None and all(row["verified"] for row in current.values()):
            new = [row for row in current.values() if row["inherits"] is None]
            removed = [row for key, row in original.items() if key not in retained]
            ar = sum(row["kind"] == "criterion" for row in new)
            at = len(new) - ar
            dr = sum(row["kind"] == "criterion" for row in removed)
            dt = len(removed) - dr
            result.update(AR=ar, AT=at, A=ar + at, DR=dr, DT=dt)
            result["omission_rate"] = ratio(ar + at, n0 + ar + at)
    return result


def main() -> None:
    try:
        data = json.loads(sys.stdin.read(), object_pairs_hook=unique_object, parse_constant=reject_constant)
        result = check_ledger(data)
    except (LedgerError, ValueError, TypeError, KeyError, OverflowError, RecursionError):
        print(json.dumps({"status": "INVALID_DECLARATION", "certifies_acceptance": False}))
        raise SystemExit(1)
    print(json.dumps(result, ensure_ascii=True))
    if result["missing_required"]:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
