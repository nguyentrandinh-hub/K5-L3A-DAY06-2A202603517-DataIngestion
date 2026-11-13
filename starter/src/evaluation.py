"""Evaluate retrieved evidence and preserve per-query traces."""

from __future__ import annotations

import re
from typing import Any


def _collapse_ws(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def _is_chunk_hit(question: dict[str, Any], hit: dict[str, Any]) -> bool:
    meta = hit.get("metadata") or {}
    if meta.get("document_id") != question["gold_source_id"]:
        return False
    if int(meta.get("page", -1)) != int(question["gold_page"]):
        return False

    evidence_norm = _collapse_ws(question["evidence_quote"])
    chunk_norm = _collapse_ws(hit.get("text", ""))
    return evidence_norm in chunk_norm


def evaluate_query(question: dict[str, Any], hits: list[dict[str, Any]], applied_filter: dict[str, Any] | None = None) -> dict[str, Any]:
    """Check source/page and gold evidence; keep hit@1, hit@3, and filter compliance trace."""
    hit_flags = [_is_chunk_hit(question, h) for h in hits]
    hit_at_1 = bool(hit_flags and hit_flags[0])
    evidence_hit_at_3 = any(hit_flags[:3])

    q_filter = question.get("filter")
    filter_compliant: bool | None = None
    if q_filter:
        filter_compliant = bool(hits) and all(
            all((h.get("metadata") or {}).get(k) == v for k, v in q_filter.items())
            for h in hits[:3]
        )

    metadata_complete = all(
        bool((h.get("metadata") or {}).get("source"))
        and (h.get("metadata") or {}).get("page") is not None
        and bool((h.get("metadata") or {}).get("section"))
        for h in hits[:3]
    )

    return {
        "question_id": question["id"],
        "split": question["split"],
        "type": question.get("type", ""),
        "question": question["question"],
        "gold_source_id": question["gold_source_id"],
        "gold_page": question["gold_page"],
        "evidence_quote": question["evidence_quote"],
        "expected_filter": q_filter,
        "applied_filter": applied_filter,
        "hit_at_1": hit_at_1,
        "evidence_hit_at_3": evidence_hit_at_3,
        "filter_compliant": filter_compliant,
        "metadata_complete": metadata_complete,
        "per_hit_match": hit_flags,
        "top_k": hits,
    }


def summarize(traces: list[dict[str, Any]]) -> dict[str, Any]:
    """Aggregate Hit@1, Evidence Hit@3, and filter compliance by split."""
    summary: dict[str, Any] = {}
    for split in ("dev", "test", "all"):
        subset = traces if split == "all" else [t for t in traces if t["split"] == split]
        n = len(subset)
        if n == 0:
            continue
        hit1 = sum(1 for t in subset if t["hit_at_1"])
        hit3 = sum(1 for t in subset if t["evidence_hit_at_3"])
        filter_items = [t for t in subset if t["filter_compliant"] is not None]
        filter_ok = sum(1 for t in filter_items if t["filter_compliant"])
        summary[split] = {
            "total": n,
            "hit_at_1": hit1,
            "hit_at_1_rate": round(hit1 / n, 4),
            "evidence_hit_at_3": hit3,
            "evidence_hit_at_3_rate": round(hit3 / n, 4),
            "filter_questions": len(filter_items),
            "filter_compliant": filter_ok if filter_items else None,
        }
    return summary
