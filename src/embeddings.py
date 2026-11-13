"""Real embedding provider adapter (OpenRouter / OpenAI / Gemini); no mock fallback."""

from __future__ import annotations

import os
import time
from typing import Protocol

import requests


class Embedder(Protocol):
    model_name: str
    dimensions: int

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        """Return one vector per input text, in the same order."""
        ...

    def embed_query(self, question: str) -> list[float]:
        """Return a query vector compatible with the stored document vectors."""
        ...


class MyEmbedder:
    """OpenRouter / OpenAI-compatible embedding adapter with usage & cost tracking."""

    def __init__(self, model_name: str | None = None, batch_size: int = 64) -> None:
        self.openrouter_key = os.getenv("OPENROUTER_API_KEY", "").strip()
        self.openai_key = os.getenv("OPENAI_API_KEY", "").strip()
        self.gemini_key = os.getenv("GEMINI_API_KEY", "").strip()
        self.batch_size = batch_size

        raw_model = (model_name or os.getenv("EMBEDDING_MODEL") or "").strip()

        if self.openrouter_key:
            self.provider = "openrouter"
            if not raw_model:
                self.model_name = "openai/text-embedding-3-small"
            elif "/" not in raw_model and raw_model == "gemini-embedding-001":
                self.model_name = "google/gemini-embedding-001"
            elif "/" not in raw_model and raw_model.startswith("text-embedding-"):
                self.model_name = f"openai/{raw_model}"
            else:
                self.model_name = raw_model
            self.api_url = "https://openrouter.ai/api/v1/embeddings"
            self.headers = {
                "Authorization": f"Bearer {self.openrouter_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://github.com/day06-data-ingestion-lab",
                "X-Title": "Day06-DataIngestionEngineering",
            }
        elif self.openai_key:
            self.provider = "openai"
            self.model_name = raw_model or "text-embedding-3-small"
            self.api_url = "https://api.openai.com/v1/embeddings"
            self.headers = {
                "Authorization": f"Bearer {self.openai_key}",
                "Content-Type": "application/json",
            }
        elif self.gemini_key:
            self.provider = "gemini"
            self.model_name = raw_model or "gemini-embedding-001"
            from google import genai  # local import only when Gemini SDK is selected

            self._gemini_client = genai.Client(api_key=self.gemini_key)
        else:
            raise RuntimeError(
                "No embedding API key found in starter/.env. "
                "Set OPENROUTER_API_KEY, OPENAI_API_KEY, or GEMINI_API_KEY."
            )

        self.total_tokens: int = 0
        self.total_cost_usd: float = 0.0

        # Probe one short string to validate credentials and detect vector dimensions
        probe = self._embed_batch(["dimension probe"])
        if not probe or not probe[0]:
            raise RuntimeError(f"Embedding provider '{self.provider}' returned empty vector.")
        self.dimensions: int = len(probe[0])

    def _embed_batch(self, texts: list[str]) -> list[list[float]]:
        if not texts:
            return []

        if self.provider == "gemini":
            result = self._gemini_client.models.embed_content(
                model=self.model_name,
                contents=texts,
            )
            return [list(e.values) for e in result.embeddings]

        payload = {"model": self.model_name, "input": texts}
        last_err: Exception | None = None
        for attempt in range(4):
            try:
                resp = requests.post(self.api_url, headers=self.headers, json=payload, timeout=60)
                if resp.status_code in (429, 500, 502, 503, 504):
                    time.sleep(1.5 * (attempt + 1))
                    continue
                if resp.status_code != 200:
                    raise RuntimeError(
                        f"{self.provider} embeddings API error {resp.status_code}: {resp.text[:400]}"
                    )
                data = resp.json()
                if "data" not in data:
                    raise RuntimeError(f"Unexpected embeddings response: {data}")
                items = sorted(data["data"], key=lambda x: x["index"])
                usage = data.get("usage") or {}
                self.total_tokens += int(usage.get("total_tokens") or usage.get("prompt_tokens") or 0)
                if "cost" in usage and usage["cost"] is not None:
                    self.total_cost_usd += float(usage["cost"])
                return [item["embedding"] for item in items]
            except requests.RequestException as exc:
                last_err = exc
                time.sleep(1.5 * (attempt + 1))

        raise RuntimeError(f"Failed to embed batch after retries: {last_err}")

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        vectors: list[list[float]] = []
        for i in range(0, len(texts), self.batch_size):
            batch = texts[i : i + self.batch_size]
            vectors.extend(self._embed_batch(batch))
        return vectors

    def embed_query(self, question: str) -> list[float]:
        return self._embed_batch([question])[0]
