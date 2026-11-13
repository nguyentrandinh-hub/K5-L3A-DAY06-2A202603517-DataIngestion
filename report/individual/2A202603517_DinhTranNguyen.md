# Báo cáo cá nhân — Day 6

## Dữ liệu và pipeline
- **Chủ đề, nguồn/quyền, số trang và quy tắc tính trang:**
  - Chủ đề: Tài liệu kỹ thuật **Google Gemini API & AI Studio Official Documentation** (lấy từ mục lục chuẩn `https://aistudio.google.com/llms.txt` dưới dạng các trang Markdown `.md`).
  - Giấy phép: **CC BY 4.0** (nội dung tài liệu) / **Apache 2.0** (code mẫu) — Google AI Developers; truy cập ngày `2026-11-13`.
  - Số đơn vị & quy tắc tính: **40 đơn vị nguồn độc lập** (vượt mức tối thiểu 30 đơn vị theo quy tắc Markdown/HTML của `GUIDE.md`), tổng cộng **1.662.318 ký tự** sau chuẩn hóa. Mỗi trang `.md` được tính là 1 đơn vị (`unit_id` 1–40); chỉ giữ các trang có **≥ 1.500 ký tự** nội dung đã chuẩn hóa (trang ngắn nhất: `18_docs_video.md` = 1.896 ký tự). Chi tiết lưu tại `data/manifest.json` và `results/corpus_fetch_log.json`.
- **Chuẩn hóa, lỗi và giới hạn:**
  - Chuẩn hóa Unicode dạng `NFC`, chuẩn hóa xuống dòng `\n`, xóa khoảng trắng cuối dòng và gộp dòng trống thừa (`>= 3` → `2`), giữ nguyên cấu trúc heading `#`, `##` và code block.
  - Quá trình nạp 40 file ghi nhận **0 lỗi đọc/rỗng** (`results/ingestion_log.json`).
  - Giới hạn dữ liệu: Một số trang docs có chứa thẻ bố cục Markdoc (`{% card %}`, `{% callout %}`, `{% tab %}`) nên vẫn còn thẻ markup trong text chunk.
- **Embedding model/provider/version/số chiều, vector store/version, metric, lệnh chạy và chi phí:**
  - Embedding: `openai/text-embedding-3-small` gọi qua **OpenRouter API** (`https://openrouter.ai/api/v1/embeddings`), **1536 chiều**.
  - Vector Store: **PostgreSQL 16.16 + pgvector 0.8.7** (chạy qua Docker Compose `starter/docker-compose.yml`), metric **Cosine distance** (`<=>`, score `1 - cosine_distance`).
  - Kiểm tra nạp lại (Idempotency): Re-ingest tài liệu vào chiến lược A cho kết quả `count_before = 3.695`, `count_after = 3.695` (`passed: true`), không bị nhân đôi nhờ xóa chunk cũ theo `document_id` và `ON CONFLICT (strategy, chunk_id) DO UPDATE`.
  - Lệnh chạy tái lập (từ thư mục `starter/`):
    1. `python scripts/fetch_corpus.py` (tải 40 file & tạo `data/manifest.json`)
    2. `python scripts/verify_benchmark.py` (kiểm chứng `benchmark/questions.json`)
    3. `docker compose -p day6_student_starter up -d --wait && python scripts/check_setup.py`
    4. `python -m src.run` (chạy toàn bộ A, B, C và xuất `results/`)
  - Tổng tài nguyên & chi phí: **838.205 tokens**, tổng chi phí **$0.016764** (A: `$0.008927`, B: `$0.007828`, C: `$0.0` do tái dùng vector của B).
- **Metadata bắt buộc, trường lọc bổ sung, nguồn giá trị và lý do chọn:**
  - Metadata bắt buộc: `document_id`, `source`, `page` (`unit_id`).
  - Trường lọc bổ sung: `section` (gồm 5 nhóm phân biệt: `tools_and_agents` [10], `models_and_pricing` [10], `core_guides` [10], `getting_started` [5], `api_reference` [5]), `title`, `url`.
  - Nguồn giá trị & lý do chọn: Suy ra trực tiếp từ đường dẫn URL và mục lục `llms.txt` (không tự đoán), giúp khoanh vùng đúng chuyên mục tài liệu khi người dùng hỏi về API errors, pricing hay agents.

## Cấu hình và benchmark
- **A / B / C (tham số cụ thể, khác biệt duy nhất B–C):**
  - **Chiến lược A:** `fixed_size(size=500, overlap=50)`, không dùng filter khi truy xuất.
  - **Chiến lược B:** `by_paragraph(max_size=800)` (chia theo heading `#`/`##` và đoạn `\n\n`, tự tách mềm nếu đoạn quá 800 ký tự), không dùng filter khi truy xuất. *(So sánh A–B: chỉ đổi thuật toán chunking).*
  - **Chiến lược C:** Dùng chung bộ chunk và vector của B, **chỉ bật SQL `WHERE section = ...`** trong `PgVectorStore.search()` đối với các câu hỏi có `filter` (`5/20` câu). *(So sánh B–C: chỉ đổi metadata filter).*
- **≥ 20 câu: phân chia ≥ 15 dev / ≥ 5 test, câu metadata filter và cách kiểm chứng evidence:**
  - Tổng **20 câu hỏi** (`benchmark/questions.json`), chia cứng trước khi chạy thử: **15 `dev`** (`q01`–`q15`) và **5 `test`** (`q16`–`q20`).
  - Có **5 câu dùng metadata filter theo `section`**: 3 câu trong `dev` (`q04`, `q09`, `q14`) và 2 câu trong `test` (`q17`, `q20`).
  - Kiểm chứng evidence: Script `starter/scripts/verify_benchmark.py` xác minh 100% `gold_source_id`, `gold_page`, `filter` khớp `data/manifest.json` và 100% `evidence_quote` tồn tại nguyên văn trong file nguồn trước khi chạy pipeline.
- **Tiêu chí chọn chiến lược đã chốt trước khi xem test:**
  - (1) Ưu tiên **Evidence Hit@3** cao nhất trên tập `dev`; (2) Nếu bằng nhau, ưu tiên **Hit@1** trên `dev`; (3) Xét thêm **Chunk Coherence**, tốc độ truy vấn và chi phí tài nguyên.

## Kết quả

| Strategy | Split | Hit@1 (n/N) | Evidence Hit@3 (n/N) | Chunk count | Thời gian | Chi phí |
|---|---|---:|---:|---:|---:|---:|
| A | dev | 3/15 (20.0%) | 5/15 (33.3%) | 3,695 | Ingest 219.92s / Query 1.455s | $0.008927 |
| A | test | 2/5 (40.0%) | 2/5 (40.0%) | 3,695 | — | — |
| B | dev | 7/15 (46.7%) | 12/15 (80.0%) | 2,630 | Ingest 185.08s / Query 1.229s | $0.007828 |
| B | test | 3/5 (60.0%) | 3/5 (60.0%) | 2,630 | — | — |
| C | dev | 7/15 (46.7%) | 12/15 (80.0%) | 2,630 | Ingest 2.71s (tái dùng B) / Query 0.965s | $0.000000 (tái dùng B) |
| C | test | 3/5 (60.0%) | 3/5 (60.0%) | 2,630 | — | — |

| Strategy | Coherence trung bình /2 (n) | Metadata đủ và đúng (n/N) | Filter tuân thủ (n/N hoặc N/A) | Grounding 0/1/2 (số câu) và trung bình /2 |
|---|---:|---:|---:|---|
| A | 0.20 / 2 (n=10) | 15/15 (100%) | 4/5 (all), 2/2 (test) | `0`: 2 câu, `1`: 1 câu, `2`: 2 câu — TB **1.00 / 2** |
| B | 1.80 / 2 (n=10) | 15/15 (100%) | 5/5 (all), 2/2 (test) | `0`: 2 câu, `1`: 0 câu, `2`: 3 câu — TB **1.20 / 2** |
| C | 1.80 / 2 (n=10) | 15/15 (100%) | 5/5 (all), 2/2 (test) | `0`: 2 câu, `1`: 0 câu, `2`: 3 câu — TB **1.20 / 2** |

- **Đường dẫn trace, nhãn thủ công và cách chọn mẫu:**
  - Trace đầy đủ: `results/traces_A.json`, `results/traces_B.json`, `results/traces_C.json`, `results/metrics_summary.json`, `results/ingestion_stats.json`.
  - Nhãn thủ công Coherence (10 vị trí nguồn đầu tiên `unit_id` 1–10): `results/audit_coherence_samples.csv` (người chấm: tác giả bài làm).
  - Nhãn thủ công Metadata & Grounding (5 câu `test` `q16`–`q20` × top-3 = 15 bản ghi/chiến lược): `results/audit_grounding_samples.csv` (người chấm: tác giả bài làm).

## Phân tích và kết luận
- **So sánh A–B và B–C; 2 ví dụ sai có ID câu và nguồn:**
  - **A → B (Tác động của Chunking):** Chuyển từ `fixed_size(500, overlap=50)` sang `by_paragraph(max_size=800)` giúp **giảm 28.8% số chunk** (3,695 → 2,630), giảm thời gian và chi phí embedding, đồng thời **Evidence Hit@3 trên dev tăng mạnh từ 33.3% (5/15) lên 80.0% (12/15)** và Coherence tăng từ **0.20/2 lên 1.80/2**. Lý do là cắt cứng 500 ký tự liên tục cắt đứt giữa từ/bảng/heading, làm mất ngữ cảnh câu văn.
  - **B → C (Tác động của Metadata Filter):** Chiến lược C đạt độ tuân thủ filter 100% (`5/5`) và rút ngắn thời gian truy vấn (`1.229s` → `0.965s`) nhờ SQL `WHERE section = ...` thu hẹp không gian tìm kiếm. Tuy nhiên, Hit@1 và Hit@3 giữa B và C bằng nhau trên bộ benchmark này vì trong câu hỏi có filter đã nhắc rõ ngữ cảnh chuyên mục (ví dụ `"In the api_reference section..."`), nên embedding của B vốn đã tìm đúng `section` (`5/5`).
  - **Ví dụ lỗi 1 (`q20`, tập `test`, nguồn `gemini-doc-27` / `27_docs_agents.md`):** Ở chiến lược **A**, top-1 truy xuất đúng trang `gemini-doc-27` nhưng bị cắt đúng ngay dòng tiêu đề `### Network access By default,`, đẩy phần quy tắc `unrestricted outbound network access` và `network allowlist` sang chunk khác ngoài top-3 (`Hit@3 = False`, Grounding = `1`). Sang **B và C**, chunk theo heading giữ trọn cả tiêu đề lẫn đoạn giải thích nên đạt `Hit@1 = True` và Grounding = `2`.
  - **Ví dụ lỗi 2 (`q16`, tập `test`, nguồn `gemini-doc-07` / `07_docs_latest-model.md`):** Cả **A, B, C** đều thất bại (`Hit@3 = False`, Grounding = `0`). Câu hỏi hỏi về model `"fast and efficient for everyday coding and agentic workflows"` và giá 1M token của **Gemini 4 Hydrogen** nằm ở bảng so sánh trong `gemini-doc-07`, nhưng top-3 lại trả về `gemini-doc-08` (Carbon), `gemini-doc-09` (Argon), `gemini-doc-11` vì các trang *What's new* này lặp lại nhiều từ khóa `"Gemini 4"`, `"coding"`, `"agentic"`, `"price"` hơn đoạn mô tả ngắn trong thẻ Markdoc của `gemini-doc-07`.
- **Chiến lược chọn, đánh đổi, điều kiện áp dụng:**
  - **Chọn Chiến lược C** (Chunk theo đoạn/heading `by_paragraph` + Metadata Filter theo `section`).
  - **Đánh đổi:** Chi phí lưu trữ/embedding giảm gần 29% so với fixed-size, Coherence và Accuracy vượt trội. Tuy nhiên, nếu dùng filter cứng `WHERE section = ...`, hệ thống phụ thuộc vào việc phân loại đúng `section` của câu hỏi đầu vào (nếu người dùng gắn sai `section`, filter sẽ loại nhầm tài liệu đúng).
  - **Điều kiện áp dụng:** Phù hợp cho tài liệu kỹ thuật/API Docs có cấu trúc heading Markdown và phân mục rõ ràng.
- **Hạn chế của dữ liệu, nhãn, test nhỏ, đo thời gian/chi phí:**
  - Tập `test` chỉ có 5 câu nên mỗi câu tương ứng 20%, độ dao động thống kê lớn; không thể suy rộng kết quả cho mọi loại tài liệu ngoài Gemini API Docs.
  - Nhãn thủ công Coherence và Grounding do chính tác giả tự chấm nên có thể tồn tại thiên lệch đánh giá (self-evaluation bias).
  - Thời gian ingest đo qua mạng gọi OpenRouter API phụ thuộc độ trễ mạng từng thời điểm; một số trang chứa thẻ Markdoc (`{% card %}`) làm giảm nhẹ điểm Coherence ở một vài chunk.
- **Nếu làm lại hoặc mở rộng, cải tiến gì?**
  - Tiền xử lý làm sạch hoặc chuyển đổi các thẻ Markdoc (`{% card %}`, `{% callout %}`) thành Markdown thuần trước khi chunk để tăng Coherence và giảm nhiễu embedding (khắc phục lỗi kiểu `q16`).
  - Kết hợp **Hybrid Search** (Dense vector + BM25/PostgreSQL `tsvector` full-text search) để bắt chính xác tên model (`gemini-4-hydrogen`) và mã lỗi (`rate_limit_exceeded`).
  - Mở rộng tập `test` lên ≥ 30 câu và có người chấm độc lập cho phần audit thủ công.

## Hướng dẫn cài đặt & chạy tái lập
- **Đường dẫn dữ liệu & artifacts:**
  - Corpus: `data/corpus/` (40 trang Markdown từ Gemini API Docs) và `data/manifest.json`
  - Benchmark: `benchmark/questions.json` (20 câu: 15 `dev` / 5 `test`, 5 câu metadata filter)
  - Mã nguồn pipeline: `starter/src/` (`models.py`, `ingestion.py`, `chunking.py`, `embeddings.py`, `store.py`, `evaluation.py`, `run.py`)
  - Kết quả & audit: `results/`, `artifacts/experiment_log.csv`
- **Các bước chạy lại từ đầu** (chạy từ thư mục `starter/`, sau khi tạo `starter/.env` từ `starter/.env.example` và điền `OPENROUTER_API_KEY`):
  ```powershell
  python -m venv .venv
  .\.venv\Scripts\Activate.ps1
  python -m pip install -r requirements.txt
  docker compose -p day6_student_starter up -d --wait
  python scripts/check_setup.py
  python scripts/fetch_corpus.py
  python scripts/verify_benchmark.py
  python -m src.run
  ```
