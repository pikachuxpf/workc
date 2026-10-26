"""Strict response probe for declared RewardKit-style judge contracts, not a scoring runner."""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any


class ContractError(ValueError):
    pass


def _unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ContractError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def _reject_constant(value: str) -> None:
    raise ContractError(f"non-finite JSON constant: {value}")


def load_json(text: str) -> Any:
    return json.loads(text, object_pairs_hook=_unique_object, parse_constant=_reject_constant)


def validate_response(text: str, contracts: list[dict[str, Any]], *, flat: bool = False) -> dict[str, float]:
    if not isinstance(contracts, list) or not contracts:
        raise ContractError("contract must be a nonempty list")
    for item in contracts:
        if not isinstance(item, dict):
            raise ContractError("criterion contract must be an object")
        if any(not isinstance(item.get(key), str) or not item[key].strip() for key in ("id", "name")):
            raise ContractError("criterion identities must be nonempty strings")
    names = [item["name"] for item in contracts]
    ids = [item["id"] for item in contracts]
    if len(set(names)) != len(names) or len(set(ids)) != len(ids):
        raise ContractError("ambiguous criterion names or IDs")
    data = load_json(text)
    if not isinstance(data, dict):
        raise ContractError("response must be an object")
    if flat:
        if len(contracts) != 1:
            raise ContractError("flat response needs exactly one request criterion")
        data = {names[0]: data}
    if set(data) != set(names):
        raise ContractError("response members differ from request members")
    normalized = {}
    for item in contracts:
        entry = data[item["name"]]
        if not isinstance(entry, dict) or set(entry) != {"score", "reasoning"}:
            raise ContractError("score/reasoning fields must match the declared schema")
        if not isinstance(entry["reasoning"], str) or not entry["reasoning"].strip():
            raise ContractError("reasoning must be a nonempty string")
        raw = entry["score"]
        kind = item["kind"]
        if kind == "binary":
            if type(raw) is not str or raw not in {"yes", "no"}:
                raise ContractError("binary score must be yes or no")
            value = float(raw == "yes")
        elif kind in {"likert", "numeric"}:
            low, high = item["min"], item["max"]
            if type(low) not in {int, float} or type(high) not in {int, float} or not (math.isfinite(low) and math.isfinite(high) and high > low):
                raise ContractError("invalid declared scale")
            if type(raw) not in {int, float} or not math.isfinite(raw):
                raise ContractError("score must be a finite number, not a boolean")
            if kind == "likert" and type(raw) is not int:
                raise ContractError("likert score must be an integer")
            if not low <= raw <= high:
                raise ContractError("raw score is outside the declared scale")
            span = high - low
            if not math.isfinite(span):
                raise ContractError("declared scale arithmetic overflows")
            value = (raw - low) / span
            if not math.isfinite(value) or not 0.0 <= value <= 1.0:
                raise ContractError("normalized value must be finite and within scale")
        else:
            raise ContractError("unsupported contract kind")
        negate = item.get("negate", False)
        if type(negate) is not bool:
            raise ContractError("negate must be boolean")
        normalized[item["id"]] = 1.0 - value if negate else value
    return normalized


def validate_runtime_scores(scores: list[dict[str, Any]], expected: dict[str, float]) -> None:
    if not isinstance(scores, list) or len(scores) != len(expected):
        raise ContractError("runtime criterion count differs from contract")
    ids = [item.get("id") for item in scores if isinstance(item, dict)]
    if len(ids) != len(scores) or any(not isinstance(identity, str) for identity in ids):
        raise ContractError("runtime criterion identities must be strings")
    if len(set(ids)) != len(ids) or set(ids) != set(expected):
        raise ContractError("runtime criterion identities are not exact-once")
    for item in scores:
        value = item.get("value")
        if type(value) not in {int, float} or not math.isfinite(value) or value != expected[item["id"]]:
            raise ContractError("runtime normalized value differs from contract")
        if item.get("error") or item.get("raw") is None:
            raise ContractError("runtime criterion has an infrastructure error")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--contract", type=Path, required=True)
    parser.add_argument("--response", type=Path, required=True)
    parser.add_argument("--flat", action="store_true")
    args = parser.parse_args()
    try:
        contract = load_json(args.contract.read_text(encoding="utf-8"))
        validate_response(args.response.read_text(encoding="utf-8"), contract, flat=args.flat)
    except (ValueError, KeyError, TypeError, OverflowError, OSError) as exc:
        print(json.dumps({"status": "FAIL", "error_type": type(exc).__name__}))
        raise SystemExit(1)
    print(json.dumps({"status": "PASS", "scope": "declared response contract only"}))


if __name__ == "__main__":
    main()
