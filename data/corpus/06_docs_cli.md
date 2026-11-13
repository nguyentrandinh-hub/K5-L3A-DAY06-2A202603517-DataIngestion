> ## AI Agent Context
> Get the complete documentation index at: https://aistudio.google.com/llms.txt
> Use this file to discover all available pages.
> For the full documentation in a single file, fetch: https://aistudio.google.com/llms-full.txt

# Gemini API CLI

The Gemini API CLI (`gemini-api`) is a stateless, zero-dependency command-line client built for AI agents with shell access, scripts, and CI pipelines. Your coding agent can use it to generate text and media, analyze files, and delegate tasks to [Gemini managed agents](/docs/agents). It works with Antigravity, Claude Code, Cursor, and any standard shell environment.

Every feature runs as a standard shell command on the [Interactions API](/docs/interactions-overview). Run the same commands from an agent subprocess, your terminal, or a CI pipeline:

```bash
# 1. Install on macOS or Linux
curl -fsSL https://raw.githubusercontent.com/google-gemini/gemini-api-cli/main/scripts/install.sh | bash

# 2. Set your API key
export GEMINI_API_KEY="YOUR_API_KEY"

# 3. Generate media, analyze a file, or launch a background managed agent
gemini-api image "Minimalist isometric icon of a cloud database" --out ./assets/db-icon.jpg
gemini-api analyze -i ./docs/quarterly-report.pdf "Summarize the key findings in three bullets."
gemini-api agent run "Compare WebRTC SFU architectures and cite sources" \
  --agent deep-research-preview-04-2026 \
  --background \
  --stream=false
```

{% callout type="note" %}
  `gemini-api` is an open-source beta release that evolves alongside the [Interactions API](/docs/interactions-overview). Breaking changes can occur between minor versions. Pin a specific [release version](https://github.com/google-gemini/gemini-api-cli/releases) in automated agent environments and CI pipelines.

{% /callout %}

## Choose the right Gemini tool  {% id="choose-tool" %}

Use `gemini-api` when an agent or script needs to **call** Gemini directly from the shell without adding SDK code to your project. Use the SDKs and [coding agent setup](/docs/coding-agents) when you are **building** Gemini into an application:

| Tool | What it does | When to use it |
| :--- | :--- | :--- |
| **Gemini API CLI** (`gemini-api`) | Calls Gemini models and managed agents from any shell. | Your coding agent, shell script, or CI job needs to generate media, analyze files, or run a background research agent with zero project dependencies. |
| **[Google GenAI SDKs](/docs/libraries)** | Imports Gemini client libraries into Python, TypeScript, JavaScript, Go, Java, or C# code. | You are building Gemini features into your application, backend service, or real-time [Live API](/docs/live-api) session. |
| **[Gemini Docs MCP & skills](/docs/coding-agents)** | Gives coding agents live documentation search and current SDK rules. | Your coding agent is writing application code that imports a Google GenAI SDK. |

{% callout type="note" %}
  `gemini-api` is a stateless API client, not an interactive coding agent like `@google/gemini-cli`. You can run `gemini-api` inside any coding agent.

{% /callout %}

## How it works  {% id="how-it-works" %}

Raw REST calls and interactive CLIs often cause issues for coding agents. Base64 media fills the context window, interactive prompts block subprocesses, and stale training data causes hallucinated flags.

Four design choices keep `gemini-api` reliable for agents:

- **Offline schema lookup:** Pass `--usage` to print the command tree (in [KDL](https://kdl.dev)), or `--schema` to print the JSON Schema for `--body` requests.
- **Files on disk, paths on `stdout`:** Media and transcription commands write files to disk and print only the output path, keeping binary data out of context.
- **Dry runs and structured output:** `--dry-run` validates inputs, redacts credentials, and previews the HTTP request offline. Pass `-o json`, `-o toon`, or `--jq` for machine-readable output. Add `--agent-mode` to return structured JSON errors on `stderr`, and check [exit codes](/docs/cli#exit-codes) to handle failures. Commands never prompt unless you pass `--interactive`.
- **Stateless by default:** Commands keep no hidden local state. Chain multi-step work explicitly with `--previous-interaction-id`, an uploaded `files/<id>` URI, or a background interaction ID.

With `-o json`, media commands still write the file to disk and print metadata to `stdout`:

```json
{
  "kind": "image",
  "mime_type": "image/jpeg",
  "path": "/path/to/project/assets/db-icon.jpg",
  "response_id": "v1_...",
  "size_bytes": 2914159,
  "status": "completed"
}
```

## Get started  {% id="get-started" %}

Install the CLI, put `gemini-api` on your `PATH`, set `GEMINI_API_KEY`, and add usage rules to your coding agent.

### 1. Install the binary  {% id="install" %}

{% tabs %}
  {% tab label="macOS and Linux" %}
  ```bash
  curl -fsSL https://raw.githubusercontent.com/google-gemini/gemini-api-cli/main/scripts/install.sh | bash
  ```

  To install a specific release, set `GEMINI_VERSION` to a release tag:

  ```bash
  curl -fsSL https://raw.githubusercontent.com/google-gemini/gemini-api-cli/main/scripts/install.sh | GEMINI_VERSION=<release-tag> bash
  ```

  {% /tab %}

  {% tab label=Windows (PowerShell) %}
  ```bash
  iwr -useb https://raw.githubusercontent.com/google-gemini/gemini-api-cli/main/scripts/install.ps1 | iex
  ```

  {% /tab %}

  {% tab label="Go" %}
  ```bash
  go install github.com/google-gemini/gemini-api-cli/cmd/gemini-api@latest
  ```

  {% /tab %}

  {% tab label="Prebuilt binaries" %}
  Download versioned archives for macOS, Linux, and Windows from [GitHub Releases](https://github.com/google-gemini/gemini-api-cli/releases) and place `gemini-api` on your `PATH`. Use prebuilt archives to pin exact versions in Docker images and CI.

  {% /tab %}

{% /tabs %}

### 2. Configure authentication and verify  {% id="authentication" %}

Create an API key in [Google AI Studio](https://aistudio.google.com/apikey) (see [API keys](/docs/api-key)). Set `GEMINI_API_KEY` in your shell and your agent's subprocess environment:

```bash
export GEMINI_API_KEY="YOUR_API_KEY"
```

On a local workstation, you can save the key in your OS keychain (macOS Keychain, Linux Secret Service, or Windows Credential Manager). Pass `--no-keyring` to store the key in `~/.config/gemini-api/config.yaml` instead:

```bash
# Save to your OS keychain (or run gemini-api configure --interactive)
gemini-api configure --api-key "YOUR_API_KEY"

# Check the active credential source, then preview a request offline
gemini-api whoami
gemini-api generate "Confirm CLI setup in one sentence." --dry-run
```

{% callout type="warning" %}
  Treat `GEMINI_API_KEY` as a secret. In CI, inject the key from your secret store instead of committing it to a repository or build file.

{% /callout %}

### 3. Give your agent instructions  {% id="agent-instructions" %}

Add this snippet to your project's `AGENTS.md`, `CLAUDE.md`, `.cursorrules`, or system prompt so your coding agent knows how to use `gemini-api`:

```markdown
## Gemini API CLI (`gemini-api`)

You have access to `gemini-api` through the shell. Use it to generate text or media (images, speech, music, video), analyze documents and recordings, or run and manage Gemini managed agents.

1. Run `gemini-api --help` or `gemini-api --usage` to choose a command, and `gemini-api <command> --schema` before building a `--body` JSON payload.
2. Preview unfamiliar or complex calls offline with `--dry-run -o json`.
3. For a single JSON result or `--jq` filtering on `generate` or `agent run`, pass `--stream=false -o json`.
4. To chain multi-step workflows, capture the output paths that media and transcription commands print to stdout, and the `id` values returned by `generate` or `agent run`.
```

Then prompt your coding agent as usual:

```none
Build a landing page for our developer tool. Use Gemini to generate a hero
illustration and a 15-second welcome voiceover, and start a background Deep
Research agent to compare competing CLI onboarding flows. Wire the assets and
findings into the page.
```

## Commands  {% id="commands" %}

Run `gemini-api --help` to list all commands, or `gemini-api explore` to browse them interactively.

| Group | Command | What it does |
| :--- | :--- | :--- |
| Create | `image` | Generates or edits images (`-i`), writes a JPEG file, and prints its path. |
| Create | `tts` | Synthesizes 24 kHz mono WAV speech (one or two speakers) and prints the output path. |
| Create | `music` | Generates music tracks or loops, writes the audio file, and prints its path. |
| Create | `video` | Generates or edits MP4 clips and waits until done (`--async` returns an ID immediately). |
| Create | `generate` | Generates text and streams it to `stdout` (`--stream=false` returns one complete result). |
| Understand | `analyze` | Answers questions about PDFs, images, audio, video, CSV and text files, or public YouTube URLs. |
| Understand | `transcribe` | Writes speaker-labeled, timestamped transcripts (`md`, `text`, `json`, or `srt`) and prints the output paths. |
| Manage agents | `agent` | Runs managed agents (`run`, `status`, `cancel`, `delete-interaction`) and manages custom agent definitions (`create`, `list`, `get`, `delete`). |
| Manage agents | `environments`, `credentials`, `webhooks`, `triggers` | Configures sandbox environments, stored credentials, webhook delivery, and scheduled runs for managed agents. |
| Setup and files | `configure`, `auth`, `whoami` | Configures credentials and defaults, and shows the active auth state. |
| Setup and files | `files` | Uploads, lists, inspects, and deletes files in the Files API. |
| Setup and files | `models` | Lists available models. |

## Workflows  {% id="workflows" %}

Each command defaults to a model suited for its task. Pass `--model` (`-m`) to pick a different model. Run `gemini-api models` to list available options.

### Image generation and editing  {% id="image" %}

Agents building web or mobile UIs can generate placeholders, icons, and hero images with [Nano Banana](/docs/image-generation). Pass a generated path back in with `-i` to edit the image:

```bash
# Generate a 16:9 image at 2K resolution (512, 1K, 2K, or 4K) and capture its path
HERO_PATH=$(gemini-api image "Friendly robot mascot in a sunlit workshop, space on left for headline" \
  --aspect-ratio 16:9 \
  --image-size 2K \
  --out ./public/images/hero.jpg)

# Edit the generated image
gemini-api image "Add a winter scarf and soft snowfall outside the window" \
  -i "$HERO_PATH" \
  --out ./public/images/hero-winter.jpg
```

Pass `-i` multiple times to combine reference images, such as a character and a style guide.

### Speech synthesis  {% id="tts" %}

`gemini-api tts` synthesizes 24 kHz WAV audio for UI cues, accessibility previews, and narrated walkthroughs. The default voice is `Kore`; choose another with `--voice`. For two-speaker dialogue, label each turn in the prompt and map speakers to voices:

```bash
gemini-api tts "Build succeeded. All integration tests passed." \
  --voice Aoede \
  --out ./public/audio/build-ok.wav

gemini-api tts "Alice: Welcome to the release walkthrough! Bob: Let's look at what shipped today." \
  --multi-speaker "Alice=Kore,Bob=Puck" \
  --out ./public/audio/release-intro.wav
```

### Music and video  {% id="music-video" %}

Compose original tracks with [Lyria](/docs/music-generation), and generate MP4 clips with [Gemini Omni](/docs/video):

```bash
gemini-api music "Warm ambient synth and acoustic guitar background loop, 95 BPM" \
  --out ./public/audio/bg-loop.mp3

gemini-api video "A drone shot of a mountain landscape at sunrise." \
  --aspect-ratio 16:9 \
  --resolution 1080p \
  --out ./public/video/mountain-sunrise.mp4
```

By default, the `video` command waits for generation to finish and writes the MP4 file to disk. Pass `--async` to return an interaction ID immediately, then run `gemini-api video --resume <id> --out <path>` later. Pass `-i` to animate an existing image.

### Text generation  {% id="generate" %}

`gemini-api generate` streams text to `stdout`:

```bash
gemini-api generate "Write a one-paragraph welcome message for new users of a note-taking app."
```

Add `--stdin` to pipe text into the prompt. Pass `--previous-interaction-id` to continue an earlier interaction.

### Document analysis and transcription  {% id="analyze" %}

`analyze` answers questions about PDFs, spreadsheets, screenshots, audio and video files, and public YouTube URLs. `transcribe` writes a formatted transcript (`md`, `text`, `json`, or `srt`) to disk:

```bash
gemini-api analyze -i ./docs/product-brief.pdf "List the open questions and who owns each one." > open-questions.md

gemini-api transcribe -i ./fixtures/customer-call.mp4 --format srt --out ./fixtures/customer-call.srt
```

Pass `-i` multiple times to `analyze` to compare files, such as before-and-after screenshots.

`gemini-api` sends local files inline up to 14 MB (20 MB after base64 encoding). For larger files, upload once with `files upload --wait` and reuse the returned `files/<id>` URI:

```bash
FILE_URI=$(gemini-api files upload ./recordings/all-hands.mp4 --wait)

gemini-api analyze -i "$FILE_URI" "List action items with owners and timestamps."
gemini-api transcribe -i "$FILE_URI" --format json --out ./recordings/all-hands.json
```

### Run and manage agents  {% id="managed-agents" %}

Your coding agent can delegate multi-step research or sandboxed tasks to [Gemini managed agents](/docs/agents), such as the [Deep Research agent](/docs/deep-research). Pass `--background --stream=false` to get an interaction ID immediately instead of holding a stream open:

```bash
# Launch a Deep Research job in the background and capture its interaction ID
RESEARCH_ID=$(gemini-api agent run "Compare open-source vector index benchmarks and cite primary papers." \
  --agent deep-research-preview-04-2026 \
  --background \
  --stream=false \
  --jq '.id')

# Check status or fetch the finished result while continuing other work
gemini-api agent status "$RESEARCH_ID" -o json
```

Run `gemini-api agent cancel <id>` to stop a running job. You can also launch the [Antigravity agent](/docs/antigravity-agent) in a remote sandbox with `agent run`, or manage [custom agents](/docs/custom-agents) with `agent create`, `list`, `get`, and `delete`. See [Environments](/docs/agent-environment) to configure agent sandboxes.

## Custom request bodies  {% id="custom-bodies" %}

For options without dedicated flags, pass a raw [Interactions API](/docs/interactions-overview) JSON payload with `--body` (inline or as `@file.json`). Pass `--body` to set `response_format` schemas, function-calling tools, `generation_config`, or `"store": false`. Run `gemini-api <command> --schema` first to check valid fields:

```bash
# Inspect the JSON Schema for the request body
gemini-api generate --schema > generate-schema.json

# Return schema-constrained JSON and skip storing the interaction
cat logs.txt | gemini-api generate "Extract every error message from these logs." \
  --stdin \
  --body '{
    "response_format": {
      "type": "text",
      "mime_type": "application/json",
      "schema": {
        "type": "object",
        "properties": {"errors": {"type": "array", "items": {"type": "string"}}},
        "required": ["errors"]
      }
    },
    "store": false
  }'
```

`--body` merges with command flags. If both set the same key, the command fails with exit code `2` so conflicting inputs fail fast.

## Exit codes  {% id="exit-codes" %}

Every command returns a typed exit code so scripts and agents can handle failures without parsing error text. For example, `3` signals an authentication problem and `2` signals invalid command syntax:

| Code | Meaning |
| :--- | :--- |
| `0` | The command succeeded. |
| `1` | Runtime or API error, such as a network failure, rate limit, or failed background job. |
| `2` | Usage or validation error, such as an unknown flag, missing input, or duplicate `--body` key. |
| `3` | Authentication or authorization failure, such as a missing or invalid API key or token. |

Run `gemini-api --help-global` to list global flags shared by every command (authentication, output, network, and diagnostics).

## Limitations  {% id="limitations" %}

- Streaming commands (`generate` and `agent run`) require `--stream=false` when combined with `-o json` or `--jq` to return a single JSON response object.
- Inline `-i` file inputs cap at 14 MB of raw file data (20 MB request payload including base64 encoding). Upload large files with `gemini-api files upload`. The Files API deletes uploaded files after 48 hours.
- `gemini-api` supports standard HTTP requests, SSE streaming, and async polling, not bidirectional WebSockets. For real-time voice and video streaming, use the [Live API](/docs/live-api) with the [Google GenAI SDKs](/docs/libraries).

## What's next  {% id="whats-next" %}

- [Coding agent setup](/docs/coding-agents)
- [Interactions API](/docs/interactions-overview)
- [Gemini managed agents](/docs/agents)
- [gemini-api-cli on GitHub](https://github.com/google-gemini/gemini-api-cli)