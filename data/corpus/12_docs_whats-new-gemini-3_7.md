> ## AI Agent Context
> Get the complete documentation index at: https://aistudio.google.com/llms.txt
> Use this file to discover all available pages.
> For the full documentation in a single file, fetch: https://aistudio.google.com/llms-full.txt

# What's new in Gemini 3.7 Flash

{% callout type="caution" %}
   **Deprecated:** Gemini 3.7 Flash
  (`gemini-3.7-flash`) is deprecated and has been replaced by
  [Gemini 3.8 Flash (`gemini-3.8-flash`)](/docs/whats-new-gemini-3.8). It is no longer
  available to select in Google AI Studio, and API requests to
  `gemini-3.7-flash` are automatically routed to `gemini-3.8-flash`.
  Update your model string to `gemini-3.8-flash` and review the
  [Gemini 3.8 Flash guide](/docs/whats-new-gemini-3.8). 

{% /callout %}

Gemini 3.7 Flash (`gemini-3.7-flash`) is a previous-generation Flash model in
the Gemini 3 series, now deprecated and automatically routed to
[Gemini 3.8 Flash](/docs/whats-new-gemini-3.8).

This guide is preserved for reference and documents the capabilities and changes
introduced in Gemini 3.7 Flash.

## Model overview  {% id="new-model" %}

| Model | Model ID | Default thinking level | Description |
| :--- | :--- | :---: | :--- |
| Gemini 3.7 Flash (Deprecated) | `gemini-3.7-flash` | `medium` | Previous-generation Flash model built for coding, agentic workflows, and multi-step execution. Replaced by [Gemini 3.8 Flash](/docs/whats-new-gemini-3.8). |

Gemini 3.7 Flash supports a 1M token context window, 64k max output tokens, tunable thinking levels (`low`, `medium`, `high`), and the same suite of built-in tools as 3.6 Flash.

For complete specs, see the
[Gemini 3.7 Flash model page](/docs/models/gemini-3.7-flash).

## Quickstart  {% id="quickstart" %}

{% tabs %}
  {% tab label="Python" %}
  ```python
  from google import genai
  
  client = genai.Client()
  
  interaction = client.interactions.create(
      model="gemini-3.7-flash",
      input="Write a responsive navigation component in React with smooth animations and dark mode toggle."
  )
  
  print(interaction.output_text)
  ```

  {% /tab %}

  {% tab label="JavaScript" %}
  ```javascript
  import { GoogleGenAI } from "@google/genai";
  
  const client = new GoogleGenAI({});
  
  const interaction = await client.interactions.create({
    model: "gemini-3.7-flash",
    input: "Write a responsive navigation component in React with smooth animations and dark mode toggle.",
  });
  
  console.log(interaction.output_text);
  ```

  {% /tab %}

  {% tab label="Java" %}
  ```java
  import com.google.genai.Client;
      import com.google.genai.gaos.models.interactions.CreateModelInteraction;
      import com.google.genai.gaos.models.interactions.Interaction;
      import com.google.genai.gaos.models.interactions.InteractionsInput;
      import com.google.genai.gaos.models.interactions.Model;
      import com.google.genai.gaos.models.operations.CreateInteractionRequestBody;
  
      Client client = new Client();
      CreateModelInteraction req = CreateModelInteraction.builder()
          .model(Model.of("gemini-3.7-flash"))
          .input(InteractionsInput.of("Write a responsive navigation component in React with smooth animations and dark mode toggle."))
          .build();
      Interaction interaction =
          client.interactions.create(CreateInteractionRequestBody.of(req)).interaction().get();
      System.out.println(interaction.outputText().orElse(""));
  ```

  {% /tab %}

  {% tab label="REST" %}
  ```bash
  curl "https://generativelanguage.googleapis.com/v1beta/interactions" \
    -H "x-goog-api-key: $GEMINI_API_KEY" \
    -H 'Content-Type: application/json' \
    -X POST \
    -d '{
      "model": "gemini-3.7-flash",
      "input": "Write a responsive navigation component in React with smooth animations and dark mode toggle."
    }'
  ```

  {% /tab %}

{% /tabs %}

## What's new in Gemini 3.7 Flash  {% id="whats-new-gemini-3-7-flash" %}

* **Coding and agentic tasks:** Significantly higher quality on real-world software engineering and agentic benchmarks, improving issue resolution and reducing failed agent loops.
* **Web development and stronger design parity:** Generates higher-fidelity desktop and web application code directly from design mocks, with strong gains in design adherence and in auditing existing codebases against mocks to verify 1:1 design parity.

## Understanding reasoning levels  {% id="understanding-reasoning-levels" %}

Gemini 3.7 Flash gives developers flexible control over latency and intelligence by adjusting the model's thinking level:

* **Low thinking effort**: Reduces time-to-answer for latency-critical tasks like incident response pipelines, real-time chat, writing drafts, and fast data analysis.
* **Medium (default):** Best quality for most tasks. Recommended for complex code and agentic use cases, with higher first-pass accuracy.
* **High thinking effort**: Maximizes the model's ability to think and use tools. Best for complex reasoning, hard math, and difficult coding and agent tasks. Allows extended thoughts and function calls, with higher token consumption and cost.

To configure thinking levels in Gemini 3.7 Flash:

```python
from google import genai

client = genai.Client()

interaction = client.interactions.create(
    model="gemini-3.7-flash",
    input="Analyze this payment processing pipeline for race conditions during retry attempts and rewrite the transaction locks safely.",
    generation_config={
        "thinking_level": "medium"  # Balanced reasoning effort for complex tasks
    }
)

print(interaction.output_text)
```

For multi-language code examples (JavaScript, Java, Go, REST) and in-depth reasoning concepts, see [Understanding reasoning levels in Gemini 3.8 Flash](/docs/whats-new-gemini-3.8#understanding-reasoning-levels).

## Antigravity agent support  {% id="updated-antigravity-agent" %}

Gemini 3.7 Flash introduced support for powering the [Antigravity agent](/docs/antigravity-agent) in Gemini Managed Agents and the [Google Antigravity SDK](https://antigravity.google/docs/sdk/overview/).

For current code samples and the latest default agent configuration, see the [Antigravity agent guide](/docs/antigravity-agent) and the [Gemini 3.8 Flash guide](/docs/whats-new-gemini-3.8#updated-antigravity-agent).

## Other models  {% id="other-models" %}

*   [Latest Gemini models](/docs/latest-model)
*   [Gemini 4 Hydrogen](/docs/whats-new-gemini-4-hydrogen)
*   [Gemini 4 Carbon](/docs/whats-new-gemini-4-carbon)
*   [Gemini 4 Argon](/docs/whats-new-gemini-4-argon)
*   [Gemini 3.8 Flash](/docs/whats-new-gemini-3.8)
*   [Gemini 3.6 Flash and 3.5 Flash-Lite](/docs/whats-new-gemini-3.6)
*   [See all models](/docs/models)

## What's next  {% id="whats-next" %}

* Review API specs on the [Models Overview](/docs/models).
* Explore multi-agent orchestration in the [Interactions API Guide](/docs/interactions-overview).
* Test and refine prompts in [Google AI Studio](https://aistudio.google.com/).