"""Implement fixed-size and structure-aware (paragraph/heading) chunking."""

from __future__ import annotations

import re

from .models import Chunk, DocumentPage


def fixed_size(page: DocumentPage, size: int = 500, overlap: int = 50, strategy: str = "A") -> list[Chunk]:
    """Split page text into overlapping fixed-size character windows and retain page metadata."""
    if size <= 0:
        raise ValueError("size must be > 0")
    if overlap < 0 or overlap >= size:
        raise ValueError("overlap must be >= 0 and < size")

    text = page.text
    chunks: list[Chunk] = []
    step = size - overlap
    start = 0
    idx = 0

    while start < len(text):
        end = min(start + size, len(text))
        piece = text[start:end].strip()
        if piece:
            idx += 1
            chunk_id = f"{page.document_id}::{strategy}::{idx:04d}"
            meta = {**page.metadata, "strategy": strategy, "chunk_index": idx, "char_start": start, "char_end": end}
            chunks.append(
                Chunk(
                    chunk_id=chunk_id,
                    document_id=page.document_id,
                    source=page.source,
                    page=page.page,
                    text=piece,
                    metadata=meta,
                )
            )
        if end == len(text):
            break
        start += step

    return chunks


def _split_oversized_block(block: str, max_size: int) -> list[str]:
    """Split an oversized block on sentence or line boundaries to stay within max_size."""
    if len(block) <= max_size:
        return [block]

    parts: list[str] = []
    lines = block.split("\n")
    current = ""
    for line in lines:
        candidate = f"{current}\n{line}".strip() if current else line
        if len(candidate) <= max_size:
            current = candidate
            continue
        if current:
            parts.append(current)
            current = ""
        if len(line) <= max_size:
            current = line
        else:
            # Hard-split very long single lines (e.g. minified JSON or URLs) by sentence/space
            sentences = re.split(r"(?<=[.!?])\s+", line)
            buf = ""
            for sent in sentences:
                cand = f"{buf} {sent}".strip() if buf else sent
                if len(cand) <= max_size:
                    buf = cand
                else:
                    if buf:
                        parts.append(buf)
                    if len(sent) <= max_size:
                        buf = sent
                    else:
                        for i in range(0, len(sent), max_size):
                            parts.append(sent[i : i + max_size].strip())
                        buf = ""
            if buf:
                current = buf
    if current:
        parts.append(current)
    return [p for p in parts if p]


def by_paragraph(page: DocumentPage, max_size: int = 800, strategy: str = "B") -> list[Chunk]:
    """Group paragraphs/headings up to max_size, split oversized paragraphs, and retain metadata."""
    if max_size <= 0:
        raise ValueError("max_size must be > 0")

    raw_blocks = [b.strip() for b in re.split(r"\n{2,}", page.text) if b.strip()]
    blocks: list[str] = []
    for block in raw_blocks:
        blocks.extend(_split_oversized_block(block, max_size))

    chunks: list[Chunk] = []
    current = ""
    idx = 0

    for block in blocks:
        is_heading = block.lstrip().startswith("#")
        # Start a new chunk before major headings if buffer is already substantial
        if current and is_heading and len(current) >= max_size // 2:
            idx += 1
            chunk_id = f"{page.document_id}::{strategy}::{idx:04d}"
            meta = {**page.metadata, "strategy": strategy, "chunk_index": idx}
            chunks.append(
                Chunk(
                    chunk_id=chunk_id,
                    document_id=page.document_id,
                    source=page.source,
                    page=page.page,
                    text=current,
                    metadata=meta,
                )
            )
            current = block
            continue

        candidate = f"{current}\n\n{block}" if current else block
        if len(candidate) <= max_size:
            current = candidate
        else:
            if current:
                idx += 1
                chunk_id = f"{page.document_id}::{strategy}::{idx:04d}"
                meta = {**page.metadata, "strategy": strategy, "chunk_index": idx}
                chunks.append(
                    Chunk(
                        chunk_id=chunk_id,
                        document_id=page.document_id,
                        source=page.source,
                        page=page.page,
                        text=current,
                        metadata=meta,
                    )
                )
            current = block

    if current:
        idx += 1
        chunk_id = f"{page.document_id}::{strategy}::{idx:04d}"
        meta = {**page.metadata, "strategy": strategy, "chunk_index": idx}
        chunks.append(
            Chunk(
                chunk_id=chunk_id,
                document_id=page.document_id,
                source=page.source,
                page=page.page,
                text=current,
                metadata=meta,
            )
        )

    return chunks
