> ## AI Agent Context
> Get the complete documentation index at: https://aistudio.google.com/llms.txt
> Use this file to discover all available pages.
> For the full documentation in a single file, fetch: https://aistudio.google.com/llms-full.txt

# Agents overview

Managed agents on the Gemini API give you a configurable agent
harness. A single API call provisions a Linux sandbox where the agent reasons,
executes code, manages files, and browses the web autonomously.

{% card-grid %}
  {% card description="Make your first agent call, stream responses, and build a custom\nagent." href="/docs/managed-agents-quickstart" icon="rocket_launch" title="Quickstart" /%}

  {% card description="Capabilities, tools, multimodal input, and pricing for the\ndefault agent." href="/docs/antigravity-agent" icon="smart_toy" title="Antigravity Agent" /%}

  {% card description="Visual playground for prototyping agents without writing code." href="/docs/aistudio-agents" icon="experiment" title="Agents in AI Studio" /%}

{% /card-grid %}

## Available managed agents  {% id="managed-agents" %}

*   **[Antigravity agent](/docs/antigravity-agent)**: General-purpose
  managed agent built with Gemini 4 Hydrogen. Runs code, manages files, and
  searches the web inside a secure Linux sandbox hosted by Google. You can
  extend it with your own instructions, skills, and data to
  [build a custom agent](/docs/custom-agents).

*   **[Deep Research](/docs/deep-research)**: Autonomous research agent
  that plans, executes, and synthesizes multi-step research tasks for use
  cases like market analysis, due diligence, and literature reviews.

## Security and best practices  {% id="security-best-practices" %}

{% callout type="note" %}
  Note: Managed agents are in **Public Preview**. Review the agent's actions and
  outputs before relying on them in sensitive workflows.

{% /callout %}

Every agent runs in a sandboxed environment that is isolated at the OS level.
The sandbox has unrestricted outbound network access by default. You can
restrict or disable network access using an allowlist.

### Network access  {% id="network-access" %}

By default, environments have unrestricted outbound network access. Use a
`network` allowlist to restrict outbound traffic to specific domains or
wildcard patterns. For configuration details, see
[Network Allow List](/docs/aistudio-agents#network-allow-list) (AI
Studio) or [Network rules](/docs/custom-agents#with-network-rules)
(API).

### External tools and APIs  {% id="external-tools-and-apis" %}

You can connect external tools and APIs to extend the agent. Only use tools
from trusted sources and scope permissions to the minimum required. Store
secrets as managed credentials and reference them by ID, so the egress proxy
injects them at request time and they are never exposed inside the sandbox. The agent may use any credential it has access to,
so only provide credentials whose full scope you are willing to grant.

* Use least-privilege service accounts or API keys.
* Prefer short-lived tokens over long-lived keys.
* Only provide credentials whose full scope you are willing to grant.
* Rotate credentials on a regular schedule.

For the credential types and management operations, see
[Credentials](/docs/agent-credentials). You can also set headers inline on an
allowlist rule, see [Network
configuration](/docs/agent-environment#network-configuration).

### Human oversight  {% id="human-oversight" %}

Always verify outputs (generated code, data transformations, configuration
changes) before deploying them, especially for tasks that modify data or
interact with external systems.

## Pricing  {% id="pricing" %}

Managed agents use a [pay-as-you-go model](/docs/pricing#pricing-for-agents) based on Gemini model tokens and tool usage. A single interaction can trigger multiple reasoning loops, typically consuming 100k to 3M tokens. Environment compute is **not billed** during the preview. See [estimated costs](/docs/antigravity-agent#availability-and-pricing) for per-task breakdowns.

## Limits  {% id="limits" %}

| Limit | Description |
| :--- | :--- |
| **Environment Lifetime** | Environments are permanently deleted after 7 days of inactivity. |
| **VM Spin-down** | VMs shut down after a brief period of inactivity to conserve resources. The next request restores the state (with a cold start). |
| **Pre-installed Software** | Ubuntu-based environment with Python 3.12 and Node.js 22. For more information on the environment's base image, see [Pre-installed software](/docs/agent-environment#pre-installed-software). |
| **Max agents** | You can have up to 1,000 managed agents. |

## Agent frameworks  {% id="agent-frameworks" %}

You can also build agents with Gemini using these frameworks and SDKs:

*   [**LangChain / LangGraph**](/docs/langgraph-example): Build
  stateful, complex application flows and multi-agent systems using graph
  structures.

*   [**LlamaIndex**](/docs/llama-index): Connect Gemini agents to
  your private data for RAG-enhanced workflows.

*   [**CrewAI**](/docs/crewai-example): Orchestrate collaborative,
  role-playing autonomous AI agents.

*   [**Vercel AI SDK**](/docs/vercel-ai-sdk-example): Build
  AI-powered user interfaces and agents in JavaScript/TypeScript.

*   [**Google ADK**](https://google.github.io/adk-docs/get-started/python/): An
  open-source framework for building and orchestrating interoperable AI
  agents.

*   [**Antigravity SDK**](https://antigravity.google/product/antigravity-sdk): Build
  autonomous AI agents using the same tools, agent loop, and context
  management that power Google Antigravity, programmable in Python.