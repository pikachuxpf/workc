from __future__ import annotations

import json
import unittest

from check_judge_response import ContractError, validate_response, validate_runtime_scores


class ResponseContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.contract = [
            {"id": "q-a", "name": "alpha", "kind": "likert", "min": 1, "max": 5},
            {"id": "q-b", "name": "beta", "kind": "likert", "min": 1, "max": 5},
        ]
        self.response = {
            "alpha": {"score": 5, "reasoning": "Observed alpha."},
            "beta": {"score": 1, "reasoning": "Observed beta."},
        }

    def check_bad(self, data) -> None:
        with self.assertRaises((ContractError, ValueError)):
            validate_response(json.dumps(data), self.contract)

    def test_correct_binding(self) -> None:
        self.assertEqual(validate_response(json.dumps(self.response), self.contract), {"q-a": 1.0, "q-b": 0.0})

    def test_boundaries_and_middle(self) -> None:
        self.response["alpha"]["score"] = 3
        self.assertEqual(validate_response(json.dumps(self.response), self.contract)["q-a"], 0.5)

    def test_missing_member(self) -> None:
        self.response.pop("beta")
        self.check_bad(self.response)

    def test_extra_member(self) -> None:
        self.response["gamma"] = self.response["beta"]
        self.check_bad(self.response)

    def test_duplicate_json_key(self) -> None:
        with self.assertRaises(ContractError):
            validate_response('{"alpha":{"score":5,"reasoning":"ok"},"alpha":{"score":1,"reasoning":"bad"},"beta":{"score":1,"reasoning":"bad"}}', self.contract)

    def test_bad_raw_values(self) -> None:
        for raw in [0, 6, True, "5", 1.5, float("nan"), float("inf")]:
            with self.subTest(raw=raw):
                self.response["alpha"]["score"] = raw
                self.check_bad(self.response)

    def test_missing_or_bad_reason(self) -> None:
        for reason in [None, 4, ""]:
            self.response["alpha"]["reasoning"] = reason
            self.check_bad(self.response)
        self.response["alpha"].pop("reasoning")
        self.check_bad(self.response)

    def test_extra_field(self) -> None:
        self.response["alpha"]["wrong_id"] = "beta"
        self.check_bad(self.response)

    def test_flat_response(self) -> None:
        text = '{"score":5,"reasoning":"observed"}'
        self.assertEqual(validate_response(text, self.contract[:1], flat=True), {"q-a": 1.0})
        with self.assertRaises(ContractError):
            validate_response(text, self.contract, flat=True)

    def test_duplicate_identity(self) -> None:
        self.contract[1]["id"] = "q-a"
        with self.assertRaises(ContractError):
            validate_response(json.dumps(self.response), self.contract)

    def test_negate_and_numeric(self) -> None:
        contract = [{"id": "n", "name": "numeric", "kind": "numeric", "min": 0, "max": 10, "negate": True}]
        self.assertEqual(validate_response('{"score":2,"reasoning":"observed"}', contract, flat=True), {"n": 0.8})

    def test_extreme_finite_scale_rejected(self) -> None:
        contract = [{"id": "n", "name": "numeric", "kind": "numeric", "min": -1e308, "max": 1e308}]
        for raw in [0, 1e308]:
            with self.subTest(raw=raw), self.assertRaises(ContractError):
                validate_response(json.dumps({"score": raw, "reasoning": "observed"}), contract, flat=True)

    def test_malformed_contract(self) -> None:
        for contract in [None, {}, [None], [{"id": [], "name": "a"}], [{"id": "", "name": "a"}]]:
            with self.subTest(contract=contract), self.assertRaises(ContractError):
                validate_response(json.dumps(self.response), contract)

    def test_runtime_exact_once(self) -> None:
        scores = [{"id": "q-a", "value": 1.0, "raw": 5}, {"id": "q-b", "value": 0.0, "raw": 1}]
        expected = {"q-a": 1.0, "q-b": 0.0}
        validate_runtime_scores(scores, expected)
        bad_cases = [scores + [{"id": "q-a", "value": 0.0, "raw": 1}], [scores[0], scores[0]], scores[:1], [scores[0], {"id": "ghost", "value": 0.0, "raw": 1}]]
        for bad in bad_cases:
            with self.subTest(scores=bad), self.assertRaises(ContractError):
                validate_runtime_scores(bad, expected)

    def test_runtime_error_and_invalid_value(self) -> None:
        for values in [{"value": True, "raw": 5}, {"value": float("nan"), "raw": 5}, {"value": 1.0, "raw": None}, {"value": 1.0, "raw": 5, "error": "timeout"}]:
            with self.subTest(values=values), self.assertRaises(ContractError):
                validate_runtime_scores([{"id": "q-a", **values}], {"q-a": 1.0})

    def test_binary(self) -> None:
        contract = [{"id": "b", "name": "binary", "kind": "binary"}]
        self.assertEqual(validate_response('{"score":"yes","reasoning":"observed"}', contract, flat=True), {"b": 1.0})


if __name__ == "__main__":
    unittest.main()
