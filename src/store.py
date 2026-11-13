"""Store and search vectors using PostgreSQL + pgvector with cosine distance."""

from __future__ import annotations

import json
from typing import Any

import psycopg
from psycopg import sql

from .models import Chunk

ALLOWED_FILTER_COLUMNS = {"section", "document_id", "page"}


class PgVectorStore:
    def __init__(self, database_url: str, dimensions: int) -> None:
        if not database_url:
            raise ValueError("database_url is required")
        if dimensions <= 0:
            raise ValueError("dimensions must be > 0")
        self.database_url = database_url
        self.dimensions = dimensions

    @staticmethod
    def _vector_literal(vec: list[float]) -> str:
        return "[" + ",".join(f"{v:.8f}" for v in vec) + "]"

    def create_schema(self) -> None:
        """Create chunks table with vector(dimensions) and metadata columns/indexes."""
        with psycopg.connect(self.database_url) as conn:
            with conn.cursor() as cur:
                cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")
                cur.execute(
                    f"""
                    CREATE TABLE IF NOT EXISTS chunks (
                        strategy TEXT NOT NULL,
                        chunk_id TEXT NOT NULL,
                        document_id TEXT NOT NULL,
                        source TEXT NOT NULL,
                        page INTEGER NOT NULL,
                        section TEXT NOT NULL,
                        text TEXT NOT NULL,
                        metadata JSONB NOT NULL,
                        embedding VECTOR({self.dimensions}) NOT NULL,
                        PRIMARY KEY (strategy, chunk_id)
                    );
                    """
                )
                cur.execute("CREATE INDEX IF NOT EXISTS idx_chunks_strategy_section ON chunks (strategy, section);")
                cur.execute("CREATE INDEX IF NOT EXISTS idx_chunks_strategy_doc ON chunks (strategy, document_id);")
            conn.commit()

    def count_chunks(self, strategy: str) -> int:
        with psycopg.connect(self.database_url) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT COUNT(*) FROM chunks WHERE strategy = %s;", (strategy,))
                row = cur.fetchone()
                return int(row[0]) if row else 0

    def upsert(self, strategy: str, chunks: list[Chunk], vectors: list[list[float]]) -> None:
        """Validate lengths/dimensions, remove obsolete chunks for re-ingested docs, and upsert."""
        if len(chunks) != len(vectors):
            raise ValueError(f"chunks ({len(chunks)}) and vectors ({len(vectors)}) length mismatch")
        if not chunks:
            return

        for idx, vec in enumerate(vectors):
            if len(vec) != self.dimensions:
                raise ValueError(f"Vector {idx} has {len(vec)} dims, expected {self.dimensions}")

        doc_to_ids: dict[str, list[str]] = {}
        for c in chunks:
            doc_to_ids.setdefault(c.document_id, []).append(c.chunk_id)

        with psycopg.connect(self.database_url) as conn:
            with conn.cursor() as cur:
                # Delete obsolete chunks for each document being re-ingested
                for doc_id, keep_ids in doc_to_ids.items():
                    cur.execute(
                        "DELETE FROM chunks WHERE strategy = %s AND document_id = %s AND NOT (chunk_id = ANY(%s));",
                        (strategy, doc_id, keep_ids),
                    )

                upsert_sql = """
                    INSERT INTO chunks (strategy, chunk_id, document_id, source, page, section, text, metadata, embedding)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s::jsonb, %s::vector)
                    ON CONFLICT (strategy, chunk_id) DO UPDATE SET
                        document_id = EXCLUDED.document_id,
                        source = EXCLUDED.source,
                        page = EXCLUDED.page,
                        section = EXCLUDED.section,
                        text = EXCLUDED.text,
                        metadata = EXCLUDED.metadata,
                        embedding = EXCLUDED.embedding;
                """
                rows = [
                    (
                        strategy,
                        c.chunk_id,
                        c.document_id,
                        c.source,
                        int(c.page),
                        str(c.metadata.get("section", "general")),
                        c.text,
                        json.dumps(c.metadata, ensure_ascii=False),
                        self._vector_literal(vec),
                    )
                    for c, vec in zip(chunks, vectors)
                ]
                cur.executemany(upsert_sql, rows)
            conn.commit()

    def search(
        self,
        strategy: str,
        query_vector: list[float],
        top_k: int = 3,
        filters: dict[str, Any] | None = None,
    ) -> list[dict[str, Any]]:
        """Filter permitted metadata in SQL, rank by cosine distance, and return top-k."""
        if len(query_vector) != self.dimensions:
            raise ValueError(f"Query vector has {len(query_vector)} dims, expected {self.dimensions}")

        where_clauses = [sql.SQL("strategy = %s")]
        params: list[Any] = [strategy]

        if filters:
            for col, val in filters.items():
                if col not in ALLOWED_FILTER_COLUMNS:
                    raise ValueError(f"Unsupported filter column: {col}")
                where_clauses.append(sql.SQL("{} = %s").format(sql.Identifier(col)))
                params.append(val)

        vec_str = self._vector_literal(query_vector)
        query = sql.SQL(
            """
            SELECT chunk_id, text, (1 - (embedding <=> %s::vector)) AS score, metadata
            FROM chunks
            WHERE {where_sql}
            ORDER BY embedding <=> %s::vector ASC
            LIMIT %s;
            """
        ).format(where_sql=sql.SQL(" AND ").join(where_clauses))

        full_params = [vec_str, *params, vec_str, top_k]
        with psycopg.connect(self.database_url) as conn:
            with conn.cursor() as cur:
                cur.execute(query, full_params)
                rows = cur.fetchall()

        return [
            {
                "chunk_id": row[0],
                "text": row[1],
                "score": round(float(row[2]), 6),
                "metadata": row[3] if isinstance(row[3], dict) else json.loads(row[3]),
            }
            for row in rows
        ]
