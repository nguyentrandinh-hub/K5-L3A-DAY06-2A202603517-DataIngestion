"""Read and normalize source data from manifest or PDF."""

from __future__ import annotations

import json
import re
import unicodedata
from pathlib import Path
from typing import Any

from pypdf import PdfReader

from .models import DocumentPage


def normalize_text(text: str) -> str:
    """Normalize Unicode (NFC) and clean excessive whitespace while preserving headings/paragraphs."""
    text = unicodedata.normalize("NFC", text)
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[ \t]+\n", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def load_pdf(path: Path, document_id: str, source: str, extra_metadata: dict[str, Any] | None = None) -> tuple[list[DocumentPage], list[dict[str, Any]]]:
    """Extract each physical page of a PDF; keep page number, source, and log empty pages."""
    reader = PdfReader(str(path))
    pages: list[DocumentPage] = []
    errors: list[dict[str, Any]] = []
    base_meta = dict(extra_metadata or {})

    for idx, page in enumerate(reader.pages, start=1):
        try:
            raw = page.extract_text() or ""
            norm = normalize_text(raw)
            if not norm:
                errors.append({"document_id": document_id, "page": idx, "reason": "Empty or unreadable page"})
                continue
            meta = {**base_meta, "document_id": document_id, "source": source, "page": idx}
            pages.append(DocumentPage(document_id=document_id, source=source, page=idx, text=norm, metadata=meta))
        except Exception as exc:  # pragma: no cover - defensive PDF error logging
            errors.append({"document_id": document_id, "page": idx, "reason": str(exc)})
    return pages, errors


def load_corpus_from_manifest(manifest_path: Path, root_dir: Path) -> tuple[list[DocumentPage], list[dict[str, Any]]]:
    """Load and normalize all corpus units listed in data/manifest.json."""
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    pages: list[DocumentPage] = []
    errors: list[dict[str, Any]] = []

    for doc in manifest.get("documents", []):
        file_path = root_dir / doc["file_path"]
        doc_id = doc["source_id"]
        unit_id = int(doc["unit_id"])
        source = doc["file_path"]

        if not file_path.exists():
            errors.append({"document_id": doc_id, "page": unit_id, "reason": f"Missing file: {file_path}"})
            continue

        raw_text = file_path.read_text(encoding="utf-8", errors="replace")
        norm = normalize_text(raw_text)
        if not norm:
            errors.append({"document_id": doc_id, "page": unit_id, "reason": "Empty content after normalization"})
            continue

        meta = {
            "document_id": doc_id,
            "source": source,
            "page": unit_id,
            "section": doc.get("section", "general"),
            "title": doc.get("title", ""),
            "url": doc.get("source_path_or_url", ""),
        }
        pages.append(
            DocumentPage(
                document_id=doc_id,
                source=source,
                page=unit_id,
                text=norm,
                metadata=meta,
            )
        )

    return pages, errors
