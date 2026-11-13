> ## AI Agent Context
> Get the complete documentation index at: https://aistudio.google.com/llms.txt
> Use this file to discover all available pages.
> For the full documentation in a single file, fetch: https://aistudio.google.com/llms-full.txt

# Long decode

By default, Gemini 4 models (`gemini-4-carbon`, `gemini-4-argon`, and `gemini-4-hydrogen`) generate up to 64K tokens (65,536) of thinking and output per response. Long decode lets you raise `max_output_tokens` past 64K for hard reasoning, math, and coding tasks, up to the unified 1M-token context window (1,048,576 tokens shared across input, thinking, and output). On the Interactions API, you can run long decode with [background execution](/docs/background-execution) so our servers run every hop for you, or in the foreground with [client-side continuation](/docs/long-decode#client-side-continuation).

## How long decode works  {% id="how-long-decode-works" %}

Generating hundreds of thousands of tokens can take longer than a single HTTP request can stay open, so long decode splits generation into sequential hops that continue from where the previous hop stopped: up to 64K tokens (65,536) per hop on background calls, streaming calls, and non-streaming `gemini-4-hydrogen` calls, or up to 32K tokens (32,768) per non-streaming hop on `gemini-4-carbon` and `gemini-4-argon`.

When you set `background: true` and `max_output_tokens` greater than 65,536 on the Interactions API:

1. The request runs asynchronously and returns an interaction with `status="in_progress"`.
2. If the response reaches 64K tokens without finishing, the server starts a continuation hop with the tokens generated so far.
3. This repeats until the model finishes or reaches `max_output_tokens`.
4. When you poll the interaction, you get the combined thinking and output from all hops in a single interaction.

To run continuation hops from your client instead, see [Choose how to run long decode](/docs/long-decode#choose-how-to-run-long-decode).

{% tabs %}
  {% tab label="Python" %}
  ```python
  import time
  from google import genai
  
  client = genai.Client()
  
  interaction = client.interactions.create(
      model="gemini-4-carbon",
      input="Write a complete, rigorous proof of the prime number theorem.",
      background=True,
      generation_config={
          "max_output_tokens": 262144,
          "thinking_level": "high",
      },
  )
  
  while interaction.status in ("in_progress", "queued"):
      time.sleep(5)
      interaction = client.interactions.get(id=interaction.id)
  
  # Each hop adds a model_output step, so join the text of all of them.
  text = "".join(
      content.text
      for step in interaction.steps
      if step.type == "model_output"
      for content in step.content
      if content.type == "text"
  )
  print(text)
  print("Status:", interaction.status)
  print("Usage:", interaction.usage)
  ```

  {% /tab %}

  {% tab label="JavaScript" %}
  ```javascript
  import { GoogleGenAI } from "@google/genai";
  
  const client = new GoogleGenAI({});
  
  let interaction = await client.interactions.create({
    model: "gemini-4-carbon",
    input: "Write a complete, rigorous proof of the prime number theorem.",
    background: true,
    generation_config: {
      max_output_tokens: 262144,
      thinking_level: "high",
    },
  });
  
  while (interaction.status === "in_progress" || interaction.status === "queued") {
    await new Promise((resolve) => setTimeout(resolve, 5000));
    interaction = await client.interactions.get(interaction.id);
  }
  
  // Each hop adds a model_output step, so join the text of all of them.
  const text = interaction.steps
    .filter((step) => step.type === "model_output")
    .flatMap((step) => step.content ?? [])
    .filter((content) => content.type === "text")
    .map((content) => content.text)
    .join("");
  console.log(text);
  console.log("Status:", interaction.status);
  console.log("Usage:", interaction.usage);
  ```

  {% /tab %}

  {% tab label="REST" %}
  ```bash
  # 1. Create the background interaction. It returns an ID right away.
  ID=$(curl -s -X POST "https://generativelanguage.googleapis.com/v1beta/interactions" \
    -H "x-goog-api-key: $GEMINI_API_KEY" \
    -H "Content-Type: application/json" \
    -d '{
      "model": "gemini-4-carbon",
      "input": "Write a complete, rigorous proof of the prime number theorem.",
      "background": true,
      "generation_config": {"max_output_tokens": 262144, "thinking_level": "high"}
    }' | jq -r '.id')
  
  # 2. Poll until the status is no longer in_progress or queued.
  #    The REST response has no output_text field, so join the text of every model_output step.
  while true; do
    RESP=$(curl -s "https://generativelanguage.googleapis.com/v1beta/interactions/$ID" \
      -H "x-goog-api-key: $GEMINI_API_KEY")
    STATUS=$(echo "$RESP" | jq -r '.status')
    if [[ "$STATUS" != "in_progress" && "$STATUS" != "queued" ]]; then
      echo "$RESP" | jq -r '[.steps[]? | select(.type == "model_output") | .content[]? | select(.type == "text") | .text] | join("")'
      echo "$RESP" | jq '{status, usage}'
      break
    fi
    sleep 5
  done
  ```

  {% /tab %}

{% /tabs %}

## Output limits  {% id="output-limits" %}

Streaming and non-streaming interactions default to a 64K output token limit, so responses up to 64K tokens need no code changes. To generate past 64K tokens, raise `max_output_tokens` and use background execution or client-side continuation.

| How you create the interaction | Output limit |
| :--- | :--- |
| `background: false`, `max_output_tokens` not set | 65,536 tokens |
| `background: false`, `max_output_tokens` greater than 65,536, `automatic_continuation: true` (SDK default) | Your `max_output_tokens`, up to 1,048,576 minus your input |
| `background: false`, `max_output_tokens` greater than 65,536, `automatic_continuation: false` or REST | 65,536 tokens per streaming hop (or non-streaming hop on `gemini-4-hydrogen`), or 32,768 per non-streaming hop on `gemini-4-carbon` and `gemini-4-argon`. Loop with `continuation_token` to generate up to your `max_output_tokens`. |
| `background: true`, `max_output_tokens` not set | 65,536 tokens |
| `background: true`, `max_output_tokens` greater than 65,536 | Your `max_output_tokens`, up to 1,048,576 minus your input |

{% callout type="warning" %}
  Always set `max_output_tokens` greater than 65,536 for long decode. Also check the value in your agent framework or evaluation tool. A low value, such as 8,192, stops the model before it finishes thinking.

{% /callout %}

## When to use long decode  {% id="when-to-use-long-decode" %}

Most requests finish within 64K tokens. Use long decode only when one response needs more thinking and output than that.

| Workload | Use long decode? | Why |
| :--- | :--- | :--- |
| Hard math, science, research, and formal proofs | Yes | The model can spend more than 64K tokens to explore and check its reasoning. |
| The hardest coding and agentic tasks | Yes | Some tasks need more than 64K tokens of thinking and code in one response. Most coding and agentic tasks finish under 64K. |
| Evaluation tools that stop at the output limit | Yes | Long decode prevents cut-off answers when the model spends a whole 64K response on thinking. |
| Chat, Q&A, summarization, classification, and extraction | No | These tasks finish well under 32K tokens. |
| Requests for a fixed length, such as "write a 700,000-word book" | No | The model doesn't follow length targets. |
| Agents that call tools in many short turns | No | Each turn is short. Large outputs on each turn fill the shared context window fast. |
| Prompts near the input limit | No | Output can use only 1,048,576 tokens minus your input. |
| Latency-sensitive requests | No | Long decode can run for several minutes. |

Setting a high `max_output_tokens` gives the model room to think longer on hard problems, but the model still decides how much to write. To control how much reasoning effort the model uses, set [`thinking_level`](/docs/thinking).

## Choose how to run long decode  {% id="choose-how-to-run-long-decode" %}

Background execution is the easiest way to run long decode on the Interactions API. Our servers run every hop, so a dropped client connection won't interrupt generation. Client-side continuation, where the Google GenAI SDK or your own code starts each hop, is also available on the Interactions API for foreground calls, stateless requests, or managing your own retry resilience.

|  | Background execution (Interactions API) | Client-side continuation (Interactions API) |
| :--- | :--- | :--- |
| **Who starts each hop** | Our servers | The Google GenAI SDK (by default), or your own code |
| **Tokens per request** | Your `max_output_tokens`, in one interaction (up to 64K per internal hop) | 64K per stream (and non-streaming on `gemini-4-hydrogen`); 32K per non-streaming request on `gemini-4-carbon` and `gemini-4-argon` |
| **Run time** | Up to 24 hours | 20 minutes per streaming hop, 10 minutes per non-streaming hop |
| **Storage** | Requires `store: true` | Stored by default (`store: true`), or stateless with `store: false` |
| **Best for** | The easiest way to run long decode | Foreground calls, stateless apps, or finer-grained control over retries, so you can build your own backoff, error handling, and resilience |

If you use the GenerateContent API instead, see [long decode with the GenerateContent API](/docs/long-decode?generate-content=true).

## Client-side continuation  {% id="client-side-continuation" %}

The following sections apply when `background: false` (the default). Your client drives each continuation hop instead of our servers, either automatically with the Google GenAI SDK or with your own loop.

### Automatic continuation with the SDK  {% id="automatic-continuation" %}

{% callout type="note" %}
  Client-side continuation requires Google GenAI SDK version 2.34.0+ for Python, 2.32.0+ for JavaScript, 1.77.0+ for Go, 1.80.0+ for Java, or 1.28.0+ for .NET.

{% /callout %}

When `max_output_tokens` exceeds the single-hop limit, the Google GenAI SDK runs the continuation hops and returns one combined interaction. For REST or custom loop control, see [Client-side continuation with your own loop](/docs/long-decode#client-side-loop).

{% tabs %}
  {% tab label="Python" %}
  ```python
  from google import genai
  
  client = genai.Client()
  
  interaction = client.interactions.create(
      model="gemini-4-carbon",
      input="Write a complete, rigorous proof of the prime number theorem.",
      generation_config={
          "max_output_tokens": 262144,
          "thinking_level": "high",
      },
  )
  
  print(interaction.output_text)
  print("Status:", interaction.status)
  print("Usage:", interaction.usage)
  ```

  {% /tab %}

  {% tab label="JavaScript" %}
  ```javascript
  import { GoogleGenAI } from "@google/genai";
  
  const client = new GoogleGenAI({});
  
  const interaction = await client.interactions.create({
    model: "gemini-4-carbon",
    input: "Write a complete, rigorous proof of the prime number theorem.",
    generation_config: {
      max_output_tokens: 262144,
      thinking_level: "high",
    },
  });
  
  console.log(interaction.output_text);
  console.log("Status:", interaction.status);
  console.log("Usage:", interaction.usage);
  ```

  {% /tab %}

{% /tabs %}

Keep these SDK behaviors in mind:

* **Save the merged response:** `interactions.create` merges text, steps, and usage across all hops, using the final hop's `id`. Because each hop is stored separately, `interactions.get` returns only the last hop's output, so save the response from `create`. Passing that `id` as `previous_interaction_id` on the next turn keeps the full history.
* **Timeouts:** Client `http_options` sets the HTTP timeout for each hop. Passing `timeout` to `interactions.create` caps total time across all hops.
* **Interrupted runs:** If a hop fails after earlier progress, the SDK raises `ContinuationInterruptedError`. For non-streaming calls, `partial_interaction` holds the merged output from completed hops. To resume, pass the error's interaction ID and `continuation_token` to `interactions.create` (or resend `input` when `store` is `false`).

### Client-side continuation with your own loop  {% id="client-side-loop" %}

To call REST directly or manage retries, backoff, and logging between hops yourself, run the continuation loop in your code (in the SDK, disable `automatic_continuation`). Keep the same model, tools, system instruction, and generation config on each hop, and resend the prompt instead of the previous interaction ID if storage is disabled.

{% tabs %}
  {% tab label="Python" %}
  ```python
  from google import genai
  
  client = genai.Client()
  
  interaction = client.interactions.create(
      model="gemini-4-carbon",
      input="Write a complete, rigorous proof of the prime number theorem.",
      automatic_continuation=False,
      generation_config={
          "max_output_tokens": 262144,
          "thinking_level": "high",
      },
  )
  full_text = interaction.output_text or ""
  
  while interaction.status == "requires_continuation":
      interaction = client.interactions.create(
          model="gemini-4-carbon",
          previous_interaction_id=interaction.id,
          continuation_token=interaction.continuation_token,
          automatic_continuation=False,
          generation_config={
              "max_output_tokens": 262144,
              "thinking_level": "high",
          },
      )
      full_text += interaction.output_text or ""
  
  print(full_text)
  ```

  {% /tab %}

  {% tab label="JavaScript" %}
  ```javascript
  import { GoogleGenAI } from "@google/genai";
  
  const client = new GoogleGenAI({});
  
  let interaction = await client.interactions.create({
    model: "gemini-4-carbon",
    input: "Write a complete, rigorous proof of the prime number theorem.",
    automatic_continuation: false,
    generation_config: {
      max_output_tokens: 262144,
      thinking_level: "high",
    },
  });
  let fullText = interaction.output_text ?? "";
  
  while (interaction.status === "requires_continuation") {
    interaction = await client.interactions.create({
      model: "gemini-4-carbon",
      previous_interaction_id: interaction.id,
      continuation_token: interaction.continuation_token,
      automatic_continuation: false,
      generation_config: {
        max_output_tokens: 262144,
        thinking_level: "high",
      },
    });
    fullText += interaction.output_text ?? "";
  }
  
  console.log(fullText);
  ```

  {% /tab %}

  {% tab label="REST" %}
  ```bash
  RESP=$(curl -s -X POST "https://generativelanguage.googleapis.com/v1beta/interactions" \
    -H "x-goog-api-key: $GEMINI_API_KEY" \
    -H "Content-Type: application/json" \
    -d '{
      "model": "gemini-4-carbon",
      "input": "Write a complete, rigorous proof of the prime number theorem.",
      "generation_config": {"max_output_tokens": 262144, "thinking_level": "high"}
    }')
  
  while [[ "$(echo "$RESP" | jq -r '.status')" == "requires_continuation" ]]; do
    echo "$RESP" | jq -rj '[.steps[]? | select(.type == "model_output") | .content[]? | select(.type == "text") | .text] | join("")'
    PREV_ID=$(echo "$RESP" | jq -r '.id')
    TOKEN=$(echo "$RESP" | jq -r '.continuation_token')
    RESP=$(curl -s -X POST "https://generativelanguage.googleapis.com/v1beta/interactions" \
      -H "x-goog-api-key: $GEMINI_API_KEY" \
      -H "Content-Type: application/json" \
      -d "{
        \"model\": \"gemini-4-carbon\",
        \"previous_interaction_id\": \"$PREV_ID\",
        \"continuation_token\": \"$TOKEN\",
        \"generation_config\": {\"max_output_tokens\": 262144, \"thinking_level\": \"high\"}
      }")
  done
  
  echo "$RESP" | jq -r '[.steps[]? | select(.type == "model_output") | .content[]? | select(.type == "text") | .text] | join("")'
  ```

  {% /tab %}

{% /tabs %}

## Stream long decode  {% id="streaming" %}

To stream outputs and thought summaries as they arrive, add `stream: true` and `thinking_summaries: "auto"`. Long streams can drop, so your client must reconnect. Follow the reconnect pattern in the [background execution guide](/docs/background-execution). Long decode adds these rules:

* **Save the interaction ID:** Read it from the `interaction.created` event.
* **Save every `event_id`:** An `event_id` can arrive on `interaction.status_update` events, not only on text deltas.
* **Reconnect with `last_event_id`:** Call `interactions.get` with `stream: true` and the last `event_id`. The stream continues after that event.
* **Read to the end:** After you reconnect, read the stream to the end before you check the status. The server replays missed events, even after the interaction completes.
* **Set long timeouts:** Set HTTP read timeouts to 15 to 20 minutes per stream.
* **Expect output in 5K-token chunks:** After the first 32K tokens on `gemini-4-carbon` and `gemini-4-argon` (or after 64K tokens on `gemini-4-hydrogen`, starting on the second hop), the stream sends output in chunks of about 5,000 tokens at each checkpoint. Pauses between chunks are normal. The interaction isn't stuck, so keep the connection open.

For foreground streams with the Google GenAI SDK, the SDK chains continuation hops into a single stream:

* **Keep reading across hops:** Each hop is its own interaction and emits `interaction.created` and `interaction.completed` events. Don't reset your stream parser on `interaction.created`, and don't stop on `interaction.completed` while status is `requires_continuation`. Save the final hop's ID if you continue the conversation.
* **Handle mid-hop disconnects:** If a connection drops at a checkpoint before new deltas arrive, the SDK reconnects for you. If the stream already yielded deltas after the latest checkpoint, the SDK raises `ContinuationInterruptedError` to avoid duplicate output.

## Interaction status  {% id="background-status" %}

A background interaction can run for up to 24 hours. Once the status is no longer `in_progress` or `queued`, handle the interaction status using this table:

| Status | Meaning | What to do |
| :--- | :--- | :--- |
| `completed` | The model finished. | Join the `model_output` steps in `steps` and read `usage`. To continue the conversation, pass this interaction's `id` as `previous_interaction_id`. |
| `requires_continuation` | A foreground hop reached its single-request cap (64K for streaming and `gemini-4-hydrogen` non-streaming, or 32K for `gemini-4-carbon` and `gemini-4-argon` non-streaming) with token budget left. | The Google GenAI SDK continues this for you by default. In REST, send the next hop with `previous_interaction_id` and `continuation_token`. |
| `requires_action` | The model asked for a tool call. | Run the tool. Then send the result with this interaction's `id`. |
| `incomplete` | The model used all of `max_output_tokens`. Text can be empty if the model was still thinking. | Resume with `previous_interaction_id`, `continuation_token`, and a higher `max_output_tokens`, or send the request again with a higher `max_output_tokens`. |
| `failed` | The server couldn't finish, or the interaction ran longer than 24 hours. | Retry the request. If it fails again, share the interaction `id` with support. |
| `cancelled` | You cancelled the interaction. | Read `usage` to see the billed tokens. |

To stop a running interaction, call `client.interactions.cancel(id=interaction.id)` in Python, `client.interactions.cancel(interaction.id)` in JavaScript, or `POST /v1beta/interactions/{id}/cancel` in REST.

## Set `max_output_tokens` {% id="set-max-output-tokens" %}

`max_output_tokens` sets the combined limit for thinking and output across the interaction. Lowering it doesn't make the model think more concisely, and instead cuts the response off sooner.

| Your workload | Recommended `max_output_tokens` |
| :--- | :--- |
| Existing apps with a limit lower than 32K | Raise to 32,768. Background execution isn't needed. |
| Long coding and agentic tasks | Start at 65,536 (the default). Background execution isn't needed. |
| Complex reasoning, hard math, science, and proofs | Set `background: true` (or use client-side continuation) and start at 262,144, up to 1,048,576 minus your input tokens. |

To use fewer tokens, lower `thinking_level`. Use `high` for the hardest reasoning tasks. Use `medium` (the default) for most coding and agentic work.

## Count tokens  {% id="count-tokens" %}

`interaction.usage` reports the totals across all hops. Read these fields: `total_input_tokens`, `total_cached_tokens`, `total_output_tokens`, `total_thought_tokens`, and `total_tokens`.

`total_input_tokens` adds up the input tokens of every hop. Each hop sends your prompt plus everything generated so far back to the model as input, so the same tokens are counted again in every later hop. For example, a 1,000-token prompt that produces 200,000 tokens of thinking and output takes four 64K hops (or seven 32K non-streaming hops on `gemini-4-carbon` and `gemini-4-argon`):

| Hop | Input sent to the model | Input tokens |
| :--- | :--- | ---: |
| 1 | Prompt | 1,000 |
| 2 | Prompt + hop 1 | 66,536 |
| 3 | Prompt + hops 1 and 2 | 132,072 |
| 4 | Prompt + hops 1 to 3 | 197,608 |
| **Total** |  | **397,216** |

`total_input_tokens` reports about 397,000 tokens (with repeated hop inputs automatically discounted 95% by implicit caching), even though the actual context size is only about 201,000 tokens: the 1,000-token prompt plus 200,000 tokens of thinking and output.

{% callout type="warning" %}
  `total_input_tokens` is the sum of every hop's input, not the size of your context. Don't use it to decide when to summarize or trim your conversation history (context compaction). To estimate the context size, add your prompt size (or `usage.initial_input_tokens` on non-streaming SDK responses) to `total_output_tokens` and `total_thought_tokens`.

{% /callout %}

During a stream, `interaction.status_update` and `interaction.completed` events include `usage` (cumulative for that hop, or for the full interaction in background mode). Within a background stream or a single foreground hop, read the latest `usage` value instead of adding them together. In a foreground stream, each hop is a separate interaction, so sum the final `usage` of each hop.

## Understand billing  {% id="understand-billing" %}

You pay for every token in every hop, including hops that contain only thinking.

* **Cache discount:** Implicit caching discounts the repeated input in each hop by 95%. Cached input costs $0.10 per 1M tokens instead of $2.00 during the introductory period.
* **Cancelled and failed interactions:** You pay for all work completed before the interaction ends.

## Troubleshooting  {% id="troubleshooting" %}

| Symptom | Cause and fix |
| :--- | :--- |
| Output stops at 64K | Set `max_output_tokens` greater than 65,536, and use background execution or upgrade the Google GenAI SDK. |
| Output stops with status `requires_continuation` | The hop reached its single-request cap with budget left. Upgrade the SDK, enable `automatic_continuation`, or add a continuation loop. |
| 400: "store=true is required for background interactions" | Background execution needs `store: true`. |
| Status `incomplete` with empty text | The model used all tokens on thinking. Raise `max_output_tokens` or lower `thinking_level`. |
| Context compaction starts too early | Your agent framework or evaluation tool reads `total_input_tokens`. See [Count tokens](/docs/long-decode#count-tokens). |

## Limitations  {% id="limitations" %}

* **Earlier SDKs:** Versions earlier than Python 2.34.0, JavaScript 2.32.0, Go 1.77.0, Java 1.80.0, and .NET 1.28.0 don't continue foreground interactions.
* **No length targets:** The model doesn't follow token-length or word-count targets.

## Next steps  {% id="next-steps" %}

* Learn about the [latest Gemini models](/docs/latest-model)
* [Background execution](/docs/background-execution)
* [Thinking](/docs/thinking)
* [Long decode with the GenerateContent API](/docs/long-decode?generate-content=true)