"""Verify benchmark/questions.json against data/manifest.json and data/corpus/."""

from __future__ import annotations

import json
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[2]
MANIFEST_PATH = ROOT_DIR / "data" / "manifest.json"
BENCHMARK_PATH = ROOT_DIR / "benchmark" / "questions.json"


def main() -> None:
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    docs_by_id = {doc["source_id"]: doc for doc in manifest["documents"]}

    benchmark = json.loads(BENCHMARK_PATH.read_text(encoding="utf-8"))
    questions = benchmark["questions"]

    dev_qs = [q for q in questions if q["split"] == "dev"]
    test_qs = [q for q in questions if q["split"] == "test"]
    filter_qs = [q for q in questions if q.get("filter")]
    test_filter_qs = [q for q in test_qs if q.get("filter")]

    assert len(questions) >= 20, f"Need >= 20 questions, got {len(questions)}"
    assert len(dev_qs) >= 15, f"Need >= 15 dev questions, got {len(dev_qs)}"
    assert len(test_qs) >= 5, f"Need >= 5 test questions, got {len(test_qs)}"
    assert len(filter_qs) >= 3, f"Need >= 3 filter questions, got {len(filter_qs)}"
    assert len(test_filter_qs) >= 1, f"Need >= 1 test filter question, got {len(test_filter_qs)}"

    errors: list[str] = []
    for q in questions:
        qid = q["id"]
        sid = q["gold_source_id"]
        if sid not in docs_by_id:
            errors.append(f"{qid}: gold_source_id '{sid}' not found in manifest")
            continue
        doc = docs_by_id[sid]
        if q["gold_page"] != doc["unit_id"]:
            errors.append(f"{qid}: gold_page {q['gold_page']} != manifest unit_id {doc['unit_id']}")

        doc_path = ROOT_DIR / doc["file_path"]
        text = doc_path.read_text(encoding="utf-8")
        if q["evidence_quote"] not in text:
            errors.append(f"{qid}: evidence_quote not found verbatim in {doc['file_path']}")

        if q.get("filter"):
            for k, v in q["filter"].items():
                if doc.get(k) != v:
                    errors.append(f"{qid}: filter {k}={v} does not match doc[{k}]={doc.get(k)}")

    if errors:
        for err in errors:
            print(f"ERROR: {err}")
        raise SystemExit(1)

    print(
        f"Benchmark OK: {len(questions)} questions "
        f"(dev={len(dev_qs)}, test={len(test_qs)}, filter_total={len(filter_qs)}, filter_test={len(test_filter_qs)})."
    )
    print("All gold_source_id, gold_page, filter metadata, and evidence_quote strings verified 100% verbatim!")


if __name__ == "__main__":
    main()

