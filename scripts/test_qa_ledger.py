from __future__ import annotations

import copy
import io
import json
import unittest
from unittest.mock import patch

from check_qa_ledger import LedgerError, check_ledger, main, ratio


def identity(key, kind="check", **fields):
    return {"key": key, "kind": kind, "source_ref": "allowed:source", "verified": True, **fields}


def ledger():
    return {
        "schema_version": 1,
        "baseline": {
            "id": "b0", "origin": "original", "scope": "whole-task",
            "source_ref": "authoritative:mapping", "captured_at": "before-edit",
            "verified": True,
            "identities": [identity("r0", "criterion"), identity("t0")],
        },
        "current": [identity("r1", "criterion", inherits="r0"), identity("t1", inherits="t0")],
        "fixes": [],
        "requirements": [{"id": "preimage", "kind": "ROUND_PREIMAGE", "scope": "target",
                          "required": True, "state": "VERIFIED", "actual_ref": "report:preimage",
                          "source_authority": "observed-before-edit"}],
    }


class LedgerTests(unittest.TestCase):
    def test_complete_no_change(self):
        result = check_ledger(ledger())
        self.assertEqual((result["N0"], result["F"], result["A"]), (2, 0, 0))
        self.assertEqual(result["error_rate"], "0%（0/2）")
        self.assertEqual(result["omission_rate"], "0%（0/2）")
        self.assertFalse(result["certifies_acceptance"])

    def test_fix_and_addition(self):
        data = ledger()
        data["current"].append(identity("new", inherits=None))
        data["fixes"] = [{"root_id": "issue", "baseline_root": True, "fixed": True,
                          "verified": True, "freshness": "FRESH", "evidence_ref": "run:actual"}]
        result = check_ledger(data)
        self.assertEqual(result["error_rate"], "50%（1/2）")
        self.assertEqual(result["omission_rate"], "33.33%（1/3）")
        self.assertEqual((result["AR"], result["AT"]), (0, 1))

    def test_delete_does_not_change_denominator(self):
        data = ledger()
        data["current"].pop()
        result = check_ledger(data)
        self.assertEqual((result["N0"], result["DT"], result["A"]), (2, 1, 0))

    def test_handoff_is_labelled(self):
        data = ledger()
        data["baseline"]["origin"] = "handoff"
        self.assertEqual(check_ledger(data)["metric_label"], "接手阶段指标")

    def test_unknowns_do_not_become_zero(self):
        for field in ("baseline", "current", "fixes"):
            data = ledger()
            data[field] = None
            result = check_ledger(data)
            rate = "error_rate" if field == "fixes" else "omission_rate"
            self.assertTrue(result[rate].startswith("N/A"))
        data = ledger()
        data["current"] = None
        self.assertEqual(check_ledger(data)["error_rate"], "0%（0/2）")

    def test_unverified_identity_keeps_unknown(self):
        data = ledger()
        data["baseline"]["identities"][0]["verified"] = False
        self.assertIsNone(check_ledger(data)["N0"])

    def test_duplicate_and_invalid_inheritance(self):
        for mode in ("duplicate", "reuse", "unknown", "kind"):
            data = ledger()
            if mode == "duplicate":
                data["baseline"]["identities"].append(identity("t0"))
            elif mode == "reuse":
                data["current"].append(identity("x", inherits="t0"))
            elif mode == "unknown":
                data["current"][0]["inherits"] = "missing"
            else:
                data["current"][0]["kind"] = "check"
            with self.subTest(mode=mode), self.assertRaises(LedgerError):
                check_ledger(data)

    def test_duplicate_root_requires_merge(self):
        data = ledger()
        row = {"root_id": "issue", "baseline_root": True, "fixed": True,
               "verified": True, "freshness": "FRESH", "evidence_ref": "run:actual"}
        data["fixes"] = [row, copy.deepcopy(row)]
        with self.assertRaises(LedgerError):
            check_ledger(data)

    def test_stale_and_newly_introduced_not_counted(self):
        for change in ({"freshness": "STALE"}, {"baseline_root": False}, {"fixed": False}, {"verified": False}):
            data = ledger()
            data["fixes"] = [{"root_id": "issue", "baseline_root": True, "fixed": True,
                              "verified": True, "freshness": "FRESH", "evidence_ref": "run:actual", **change}]
            self.assertEqual(check_ledger(data)["F"], 0)

    def test_rates_zero_large_and_rounding(self):
        self.assertEqual(ratio(3, 2), "150%（3/2）")
        self.assertEqual(ratio(0, 0), "N/A（0/0）")
        self.assertEqual(ratio(5, 5), "100%（5/5）")
        self.assertEqual(ratio(1, 6), "16.67%（1/6）")

    def test_empty_baseline_with_addition(self):
        data = ledger()
        data["baseline"]["identities"] = []
        data["current"] = [identity("new", inherits=None)]
        result = check_ledger(data)
        self.assertEqual(result["error_rate"], "N/A（0/0）")
        self.assertEqual(result["omission_rate"], "100%（1/1）")

    def test_missing_material_has_action_and_owner(self):
        data = ledger()
        data["requirements"] = [{"id": "history", "kind": "HISTORICAL_TRAJECTORY", "scope": "old-attempt",
                                 "required": True, "state": "EXHAUSTED", "acquisition_actions": ["checked formal index"],
                                 "remaining_gap": "original trajectory absent", "owner": "source-owner"}]
        result = check_ledger(data)
        self.assertFalse(result["checklist_ready"])
        self.assertEqual(result["missing_required"][0]["state"], "EXHAUSTED")
        data["requirements"][0]["acquisition_actions"] = []
        with self.assertRaises(LedgerError):
            check_ledger(data)

    def test_na_requires_reason(self):
        data = ledger()
        data["requirements"][0] = {"id": "no-object", "kind": "ORIGINAL_TASK", "scope": "report",
                                     "required": True, "state": "N/A"}
        with self.assertRaises(LedgerError):
            check_ledger(data)
        data["requirements"][0]["reason"] = "confirmed no report object"
        self.assertTrue(check_ledger(data)["checklist_ready"])

    def test_types_not_coerced(self):
        data = ledger()
        data["schema_version"] = True
        with self.assertRaises(LedgerError):
            check_ledger(data)
        data = ledger()
        data["baseline"]["verified"] = "yes"
        with self.assertRaises(LedgerError):
            check_ledger(data)

    def invoke(self, input_text):
        output = io.StringIO()
        code = 0
        with patch("sys.stdin", io.StringIO(input_text)), patch("sys.stdout", output):
            try:
                main()
            except SystemExit as exc:
                code = exc.code
        return code, output.getvalue()

    def test_cli_deep_json_is_controlled(self):
        code, output = self.invoke("[" * 2000 + "0" + "]" * 2000)
        self.assertEqual(code, 1)
        self.assertEqual(json.loads(output)["status"], "INVALID_DECLARATION")

    def test_cli_surrogate_is_ascii_safe(self):
        data = ledger()
        data["baseline"]["id"] = "\ud800"
        code, output = self.invoke(json.dumps(data))
        self.assertEqual(code, 0)
        output.encode("utf-8", errors="strict")
        self.assertEqual(json.loads(output)["baseline"]["id"], "\ud800")

    def test_cli_rc_and_no_input_echo(self):
        code, output = self.invoke(json.dumps(ledger()))
        self.assertEqual(code, 0)
        self.assertEqual(json.loads(output)["status"], "VALID_DECLARATION")
        code, output = self.invoke('{"schema_version":1,"schema_version":1,"private":"never echo"}')
        self.assertEqual(code, 1)
        self.assertNotIn("never echo", output)
        data = ledger()
        data["requirements"][0].update(state="NEEDS_AUTHORIZATION", acquisition_actions=[], remaining_gap="permission missing", owner="operator")
        self.assertEqual(self.invoke(json.dumps(data))[0], 2)


if __name__ == "__main__":
    unittest.main()
