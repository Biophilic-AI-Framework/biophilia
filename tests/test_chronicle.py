"""Tests for IntegrityChronicle: record, hash-chain, and tamper detection."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from biophilia.audit.chronicle import IntegrityChronicle


@pytest.fixture()
def chronicle(tmp_path: Path) -> IntegrityChronicle:
    return IntegrityChronicle(log_dir=tmp_path)


class TestRecordAndVerify:
    def test_empty_chronicle_is_intact(self, chronicle: IntegrityChronicle) -> None:
        assert chronicle.verify_integrity() is True

    def test_single_record_is_intact(self, chronicle: IntegrityChronicle) -> None:
        chronicle.record_action("Node_01", "TEST", "Pillar I", "unit test", 1.0)
        assert chronicle.verify_integrity() is True

    def test_multiple_records_build_valid_chain(self, chronicle: IntegrityChronicle) -> None:
        for i in range(5):
            chronicle.record_action("Node_01", f"ACTION_{i}", "P", f"reason {i}", float(i))
        assert chronicle.verify_integrity() is True

    def test_genesis_hash_on_first_record(self, chronicle: IntegrityChronicle) -> None:
        chronicle.record_action("Node_01", "FIRST", "P", "genesis test", 0.0)
        history = json.loads(chronicle.filename.read_text())
        assert history[0]["previous_hash"] == "0" * 64

    def test_second_record_links_to_first(self, chronicle: IntegrityChronicle) -> None:
        chronicle.record_action("Node_01", "A", "P", "first", 1.0)
        chronicle.record_action("Node_01", "B", "P", "second", 2.0)
        history = json.loads(chronicle.filename.read_text())
        assert history[1]["previous_hash"] == history[0]["current_hash"]

    def test_get_last_hash_matches_file(self, chronicle: IntegrityChronicle) -> None:
        chronicle.record_action("Node_01", "X", "P", "x", 0.0)
        history = json.loads(chronicle.filename.read_text())
        assert chronicle.get_last_hash() == history[-1]["current_hash"]

    def test_get_last_hash_empty_returns_genesis(self, chronicle: IntegrityChronicle) -> None:
        assert chronicle.get_last_hash() == "0" * 64


class TestTamperDetection:
    def test_modified_reason_detected(self, chronicle: IntegrityChronicle) -> None:
        chronicle.record_action("N", "A", "P", "original", 1.0)
        history = json.loads(chronicle.filename.read_text())
        history[0]["reason"] = "TAMPERED"
        chronicle.filename.write_text(json.dumps(history))
        assert chronicle.verify_integrity() is False

    def test_removed_record_detected_via_chain_break(self, chronicle: IntegrityChronicle) -> None:
        for i in range(3):
            chronicle.record_action("N", f"A{i}", "P", "r", 0.0)
        history = json.loads(chronicle.filename.read_text())
        # Remove middle record → chain break between 0 and 1 (now the old 2).
        del history[1]
        chronicle.filename.write_text(json.dumps(history))
        assert chronicle.verify_integrity() is False

    def test_reason_dict_is_serialised_deterministically(
        self, chronicle: IntegrityChronicle
    ) -> None:
        reason = {"node": "N1", "pillar": "P1", "state": "HARMONY"}
        chronicle.record_action("N1", "ACT", "P1", reason, 2.5)
        assert chronicle.verify_integrity() is True
