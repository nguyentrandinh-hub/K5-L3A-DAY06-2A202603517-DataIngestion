> ## AI Agent Context
> Get the complete documentation index at: https://aistudio.google.com/llms.txt
> Use this file to discover all available pages.
> For the full documentation in a single file, fetch: https://aistudio.google.com/llms-full.txt

{% two-column-layout %}
  {% left-column %}
# Welcome to Gemini API  {% class="h0" %}

  Go from a quick prompt to production apps and agents with the Gemini API.
    Tackle complex coding and multimodal reasoning with Gemini, score calibrated
    decisions with the Decisions API, or hand multi-step work to a managed agent.
    Stream voice and video with the Live API, or generate images with Nano Banana,
    video with Gemini Omni, and music with Lyria.

  {% button href="/docs/get-started" size="large" variant="ais" %}Get Started{% /button %} {% button href="https://aistudio.google.com/apikey" size="large" variant="primary" %}Create API Key{% /button %}

  {% /left-column %}

  {% right-column %}
  {% tabs %}
  {% tab label="Agents" %}
  ```bash
  # Set up your coding agent with these tools
  
  # Search live docs with the MCP server
  npx add-mcp "https://gemini-api-docs-mcp.dev"
  
  # Add skills for current SDK syntax and rules
  npx skills add google-gemini/gemini-skills --skill gemini-api-dev
  
  # In Antigravity, install both with one plugin
  agy plugin install https://github.com/google-gemini/gemini-skills
  
  # Let your agent call the API from the terminal
  curl -fsSL https://raw.githubusercontent.com/google-gemini/gemini-api-cli/main/scripts/install.sh | bash
  ```

  {% /tab %}

  {% tab filename="main.py" label="Python" %}
  ```python
  from google import genai
  
  client = genai.Client()
  
  interaction = client.interactions.create(
      model="gemini-4-carbon",
      input="Explain how AI works in a few words"
  )
  
  print(interaction.output_text)
  ```

  {% /tab %}

  {% tab filename="index.js" label="JavaScript" %}
  ```javascript
  import { GoogleGenAI } from "@google/genai";
  
  const ai = new GoogleGenAI({});
  
  const interaction = await ai.interactions.create({
    model: "gemini-4-carbon",
    input: "Explain how AI works in a few words",
  });
  
  console.log(interaction.output_text);
  ```

  {% /tab %}

  {% tab label="REST" %}
  ```bash
  curl -X POST "https://generativelanguage.googleapis.com/v1beta/interactions" \
    -H "x-goog-api-key: $GEMINI_API_KEY" \
    -H 'Content-Type: application/json' \
    -d '{
      "model": "gemini-4-carbon",
      "input": "Explain how AI works in a few words"
    }'
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
  
  CreateModelInteraction params =
      CreateModelInteraction.builder()
          .model(Model.of("gemini-4-carbon"))
          .input(InteractionsInput.of("Explain how AI works in a few words"))
          .build();
  
  Interaction interaction =
      client.interactions.create(CreateInteractionRequestBody.of(params)).interaction().get();
  
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
      client, err := genai.NewClient(ctx, nil)
      if err != nil {
          log.Fatal(err)
      }
  
      res, err := client.Interactions.Create(ctx, operations.CreateInteractionRequest{
          Body: operations.NewCreateInteractionRequestBody(interactions.CreateModelInteraction{
              Model: interactions.Model("gemini-4-carbon"),
              Input: interactions.NewInteractionsInput("Explain how AI works in a few words"),
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

  {% tab label="CLI" %}
  ```bash
  gemini-api generate "Explain how AI works in a few words" -m gemini-4-carbon
  ```

  {% /tab %}

  {% /tabs %}

  {% /right-column %}

{% /two-column-layout %}

## Meet the models  {% class="hide-from-toc" id="meet-the-models" %}

{% card-grid columns="3" %}
  {% card description="Our most capable reasoning model with a shared 1M context window and long decodes up to 1M tokens." title="Gemini 4 Carbon" variant="model-card" %}
  {% section class="model-specs" %}
  *   *Model code* **gemini-4-carbon**
  *   *Context* **1M tokens**
  *   *Max output* **65K / 1M tokens**
  *   *Modalities* **Text, Image, Audio, Video, PDF**

  {% /section %}

  {% section class="card-actions" %}
  {% button href="https://aistudio.google.com/prompts/new_chat?model=gemini-4-carbon" tooltip="Try Gemini 4 Carbon in AI Studio" variant="primary" %}Try in AI Studio{% /button %} {% button href="/docs/models/gemini-4-carbon" icon="arrow_forward" tooltip="View Gemini 4 Carbon model details" variant="icon-primary" /%}

  {% /section %}

  {% /card %}

  {% card description="Brings cutting-edge intelligence to everyone, with speed and efficiency for everyday coding and agentic workflows, featuring a shared 1M context window and long decodes up to 1M tokens." title="Gemini 4 Hydrogen" variant="model-card" %}
  {% section class="model-specs" %}
  *   *Model code* **gemini-4-hydrogen**
  *   *Context* **1M tokens**
  *   *Max output* **65K / 1M tokens**
  *   *Modalities* **Text, Image, Audio, Video, PDF**

  {% /section %}

  {% section class="card-actions" %}
  {% button href="https://aistudio.google.com/prompts/new_chat?model=gemini-4-hydrogen" tooltip="Try Gemini 4 Hydrogen in AI Studio" variant="primary" %}Try in AI Studio{% /button %} {% button href="/docs/models/gemini-4-hydrogen" icon="arrow_forward" tooltip="View Gemini 4 Hydrogen model details" variant="icon-primary" /%}

  {% /section %}

  {% /card %}

  {% card description="Specialized multimodal model for fast, calibrated yes/no, choice, and rubric score decisions with zero output tokens." title="Gemini Decision 1" variant="model-card" %}
  {% section class="model-specs" %}
  *   *Model code* **gemini-decision-1**
  *   *Context* **262K tokens**
  *   *Max output* **0 tokens (1,000 questions)**
  *   *Modalities* **Text, Image, Audio, Video, PDF**

  {% /section %}

  {% section class="card-actions" %}
  {% button href="https://aistudio.google.com/apps/bundled/gemini-decisions-api-playground" tooltip="Try Gemini Decision 1 in AI Studio" variant="primary" %}Try in AI Studio{% /button %} {% button href="/docs/models/gemini-decision-1" icon="arrow_forward" tooltip="View Gemini Decision 1 model details" variant="icon-primary" /%}

  {% /section %}

  {% /card %}

  {% card description="Flagship creative text-to-speech model for studio-grade voice fidelity, expressive acting, Voice design, and Voice replication." title="Gemini 3.8 Flash TTS" variant="model-card" %}
  {% section class="model-specs" %}
  *   *Model code* **gemini-3.8-flash-tts**
  *   *Context* **8K tokens**
  *   *Max output* **16K tokens**
  *   *Modalities* **Text → Audio**

  {% /section %}

  {% section class="card-actions" %}
  {% button href="https://aistudio.google.com/prompts/new_chat?model=gemini-3.8-flash-tts" tooltip="Try Gemini 3.8 Flash TTS in AI Studio" variant="primary" %}Try in AI Studio{% /button %} {% button href="/docs/models/gemini-3.8-flash-tts" icon="arrow_forward" tooltip="View Gemini 3.8 Flash TTS model details" variant="icon-primary" /%}

  {% /section %}

  {% /card %}

  {% card description="High-efficiency image generation and editing model with improved visual quality, typography, and multi-turn consistency." title="Nano Banana 2.1" variant="model-card" %}
  {% section class="model-specs" %}
  *   *Model code* **gemini-nano-banana-2.1**
  *   *Context* **128K tokens**
  *   *Max output* **32K tokens**
  *   *Modalities* **Text, Image, Video, PDF → Image, Text**

  {% /section %}

  {% section class="card-actions" %}
  {% button href="https://aistudio.google.com/prompts/new_chat?model=gemini-nano-banana-2.1" tooltip="Try Nano Banana 2.1 in AI Studio" variant="primary" %}Try in AI Studio{% /button %} {% button href="/docs/models/gemini-nano-banana-2.1" icon="arrow_forward" tooltip="View Nano Banana 2.1 model details" variant="icon-primary" /%}

  {% /section %}

  {% /card %}

  {% card href="/docs/models" title="View all models" variant="view-more" /%}

{% /card-grid %}

## Explore Capabilities  {% class="hide-from-toc" id="explore-capabilities" %}

{% tabs variant="showcase" %}
  {% tab label="Image" %}
  {% two-column-layout class="capability-panel" %}
  {% left-column %}
  {% tabs %}
  {% tab filename="image_gen.py" label="Python" %}
  ```python
  import base64
  from google import genai
  
  client = genai.Client()
  
  interaction = client.interactions.create(
      model="gemini-nano-banana-2.1",
      input="Generate an image of a nano banana dish in a fancy restaurant",
      response_format={"type": "image", "aspect_ratio": "16:9", "image_size": "2K"},
  )
  
  with open("nano_banana.png", "wb") as f:
      f.write(base64.b64decode(interaction.output_image.data))
  ```

  {% /tab %}

  {% tab filename="image_gen.js" label="JavaScript" %}
  ```javascript
  import { GoogleGenAI } from "@google/genai";
  import * as fs from "node:fs";
  
  const ai = new GoogleGenAI({});
  
  const interaction = await ai.interactions.create({
    model: "gemini-nano-banana-2.1",
    input: "Generate an image of a nano banana dish in a fancy restaurant",
    response_format: { type: "image", aspect_ratio: "16:9", image_size: "2K" },
  });
  
  fs.writeFileSync("nano_banana.png", Buffer.from(interaction.output_image.data, "base64"));
  ```

  {% /tab %}

  {% /tabs %}

  {% /left-column %}

  {% right-column class="capability-details" %}
### Image generation

  Generate and edit highly contextual images natively with Nano Banana models
        using text, image, or interleaved multimodal prompts.

  {% section class="capability-highlights" %}
  *   {% icon name="check" /%} **Up to 4K resolution** with flexible aspect ratios
  *   {% icon name="check" /%} **Multi-turn editing** and character consistency
  *   {% icon name="check" /%} **Search-grounded** visual accuracy and text
            rendering

  {% /section %}

  {% button href="/docs/image-generation" tooltip="Read Image generation docs" variant="ais" %}Read docs{% /button %}

  {% /right-column %}

  {% /two-column-layout %}

  {% /tab %}

  {% tab label="Video" %}
  {% two-column-layout class="capability-panel" %}
  {% left-column %}
  {% tabs %}
  {% tab filename="video_gen.py" label="Python" %}
  ```python
  import base64
  from google import genai
  
  client = genai.Client()
  
  interaction = client.interactions.create(
      model="gemini-omni-1.2-flash",
      input="A cinematic close-up of two people talking by a window in the rain",
  )
  
  with open("dialogue_example.mp4", "wb") as f:
      f.write(base64.b64decode(interaction.output_video.data))
  ```

  {% /tab %}

  {% tab filename="video_gen.js" label="JavaScript" %}
  ```javascript
  import { GoogleGenAI } from "@google/genai";
  import * as fs from "node:fs";
  
  const ai = new GoogleGenAI({});
  
  const interaction = await ai.interactions.create({
    model: "gemini-omni-1.2-flash",
    input: "A cinematic close-up of two people talking by a window in the rain",
  });
  
  if (interaction.output_video?.data) {
    fs.writeFileSync(
      "dialogue_example.mp4",
      Buffer.from(interaction.output_video.data, "base64")
    );
  }
  ```

  {% /tab %}

  {% /tabs %}

  {% /left-column %}

  {% right-column class="capability-details" %}
### Video generation

  Create high-definition video with natively synchronized dialogue, sound effects,
        and ambient audio from text or image prompts.

  {% section class="capability-highlights" %}
  *   {% icon name="check" /%} **Native audio & dialogue** synchronized to motion
  *   {% icon name="check" /%} **Frame interpolation** with first and last frame
            control
  *   {% icon name="check" /%} **Reference images** to preserve character and
            style

  {% /section %}

  {% button href="/docs/video" tooltip="Read Video generation docs" variant="ais" %}Read docs{% /button %}

  {% /right-column %}

  {% /two-column-layout %}

  {% /tab %}

  {% tab label="Voice" %}
  {% two-column-layout class="capability-panel" %}
  {% left-column %}
  {% tabs %}
  {% tab filename="live_agent.py" label="Python" %}
  ```python
  import asyncio
  from google import genai
  from google.genai import types
  
  client = genai.Client(http_options={"api_version": "v1beta"})
  
  async def main():
      config = types.LiveConnectConfig(response_modalities=["AUDIO"])
      async with client.aio.live.connect(
          model="gemini-3.8-live-preview", config=config
      ) as session:
          await session.send_client_content(
              turns={"parts": [{"text": "Hello! Tell me a quick fun fact."}]}
          )
          async for response in session.receive():
              if response.data is not None:
                  # Stream raw PCM audio bytes to speaker
                  pass
  
  asyncio.run(main())
  ```

  {% /tab %}

  {% tab filename="live_agent.js" label="JavaScript" %}
  ```javascript
  import { GoogleGenAI, Modality } from "@google/genai";
  
  const ai = new GoogleGenAI({ httpOptions: { apiVersion: "v1beta" } });
  
  const session = await ai.live.connect({
    model: "gemini-3.8-live-preview",
    config: { responseModalities: [Modality.AUDIO] },
    callbacks: {
      onmessage: (message) => {
        if (message.serverContent?.modelTurn) {
          // Handle low-latency streaming audio chunks
        }
      },
    },
  });
  
  session.sendClientContent({
    turns: [{ parts: [{ text: "Hello! Tell me a quick fun fact." }] }],
  });
  ```

  {% /tab %}

  {% /tabs %}

  {% /left-column %}

  {% right-column class="capability-details" %}
### Voice agents with Live API

  Build real-time, bidirectional voice and video agents with sub-second latency,
        natural barge-in, and live tool calling.

  {% section class="capability-highlights" %}
  *   {% icon name="check" /%} **Real-time WebSocket streaming** for audio and
            video
  *   {% icon name="check" /%} **Natural voice activity detection** and
            interruption handling
  *   {% icon name="check" /%} **Expressive multilingual voices** with affective
            dialogue

  {% /section %}

  {% button href="/docs/live-api" tooltip="Read Live API docs" variant="ais" %}Read docs{% /button %}

  {% /right-column %}

  {% /two-column-layout %}

  {% /tab %}

  {% tab label="Decisions" %}
  {% two-column-layout class="capability-panel" %}
  {% left-column %}
  {% tabs %}
  {% tab filename="decisions.py" label="Python" %}
  ```python
  from google import genai
  
  client = genai.Client(http_options={"api_version": "v1beta"})
  
  result = client.decisions.create(
      model="gemini-decision-1",
      input="The blue mug I ordered on Monday arrived cracked on Wednesday.",
      questions={
          "is_damaged": {
              "type": "noul",
              "instructions": "Did the item arrive damaged?",
          },
      },
  )
  
  answer = result.answers["is_damaged"]
  print(f"P(damaged)={answer.noul:.2f} confidence={answer.confidence:.2f}")
  ```

  {% /tab %}

  {% tab filename="decisions.js" label="JavaScript" %}
  ```javascript
  import { GoogleGenAI } from "@google/genai";
  
  const ai = new GoogleGenAI({ apiVersion: "v1beta" });
  
  const result = await ai.decisions.create({
    model: "gemini-decision-1",
    input: "The blue mug I ordered on Monday arrived cracked on Wednesday.",
    questions: {
      is_damaged: {
        type: "noul",
        instructions: "Did the item arrive damaged?",
      },
    },
  });
  
  const answer = result.answers?.is_damaged;
  if (answer?.type === "noul") {
    console.log(`P(damaged)=${answer.noul} confidence=${answer.confidence}`);
  }
  ```

  {% /tab %}

  {% /tabs %}

  {% /left-column %}

  {% right-column class="capability-details" %}
### Calibrated decisions

  Evaluate typed yes/no, single-select, and rubric score questions over text,
        images, video, audio, and PDFs with [Gemini Decision 1](/docs/models/gemini-decision-1)
        and zero output tokens.

  {% section class="capability-highlights" %}
  *   {% icon name="check" /%} **Calibrated probabilities** across yes/no, choice,
            and ordered score rubrics
  *   {% icon name="check" /%} **Up to 1,000 independent questions** over shared
            input in a single prefill pass
  *   {% icon name="check" /%} **Zero output tokens** across text, image, audio,
            video, and PDF inputs

  {% /section %}

  {% button href="/docs/decisions-api" tooltip="Read Decisions API docs" variant="ais" %}Read docs{% /button %}

  {% /right-column %}

  {% /two-column-layout %}

  {% /tab %}

  {% tab label="Thinking" %}
  {% two-column-layout class="capability-panel" %}
  {% left-column %}
  {% tabs %}
  {% tab filename="thinking.py" label="Python" %}
  ```python
  from google import genai
  
  client = genai.Client()
  
  interaction = client.interactions.create(
      model="gemini-4-hydrogen",
      input="Find the flaw in this distributed lock protocol and fix it.",
      generation_config={
          "thinking_level": "high",
          "thinking_summaries": "auto",
      },
  )
  
  for step in interaction.steps:
      if step.type == "thought":
          for summary in step.summary or []:
              print("Thought summary:", summary.text)
  print("Answer:", interaction.output_text)
  ```

  {% /tab %}

  {% tab filename="thinking.js" label="JavaScript" %}
  ```javascript
  import { GoogleGenAI } from "@google/genai";
  
  const ai = new GoogleGenAI({});
  
  const interaction = await ai.interactions.create({
    model: "gemini-4-hydrogen",
    input: "Find the flaw in this distributed lock protocol and fix it.",
    generation_config: {
      thinking_level: "high",
      thinking_summaries: "auto",
    },
  });
  
  for (const step of interaction.steps) {
    if (step.type === "thought") {
      for (const summary of step.summary ?? []) {
        console.log("Thought summary:", summary.text);
      }
    }
  }
  console.log("Answer:", interaction.output_text);
  ```

  {% /tab %}

  {% /tabs %}

  {% /left-column %}

  {% right-column class="capability-details" %}
### Adaptive thinking

  Control how deeply Gemini reasons before responding—from low-latency `low`
        thinking to deep multi-step `xhigh` reasoning.

  {% section class="capability-highlights" %}
  *   {% icon name="check" /%} **Configurable thinking levels** (minimal, low,
            medium, high, xhigh)
  *   {% icon name="check" /%} **Transparent thought summaries** streamed in real
            time
  *   {% icon name="check" /%} **Interleaved reasoning** across tool calls and
            code execution

  {% /section %}

  {% button href="/docs/thinking" tooltip="Read Adaptive thinking docs" variant="ais" %}Read docs{% /button %}

  {% /right-column %}

  {% /two-column-layout %}

  {% /tab %}

  {% tab label="Tools" %}
  {% two-column-layout class="capability-panel" %}
  {% left-column %}
  {% tabs %}
  {% tab filename="tools.py" label="Python" %}
  ```python
  from google import genai
  
  client = genai.Client()
  
  interaction = client.interactions.create(
      model="gemini-4-hydrogen",
      input="Who won the latest F1 Grand Prix and what were the lap times?",
      tools=[{"type": "google_search"}, {"type": "code_execution"}],
  )
  
  print(interaction.output_text)
  ```

  {% /tab %}

  {% tab filename="tools.js" label="JavaScript" %}
  ```javascript
  import { GoogleGenAI } from "@google/genai";
  
  const ai = new GoogleGenAI({});
  
  const interaction = await ai.interactions.create({
    model: "gemini-4-hydrogen",
    input: "Who won the latest F1 Grand Prix and what were the lap times?",
    tools: [{ type: "google_search" }, { type: "code_execution" }],
  });
  
  console.log(interaction.output_text);
  ```

  {% /tab %}

  {% /tabs %}

  {% /left-column %}

  {% right-column class="capability-details" %}
### Built-in tools & function calling

  Connect Gemini to live information, computation, and your own backend APIs with
        hosted tools and custom function declarations.

  {% section class="capability-highlights" %}
  *   {% icon name="check" /%} **Google Search & URL Context** for live web
            grounding
  *   {% icon name="check" /%} **Code Execution** in a secure Python sandbox
  *   {% icon name="check" /%} **Custom Function Calling** for parallel multi-tool
            orchestration

  {% /section %}

  {% button href="/docs/tools" tooltip="Read Tools and function calling docs" variant="ais" %}Read docs{% /button %}

  {% /right-column %}

  {% /two-column-layout %}

  {% /tab %}

  {% tab label="Structured" %}
  {% two-column-layout class="capability-panel" %}
  {% left-column %}
  {% tabs %}
  {% tab filename="structured.py" label="Python" %}
  ```python
  from google import genai
  from pydantic import BaseModel, Field
  
  class FeedbackAnalysis(BaseModel):
      sentiment: str = Field(description="positive, neutral, or negative")
      summary: str = Field(description="One-sentence summary of the feedback.")
      action_items: list[str]
  
  client = genai.Client()
  
  interaction = client.interactions.create(
      model="gemini-4-hydrogen",
      input="The new dashboard is fast, but exporting CSVs fails on mobile.",
      response_format={
          "type": "text",
          "mime_type": "application/json",
          "schema": FeedbackAnalysis.model_json_schema(),
      },
  )
  
  print(interaction.output_text)
  ```

  {% /tab %}

  {% tab filename="structured.js" label="JavaScript" %}
  ```javascript
  import { GoogleGenAI } from "@google/genai";
  import { z } from "zod";
  
  const FeedbackSchema = z.object({
    sentiment: z.enum(["positive", "neutral", "negative"]),
    summary: z.string(),
    actionItems: z.array(z.string()),
  });
  
  const ai = new GoogleGenAI({});
  
  const interaction = await ai.interactions.create({
    model: "gemini-4-hydrogen",
    input: "The new dashboard is fast, but exporting CSVs fails on mobile.",
    response_format: {
      type: "text",
      mime_type: "application/json",
      schema: z.toJSONSchema(FeedbackSchema),
    },
  });
  
  console.log(JSON.parse(interaction.output_text));
  ```

  {% /tab %}

  {% /tabs %}

  {% /left-column %}

  {% right-column class="capability-details" %}
### Structured outputs

  Constrain Gemini responses to follow a strict JSON Schema, Pydantic model, or
        Zod type for reliable downstream automation.

  {% section class="capability-highlights" %}
  *   {% icon name="check" /%} **Guaranteed JSON Schema** compliance on every
            response
  *   {% icon name="check" /%} **Native Pydantic & Zod** schema integration
  *   {% icon name="check" /%} **Compatible with tools** like Google Search and
            Code Execution

  {% /section %}

  {% button href="/docs/structured-output" tooltip="Read Structured outputs docs" variant="ais" %}Read docs{% /button %}

  {% /right-column %}

  {% /two-column-layout %}

  {% /tab %}

  {% tab label="Long context" %}
  {% two-column-layout class="capability-panel" %}
  {% left-column %}
  {% tabs %}
  {% tab filename="long_context.py" label="Python" %}
  ```python
  from google import genai
  
  client = genai.Client()
  
  uploaded_file = client.files.upload(file="full_codebase_archive.txt")
  
  interaction = client.interactions.create(
      model="gemini-4-hydrogen",
      input=[
          {"type": "file", "file_uri": uploaded_file.uri},
          {
              "type": "text",
              "text": "Trace how authentication tokens are refreshed across all services.",
          },
      ],
  )
  
  print(interaction.output_text)
  ```

  {% /tab %}

  {% tab filename="long_context.js" label="JavaScript" %}
  ```javascript
  import { GoogleGenAI } from "@google/genai";
  
  const ai = new GoogleGenAI({});
  
  const uploadedFile = await ai.files.upload({
    file: "full_codebase_archive.txt",
  });
  
  const interaction = await ai.interactions.create({
    model: "gemini-4-hydrogen",
    input: [
      { type: "file", fileUri: uploadedFile.uri },
      {
        type: "text",
        text: "Trace how authentication tokens are refreshed across all services.",
      },
    ],
  });
  
  console.log(interaction.output_text);
  ```

  {% /tab %}

  {% /tabs %}

  {% /left-column %}

  {% right-column class="capability-details" %}
### Long context

  Input up to 1 million tokens of code, video, audio, or documents in a single
        prompt for deep cross-file reasoning and in-context learning.

  {% section class="capability-highlights" %}
  *   {% icon name="check" /%} **1M+ token context window** (~50,000 lines of code
            or 8 novels)
  *   {% icon name="check" /%} **Near-perfect recall** across long multimodal
            inputs
  *   {% icon name="check" /%} **Context caching** to reduce cost and latency on
            repeated prompts

  {% /section %}

  {% button href="/docs/long-context" tooltip="Read Long context docs" variant="ais" %}Read docs{% /button %}

  {% /right-column %}

  {% /two-column-layout %}

  {% /tab %}

  {% tab label="Function calling" %}
  {% two-column-layout class="capability-panel" %}
  {% left-column %}
  {% tabs %}
  {% tab filename="function_calling.py" label="Python" %}
  ```python
  from google import genai
  
  schedule_meeting = {
      "type": "function",
      "name": "schedule_meeting",
      "description": "Schedules a meeting with attendees at a given date and time.",
      "parameters": {
          "type": "object",
          "properties": {
              "attendees": {"type": "array", "items": {"type": "string"}},
              "date": {"type": "string"},
              "time": {"type": "string"},
              "topic": {"type": "string"},
          },
          "required": ["attendees", "date", "time", "topic"],
      },
  }
  
  client = genai.Client()
  
  interaction = client.interactions.create(
      model="gemini-4-hydrogen",
      input="Schedule a meeting with Bob and Alice tomorrow at 10:00 AM about Q3 planning.",
      tools=[schedule_meeting],
  )
  
  for step in interaction.steps:
      if step.type == "function_call":
          print(step.name, step.arguments)
  ```

  {% /tab %}

  {% tab filename="function_calling.js" label="JavaScript" %}
  ```javascript
  import { GoogleGenAI } from "@google/genai";
  
  const ai = new GoogleGenAI({});
  
  const scheduleMeeting = {
    type: "function",
    name: "schedule_meeting",
    description: "Schedules a meeting with attendees at a given date and time.",
    parameters: {
      type: "object",
      properties: {
        attendees: { type: "array", items: { type: "string" } },
        date: { type: "string" },
        time: { type: "string" },
        topic: { type: "string" },
      },
      required: ["attendees", "date", "time", "topic"],
    },
  };
  
  const interaction = await ai.interactions.create({
    model: "gemini-4-hydrogen",
    input: "Schedule a meeting with Bob and Alice tomorrow at 10:00 AM about Q3 planning.",
    tools: [scheduleMeeting],
  });
  
  for (const step of interaction.steps) {
    if (step.type === "function_call") {
      console.log(step.name, step.arguments);
    }
  }
  ```

  {% /tab %}

  {% /tabs %}

  {% /left-column %}

  {% right-column class="capability-details" %}
### Function calling

  Connect Gemini to your own APIs, databases, and backend services with structured
        function declarations and automatic argument extraction.

  {% section class="capability-highlights" %}
  *   {% icon name="check" /%} **Parallel & compositional** multi-step function
            calls
  *   {% icon name="check" /%} **Strict schema adherence** for tool arguments
  *   {% icon name="check" /%} **Seamless integration** with built-in tools and
            thinking

  {% /section %}

  {% button href="/docs/function-calling" tooltip="Read Function calling docs" variant="ais" %}Read docs{% /button %}

  {% /right-column %}

  {% /two-column-layout %}

  {% /tab %}

  {% tab label="Document understanding" %}
  {% two-column-layout class="capability-panel" %}
  {% left-column %}
  {% tabs %}
  {% tab filename="document_understanding.py" label="Python" %}
  ```python
  import base64
  from google import genai
  
  client = genai.Client()
  
  with open("financial_report.pdf", "rb") as f:
      pdf_base64 = base64.b64encode(f.read()).decode("utf-8")
  
  interaction = client.interactions.create(
      model="gemini-4-hydrogen",
      input=[
          {
              "type": "document",
              "data": pdf_base64,
              "mime_type": "application/pdf",
          },
          {
              "type": "text",
              "text": "Summarize the key revenue drivers and extract the Q4 table.",
          },
      ],
  )
  
  print(interaction.output_text)
  ```

  {% /tab %}

  {% tab filename="document_understanding.js" label="JavaScript" %}
  ```javascript
  import { GoogleGenAI } from "@google/genai";
  import * as fs from "node:fs";
  
  const ai = new GoogleGenAI({});
  
  const pdfData = fs.readFileSync("financial_report.pdf", {
    encoding: "base64",
  });
  
  const interaction = await ai.interactions.create({
    model: "gemini-4-hydrogen",
    input: [
      {
        type: "document",
        data: pdfData,
        mime_type: "application/pdf",
      },
      {
        type: "text",
        text: "Summarize the key revenue drivers and extract the Q4 table.",
      },
    ],
  });
  
  console.log(interaction.output_text);
  ```

  {% /tab %}

  {% /tabs %}

  {% /left-column %}

  {% right-column class="capability-details" %}
### Document understanding

  Process up to 1,000 pages of PDFs with native visual and textual comprehension
        across tables, charts, diagrams, and layouts.

  {% section class="capability-highlights" %}
  *   {% icon name="check" /%} **Native vision-based PDF parsing** beyond plain
            OCR
  *   {% icon name="check" /%} **Up to 1,000 pages** per document in a single
            request
  *   {% icon name="check" /%} **Structured extraction** of complex tables, forms,
            and figures

  {% /section %}

  {% button href="/docs/document-processing" tooltip="Read Document understanding docs" variant="ais" %}Read docs{% /button %}

  {% /right-column %}

  {% /two-column-layout %}

  {% /tab %}

{% /tabs %}

## Create agents  {% class="hide-from-toc" id="create-agents" %}

{% two-column-layout %}
  {% left-column %}
  Managed Agents give Gemini a workspace to plan and complete tasks on its own. In
    a single request, Gemini can write and run code, search the web, and create
    files in a hosted sandbox environment. Start with our prebuilt Antigravity
    agent, or customize it with your own instructions and tools.

  {% button href="/docs/managed-agents-quickstart" variant="ais" %}Agents quickstart{% /button %} {% button href="https://aistudio.google.com/prompts/new_chat?model=antigravity-preview-09-2026" tooltip="Try Managed Agents in AI Studio" variant="primary" %}Try in AI Studio{% /button %}

  {% /left-column %}

  {% right-column %}
  {% tabs %}
  {% tab filename="agent.py" label="Python" %}
  ```python
  from google import genai
  
  client = genai.Client(http_options={"api_version": "v1beta"})
  
  interaction = client.interactions.create(
      agent="antigravity-preview-09-2026",
      input=(
          "Research the top 5 sustainable fashion brands, "
          "compare their materials and pricing tiers, and "
          "build an interactive dashboard in analysis.html."
      ),
      environment="remote"
  )
  
  print(interaction.output_text)
  ```

  {% /tab %}

  {% tab filename="agent.js" label="JavaScript" %}
  ```javascript
  import { GoogleGenAI } from "@google/genai";
  
  const ai = new GoogleGenAI({ httpOptions: { apiVersion: "v1beta" } });
  
  const interaction = await ai.interactions.create({
    agent: "antigravity-preview-09-2026",
    input:
      "Research the top 5 sustainable fashion brands, " +
      "compare their materials and pricing tiers, and " +
      "build an interactive dashboard in analysis.html.",
    environment: "remote",
  });
  
  console.log(interaction.output_text);
  ```

  {% /tab %}

  {% tab filename="agent.sh" label="REST" %}
  ```bash
  curl -X POST \
    "https://generativelanguage.googleapis.com/v1beta/interactions" \
    -H "x-goog-api-key: $GEMINI_API_KEY" \
    -H 'Content-Type: application/json' \
    -d '{
      "agent": "antigravity-preview-09-2026",
      "input": "Research the top 5 sustainable fashion brands, compare their materials and pricing tiers, and build an interactive dashboard in analysis.html.",
      "environment": "remote"
    }'
  ```

  {% /tab %}

  {% tab filename="AgentQuickstart.java" label="Java" %}
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
  
  CreateAgentInteraction params =
      CreateAgentInteraction.builder()
          .agent(AgentOption.of("antigravity-preview-09-2026"))
          .input(
              InteractionsInput.of(
                  "Research the top 5 sustainable fashion brands, "
                      + "compare their materials and pricing tiers, and "
                      + "build an interactive dashboard in analysis.html."))
          .environment(CreateAgentInteractionEnvironment.of("remote"))
          .build();
  
  Interaction interaction =
      client.interactions.create(CreateInteractionRequestBody.of(params))
          .interaction()
          .get();
  
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
  
      res, err := client.Interactions.Create(ctx, operations.CreateInteractionRequest{
          Body: operations.NewCreateInteractionRequestBody(interactions.CreateAgentInteraction{
              Agent: interactions.AgentOption("antigravity-preview-09-2026"),
              Input: interactions.NewInteractionsInput(
                  "Research the top 5 sustainable fashion brands, " +
                      "compare their materials and pricing tiers, and " +
                      "build an interactive dashboard in analysis.html.",
              ),
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

  {% tab filename="agent.sh" label="CLI" %}
  ```bash
  gemini-api agent run "Research the top 5 sustainable fashion brands, compare their materials and pricing tiers, and build an interactive dashboard in analysis.html." \
    --agent antigravity-preview-09-2026 \
    --body '{"environment":"remote"}'
  ```

  {% /tab %}

  {% /tabs %}

  {% /right-column %}

{% /two-column-layout %}

## Interactions API  {% class="hide-from-toc" id="interactions-api" %}

The **Interactions API** has become our default interface as of June 2026 and is
the best way to build with Gemini models and agents going forward. If you're
starting a new project, you should use the Interactions API. While it remains
supported, the `generateContent` API is now considered legacy.

{% card-grid columns="3" %}
  {% card description="Learn how the Interactions API manages conversation state, messages, and output formats." href="/docs/interactions-overview" icon="hub" title="Interactions Overview" variant="stacked-icon" /%}

  {% card description="Step-by-step guide to transition your code from generateContent to the Interactions API." href="/docs/migrate-to-interactions" icon="swap_horiz" title="Migration Guide" variant="stacked-icon" /%}

  {% card description="Stream real-time tokens, incremental thoughts, and tool call events." href="/docs/streaming" icon="sensors" title="Streaming" variant="stacked-icon" /%}

{% /card-grid %}