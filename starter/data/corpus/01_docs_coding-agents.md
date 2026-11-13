> ## AI Agent Context
> Get the complete documentation index at: https://aistudio.google.com/llms.txt
> Use this file to discover all available pages.
> For the full documentation in a single file, fetch: https://aistudio.google.com/llms-full.txt

# Coding agent setup & developer resources

AI coding agents rely on training data that cuts off at a set date. Because of this, agents often suggest deprecated models (`gemini-1.5`), older SDKs (`google-generativeai`), or outdated code patterns.

Connecting your agent to official Gemini developer resources helps it write accurate code using current models, the `google-genai` SDK, and the [Interactions API](/docs/interactions-overview).

You can connect your coding agent to Gemini documentation, rules, and CLI tools in five ways:

## Summary of agent resources  {% id="summary" %}

| Resource | What it provides | Availability |
| :--- | :--- | :--- |
| **[Gemini Agent Skills](/docs/coding-agents#available-skills)** | Step-by-step rules, SDK patterns, and helper scripts for specific features (`gemini-api-dev`, `gemini-live-api-dev`, `gemini-omni-flash-api`). | Pre-installed in [AI Studio Build](https://ai.studio/build); install with `skills.sh`, Context7, or Managed Agents. |
| **[Gemini Docs MCP Server](/docs/coding-agents#mcp-setup)** | Live search (`gemini_search_docs`) and full page reads (`gemini_get_doc`) across all documentation. | Supported in Claude Code, Cursor, OpenAI Codex, and VS Code. |
| **[Gemini API Plugin](/docs/coding-agents#gemini-api-plugin)** | Bundled package with official Gemini skills, the Docs MCP server, and API key tools. | Antigravity. |
| **[Machine-Readable Docs](/docs/coding-agents#machine-readable-docs)** | Clean Markdown pages, `llms.txt` indexes, and content negotiation headers. | All documentation pages on `aistudio.google.com/docs`. |
| **[Gemini API CLI](/docs/cli)** | Stateless CLI (`gemini-api`) to generate media, analyze files, and run managed agents from the shell without writing SDK code. | Install on macOS, Linux, or Windows with the install script, Go, or prebuilt binaries. |

## Install Gemini agent skills  {% id="available-skills" %}

Agent skills give your coding agent procedural rules, current model names, and SDK code patterns. Instead of adding long instructions to your prompt, your agent loads each skill only when needed. This helps your agent avoid deprecated SDKs and use modern Gemini patterns.

Skills work alongside the Gemini Docs MCP server. If your agent does not have the MCP server installed, the skill falls back to [`llms.txt`](https://aistudio.google.com/llms.txt). To learn more about how skills work, read the [Gemini API Skills guide](https://aistudio.google.com/learn/gemini-api-skills).

{% callout type="note" %}
  Skills come pre-installed in [Google AI Studio Build](https://ai.studio/build) and are bundled in the [Gemini API plugin](/docs/coding-agents#gemini-api-plugin) for Antigravity.

{% /callout %}

### Install with the CLI (`skills.sh` or Context7)  {% id="install-skills-cli" %}

Install skills using [skills.sh](https://skills.sh) (recommended) or [Context7](https://context7.com):

```bash
# List all available skills in the repository
npx skills add google-gemini/gemini-skills --list

# Install a specific skill globally with skills.sh
npx skills add google-gemini/gemini-skills --skill <skill-name> --global

# Or install with Context7
npx ctx7 skills install /google-gemini/gemini-skills <skill-name>
```

### Available skills  {% id="skills-catalog" %}

#### `gemini-api-dev` {% id="gemini-api-dev" %}

Skill for building applications with the [Interactions API](/docs/interactions-overview) and the official Gemini API SDKs (`google-genai` for Python and `@google/genai` for TypeScript). This skill covers:

- Text generation, multi-turn chat, streaming, structured outputs, and function calling
- Image generation, text-to-speech (TTS), and multimodal inputs
- Server-side conversation state management, background execution, Deep Research, and managed agents
- Current model names and migrating legacy `generateContent` or `google-generativeai` code

```bash
npx skills add google-gemini/gemini-skills --skill gemini-api-dev --global
```

#### `gemini-live-api-dev` {% id="gemini-live-api-dev" %}

Skill for building real-time audio and video streaming applications with the [Gemini Live API](/docs/live-api). This skill covers:

- WebSocket session management, ephemeral client tokens, and session resumption
- Streaming audio, video, and text with voice activity detection (VAD) and barge-in support
- Background reasoning (extended thinking), non-blocking asynchronous tool calls, transcription, and live speech translation

```bash
npx skills add google-gemini/gemini-skills --skill gemini-live-api-dev --global
```

#### `gemini-omni-flash-api` {% id="gemini-omni-flash-api" %}

Skill for generating and editing video with Gemini Omni Flash using the Interactions API. Includes helper scripts (`upload_file.py`, `generate_video.py`, `prep_video.py`, `inspect_video.py`) and covers:

- Text-to-video generation and prompt crafting
- First-and-last-frame transitions and reference-guided video generation
- Video extensions and media preprocessing workflows

```bash
npx skills add google-gemini/gemini-skills --skill gemini-omni-flash-api --global
```

### Mount skills in Managed Agents  {% id="managed-agents-skills" %}

When you run remote managed agents with the Interactions API, you can mount the `google-gemini/gemini-skills` repository into the agent's workspace. See the [Gemini API Skills guide](https://aistudio.google.com/learn/gemini-api-skills) for details:

```python
from google import genai

client = genai.Client(http_options={"api_version": "v1beta"})

interaction = client.interactions.create(
    agent="antigravity-preview-09-2026",
    input="Build a script that generates a 5-second video of a neon cityscape.",
    environment={
        "type": "remote",
        "sources": [
            {
                "type": "repository",
                "source": "https://github.com/google-gemini/gemini-skills",
                "target": ".agents",
            }
        ],
    },
)
```

## Connect the Gemini Docs MCP server  {% id="mcp-setup" %}

The public **Gemini Docs MCP server** (`https://gemini-api-docs-mcp.dev`) gives your agent live access to the entire documentation site. Your agent can search and read documentation pages to check request schemas, model limits, and new features:

- `gemini_search_docs`: Searches Gemini API documentation by topic or query.
- `gemini_get_doc`: Reads the full Markdown content of a specific documentation page.

### Quick setup  {% id="mcp-quick-setup" %}

Run this command in your terminal or project root to configure your detected coding agents automatically:

```bash
npx add-mcp "https://gemini-api-docs-mcp.dev"
```

### Configuration by environment  {% id="mcp-by-environment" %}

{% tabs %}
  {% tab label="Claude Code" %}
  Run in your terminal:

  ```bash
  $ claude mcp add --transport http geminiDocs https://gemini-api-docs-mcp.dev
  ```

  {% /tab %}

  {% tab label="Cursor" %}
  Add to `~/.cursor/mcp.json` (global) or `.cursor/mcp.json` (project):

  ```json
  {
    "mcpServers": {
      "geminiDocs": {
        "url": "https://gemini-api-docs-mcp.dev"
      }
    }
  }
  ```

  {% /tab %}

  {% tab label="OpenAI Codex" %}
  Run in your terminal:

  ```bash
  $ codex mcp add geminiDocs --url https://gemini-api-docs-mcp.dev
  ```

  Or add to `~/.codex/config.toml`:

  ```toml
  [mcp_servers.geminiDocs]
  url = "https://gemini-api-docs-mcp.dev"
  ```

  {% /tab %}

  {% tab label=VS Code (Copilot) %}
  Add to `.vscode/mcp.json` in your workspace:

  ```json
  {
    "servers": {
      "geminiDocs": {
        "type": "http",
        "url": "https://gemini-api-docs-mcp.dev"
      }
    }
  }
  ```

  {% /tab %}

{% /tabs %}

## Gemini API plugin  {% id="gemini-api-plugin" %}

If you use **Antigravity**, the **Gemini API plugin** is the fastest way to set up your workspace. It bundles the Gemini Docs MCP server, all official Gemini skills (`gemini-api-dev`, `gemini-live-api-dev`, `gemini-omni-flash-api`), and API key tools in one download.

- **Install in Antigravity (UI):** Go to **Settings > Customizations > Build with Google Plugins** and download **Gemini API**.
- **Install with the CLI:**  ```bash
  agy plugin install https://github.com/google-gemini/gemini-skills
  ```

## Machine-readable documentation  {% id="machine-readable-docs" %}

Standard web pages include HTML tags, navigation bars, and scripts that take up context window space. AI Studio serves documentation as clean Markdown to save tokens and help agents read documentation directly.

### How to access Markdown  {% id="markdown-access-methods" %}

| Method | How to use | Why use it |
| :--- | :--- | :--- |
| **Accept header (content negotiation)** | Send `Accept: text/markdown` on any `/docs/...` URL | Gets raw Markdown from the same URL you visit in a browser without changing the path. |
| **Direct `.md` URLs** | Add `.md` to any doc URL (such as `/docs/coding-agents.md`) | Gives you a clean Markdown link to share in prompts, `AGENTS.md` files, or scripts. |
| **`llms.txt` index** | [`https://aistudio.google.com/llms.txt`](https://aistudio.google.com/llms.txt) | Lists every documentation page with links to each raw Markdown file. |
| **`llms-full.txt` file** | [`https://aistudio.google.com/llms-full.txt`](https://aistudio.google.com/llms-full.txt) | Combines all Gemini API documentation pages into a single file for full context loading. |
| **Discovery headers** | Included on all `/docs` HTTP responses | Sets `Link` and `X-Llms-Txt` headers, and adds an `AI Agent Context` block to Markdown pages to point agents to the documentation indexes. |

To fetch Markdown from any documentation URL using the `Accept` header:

```bash
curl --header "Accept: text/markdown" https://aistudio.google.com/docs/interactions-overview
```

You can also click **Copy page** at the top of any documentation page to copy the Markdown source to your clipboard.

## Recommended project rules (`AGENTS.md`)  {% id="project-rules" %}

A project rules file (`AGENTS.md`, `.cursorrules`, or `CLAUDE.md`) sets baseline rules that load at the start of every agent session. Add these guidelines to your project root so coding agents default to current models and SDKs:

```markdown
# Gemini API Guidelines

- Before writing Gemini API code, consult the `geminiDocs` MCP server (`gemini_search_docs` / `gemini_get_doc`) or `https://aistudio.google.com/llms.txt`.
- Always use the current Google Gen AI SDK (`google-genai` for Python, `@google/genai` for TypeScript/JavaScript). Never use legacy SDKs (`google-generativeai` or `@google/generative-ai`).
- Use the Interactions API (`client.interactions.create`) for new applications unless a specific feature requires `generateContent`.
- Use current recommended models (see https://aistudio.google.com/docs/models) and avoid deprecated models.
```

## Verify and troubleshoot  {% id="verification-troubleshooting" %}

### Verify your setup  {% id="verify-setup" %}

To test your setup, ask your coding agent:

```none
Look up the request schema for the Gemini Interactions API in the documentation.
```

A configured agent will use `gemini_search_docs` on the `geminiDocs` MCP server and write code using `client.interactions.create` with the `google-genai` or `@google/genai` SDK.

### Status commands  {% id="status-commands" %}

| Environment | MCP verification | Skills verification |
| :--- | :--- | :--- |
| **Claude Code** | Run `/mcp` | Run `/skills` |
| **Cursor** | Open **Settings > Features > MCP** | Open **Settings > Rules** |
| **OpenAI Codex** | Run `codex mcp list` | Check `.codex/skills/` or `~/.codex/skills/` |
| **Antigravity** | Open **Customizations > Connections** | Open **Customizations > Rules** or run `/skills list` |
| **VS Code (Copilot)** | Open **Extensions > MCP** or Output panel | Click **Select Tools** in Copilot Chat |

### Troubleshooting  {% id="troubleshooting" %}

- **Skill or MCP server not detected:** Restart your editor (Cursor or VS Code) or terminal session (Claude Code or Codex). Most agents load MCP servers and skills only when they start.
- **Global skill conflict:** If your agent ignores a globally installed skill, install the skill in your project root without `--global`:  ```bash
  npx skills add google-gemini/gemini-skills --skill gemini-api-dev
  ```

- **Rules ignored:** Make sure your `AGENTS.md`, `.cursorrules`, or `CLAUDE.md` file is in the root directory of your project.

## What's next  {% id="whats-next" %}

- [Gemini API CLI](/docs/cli)
- [Gemini API Skills guide](https://aistudio.google.com/learn/gemini-api-skills)
- [Gemini API skills on GitHub](https://github.com/google-gemini/gemini-skills)
- [Interactions API](/docs/interactions-overview)
- [Available models](/docs/models)
- [Libraries and SDKs](/docs/libraries)