"""End-to-end Day 06 pipeline: ingest, chunk (A/B/C), embed, store in pgvector, and evaluate."""

from __future__ import annotations

import csv
import json
import os
import statistics
import time
from pathlib import Path
from typing import Any

from dotenv import load_dotenv

from .chunking import by_paragraph, fixed_size
from .embeddings import MyEmbedder
from .evaluation import evaluate_query, summarize
from .ingestion import load_corpus_from_manifest
from .models import Chunk
from .store import PgVectorStore


def _chunk_stats(chunks: list[Chunk]) -> dict[str, Any]:
    lengths = [len(c.text) for c in chunks]
    return {
        "chunk_count": len(chunks),
        "total_chars": sum(lengths),
        "min_len": min(lengths) if lengths else 0,
        "avg_len": round(statistics.mean(lengths), 1) if lengths else 0.0,
        "max_len": max(lengths) if lengths else 0,
    }


def _clone_chunks_for_strategy(chunks: list[Chunk], target_strategy: str) -> list[Chunk]:
    cloned: list[Chunk] = []
    for c in chunks:
        new_id = c.chunk_id.replace("::B::", f"::{target_strategy}::")
        new_meta = {**c.metadata, "strategy": target_strategy}
        cloned.append(
            Chunk(
                chunk_id=new_id,
                document_id=c.document_id,
                source=c.source,
                page=c.page,
                text=c.text,
                metadata=new_meta,
            )
        )
    return cloned


def _export_audit_samples(
    pages: list[Any],
    chunks_a: list[Chunk],
    chunks_b: list[Chunk],
    traces_by_strategy: dict[str, list[dict[str, Any]]],
    results_dir: Path,
) -> None:
    # 1. Coherence sample: first 10 unit_ids (sorted) across A and B (C shares B's chunks)
    coherence_path = results_dir / "audit_coherence_samples.csv"
    first_10_pages = sorted(pages, key=lambda p: p.page)[:10]
    with coherence_path.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                "unit_id",
                "document_id",
                "section",
                "source_preview_400chars",
                "strategy_A_first_2_chunks",
                "strategy_BC_first_2_chunks",
                "coherence_A_0_to_2",
                "reason_A",
                "coherence_BC_0_to_2",
                "reason_BC",
            ]
        )
        for p in first_10_pages:
            a_sample = " || ".join(c.text[:350] for c in chunks_a if c.document_id == p.document_id)[:750]
            b_sample = " || ".join(c.text[:350] for c in chunks_b if c.document_id == p.document_id)[:750]
            writer.writerow(
                [
                    p.page,
                    p.document_id,
                    p.metadata.get("section", ""),
                    p.text[:400].replace("\n", " "),
                    a_sample.replace("\n", " "),
                    b_sample.replace("\n", " "),
                    "",
                    "",
                    "",
                    "",
                ]
            )

    # 2. Grounding & Metadata sample: 5 test questions across A, B, C
    grounding_path = results_dir / "audit_grounding_samples.csv"
    with grounding_path.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                "strategy",
                "question_id",
                "question",
                "gold_source_id",
                "gold_page",
                "expected_filter",
                "hit_at_1",
                "evidence_hit_at_3",
                "filter_compliant",
                "top3_sources_pages",
                "top1_preview",
                "metadata_ok_count_out_of_3",
                "grounding_score_0_to_2",
                "grounding_reason",
            ]
        )
        for strat in ("A", "B", "C"):
            for tr in traces_by_strategy[strat]:
                if tr["split"] != "test":
                    continue
                top3_loc = "; ".join(
                    f"{h['metadata'].get('document_id')}:p{h['metadata'].get('page')}({h['metadata'].get('section')})"
                    for h in tr["top_k"]
                )
                top1_txt = tr["top_k"][0]["text"][:350].replace("\n", " ") if tr["top_k"] else ""
                writer.writerow(
                    [
                        strat,
                        tr["question_id"],
                        tr["question"],
                        tr["gold_source_id"],
                        tr["gold_page"],
                        json.dumps(tr["expected_filter"]) if tr["expected_filter"] else "None",
                        tr["hit_at_1"],
                        tr["evidence_hit_at_3"],
                        tr["filter_compliant"] if tr["filter_compliant"] is not None else "N/A",
                        top3_loc,
                        top1_txt,
                        "",
                        "",
                        "",
                    ]
                )


def main() -> None:
    starter_dir = Path(__file__).resolve().parents[1]
    root_dir = starter_dir.parent
    load_dotenv(starter_dir / ".env")

    database_url = os.getenv("DATABASE_URL", "").strip()
    if not database_url:
        raise RuntimeError("DATABASE_URL missing in starter/.env")

    manifest_path = root_dir / "data" / "manifest.json"
    benchmark_path = root_dir / "benchmark" / "questions.json"
    results_dir = root_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    # 1. Load & validate corpus (>= 30 content units)
    pages, ingestion_errors = load_corpus_from_manifest(manifest_path, root_dir)
    if len(pages) < 30:
        raise RuntimeError(f"Corpus must have >= 30 valid units, found {len(pages)}")
    (results_dir / "ingestion_log.json").write_text(
        json.dumps({"valid_units": len(pages), "errors": ingestion_errors}, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    print(f"Loaded {len(pages)} valid corpus units (errors={len(ingestion_errors)}).")

    # 2. Load benchmark
    benchmark = json.loads(benchmark_path.read_text(encoding="utf-8"))
    questions = benchmark["questions"]
    print(f"Loaded {len(questions)} benchmark questions.")

    # 3. Initialize embedder and PgVectorStore
    embedder = MyEmbedder()
    print(f"Initialized embedder: provider={embedder.provider}, model={embedder.model_name}, dims={embedder.dimensions}")
    store = PgVectorStore(database_url=database_url, dimensions=embedder.dimensions)
    store.create_schema()

    # 4. Build chunks for A, B, and C
    chunks_a: list[Chunk] = []
    chunks_b: list[Chunk] = []
    for p in pages:
        chunks_a.extend(fixed_size(p, size=500, overlap=50, strategy="A"))
        chunks_b.extend(by_paragraph(p, max_size=800, strategy="B"))
    chunks_c = _clone_chunks_for_strategy(chunks_b, "C")

    # 5. Embed & upsert A
    t0 = time.perf_counter()
    tokens_before_a = embedder.total_tokens
    cost_before_a = embedder.total_cost_usd
    vectors_a = embedder.embed_documents([c.text for c in chunks_a])
    store.upsert("A", chunks_a, vectors_a)
    time_a = round(time.perf_counter() - t0, 2)
    tokens_a = embedder.total_tokens - tokens_before_a
    cost_a = round(embedder.total_cost_usd - cost_before_a, 6)
    print(f"Strategy A ingested: {len(chunks_a)} chunks in {time_a}s (tokens={tokens_a}).")

    # 6. Embed & upsert B, then reuse B's vectors for C (controlled comparison: B vs C only differs by filter)
    t1 = time.perf_counter()
    tokens_before_b = embedder.total_tokens
    cost_before_b = embedder.total_cost_usd
    vectors_b = embedder.embed_documents([c.text for c in chunks_b])
    store.upsert("B", chunks_b, vectors_b)
    time_b = round(time.perf_counter() - t1, 2)
    tokens_b = embedder.total_tokens - tokens_before_b
    cost_b = round(embedder.total_cost_usd - cost_before_b, 6)
    print(f"Strategy B ingested: {len(chunks_b)} chunks in {time_b}s (tokens={tokens_b}).")

    t2 = time.perf_counter()
    store.upsert("C", chunks_c, vectors_b)
    time_c = round(time.perf_counter() - t2, 2)
    print(f"Strategy C ingested (reused B vectors): {len(chunks_c)} chunks in {time_c}s.")

    # 7. Idempotency check: re-upsert doc 1 into A and verify chunk count does not double
    count_a_before = store.count_chunks("A")
    doc1_chunks = [c for c in chunks_a if c.document_id == pages[0].document_id]
    doc1_vecs = vectors_a[: len(doc1_chunks)]
    store.upsert("A", doc1_chunks, doc1_vecs)
    count_a_after = store.count_chunks("A")
    idempotency_ok = count_a_before == count_a_after == len(chunks_a)
    print(f"Idempotency check on A: before={count_a_before}, after={count_a_after}, ok={idempotency_ok}")

    # 8. Embed all queries once, then evaluate A, B, C
    query_vectors = embedder.embed_documents([q["question"] for q in questions])

    traces_by_strategy: dict[str, list[dict[str, Any]]] = {}
    metrics_by_strategy: dict[str, Any] = {}
    query_times: dict[str, float] = {}

    for strat in ("A", "B", "C"):
        qt0 = time.perf_counter()
        strat_traces: list[dict[str, Any]] = []
        for q, qvec in zip(questions, query_vectors):
            applied_filter = q.get("filter") if strat == "C" else None
            hits = store.search(strategy=strat, query_vector=qvec, top_k=3, filters=applied_filter)
            strat_traces.append(evaluate_query(q, hits, applied_filter=applied_filter))
        query_times[strat] = round(time.perf_counter() - qt0, 3)
        traces_by_strategy[strat] = strat_traces
        metrics_by_strategy[strat] = summarize(strat_traces)

        (results_dir / f"traces_{strat}.json").write_text(
            json.dumps(strat_traces, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

    # 9. Save stats, metrics summary, and audit CSV templates
    ingestion_stats = {
        "provider": embedder.provider,
        "model_name": embedder.model_name,
        "dimensions": embedder.dimensions,
        "metric": "cosine",
        "total_tokens": embedder.total_tokens,
        "total_cost_usd": round(embedder.total_cost_usd, 6),
        "idempotency_check": {
            "strategy": "A",
            "count_before_reingest": count_a_before,
            "count_after_reingest": count_a_after,
            "passed": idempotency_ok,
        },
        "strategies": {
            "A": {**_chunk_stats(chunks_a), "ingest_seconds": time_a, "query_seconds": query_times["A"], "embed_tokens": tokens_a, "cost_usd": cost_a},
            "B": {**_chunk_stats(chunks_b), "ingest_seconds": time_b, "query_seconds": query_times["B"], "embed_tokens": tokens_b, "cost_usd": cost_b},
            "C": {**_chunk_stats(chunks_c), "ingest_seconds": time_c, "query_seconds": query_times["C"], "embed_tokens": 0, "cost_usd": 0.0, "note": "Reused B chunks & vectors; added SQL metadata filter at query time"},
        },
    }
    (results_dir / "ingestion_stats.json").write_text(
        json.dumps(ingestion_stats, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    (results_dir / "metrics_summary.json").write_text(
        json.dumps(metrics_by_strategy, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    _export_audit_samples(pages, chunks_a, chunks_b, traces_by_strategy, results_dir)

    print("\n=== RETRIEVAL METRICS SUMMARY ===")
    for strat in ("A", "B", "C"):
        d = metrics_by_strategy[strat]["dev"]
        t = metrics_by_strategy[strat]["test"]
        print(
            f"Strategy {strat} | DEV: Hit@1={d['hit_at_1']}/{d['total']} ({d['hit_at_1_rate']:.1%}), "
            f"Hit@3={d['evidence_hit_at_3']}/{d['total']} ({d['evidence_hit_at_3_rate']:.1%}) | "
            f"TEST: Hit@1={t['hit_at_1']}/{t['total']} ({t['hit_at_1_rate']:.1%}), "
            f"Hit@3={t['evidence_hit_at_3']}/{t['total']} ({t['evidence_hit_at_3_rate']:.1%})"
        )


if __name__ == "__main__":
    main()
