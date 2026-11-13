> ## AI Agent Context
> Get the complete documentation index at: https://aistudio.google.com/llms.txt
> Use this file to discover all available pages.
> For the full documentation in a single file, fetch: https://aistudio.google.com/llms-full.txt

# Building managed agents

Managed agents on the Gemini API let you extend the Antigravity agent with your own instructions, skills, and data. You can [customize the agent inline](/docs/custom-agents#customize-inline) at interaction time, or [save the configuration](/docs/custom-agents#save-agent) as a managed agent you invoke by ID.

## Customize the Antigravity agent  {% id="customize-inline" %}

The fastest way to build a custom agent is to pass your configuration inline while creating a new interaction with no registration step required. You can extend the agent in several key ways:

* **[Model selection](/docs/antigravity-agent#model-selection)**: Choose the underlying Gemini model via `agent_config` (defaults to **Gemini 4 Hydrogen**).
* **System instructions**: Pass inline text via `system_instruction` to shape behavior.
* **Tools**: Override default tools (Code Execution, Search, URL Context), register remote MCP servers, or define custom functions (Function Calling).
* **Files and skills**: Mount files like `AGENTS.md` and `SKILL.md` into the environment.

Here is an example of passing all three inline:

{% tabs %}
  {% tab filename="sample.py" label="Python" %}
  ```python
  from google import genai
  
  client = genai.Client(http_options={"api_version": "v1beta"})
  
  interaction = client.interactions.create(
      agent="antigravity-preview-09-2026",
      input="Analyze the Q1 revenue data and create a slide deck.",
      system_instruction="You are a data analyst. Always include visualizations and export results as PDF.",
      environment={
          "type": "remote",
          "sources": [
              {
                  "type": "inline",
                  "target": ".agents/AGENTS.md",
                  "content": "Always use matplotlib for charts. Include a summary table in every report.",
              },
              {
                  "type": "inline",
                  "target": ".agents/skills/slide-maker/SKILL.md",
                  "content": "---\nname: slide-maker\n---\n# Slide Maker\nCreate HTML slide decks from data analysis results.",
              },
          ],
      },
  )
  
  print(interaction.output_text)
  ```

  {% /tab %}

  {% tab filename="sample.js" label="JavaScript" %}
  ```javascript
  import { GoogleGenAI } from "@google/genai";
  
  const client = new GoogleGenAI({ httpOptions: { apiVersion: "v1beta" } });
  
  const interaction = await client.interactions.create({
      agent: "antigravity-preview-09-2026",
      input: "Analyze the Q1 revenue data and create a slide deck.",
      system_instruction: "You are a data analyst. Always include visualizations and export results as PDF.",
      environment: {
          type: "remote",
          sources: [
              {
                  type: "inline",
                  target: ".agents/AGENTS.md",
                  content: "Always use matplotlib for charts. Include a summary table in every report.",
              },
              {
                  type: "inline",
                  target: ".agents/skills/slide-maker/SKILL.md",
                  content: "---\nname: slide-maker\n---\n# Slide Maker\nCreate HTML slide decks from data analysis results.",
              },
          ],
      },
  }, { timeout: 300000 });
  
  console.log(interaction.output_text);
  ```

  {% /tab %}

  {% tab filename="sample.sh" label="REST" %}
  ```shell
  curl -X POST "https://generativelanguage.googleapis.com/v1beta/interactions" \
  -H "Content-Type: application/json" \
  -H "x-goog-api-key: $GEMINI_API_KEY" \
  -d '{
      "agent": "antigravity-preview-09-2026",
      "input": "Analyze the Q1 revenue data and create a slide deck.",
      "system_instruction": "You are a data analyst. Always include visualizations and export results as PDF.",
      "environment": {
          "type": "remote",
          "sources": [
              {
                  "type": "inline",
                  "target": ".agents/AGENTS.md",
                  "content": "Always use matplotlib for charts. Include a summary table in every report."
              },
              {
                  "type": "inline",
                  "target": ".agents/skills/slide-maker/SKILL.md",
                  "content": "---\nname: slide-maker\n---\n# Slide Maker\nCreate HTML slide decks from data analysis results."
              }
          ]
      }
  }'
  ```

  Everything is defined at interaction time. No need to register anything first. The Antigravity agent harness provides the runtime (code execution, file management, web access) and your configuration layers on top.

  {% /tab %}

  {% tab label="Java" %}
  ```java
  import com.google.genai.Client;
  import com.google.genai.types.HttpOptions;
  import com.google.genai.gaos.models.interactions.AgentOption;
  import com.google.genai.gaos.models.interactions.CreateAgentInteraction;
  import com.google.genai.gaos.models.interactions.CreateAgentInteractionEnvironment;
  import com.google.genai.gaos.models.interactions.Environment;
  import com.google.genai.gaos.models.interactions.Interaction;
  import com.google.genai.gaos.models.interactions.InteractionsInput;
  import com.google.genai.gaos.models.interactions.Source;
  import com.google.genai.gaos.models.interactions.SourceType;
  import com.google.genai.gaos.models.operations.CreateInteractionRequestBody;
  import java.util.List;
  
  Client client = Client.builder().httpOptions(HttpOptions.builder().apiVersion("v1beta").build()).build();
  
  Environment env = Environment.builder()
      .sources(List.of(
          Source.builder()
              .type(SourceType.INLINE)
              .target(".agents/AGENTS.md")
              .content("Always use matplotlib for charts. Include a summary table in every report.")
              .build(),
          Source.builder()
              .type(SourceType.INLINE)
              .target(".agents/skills/slide-maker/SKILL.md")
              .content("---\nname: slide-maker\n---\n# Slide Maker\nCreate HTML slide decks from data analysis results.")
              .build()
      ))
      .build();
  
  CreateAgentInteraction params = CreateAgentInteraction.builder()
      .agent(AgentOption.of("antigravity-preview-09-2026"))
      .input(InteractionsInput.of("Analyze the Q1 revenue data and create a slide deck."))
      .systemInstruction("You are a data analyst. Always include visualizations and export results as PDF.")
      .environment(CreateAgentInteractionEnvironment.of(env))
      .build();
  
  Interaction interaction = client.interactions.create(CreateInteractionRequestBody.of(params)).interaction().get();
  System.out.println(interaction.outputText().orElse(""));
  ```

  {% /tab %}

  {% tab label="Go" %}
  ```go
  package main
  
  import (
      "context"
      "fmt"
      "log"
  
      "google.golang.org/genai"
      "google.golang.org/genai/interactions/models/interactions"
      "google.golang.org/genai/interactions/models/operations"
  )
  
  func main() {
      ctx := context.Background()
      client, err := genai.NewClient(ctx, &genai.ClientConfig{HTTPOptions: genai.HTTPOptions{APIVersion: "v1beta"}})
      if err != nil {
          log.Fatal(err)
      }
  
      env := interactions.Environment{
          Sources: []interactions.Source{
              {
                  Type:    interactions.SourceTypeInline.ToPointer(),
                  Target:  genai.Ptr(".agents/AGENTS.md"),
                  Content: genai.Ptr("Always use matplotlib for charts. Include a summary table in every report."),
              },
              {
                  Type:    interactions.SourceTypeInline.ToPointer(),
                  Target:  genai.Ptr(".agents/skills/slide-maker/SKILL.md"),
                  Content: genai.Ptr("---\nname: slide-maker\n---\n# Slide Maker\nCreate HTML slide decks from data analysis results."),
              },
          },
      }
  
      res, err := client.Interactions.Create(ctx, operations.CreateInteractionRequest{
          Body: operations.NewCreateInteractionRequestBody(interactions.CreateAgentInteraction{
              Agent:             interactions.AgentOption("antigravity-preview-09-2026"),
              Input:             interactions.NewInteractionsInput("Analyze the Q1 revenue data and create a slide deck."),
              SystemInstruction: genai.Ptr("You are a data analyst. Always include visualizations and export results as PDF."),
              Environment:       genai.Ptr(interactions.NewCreateAgentInteractionEnvironment(env)),
          }),
      })
      if err != nil {
          log.Fatal(err)
      }
      if res.Interaction.OutputText != nil {
          fmt.Println(*res.Interaction.OutputText)
      }
  }
  ```

  {% /tab %}

{% /tabs %}

### Tools and system instructions

You can customize the agent's behavior and capabilities for a specific interaction using the `system_instruction` and `tools` parameters.

- **System instructions**: Use the `system_instruction` parameter to pass inline text that shapes the agent's behavior. This is ideal for quick tweaks you want to change per call. The `system_instruction` and `AGENTS.md` are additive; both apply when present.
- **Tools**: By default, the Antigravity agent has access to `code_execution`, `google_search`, and `url_context`. You can override this list by passing the `tools` parameter at interaction time. You can also register [remote MCP servers](/docs/antigravity-agent#mcp-servers) or define [custom functions (function calling)](/docs/antigravity-agent#function-calling) to connect the agent to your own APIs and databases. For full details on available tools, see [Antigravity Agent: Supported tools](/docs/antigravity-agent#supported-tools).

### File-based customization

#### Agent directory structure

While you can pass configuration inline, we recommend organizing your agent's files in a structured directory. This makes it easier to manage, version control, and mount into the agent's environment.

{% callout type="note" %}
  You can also use the open-source [Gemini API CLI](/docs/cli) to create and run custom agents or connect local sandbox environments directly from your terminal.

{% /callout %}

A typical agent project directory looks like this:

```text
my-agent/
├── AGENTS.md        # Instructions on how the agent should operate
├── skills/          # Custom skills (subfolders and SKILL.md files)
│   └── slide-maker/
│       └── SKILL.md
└── workspace/       # Initial data files and knowledge
```

The Antigravity runtime scans `.agents/` (and the root of the environment) for these files.

#### AGENTS.md

The agent automatically loads `.agents/AGENTS.md` (or `/.agents/AGENTS.md`) from the environment as system instructions on startup. Use `AGENTS.md` for long-form persona definitions, detailed guidelines, and instructions you want to version control alongside your code.

Mount an `AGENTS.md` using an inline source:

{% tabs %}
  {% tab filename="sample.py" label="Python" %}
  ```python
  from google import genai
  
  client = genai.Client(http_options={"api_version": "v1beta"})
  
  interaction = client.interactions.create(
      agent="antigravity-preview-09-2026",
      input="Analyze the Q1 revenue data and create a report.",
      system_instruction="You are a data analyst. Always include visualizations and export results as PDF.",
      environment={
          "type": "remote",
          "sources": [
              {
                  "type": "inline",
                  "target": ".agents/AGENTS.md",
                  "content": "Always use matplotlib for charts. Include a summary table in every report.",
              },
          ],
      },
  )
  
  print(interaction.output_text)
  ```

  {% /tab %}

  {% tab filename="sample.js" label="JavaScript" %}
  ```javascript
  import { GoogleGenAI } from "@google/genai";
  
  const client = new GoogleGenAI({ httpOptions: { apiVersion: "v1beta" } });
  
  const interaction = await client.interactions.create({
      agent: "antigravity-preview-09-2026",
      input: "Analyze the Q1 revenue data and create a report.",
      system_instruction: "You are a data analyst. Always include visualizations and export results as PDF.",
      environment: {
          type: "remote",
          sources: [
              {
                  type: "inline",
                  target: ".agents/AGENTS.md",
                  content: "Always use matplotlib for charts. Include a summary table in every report.",
              },
          ],
      },
  }, { timeout: 300000 });
  
  console.log(interaction.output_text);
  ```

  {% /tab %}

  {% tab filename="sample.sh" label="REST" %}
  ```shell
  curl -X POST "https://generativelanguage.googleapis.com/v1beta/interactions" \
    -H "Content-Type: application/json" \
    -H "x-goog-api-key: $GEMINI_API_KEY" \
    -d '{
        "agent": "antigravity-preview-09-2026",
        "input": "Analyze the Q1 revenue data and create a report.",
        "system_instruction": "You are a data analyst. Always include visualizations and export results as PDF.",
        "environment": {
            "type": "remote",
            "sources": [
                {
                    "type": "inline",
                    "target": ".agents/AGENTS.md",
                    "content": "Always use matplotlib for charts. Include a summary table in every report."
                }
            ]
        }
    }'
  ```

  {% /tab %}

  {% tab label="Java" %}
  ```java
  import com.google.genai.Client;
  import com.google.genai.types.HttpOptions;
  import com.google.genai.gaos.models.interactions.AgentOption;
  import com.google.genai.gaos.models.interactions.CreateAgentInteraction;
  import com.google.genai.gaos.models.interactions.CreateAgentInteractionEnvironment;
  import com.google.genai.gaos.models.interactions.Environment;
  import com.google.genai.gaos.models.interactions.Interaction;
  import com.google.genai.gaos.models.interactions.InteractionsInput;
  import com.google.genai.gaos.models.interactions.Source;
  import com.google.genai.gaos.models.interactions.SourceType;
  import com.google.genai.gaos.models.operations.CreateInteractionRequestBody;
  import java.util.List;
  
  Client client = Client.builder().httpOptions(HttpOptions.builder().apiVersion("v1beta").build()).build();
  
  Environment env = Environment.builder()
      .sources(List.of(
          Source.builder()
              .type(SourceType.INLINE)
              .target(".agents/AGENTS.md")
              .content("Always use matplotlib for charts. Include a summary table in every report.")
              .build()
      ))
      .build();
  
  CreateAgentInteraction params = CreateAgentInteraction.builder()
      .agent(AgentOption.of("antigravity-preview-09-2026"))
      .input(InteractionsInput.of("Analyze the Q1 revenue data and create a report."))
      .systemInstruction("You are a data analyst. Always include visualizations and export results as PDF.")
      .environment(CreateAgentInteractionEnvironment.of(env))
      .build();
  
  Interaction interaction = client.interactions.create(CreateInteractionRequestBody.of(params)).interaction().get();
  System.out.println(interaction.outputText().orElse(""));
  ```

  {% /tab %}

  {% tab label="Go" %}
  ```go
  package main
  
  import (
      "context"
      "fmt"
      "log"
  
      "google.golang.org/genai"
      "google.golang.org/genai/interactions/models/interactions"
      "google.golang.org/genai/interactions/models/operations"
  )
  
  func main() {
      ctx := context.Background()
      client, err := genai.NewClient(ctx, &genai.ClientConfig{HTTPOptions: genai.HTTPOptions{APIVersion: "v1beta"}})
      if err != nil {
          log.Fatal(err)
      }
  
      env := interactions.Environment{
          Sources: []interactions.Source{
              {
                  Type:    interactions.SourceTypeInline.ToPointer(),
                  Target:  genai.Ptr(".agents/AGENTS.md"),
                  Content: genai.Ptr("Always use matplotlib for charts. Include a summary table in every report."),
              },
          },
      }
  
      res, err := client.Interactions.Create(ctx, operations.CreateInteractionRequest{
          Body: operations.NewCreateInteractionRequestBody(interactions.CreateAgentInteraction{
              Agent:             interactions.AgentOption("antigravity-preview-09-2026"),
              Input:             interactions.NewInteractionsInput("Analyze the Q1 revenue data and create a report."),
              SystemInstruction: genai.Ptr("You are a data analyst. Always include visualizations and export results as PDF."),
              Environment:       genai.Ptr(interactions.NewCreateAgentInteractionEnvironment(env)),
          }),
      })
      if err != nil {
          log.Fatal(err)
      }
      if res.Interaction.OutputText != nil {
          fmt.Println(*res.Interaction.OutputText)
      }
  }
  ```

  {% /tab %}

{% /tabs %}

#### Skills: SKILL.md

Skills are files that extend the agent's capabilities. Place them under `.agents/skills/<skill-name>/SKILL.md` and the harness auto-discovers and registers them.

```text
.agents/
├── AGENTS.md
└── skills/
    └── slide-maker/
        └── SKILL.md
```

Mount a skill using an inline source:

{% tabs %}
  {% tab filename="sample.py" label="Python" %}
  ```python
  from google import genai
  
  client = genai.Client(http_options={"api_version": "v1beta"})
  
  interaction = client.interactions.create(
      agent="antigravity-preview-09-2026",
      input="Create a presentation about our Q1 results.",
      system_instruction="You create presentations from data.",
      environment={
          "type": "remote",
          "sources": [
              {
                  "type": "inline",
                  "target": ".agents/skills/slide-maker/SKILL.md",
                  "content": "---\nname: slide-maker\ndescription: Create HTML slide decks\n---\n# Slide Maker\n\nWhen asked to create a presentation:\n1. Analyze the input data\n2. Create an HTML slide deck with reveal.js\n3. Save to /workspace/output/slides.html",
              },
          ],
      },
  )
  
  print(interaction.output_text)
  ```

  {% /tab %}

  {% tab filename="sample.js" label="JavaScript" %}
  ```javascript
  import { GoogleGenAI } from "@google/genai";
  
  const client = new GoogleGenAI({ httpOptions: { apiVersion: "v1beta" } });
  
  const interaction = await client.interactions.create({
      agent: "antigravity-preview-09-2026",
      input: "Create a presentation about our Q1 results.",
      system_instruction: "You create presentations from data.",
      environment: {
          type: "remote",
          sources: [
              {
                  type: "inline",
                  target: ".agents/skills/slide-maker/SKILL.md",
                  content: "---\nname: slide-maker\ndescription: Create HTML slide decks\n---\n# Slide Maker\n\nWhen asked to create a presentation:\n1. Analyze the input data\n2. Create an HTML slide deck with reveal.js\n3. Save to /workspace/output/slides.html",
              },
          ],
      },
  }, { timeout: 300000 });
  
  console.log(interaction.output_text);
  ```

  {% /tab %}

  {% tab filename="sample.sh" label="REST" %}
  ```shell
  curl -X POST "https://generativelanguage.googleapis.com/v1beta/interactions" \
    -H "Content-Type: application/json" \
    -H "x-goog-api-key: $GEMINI_API_KEY" \
    -d '{
        "agent": "antigravity-preview-09-2026",
        "input": "Create a presentation about our Q1 results.",
        "system_instruction": "You create presentations from data.",
        "environment": {
            "type": "remote",
            "sources": [
                {
                    "type": "inline",
                    "target": ".agents/skills/slide-maker/SKILL.md",
                    "content": "---\nname: slide-maker\ndescription: Create HTML slide decks\n---\n# Slide Maker\n\nWhen asked to create a presentation:\n1. Analyze the input data\n2. Create an HTML slide deck with reveal.js\n3. Save to /workspace/output/slides.html"
                }
            ]
        }
    }'
  ```

  Skills loaded from `.agents/skills/` and `/.agents/skills/` are both discovered automatically.

  {% /tab %}

  {% tab label="Java" %}
  ```java
  import com.google.genai.Client;
  import com.google.genai.types.HttpOptions;
  import com.google.genai.gaos.models.interactions.AgentOption;
  import com.google.genai.gaos.models.interactions.CreateAgentInteraction;
  import com.google.genai.gaos.models.interactions.CreateAgentInteractionEnvironment;
  import com.google.genai.gaos.models.interactions.Environment;
  import com.google.genai.gaos.models.interactions.Interaction;
  import com.google.genai.gaos.models.interactions.InteractionsInput;
  import com.google.genai.gaos.models.interactions.Source;
  import com.google.genai.gaos.models.interactions.SourceType;
  import com.google.genai.gaos.models.operations.CreateInteractionRequestBody;
  import java.util.List;
  
  Client client = Client.builder().httpOptions(HttpOptions.builder().apiVersion("v1beta").build()).build();
  
  Environment env = Environment.builder()
      .sources(List.of(
          Source.builder()
              .type(SourceType.INLINE)
              .target(".agents/skills/slide-maker/SKILL.md")
              .content("---\nname: slide-maker\ndescription: Create HTML slide decks\n---\n# Slide Maker\n\nWhen asked to create a presentation:\n1. Analyze the input data\n2. Create an HTML slide deck with reveal.js\n3. Save to /workspace/output/slides.html")
              .build()
      ))
      .build();
  
  CreateAgentInteraction params = CreateAgentInteraction.builder()
      .agent(AgentOption.of("antigravity-preview-09-2026"))
      .input(InteractionsInput.of("Create a presentation about our Q1 results."))
      .systemInstruction("You create presentations from data.")
      .environment(CreateAgentInteractionEnvironment.of(env))
      .build();
  
  Interaction interaction = client.interactions.create(CreateInteractionRequestBody.of(params)).interaction().get();
  System.out.println(interaction.outputText().orElse(""));
  ```

  {% /tab %}

  {% tab label="Go" %}
  ```go
  package main
  
  import (
      "context"
      "fmt"
      "log"
  
      "google.golang.org/genai"
      "google.golang.org/genai/interactions/models/interactions"
      "google.golang.org/genai/interactions/models/operations"
  )
  
  func main() {
      ctx := context.Background()
      client, err := genai.NewClient(ctx, &genai.ClientConfig{HTTPOptions: genai.HTTPOptions{APIVersion: "v1beta"}})
      if err != nil {
          log.Fatal(err)
      }
  
      env := interactions.Environment{
          Sources: []interactions.Source{
              {
                  Type:    interactions.SourceTypeInline.ToPointer(),
                  Target:  genai.Ptr(".agents/skills/slide-maker/SKILL.md"),
                  Content: genai.Ptr("---\nname: slide-maker\ndescription: Create HTML slide decks\n---\n# Slide Maker\n\nWhen asked to create a presentation:\n1. Analyze the input data\n2. Create an HTML slide deck with reveal.js\n3. Save to /workspace/output/slides.html"),
              },
          },
      }
  
      res, err := client.Interactions.Create(ctx, operations.CreateInteractionRequest{
          Body: operations.NewCreateInteractionRequestBody(interactions.CreateAgentInteraction{
              Agent:             interactions.AgentOption("antigravity-preview-09-2026"),
              Input:             interactions.NewInteractionsInput("Create a presentation about our Q1 results."),
              SystemInstruction: genai.Ptr("You create presentations from data."),
              Environment:       genai.Ptr(interactions.NewCreateAgentInteractionEnvironment(env)),
          }),
      })
      if err != nil {
          log.Fatal(err)
      }
      if res.Interaction.OutputText != nil {
          fmt.Println(*res.Interaction.OutputText)
      }
  }
  ```

  {% /tab %}

{% /tabs %}

## Create a managed agent  {% id="save-agent" %}

Once you've iterated on your configuration, you can create it as a managed agent with `agents.create`. This lets you invoke the agent by ID without repeating the configuration each time.

The `id` you specify when creating a managed agent must be unique to your project and must not start with reserved prefixes (e.g., `google-`, `gemini-`). See [Agent ID restrictions](/docs/custom-agents#agent-id-restrictions) for the full list of restricted prefixes.

### From sources

Specify `base_agent`, `id`, `agent_config`, `system_instruction` and `base_environment` with sources. The platform provisions a fresh sandbox with your files on every invocation. See [Environments](/docs/agent-environment) for available source types (Git, GCS, inline).

{% tabs %}
  {% tab filename="sample.py" label="Python" %}
  ```python
  from google import genai
  
  client = genai.Client(http_options={"api_version": "v1beta"})
  
  agent = client.agents.create(
      id="data-analyst",
      base_agent="antigravity-preview-09-2026",
      agent_config={
          "type": "antigravity",
          "model": "gemini-4-hydrogen",
      },
      system_instruction="You are a data analyst. Always include visualizations and export results as PDF.",
      base_environment={
          "type": "remote",
          "sources": [
              {
                  "type": "inline",
                  "target": ".agents/AGENTS.md",
                  "content": "Always use matplotlib for charts. Include a summary table in every report.",
              },
              {
                  "type": "inline",
                  "target": ".agents/skills/slide-maker/SKILL.md",
                  "content": "---\nname: slide-maker\n---\n# Slide Maker\nCreate HTML slide decks from data analysis results.",
              },
              {
                  "type": "repository",
                  "source": "https://github.com/my-org/analysis-templates",
                  "target": "/workspace/templates",
              },
          ],
      },
  )
  
  print(f"Created agent: {agent.id}")
  ```

  {% /tab %}

  {% tab filename="sample.js" label="JavaScript" %}
  ```javascript
  import { GoogleGenAI } from "@google/genai";
  
  const client = new GoogleGenAI({ httpOptions: { apiVersion: "v1beta" } });
  
  const agent = await client.agents.create({
      id: "data-analyst",
      base_agent: "antigravity-preview-09-2026",
      agent_config: {
          type: "antigravity",
          model: "gemini-4-hydrogen",
      },
      system_instruction: "You are a data analyst. Always include visualizations and export results as PDF.",
      base_environment: {
          type: "remote",
          sources: [
              {
                  type: "inline",
                  target: ".agents/AGENTS.md",
                  content: "Always use matplotlib for charts. Include a summary table in every report.",
              },
              {
                  type: "inline",
                  target: ".agents/skills/slide-maker/SKILL.md",
                  content: "---\nname: slide-maker\n---\n# Slide Maker\nCreate HTML slide decks from data analysis results.",
              },
              {
                  type: "repository",
                  source: "https://github.com/my-org/analysis-templates",
                  target: "/workspace/templates",
              },
          ],
      },
  });
  
  console.log(`Created agent: ${agent.id}`);
  ```

  {% /tab %}

  {% tab filename="sample.sh" label="REST" %}
  ```shell
  curl -X POST "https://generativelanguage.googleapis.com/v1beta/agents" \
  -H "Content-Type: application/json" \
  -H "x-goog-api-key: $GEMINI_API_KEY" \
  -d '{
      "id": "data-analyst",
      "base_agent": "antigravity-preview-09-2026",
      "agent_config": {
          "type": "antigravity",
          "model": "gemini-4-hydrogen"
      },
      "system_instruction": "You are a data analyst. Always include visualizations and export results as PDF.",
      "base_environment": {
          "type": "remote",
          "sources": [
              {
                  "type": "inline",
                  "target": ".agents/AGENTS.md",
                  "content": "Always use matplotlib for charts. Include a summary table in every report."
              },
              {
                  "type": "inline",
                  "target": ".agents/skills/slide-maker/SKILL.md",
                  "content": "---\nname: slide-maker\n---\n# Slide Maker\nCreate HTML slide decks from data analysis results."
              },
              {
                  "type": "repository",
                  "source": "https://github.com/my-org/analysis-templates",
                  "target": "/workspace/templates"
              }
          ]
      }
  }'
  ```

  {% /tab %}

  {% tab label="Java" %}
  ```java
  import com.google.genai.Client;
  import com.google.genai.types.HttpOptions;
  import com.google.genai.gaos.models.agents.Agent;
  import com.google.genai.gaos.models.agents.AgentConfig;
  import com.google.genai.gaos.models.agents.BaseEnvironment;
  import com.google.genai.gaos.models.interactions.AntigravityAgentConfig;
  import com.google.genai.gaos.models.interactions.Environment;
  import com.google.genai.gaos.models.interactions.Source;
  import com.google.genai.gaos.models.interactions.SourceType;
  import java.util.List;
  
  Client client = Client.builder().httpOptions(HttpOptions.builder().apiVersion("v1beta").build()).build();
  
  Environment env = Environment.builder()
      .sources(List.of(
          Source.builder()
              .type(SourceType.INLINE)
              .target(".agents/AGENTS.md")
              .content("Always use matplotlib for charts. Include a summary table in every report.")
              .build(),
          Source.builder()
              .type(SourceType.INLINE)
              .target(".agents/skills/slide-maker/SKILL.md")
              .content("---\nname: slide-maker\n---\n# Slide Maker\nCreate HTML slide decks from data analysis results.")
              .build(),
          Source.builder()
              .type(SourceType.REPOSITORY)
              .source("https://github.com/my-org/analysis-templates")
              .target("/workspace/templates")
              .build()
      ))
      .build();
  
  Agent agentParams = Agent.builder()
      .id("data-analyst")
      .baseAgent("antigravity-preview-09-2026")
      .agentConfig(AgentConfig.of(
          AntigravityAgentConfig.builder()
              .model("gemini-4-hydrogen")
              .build()
      ))
      .systemInstruction("You are a data analyst. Always include visualizations and export results as PDF.")
      .baseEnvironment(BaseEnvironment.of(env))
      .build();
  
  Agent agent = client.agents.create(agentParams).agent().get();
  System.out.println("Created agent: " + agent.id().orElse(""));
  ```

  {% /tab %}

  {% tab label="Go" %}
  ```go
  package main
  
  import (
      "context"
      "fmt"
      "log"
  
      "google.golang.org/genai"
      "google.golang.org/genai/interactions/models/agents"
      "google.golang.org/genai/interactions/models/interactions"
      "google.golang.org/genai/interactions/models/operations"
  )
  
  func main() {
      ctx := context.Background()
      client, err := genai.NewClient(ctx, &genai.ClientConfig{HTTPOptions: genai.HTTPOptions{APIVersion: "v1beta"}})
      if err != nil {
          log.Fatal(err)
      }
  
      env := interactions.Environment{
          Sources: []interactions.Source{
              {
                  Type:    interactions.SourceTypeInline.ToPointer(),
                  Target:  genai.Ptr(".agents/AGENTS.md"),
                  Content: genai.Ptr("Always use matplotlib for charts. Include a summary table in every report."),
              },
              {
                  Type:    interactions.SourceTypeInline.ToPointer(),
                  Target:  genai.Ptr(".agents/skills/slide-maker/SKILL.md"),
                  Content: genai.Ptr("---\nname: slide-maker\n---\n# Slide Maker\nCreate HTML slide decks from data analysis results."),
              },
              {
                  Type:   interactions.SourceTypeRepository.ToPointer(),
                  Source: genai.Ptr("https://github.com/my-org/analysis-templates"),
                  Target: genai.Ptr("/workspace/templates"),
              },
          },
      }
  
      res, err := client.Agents.Create(ctx, operations.CreateAgentRequest{
          Body: agents.Agent{
              ID:        genai.Ptr("data-analyst"),
              BaseAgent: genai.Ptr("antigravity-preview-09-2026"),
              AgentConfig: genai.Ptr(agents.NewAgentConfig(interactions.AntigravityAgentConfig{
                  Model: genai.Ptr("gemini-4-hydrogen"),
              })),
              SystemInstruction: genai.Ptr("You are a data analyst. Always include visualizations and export results as PDF."),
              BaseEnvironment:   genai.Ptr(agents.NewBaseEnvironment(env)),
          },
      })
      if err != nil {
          log.Fatal(err)
      }
  
      fmt.Printf("Created agent: %s\n", *res.Agent.ID)
  }
  ```

  {% /tab %}

{% /tabs %}

### From an existing environment (fork)

Iterate with the base Antigravity agent until the environment is right (packages installed, files in place), then fork it into a managed agent.

{% tabs %}
  {% tab filename="sample.py" label="Python" %}
  ```python
  from google import genai
  
  client = genai.Client(http_options={"api_version": "v1beta"})
  
  # Step 1: set up the environment interactively
  interaction = client.interactions.create(
      agent="antigravity-preview-09-2026",
      input="Install pandas, matplotlib, and seaborn. Create an analysis template at /workspace/template.py.",
      environment="remote",
  )
  
  # Step 2: fork that environment into a managed agent
  
  agent = client.agents.create(
      id="my-data-analyst",
      base_agent="antigravity-preview-09-2026",
      system_instruction="You are a data analyst. Use the template at /workspace/template.py for all reports.",
      base_environment=interaction.environment_id,
  )
  
  print(f"Forked agent successfully: {agent.id}")
  ```

  {% /tab %}

  {% tab filename="sample.js" label="JavaScript" %}
  ```javascript
  import { GoogleGenAI } from "@google/genai";
  
  const client = new GoogleGenAI({ httpOptions: { apiVersion: "v1beta" } });
  
  const interaction = await client.interactions.create({
      agent: "antigravity-preview-09-2026",
      input: "Install pandas, matplotlib, and seaborn. Create an analysis template at /workspace/template.py.",
      environment: "remote",
  }, { timeout: 300000 });
  
  const agent = await client.agents.create({
      id: "my-data-analyst",
      base_agent: "antigravity-preview-09-2026",
      system_instruction: "You are a data analyst. Use the template at /workspace/template.py for all reports.",
      base_environment: interaction.environment_id,
  });
  
  console.log(`Forked agent successfully: ${agent.id}`);
  ```

  {% /tab %}

  {% tab filename="sample.sh" label="REST" %}
  ```shell
  curl -X POST "https://generativelanguage.googleapis.com/v1beta/interactions" \
    -H "Content-Type: application/json" \
    -H "x-goog-api-key: $GEMINI_API_KEY" \
    -d '{
        "agent": "antigravity-preview-09-2026",
        "input": "Install pandas, matplotlib, and seaborn. Create an analysis template at /workspace/template.py.",
        "environment": "remote"
    }'
  ```

  {% /tab %}

  {% tab label="Java" %}
  ```java
  import com.google.genai.Client;
  import com.google.genai.types.HttpOptions;
  import com.google.genai.gaos.models.agents.Agent;
  import com.google.genai.gaos.models.agents.BaseEnvironment;
  import com.google.genai.gaos.models.interactions.AgentOption;
  import com.google.genai.gaos.models.interactions.CreateAgentInteraction;
  import com.google.genai.gaos.models.interactions.CreateAgentInteractionEnvironment;
  import com.google.genai.gaos.models.interactions.Interaction;
  import com.google.genai.gaos.models.interactions.InteractionsInput;
  import com.google.genai.gaos.models.operations.CreateInteractionRequestBody;
  
  Client client = Client.builder().httpOptions(HttpOptions.builder().apiVersion("v1beta").build()).build();
  
  // Step 1: set up the environment interactively
  CreateAgentInteraction params = CreateAgentInteraction.builder()
      .agent(AgentOption.of("antigravity-preview-09-2026"))
      .input(InteractionsInput.of("Install pandas, matplotlib, and seaborn. Create an analysis template at /workspace/template.py."))
      .environment(CreateAgentInteractionEnvironment.of("remote"))
      .build();
  
  Interaction interaction = client.interactions.create(CreateInteractionRequestBody.of(params)).interaction().get();
  
  // Step 2: fork that environment into a managed agent
  Agent agentParams = Agent.builder()
      .id("my-data-analyst")
      .baseAgent("antigravity-preview-09-2026")
      .systemInstruction("You are a data analyst. Use the template at /workspace/template.py for all reports.")
      .baseEnvironment(BaseEnvironment.of(interaction.environmentId().orElse("")))
      .build();
  
  Agent agent = client.agents.create(agentParams).agent().get();
  System.out.println("Forked agent successfully: " + agent.id().orElse(""));
  ```

  {% /tab %}

  {% tab label="Go" %}
  ```go
  package main
  
  import (
      "context"
      "fmt"
      "log"
  
      "google.golang.org/genai"
      "google.golang.org/genai/interactions/models/agents"
      "google.golang.org/genai/interactions/models/interactions"
      "google.golang.org/genai/interactions/models/operations"
  )
  
  func main() {
      ctx := context.Background()
      client, err := genai.NewClient(ctx, &genai.ClientConfig{HTTPOptions: genai.HTTPOptions{APIVersion: "v1beta"}})
      if err != nil {
          log.Fatal(err)
      }
  
      // Step 1: set up the environment interactively
      intRes, err := client.Interactions.Create(ctx, operations.CreateInteractionRequest{
          Body: operations.NewCreateInteractionRequestBody(interactions.CreateAgentInteraction{
              Agent:       interactions.AgentOption("antigravity-preview-09-2026"),
              Input:       interactions.NewInteractionsInput("Install pandas, matplotlib, and seaborn. Create an analysis template at /workspace/template.py."),
              Environment: genai.Ptr(interactions.NewCreateAgentInteractionEnvironment("remote")),
          }),
      })
      if err != nil {
          log.Fatal(err)
      }
      interaction := intRes.Interaction
  
      // Step 2: fork that environment into a managed agent
      agentRes, err := client.Agents.Create(ctx, operations.CreateAgentRequest{
          Body: agents.Agent{
              ID:                genai.Ptr("my-data-analyst"),
              BaseAgent:         genai.Ptr("antigravity-preview-09-2026"),
              SystemInstruction: genai.Ptr("You are a data analyst. Use the template at /workspace/template.py for all reports."),
              BaseEnvironment:   genai.Ptr(agents.NewBaseEnvironment(*interaction.EnvironmentID)),
          },
      })
      if err != nil {
          log.Fatal(err)
      }
  
      fmt.Printf("Forked agent successfully: %s\n", *agentRes.Agent.ID)
  }
  ```

  {% /tab %}

{% /tabs %}

### With network rules  {% id="with-network-rules" %}

You can lock down outbound access or inject credentials when saving a managed agent. For the full allowlist schema, credential patterns, and wildcards, see [Environments: Network configuration](/docs/agent-environment#network-configuration).

Reference a stored [credential](/docs/agent-credentials) by ID on an allowlist rule (`"credential": "github-production"`) and the egress proxy injects the secret at request time, so it never lands in your agent definition. This example sets the header inline with `transform` instead. The proxy applies both forms the same way, a credential additionally lets you reuse the secret across agents and rotate it in one place.

The following example creates an `issue-resolver` agent that can only access GitHub and PyPI, with credentials injected for GitHub:

{% tabs %}
  {% tab filename="sample.py" label="Python" %}
  ```python
  from google import genai
  
  client = genai.Client(http_options={"api_version": "v1beta"})
  
  agent = client.agents.create(
      id="issue-resolver",
      base_agent="antigravity-preview-09-2026",
      system_instruction="You resolve GitHub issues. Clone the repo, find the bug, write the fix, run the tests, and open a PR.",
      base_environment={
          "type": "remote",
          "sources": [
              {
                  "type": "repository",
                  "source": "https://github.com/my-org/backend",
                  "target": "/workspace/repo",
              }
          ],
          "network": {
              "allowlist": [
                  {
                      "domain": "api.github.com",
                      "transform": {
                          "Authorization": "Basic YOUR_BASE64_TOKEN"
                      },
                  },
                  {"domain": "pypi.org"},
              ]
          },
      },
  )
  
  print(f"Created issue-resolver agent successfully: {agent.id}")
  ```

  {% /tab %}

  {% tab filename="sample.js" label="JavaScript" %}
  ```javascript
  import { GoogleGenAI } from "@google/genai";
  
  const client = new GoogleGenAI({ httpOptions: { apiVersion: "v1beta" } });
  
  const agent = await client.agents.create({
      id: "issue-resolver",
      base_agent: "antigravity-preview-09-2026",
      system_instruction: "You resolve GitHub issues. Clone the repo, find the bug, write the fix, run the tests, and open a PR.",
      base_environment: {
          type: "remote",
          sources: [
              {
                  type: "repository",
                  source: "https://github.com/my-org/backend",
                  target: "/workspace/repo",
              }
          ],
          network: {
              allowlist: [
                  {
                      domain: "api.github.com",
                      transform: {
                          "Authorization": "Basic YOUR_BASE64_TOKEN"
                      },
                  },
                  { domain: "pypi.org" },
              ]
          }
      },
  });
  
  console.log(`Created issue-resolver agent successfully: ${agent.id}`);
  ```

  {% /tab %}

  {% tab filename="sample.sh" label="REST" %}
  ```shell
  curl -X POST "https://generativelanguage.googleapis.com/v1beta/agents" \
    -H "Content-Type: application/json" \
    -H "x-goog-api-key: $GEMINI_API_KEY" \
    -d '{
        "id": "issue-resolver",
        "base_agent": "antigravity-preview-09-2026",
        "system_instruction": "You resolve GitHub issues. Clone the repo, find the bug, write the fix, run the tests, and open a PR.",
        "base_environment": {
            "type": "remote",
            "sources": [
                {
                    "type": "repository",
                    "source": "https://github.com/my-org/backend",
                    "target": "/workspace/repo"
                }
            ],
            "network": {
                "allowlist": [
                    {
                        "domain": "api.github.com",
                        "transform": {
                            "Authorization": "Basic YOUR_BASE64_TOKEN"
                        }
                    },
                    {"domain": "pypi.org"}
                ]
            }
        }
    }'
  ```

  {% /tab %}

  {% tab label="Java" %}
  ```java
  import com.google.genai.Client;
  import com.google.genai.types.HttpOptions;
  import com.google.genai.gaos.models.agents.Agent;
  import com.google.genai.gaos.models.agents.BaseEnvironment;
  import com.google.genai.gaos.models.interactions.Allowlist;
  import com.google.genai.gaos.models.interactions.AllowlistEntry;
  import com.google.genai.gaos.models.interactions.Environment;
  import com.google.genai.gaos.models.interactions.EnvironmentNetworkEgressAllowlist;
  import com.google.genai.gaos.models.interactions.Network;
  import com.google.genai.gaos.models.interactions.Source;
  import com.google.genai.gaos.models.interactions.SourceType;
  import com.google.genai.gaos.models.interactions.Transform;
  import java.util.List;
  import java.util.Map;
  
  Client client = Client.builder().httpOptions(HttpOptions.builder().apiVersion("v1beta").build()).build();
  
  Environment env = Environment.builder()
      .sources(List.of(
          Source.builder()
              .type(SourceType.REPOSITORY)
              .source("https://github.com/my-org/backend")
              .target("/workspace/repo")
              .build()
      ))
      .network(Network.of(
          EnvironmentNetworkEgressAllowlist.builder()
              .allowlist(Allowlist.of(List.of(
                  AllowlistEntry.builder()
                      .domain("api.github.com")
                      .transform(Transform.of(Map.of(
                          "Authorization", "Basic YOUR_BASE64_TOKEN"
                      )))
                      .build(),
                  AllowlistEntry.builder().domain("pypi.org").build()
              )))
              .build()
      ))
      .build();
  
  Agent agentParams = Agent.builder()
      .id("issue-resolver")
      .baseAgent("antigravity-preview-09-2026")
      .systemInstruction("You resolve GitHub issues. Clone the repo, find the bug, write the fix, run the tests, and open a PR.")
      .baseEnvironment(BaseEnvironment.of(env))
      .build();
  
  Agent agent = client.agents.create(agentParams).agent().get();
  System.out.println("Created issue-resolver agent successfully: " + agent.id().orElse(""));
  ```

  {% /tab %}

  {% tab label="Go" %}
  ```go
  package main
  
  import (
      "context"
      "fmt"
      "log"
  
      "google.golang.org/genai"
      "google.golang.org/genai/interactions/models/agents"
      "google.golang.org/genai/interactions/models/interactions"
      "google.golang.org/genai/interactions/models/operations"
  )
  
  func main() {
      ctx := context.Background()
      client, err := genai.NewClient(ctx, &genai.ClientConfig{HTTPOptions: genai.HTTPOptions{APIVersion: "v1beta"}})
      if err != nil {
          log.Fatal(err)
      }
  
      env := interactions.Environment{
          Sources: []interactions.Source{
              {
                  Type:   interactions.SourceTypeRepository.ToPointer(),
                  Source: genai.Ptr("https://github.com/my-org/backend"),
                  Target: genai.Ptr("/workspace/repo"),
              },
          },
          Network: genai.Ptr(interactions.NewNetwork(interactions.EnvironmentNetworkEgressAllowlist{
              Allowlist: genai.Ptr(interactions.NewAllowlist([]interactions.AllowlistEntry{
                  {
                      Domain: "api.github.com",
                      Transform: genai.Ptr(interactions.NewTransform(map[string]string{
                          "Authorization": "Basic YOUR_BASE64_TOKEN",
                      })),
                  },
                  {
                      Domain: "pypi.org",
                  },
              })),
          })),
      }
  
      res, err := client.Agents.Create(ctx, operations.CreateAgentRequest{
          Body: agents.Agent{
              ID:                genai.Ptr("issue-resolver"),
              BaseAgent:         genai.Ptr("antigravity-preview-09-2026"),
              SystemInstruction: genai.Ptr("You resolve GitHub issues. Clone the repo, find the bug, write the fix, run the tests, and open a PR."),
              BaseEnvironment:   genai.Ptr(agents.NewBaseEnvironment(env)),
          },
      })
      if err != nil {
          log.Fatal(err)
      }
  
      fmt.Printf("Created issue-resolver agent successfully: %s\n", *res.Agent.ID)
  }
  ```

  {% /tab %}

{% /tabs %}

## Invoke the agent

Call your managed agent with your agent ID by creating a new interaction. Each invocation forks the base environment, so every run starts clean.

{% tabs %}
  {% tab filename="sample.py" label="Python" %}
  ```python
  result = client.interactions.create(
      agent="data-analyst",
      input="Analyze Q1 revenue data from /workspace/templates/sample.csv and create a slide deck.",
      environment="remote",
  )
  
  print(result.output_text)
  ```

  {% /tab %}

  {% tab filename="sample.js" label="JavaScript" %}
  ```javascript
  const result = await client.interactions.create({
      agent: "data-analyst",
      input: "Analyze Q1 revenue data from /workspace/templates/sample.csv and create a slide deck.",
      environment: "remote",
  }, { timeout: 300000 });
  
  console.log(result.output_text);
  ```

  {% /tab %}

  {% tab filename="sample.sh" label="REST" %}
  ```shell
  curl -X POST "https://generativelanguage.googleapis.com/v1beta/interactions" \
    -H "Content-Type: application/json" \
    -H "x-goog-api-key: $GEMINI_API_KEY" \
    -d '{
        "agent": "data-analyst",
        "input": "Analyze Q1 revenue data from /workspace/templates/sample.csv and create a slide deck.",
        "environment": "remote"
    }'
  ```

  For multi-turn conversations and streaming, see the [Quickstart](/docs/managed-agents-quickstart). The same `previous_interaction_id` and `environment` patterns apply to managed agents.

  Managed agents also support background execution and cancellation. For details and code examples, see [Antigravity Agent: Background execution](/docs/antigravity-agent#background-execution).

  {% /tab %}

  {% tab label="Java" %}
  ```java
  import com.google.genai.Client;
  import com.google.genai.types.HttpOptions;
  import com.google.genai.gaos.models.interactions.AgentOption;
  import com.google.genai.gaos.models.interactions.CreateAgentInteraction;
  import com.google.genai.gaos.models.interactions.CreateAgentInteractionEnvironment;
  import com.google.genai.gaos.models.interactions.Interaction;
  import com.google.genai.gaos.models.interactions.InteractionsInput;
  import com.google.genai.gaos.models.operations.CreateInteractionRequestBody;
  
  Client client = Client.builder().httpOptions(HttpOptions.builder().apiVersion("v1beta").build()).build();
  
  CreateAgentInteraction params = CreateAgentInteraction.builder()
      .agent(AgentOption.of("data-analyst"))
      .input(InteractionsInput.of("Analyze Q1 revenue data from /workspace/templates/sample.csv and create a slide deck."))
      .environment(CreateAgentInteractionEnvironment.of("remote"))
      .build();
  
  Interaction result = client.interactions.create(CreateInteractionRequestBody.of(params)).interaction().get();
  System.out.println(result.outputText().orElse(""));
  ```

  {% /tab %}

  {% tab label="Go" %}
  ```go
  package main
  
  import (
      "context"
      "fmt"
      "log"
  
      "google.golang.org/genai"
      "google.golang.org/genai/interactions/models/interactions"
      "google.golang.org/genai/interactions/models/operations"
  )
  
  func main() {
      ctx := context.Background()
      client, err := genai.NewClient(ctx, &genai.ClientConfig{HTTPOptions: genai.HTTPOptions{APIVersion: "v1beta"}})
      if err != nil {
          log.Fatal(err)
      }
  
      res, err := client.Interactions.Create(ctx, operations.CreateInteractionRequest{
          Body: operations.NewCreateInteractionRequestBody(interactions.CreateAgentInteraction{
              Agent:       interactions.AgentOption("data-analyst"),
              Input:       interactions.NewInteractionsInput("Analyze Q1 revenue data from /workspace/templates/sample.csv and create a slide deck."),
              Environment: genai.Ptr(interactions.NewCreateAgentInteractionEnvironment("remote")),
          }),
      })
      if err != nil {
          log.Fatal(err)
      }
      if res.Interaction.OutputText != nil {
          fmt.Println(*res.Interaction.OutputText)
      }
  }
  ```

  {% /tab %}

{% /tabs %}

## Overriding configuration at invocation

You can override the agent's default `system_instruction`, `tools`, and
`environment` network configuration when creating an interaction. This
lets you modify the agent's behavior, capabilities, or credentials for a
specific run without changing the stored agent definition.

### Override system instruction and tools

{% tabs %}
  {% tab filename="sample.py" label="Python" %}
  ```python
  result = client.interactions.create(
      agent="data-analyst",
      input="Analyze Q1 revenue data, but do not create a slide deck. Just output a summary table.",
      system_instruction="You are a data analyst. Focus ONLY on summary tables. Ignore default instructions about slides.",
      tools=[{"type": "code_execution"}], # Override to only use code execution
      environment="remote",
  )
  print(result.output_text)
  ```

  {% /tab %}

  {% tab filename="sample.js" label="JavaScript" %}
  ```javascript
  const result = await client.interactions.create({
      agent: "data-analyst",
      input: "Analyze Q1 revenue data, but do not create a slide deck. Just output a summary table.",
      system_instruction: "You are a data analyst. Focus ONLY on summary tables. Ignore default instructions about slides.",
      tools: [{ type: "code_execution" }], // Override to only use code execution
      environment: "remote",
  }, { timeout: 300000 });
  
  console.log(result.output_text);
  ```

  {% /tab %}

  {% tab filename="sample.sh" label="REST" %}
  ```shell
  curl -X POST "https://generativelanguage.googleapis.com/v1beta/interactions" \
    -H "Content-Type: application/json" \
    -H "x-goog-api-key: $GEMINI_API_KEY" \
    -d '{
        "agent": "data-analyst",
        "input": "Analyze Q1 revenue data, but do not create a slide deck. Just output a summary table.",
        "system_instruction": "You are a data analyst. Focus ONLY on summary tables. Ignore default instructions about slides.",
        "tools": [{"type": "code_execution"}],
        "environment": "remote"
    }'
  ```

  {% /tab %}

  {% tab label="Java" %}
  ```java
  import com.google.genai.Client;
  import com.google.genai.types.HttpOptions;
  import com.google.genai.gaos.models.interactions.AgentOption;
  import com.google.genai.gaos.models.interactions.CodeExecution;
  import com.google.genai.gaos.models.interactions.CreateAgentInteraction;
  import com.google.genai.gaos.models.interactions.CreateAgentInteractionEnvironment;
  import com.google.genai.gaos.models.interactions.Interaction;
  import com.google.genai.gaos.models.interactions.InteractionsInput;
  import com.google.genai.gaos.models.operations.CreateInteractionRequestBody;
  import java.util.List;
  
  Client client = Client.builder().httpOptions(HttpOptions.builder().apiVersion("v1beta").build()).build();
  
  CreateAgentInteraction params = CreateAgentInteraction.builder()
      .agent(AgentOption.of("data-analyst"))
      .input(InteractionsInput.of("Analyze Q1 revenue data, but do not create a slide deck. Just output a summary table."))
      .systemInstruction("You are a data analyst. Focus ONLY on summary tables. Ignore default instructions about slides.")
      .tools(List.of(CodeExecution.builder().build())) // Override to only use code execution
      .environment(CreateAgentInteractionEnvironment.of("remote"))
      .build();
  
  Interaction result = client.interactions.create(CreateInteractionRequestBody.of(params)).interaction().get();
  System.out.println(result.outputText().orElse(""));
  ```

  {% /tab %}

  {% tab label="Go" %}
  ```go
  package main
  
  import (
      "context"
      "fmt"
      "log"
  
      "google.golang.org/genai"
      "google.golang.org/genai/interactions/models/interactions"
      "google.golang.org/genai/interactions/models/operations"
  )
  
  func main() {
      ctx := context.Background()
      client, err := genai.NewClient(ctx, &genai.ClientConfig{HTTPOptions: genai.HTTPOptions{APIVersion: "v1beta"}})
      if err != nil {
          log.Fatal(err)
      }
  
      res, err := client.Interactions.Create(ctx, operations.CreateInteractionRequest{
          Body: operations.NewCreateInteractionRequestBody(interactions.CreateAgentInteraction{
              Agent:             interactions.AgentOption("data-analyst"),
              Input:             interactions.NewInteractionsInput("Analyze Q1 revenue data, but do not create a slide deck. Just output a summary table."),
              SystemInstruction: genai.Ptr("You are a data analyst. Focus ONLY on summary tables. Ignore default instructions about slides."),
              Tools:             []interactions.Tool{interactions.NewTool(interactions.CodeExecution{})}, // Override to only use code execution
              Environment:       genai.Ptr(interactions.NewCreateAgentInteractionEnvironment("remote")),
          }),
      })
      if err != nil {
          log.Fatal(err)
      }
      if res.Interaction.OutputText != nil {
          fmt.Println(*res.Interaction.OutputText)
      }
  }
  ```

  {% /tab %}

{% /tabs %}

### Override network configuration (refresh credentials)  {% id="override-network" %}

If your managed agent has network credentials baked into its `base_environment`,
you can override them at invocation time to refresh expired tokens or rotate API
keys. Pass an `environment` object with a new `network` configuration. The new
network rules fully replace the previous ones for that interaction. The base
environment's sources (files, repositories) are preserved.

If the `base_environment` references a stored
[credential](/docs/agent-credentials) instead of an inline token, you don't need
to override anything. Rotate the credential with a `PATCH` and every agent
referencing it picks up the new secret on the next run.

{% tabs %}
  {% tab filename="sample.py" label="Python" %}
  ```python
  # Invoke the agent with a fresh token, overriding the base_environment credentials
  result = client.interactions.create(
      agent="issue-resolver",
      input="Fix issue #42 and open a PR.",
      environment={
          "type": "remote",
          "network": {
              "allowlist": [
                  {
                      "domain": "api.github.com",
                      "transform": {
                          "Authorization": "Bearer ghp_REFRESHED_TOKEN"
                      },
                  },
                  {"domain": "pypi.org"},
              ]
          },
      },
  )
  
  print(result.output_text)
  ```

  {% /tab %}

  {% tab filename="sample.js" label="JavaScript" %}
  ```javascript
  // Invoke the agent with a fresh token, overriding the base_environment credentials
  const result = await client.interactions.create({
      agent: "issue-resolver",
      input: "Fix issue #42 and open a PR.",
      environment: {
          type: "remote",
          network: {
              allowlist: [
                  {
                      domain: "api.github.com",
                      transform: {
                          "Authorization": "Bearer ghp_REFRESHED_TOKEN"
                      },
                  },
                  { domain: "pypi.org" },
              ]
          },
      },
  }, { timeout: 300000 });
  
  console.log(result.output_text);
  ```

  {% /tab %}

  {% tab filename="sample.sh" label="REST" %}
  ```shell
  curl -X POST "https://generativelanguage.googleapis.com/v1beta/interactions" \
    -H "Content-Type: application/json" \
    -H "x-goog-api-key: $GEMINI_API_KEY" \
    -d '{
        "agent": "issue-resolver",
        "input": "Fix issue #42 and open a PR.",
        "environment": {
            "type": "remote",
            "network": {
                "allowlist": [
                    {
                        "domain": "api.github.com",
                        "transform": {
                            "Authorization": "Bearer ghp_REFRESHED_TOKEN"
                        }
                    },
                    {"domain": "pypi.org"}
                ]
            }
        }
    }'
  ```

  {% /tab %}

  {% tab label="Java" %}
  ```java
  import com.google.genai.Client;
  import com.google.genai.types.HttpOptions;
  import com.google.genai.gaos.models.interactions.AgentOption;
  import com.google.genai.gaos.models.interactions.Allowlist;
  import com.google.genai.gaos.models.interactions.AllowlistEntry;
  import com.google.genai.gaos.models.interactions.CreateAgentInteraction;
  import com.google.genai.gaos.models.interactions.CreateAgentInteractionEnvironment;
  import com.google.genai.gaos.models.interactions.Environment;
  import com.google.genai.gaos.models.interactions.EnvironmentNetworkEgressAllowlist;
  import com.google.genai.gaos.models.interactions.Interaction;
  import com.google.genai.gaos.models.interactions.InteractionsInput;
  import com.google.genai.gaos.models.interactions.Network;
  import com.google.genai.gaos.models.interactions.Transform;
  import com.google.genai.gaos.models.operations.CreateInteractionRequestBody;
  import java.util.List;
  import java.util.Map;
  
  Client client = Client.builder().httpOptions(HttpOptions.builder().apiVersion("v1beta").build()).build();
  
  // Invoke the agent with a fresh token, overriding the base_environment credentials
  Environment env = Environment.builder()
      .network(Network.of(
          EnvironmentNetworkEgressAllowlist.builder()
              .allowlist(Allowlist.of(List.of(
                  AllowlistEntry.builder()
                      .domain("api.github.com")
                      .transform(Transform.of(Map.of(
                          "Authorization", "Bearer ghp_REFRESHED_TOKEN"
                      )))
                      .build(),
                  AllowlistEntry.builder().domain("pypi.org").build()
              )))
              .build()
      ))
      .build();
  
  CreateAgentInteraction params = CreateAgentInteraction.builder()
      .agent(AgentOption.of("issue-resolver"))
      .input(InteractionsInput.of("Fix issue #42 and open a PR."))
      .environment(CreateAgentInteractionEnvironment.of(env))
      .build();
  
  Interaction result = client.interactions.create(CreateInteractionRequestBody.of(params)).interaction().get();
  System.out.println(result.outputText().orElse(""));
  ```

  {% /tab %}

  {% tab label="Go" %}
  ```go
  package main
  
  import (
      "context"
      "fmt"
      "log"
  
      "google.golang.org/genai"
      "google.golang.org/genai/interactions/models/interactions"
      "google.golang.org/genai/interactions/models/operations"
  )
  
  func main() {
      ctx := context.Background()
      client, err := genai.NewClient(ctx, &genai.ClientConfig{HTTPOptions: genai.HTTPOptions{APIVersion: "v1beta"}})
      if err != nil {
          log.Fatal(err)
      }
  
      // Invoke the agent with a fresh token, overriding the base_environment credentials
      env := interactions.Environment{
          Network: genai.Ptr(interactions.NewNetwork(interactions.EnvironmentNetworkEgressAllowlist{
              Allowlist: genai.Ptr(interactions.NewAllowlist([]interactions.AllowlistEntry{
                  {
                      Domain: "api.github.com",
                      Transform: genai.Ptr(interactions.NewTransform(map[string]string{
                          "Authorization": "Bearer ghp_REFRESHED_TOKEN",
                      })),
                  },
                  {
                      Domain: "pypi.org",
                  },
              })),
          })),
      }
  
      res, err := client.Interactions.Create(ctx, operations.CreateInteractionRequest{
          Body: operations.NewCreateInteractionRequestBody(interactions.CreateAgentInteraction{
              Agent:       interactions.AgentOption("issue-resolver"),
              Input:       interactions.NewInteractionsInput("Fix issue #42 and open a PR."),
              Environment: genai.Ptr(interactions.NewCreateAgentInteractionEnvironment(env)),
          }),
      })
      if err != nil {
          log.Fatal(err)
      }
      if res.Interaction.OutputText != nil {
          fmt.Println(*res.Interaction.OutputText)
      }
  }
  ```

  {% /tab %}

{% /tabs %}

## Manage agents

You can list, get, and delete agents.

### List agents

{% tabs %}
  {% tab filename="sample.py" label="Python" %}
  ```python
  agents = client.agents.list()
  for a in agents.agents:
      print(f"{a.id}: {a.description}")
  ```

  {% /tab %}

  {% tab filename="sample.js" label="JavaScript" %}
  ```javascript
  const agents = await client.agents.list();
  if (agents.agents) {
      for (const a of agents.agents) {
          console.log(`${a.id}: ${a.description}`);
      }
  }
  ```

  {% /tab %}

  {% tab filename="sample.sh" label="REST" %}
  ```shell
  curl -X GET "https://generativelanguage.googleapis.com/v1beta/agents" \
    -H "x-goog-api-key: $GEMINI_API_KEY"
  ```

  {% /tab %}

  {% tab label="Java" %}
  ```java
  import com.google.genai.Client;
  import com.google.genai.types.HttpOptions;
  import com.google.genai.gaos.models.agents.Agent;
  import java.util.List;
  
  Client client = Client.builder().httpOptions(HttpOptions.builder().apiVersion("v1beta").build()).build();
  
  List<Agent> agents = client.agents.listDirect().agentListResponse().get().agents().orElse(List.of());
  for (Agent a : agents) {
      System.out.println(a.id().orElse("") + ": " + a.description().orElse(""));
  }
  ```

  {% /tab %}

  {% tab label="Go" %}
  ```go
  package main
  
  import (
      "context"
      "fmt"
      "log"
  
      "google.golang.org/genai"
      "google.golang.org/genai/interactions/models/operations"
  )
  
  func main() {
      ctx := context.Background()
      client, err := genai.NewClient(ctx, &genai.ClientConfig{HTTPOptions: genai.HTTPOptions{APIVersion: "v1beta"}})
      if err != nil {
          log.Fatal(err)
      }
  
      res, err := client.Agents.List(ctx, operations.ListAgentsRequest{})
      if err != nil {
          log.Fatal(err)
      }
  
      if res.AgentListResponse != nil {
          for _, a := range res.AgentListResponse.Agents {
              fmt.Printf("%s: %v\n", *a.ID, a.Description)
          }
      }
  }
  ```

  {% /tab %}

{% /tabs %}

### Get an agent

{% tabs %}
  {% tab filename="sample.py" label="Python" %}
  ```python
  agent = client.agents.get(id="data-analyst")
  print(agent)
  ```

  {% /tab %}

  {% tab filename="sample.js" label="JavaScript" %}
  ```javascript
  const agent = await client.agents.get("data-analyst");
  console.log(agent);
  ```

  {% /tab %}

  {% tab filename="sample.sh" label="REST" %}
  ```shell
  curl -X GET "https://generativelanguage.googleapis.com/v1beta/agents/data-analyst" \
    -H "x-goog-api-key: $GEMINI_API_KEY"
  ```

  {% /tab %}

  {% tab label="Java" %}
  ```java
  import com.google.genai.Client;
  import com.google.genai.types.HttpOptions;
  import com.google.genai.gaos.models.agents.Agent;
  
  Client client = Client.builder().httpOptions(HttpOptions.builder().apiVersion("v1beta").build()).build();
  
  Agent agent = client.agents.get("data-analyst").agent().get();
  System.out.println(agent);
  ```

  {% /tab %}

  {% tab label="Go" %}
  ```go
  package main
  
  import (
      "context"
      "fmt"
      "log"
  
      "google.golang.org/genai"
      "google.golang.org/genai/interactions/models/operations"
  )
  
  func main() {
      ctx := context.Background()
      client, err := genai.NewClient(ctx, &genai.ClientConfig{HTTPOptions: genai.HTTPOptions{APIVersion: "v1beta"}})
      if err != nil {
          log.Fatal(err)
      }
  
      res, err := client.Agents.Get(ctx, operations.GetAgentRequest{
          ID: "data-analyst",
      })
      if err != nil {
          log.Fatal(err)
      }
  
      fmt.Printf("%+v\n", res.Agent)
  }
  ```

  {% /tab %}

{% /tabs %}

### Delete an agent

Deleting removes the configuration. Existing environments and interactions created by the agent are not affected.

{% tabs %}
  {% tab filename="sample.py" label="Python" %}
  ```python
  client.agents.delete(id="data-analyst")
  ```

  {% /tab %}

  {% tab filename="sample.js" label="JavaScript" %}
  ```javascript
  await client.agents.delete("data-analyst");
  ```

  {% /tab %}

  {% tab filename="sample.sh" label="REST" %}
  ```shell
  curl -X DELETE "https://generativelanguage.googleapis.com/v1beta/agents/data-analyst" \
    -H "x-goog-api-key: $GEMINI_API_KEY"
  ```

  {% /tab %}

  {% tab label="Java" %}
  ```java
  import com.google.genai.Client;
  import com.google.genai.types.HttpOptions;
  
  Client client = Client.builder().httpOptions(HttpOptions.builder().apiVersion("v1beta").build()).build();
  
  client.agents.delete("data-analyst");
  ```

  {% /tab %}

  {% tab label="Go" %}
  ```go
  package main
  
  import (
      "context"
      "log"
  
      "google.golang.org/genai"
      "google.golang.org/genai/interactions/models/operations"
  )
  
  func main() {
      ctx := context.Background()
      client, err := genai.NewClient(ctx, &genai.ClientConfig{HTTPOptions: genai.HTTPOptions{APIVersion: "v1beta"}})
      if err != nil {
          log.Fatal(err)
      }
  
      _, err = client.Agents.Delete(ctx, operations.DeleteAgentRequest{
          ID: "data-analyst",
      })
      if err != nil {
          log.Fatal(err)
      }
  }
  ```

  {% /tab %}

{% /tabs %}

## Agent definition reference

| Field | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `id` | string | Yes | Unique agent identifier within the Google Cloud project. Used to invoke the agent. Must not use reserved prefixes. See [Agent ID restrictions](/docs/custom-agents#agent-id-restrictions). |
| `description` | string | No | Human-readable description of the agent. |
| `base_agent` | string | Yes | Base agent ID (e.g., `antigravity-preview-09-2026`). |
| `agent_config` | object | No | Configuration for the base agent, including model selection (`{"type": "antigravity", "model": "gemini-4-hydrogen"}`). Defaults to `gemini-4-hydrogen` if omitted. Cannot be overridden at interaction time for named agents. |
| `system_instruction` | string | No | System prompt defining behavior and persona. |
| `tools` | array | No | Tools the agent can use. If omitted, defaults to `code_execution`, `google_search`, and `url_context`. Supported tools include `code_execution`, `google_search`, `url_context`, `mcp_server`, and custom `function` definitions. |
| `base_environment` | string or object | No | `"remote"`, an `environment_id`, or a config object with `sources` and `network`. See Environments. |

### Agent ID restrictions  {% id="agent-id-restrictions" %}

When creating a managed agent, the `id` you specify must follow these rules:

* It must be unique to your Google Cloud project.
* It must **not** start with any of the following reserved prefixes (case-insensitive), otherwise creation will fail:  *   `antigravity-`
  *   `veo-`
  *   `omni-`
  *   `lyria-`
  *   `imagen-`
  *   `gemma-`
  *   `gemini-`
  *   `google-`
  *   `youtube-`
  *   `android-`
  *   `chrome-`
  *   `pixel-`
  *   `waze-`
  *   `fitbit-`
  *   `nest-`
  *   `kaggle-`

## Iteration workflow  {% id="iteration-workflow" %}

1. **Prototype** with the base Antigravity agent. Pass system instruction and environment sources inline. Test instructions, skills, and environment setup interactively.
2. **Stabilize** the environment. Install packages, mount sources, verify everything works.
3. **Persist** as a managed agent by creating a new agent, either from sources or by forking the environment.
4. **Update** the agent definition. Change system instruction, swap skills, or add sources. The next invocation picks up the new configuration.

## Limitations  {% id="limitations" %}

* **Preview status**: Managed agents are in preview. Features and schemas may change.
*   **Base agent and models**: Only `antigravity-preview-09-2026` is supported
  as `base_agent`. Supported model options in `agent_config` are
  `gemini-4-hydrogen` (default), `gemini-4-carbon`, `gemini-4-argon`,
  `gemini-3.8-flash`, `gemini-3.6-flash`, and
  `gemini-3.5-flash-lite`. For named agents, the model cannot be overridden at
  interaction time.
* **No versioning**: Agent versioning and rollback are not yet available.
* **No subagent nesting**: Subagent delegation is not yet supported.
* You can have up to 1000 managed agents.

## What's next  {% id="whats-next" %}

* [Agents Overview](/docs/agents): Learn about the core concepts of managed agents.
* [Quickstart](/docs/managed-agents-quickstart): Start building with multi-turn conversations and streaming.
* [Antigravity Agent](/docs/antigravity-agent): Explore capabilities, tools, and pricing for the default agent.
* [Agent Environments](/docs/agent-environment): Configure sandboxes, sources, and networking.
* [Managed Agents API on Agent Platform](https://docs.cloud.google.com/gemini-enterprise-agent-platform/build/managed-agents): For creating agents with built-in organizational governance.