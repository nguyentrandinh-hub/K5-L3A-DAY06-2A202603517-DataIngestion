"""Fetch official Gemini API documentation pages in Markdown format and build data/manifest.json."""

from __future__ import annotations

import json
import re
import time
import unicodedata
from datetime import date
from pathlib import Path
from urllib.parse import urlparse

import requests

ROOT_DIR = Path(__file__).resolve().parents[2]
CORPUS_DIR = ROOT_DIR / "data" / "corpus"
MANIFEST_PATH = ROOT_DIR / "data" / "manifest.json"
LOG_PATH = ROOT_DIR / "results" / "corpus_fetch_log.json"

LLMS_INDEX_URLS = [
    "https://aistudio.google.com/llms.txt",
    "https://ai.google.dev/gemini-api/docs/llms.txt",
]

MIN_CHARS = 1500
TARGET_COUNT = 40
MAX_PER_SECTION = 10
HEADERS = {"User-Agent": "K5-L3-Day06-DataIngestionEngineering/1.0"}


def normalize_text(text: str) -> str:
    text = unicodedata.normalize("NFC", text)
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def infer_section(url: str, heading: str) -> str:
    path = urlparse(url).path.lower()
    if "/models" in path or "model" in heading.lower() or "pricing" in path:
        return "models_and_pricing"
    if "/function-calling" in path or "/tools" in path or "/interactions" in path or "agent" in heading.lower():
        return "tools_and_agents"
    if "/api" in path or "/reference" in path or "reference" in heading.lower():
        return "api_reference"
    if "/get-started" in path or "/quickstart" in path or "/api-key" in path or "start" in heading.lower():
        return "getting_started"
    return "core_guides"


def fetch_llms_links() -> tuple[str, list[dict[str, str]]]:
    for index_url in LLMS_INDEX_URLS:
        try:
            resp = requests.get(index_url, headers=HEADERS, timeout=20)
            if resp.status_code == 200 and ".md" in resp.text:
                links: list[dict[str, str]] = []
                current_heading = "general"
                seen_urls: set[str] = set()
                for line in resp.text.splitlines():
                    stripped = line.strip()
                    if stripped.startswith("#"):
                        current_heading = stripped.lstrip("#").strip()
                        continue
                    match = re.search(r"\[([^\]]+)\]\((https?://[^\s)]+)\)", stripped)
                    if not match:
                        continue
                    title, url = match.group(1).strip(), match.group(2).strip()
                    if not url.endswith(".md"):
                        continue
                    if "llms" in url or url in seen_urls:
                        continue
                    seen_urls.add(url)
                    links.append(
                        {
                            "title": title,
                            "url": url,
                            "section": infer_section(url, current_heading),
                        }
                    )
                if links:
                    return index_url, links
        except requests.RequestException:
            continue
    raise RuntimeError("Could not fetch llms.txt index from official Gemini API Docs.")


def slugify_url(url: str) -> str:
    path = urlparse(url).path.strip("/")
    if path.endswith(".md"):
        path = path[:-3]
    slug = re.sub(r"[^a-zA-Z0-9_-]+", "_", path).strip("_")
    return slug or "index"


def main() -> None:
    CORPUS_DIR.mkdir(parents=True, exist_ok=True)
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)

    index_url, links = fetch_llms_links()
    print(f"Loaded {len(links)} candidate markdown links from {index_url}")

    valid_docs: list[dict] = []
    skipped_docs: list[dict] = []
    section_counts: dict[str, int] = {}

    # Clear previous corpus files so re-running stays clean
    for old_file in CORPUS_DIR.glob("*.md"):
        old_file.unlink()

    for item in links:
        if len(valid_docs) >= TARGET_COUNT:
            break
        sec = item["section"]
        if section_counts.get(sec, 0) >= MAX_PER_SECTION:
            continue
        url = item["url"]
        try:
            resp = requests.get(url, headers=HEADERS, timeout=20)
            if resp.status_code != 200:
                skipped_docs.append({"url": url, "reason": f"HTTP {resp.status_code}"})
                continue
            content = normalize_text(resp.text)
            char_count = len(content)
            if char_count < MIN_CHARS:
                skipped_docs.append({"url": url, "reason": f"Too short ({char_count} < {MIN_CHARS} chars)"})
                continue

            idx = len(valid_docs) + 1
            source_id = f"gemini-doc-{idx:02d}"
            filename = f"{idx:02d}_{slugify_url(url)}.md"
            file_path = CORPUS_DIR / filename
            file_path.write_text(content, encoding="utf-8")

            valid_docs.append(
                {
                    "source_id": source_id,
                    "unit_id": idx,
                    "title": item["title"],
                    "section": item["section"],
                    "file_path": f"data/corpus/{filename}",
                    "source_path_or_url": url,
                    "license_or_permission": "CC BY 4.0 (documentation) / Apache 2.0 (code samples) - Google AI Developers",
                    "accessed_at": date.today().isoformat(),
                    "normalized_char_count": char_count,
                }
            )
            section_counts[item["section"]] = section_counts.get(item["section"], 0) + 1
            print(f"[{idx:02d}/{TARGET_COUNT}] Saved {filename} ({char_count} chars, section={item['section']})")
            time.sleep(0.15)
        except requests.RequestException as exc:
            skipped_docs.append({"url": url, "reason": str(exc)})

    sections_summary: dict[str, int] = {}
    for doc in valid_docs:
        sec = doc["section"]
        sections_summary[sec] = sections_summary.get(sec, 0) + 1

    manifest = {
        "corpus_topic": "Google Gemini API & AI Studio Official Documentation",
        "index_source": index_url,
        "unit_counting_rule": (
            "Each Markdown documentation page from the official Gemini API Docs is treated as 1 independent "
            f"source unit. Only pages with >= {MIN_CHARS} normalized characters (NFC) are included; "
            "short index/stub pages are excluded and logged."
        ),
        "total_valid_units": len(valid_docs),
        "total_normalized_chars": sum(d["normalized_char_count"] for d in valid_docs),
        "sections_distribution": sections_summary,
        "documents": valid_docs,
    }
    MANIFEST_PATH.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")

    fetch_log = {
        "index_url": index_url,
        "candidate_links_found": len(links),
        "valid_units_saved": len(valid_docs),
        "skipped_count": len(skipped_docs),
        "skipped_details": skipped_docs,
    }
    LOG_PATH.write_text(json.dumps(fetch_log, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"\nDone! Saved {len(valid_docs)} valid units to {CORPUS_DIR}")
    print(f"Manifest written to {MANIFEST_PATH}")
    print(f"Fetch log written to {LOG_PATH}")
    print(f"Sections distribution: {sections_summary}")


if __name__ == "__main__":
    main()

