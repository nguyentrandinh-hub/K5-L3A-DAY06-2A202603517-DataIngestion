> ## AI Agent Context
> Get the complete documentation index at: https://aistudio.google.com/llms.txt
> Use this file to discover all available pages.
> For the full documentation in a single file, fetch: https://aistudio.google.com/llms-full.txt

# Get started with Gemini Live API using the Google GenAI SDK

The Gemini Live API allows for real-time, bidirectional interaction with Gemini
models, supporting audio, video, and text inputs and native audio outputs. This
guide explains how to integrate with the API using the Google GenAI SDK on your
server.

{% button href="https://aistudio.google.com/live" icon="mic" variant="primary" %}
  Try the Live API in Google AI Studio

{% /button %}

{% button href="https://github.com/google-gemini/gemini-live-api-examples/tree/main/gemini-live-genai-python-sdk" icon="code" variant="primary" %}
  Clone the example app from GitHub

{% /button %}

{% button href="/docs/coding-agents" icon="terminal" variant="primary" %}
  Use coding agent skills

{% /button %}

## Overview  {% id="overview" %}

The Gemini Live API uses WebSockets for real-time communication. The
`google-genai` SDK provides a high-level asynchronous interface for managing
these connections.

Key concepts:

* **Session**: A persistent connection to the model.
* **Config**: Setting up modalities (audio/text), voice, and system instructions.
* **Real-time Input**: Sending audio and video frames as blobs.

## Connecting to the Live API  {% id="connecting-to-the-live-api" %}

Start a Live API session with an API key:

{% tabs %}
  {% tab label="Python" %}
  ```python
  import asyncio
  from google import genai
  
  client = genai.Client(api_key="YOUR_API_KEY", http_options={"api_version": "v1beta"})
  
  model = "gemini-3.8-live"
  config = {"response_modalities": ["AUDIO"]}
  
  async def main():
      async with client.aio.live.connect(model=model, config=config) as session:
          print("Session started")
          # Send content...
  
  if __name__ == "__main__":
      asyncio.run(main())
  ```

  {% /tab %}

  {% tab label="JavaScript" %}
  ```js
  import { GoogleGenAI, Modality } from '@google/genai';
  
  const ai = new GoogleGenAI({ apiKey: "YOUR_API_KEY", httpOptions: { apiVersion: "v1beta" } });
  const model = 'gemini-3.8-live';
  const config = { responseModalities: [Modality.AUDIO] };
  
  async function main() {
  
    const session = await ai.live.connect({
      model: model,
      callbacks: {
        onopen: function () {
          console.debug('Opened');
        },
        onmessage: function (message) {
          console.debug(message);
        },
        onerror: function (e) {
          console.debug('Error:', e.message);
        },
        onclose: function (e) {
          console.debug('Close:', e.reason);
        },
      },
      config: config,
    });
  
    console.debug("Session started");
    // Send content...
  
    session.close();
  }
  
  await main();
  ```

  {% /tab %}

{% /tabs %}

## Sending text  {% id="sending-text" %}

Text can be sent using `send_realtime_input` (Python) or `sendRealtimeInput`
(JavaScript).

{% tabs %}
  {% tab label="Python" %}
  ```python
  await session.send_realtime_input(text="Hello, how are you?")
  ```

  {% /tab %}

  {% tab label="JavaScript" %}
  ```js
  session.sendRealtimeInput({
    text: 'Hello, how are you?'
  });
  ```

  {% /tab %}

{% /tabs %}

## Sending audio  {% id="sending-audio" %}

Audio needs to be sent as raw PCM data (raw 16-bit PCM audio, 16kHz,
little-endian).

{% tabs %}
  {% tab label="Python" %}
  ```python
  # Assuming 'chunk' is your raw PCM audio bytes
  await session.send_realtime_input(
      audio=types.Blob(
          data=chunk,
          mime_type="audio/pcm;rate=16000"
      )
  )
  ```

  {% /tab %}

  {% tab label="JavaScript" %}
  ```js
  // Assuming 'chunk' is a Buffer of raw PCM audio
  session.sendRealtimeInput({
    audio: {
      data: chunk.toString('base64'),
      mimeType: 'audio/pcm;rate=16000'
    }
  });
  ```

  {% /tab %}

{% /tabs %}

For an example of how to get the audio from the client device (e.g. the browser)
see the end-to-end example on [GitHub](https://github.com/google-gemini/gemini-live-api-examples/blob/main/gemini-live-genai-python-sdk/frontend/media-handler.js#L31-L70).

## Sending video  {% id="sending-video" %}

Video frames are sent as individual images (e.g., JPEG or PNG) at a specific
frame rate (max 1 frame per second).

{% tabs %}
  {% tab label="Python" %}
  ```python
  # Assuming 'frame' is your JPEG-encoded image bytes
  await session.send_realtime_input(
      video=types.Blob(
          data=frame,
          mime_type="image/jpeg"
      )
  )
  ```

  {% /tab %}

  {% tab label="JavaScript" %}
  ```js
  // Assuming 'frame' is a Buffer of JPEG-encoded image data
  session.sendRealtimeInput({
    video: {
      data: frame.toString('base64'),
      mimeType: 'image/jpeg'
    }
  });
  ```

  {% /tab %}

{% /tabs %}

For an example of how to get the video from the client device (e.g. the browser)
see the end-to-end example on [GitHub](https://github.com/google-gemini/gemini-live-api-examples/blob/main/gemini-live-genai-python-sdk/frontend/media-handler.js#L84-L120).

## Receiving audio  {% id="receiving-audio" %}

The model's audio responses are received as chunks of data.

{% tabs %}
  {% tab label="Python" %}
  ```python
  async for response in session.receive():
      if response.server_content and response.server_content.model_turn:
          for part in response.server_content.model_turn.parts:
              if part.inline_data:
                  audio_data = part.inline_data.data
                  # Process or play the audio data
  ```

  {% /tab %}

  {% tab label="JavaScript" %}
  ```js
  // Inside the onmessage callback
  const content = response.serverContent;
  if (content?.modelTurn?.parts) {
    for (const part of content.modelTurn.parts) {
      if (part.inlineData) {
        const audioData = part.inlineData.data;
        // Process or play audioData (base64 encoded string)
      }
    }
  }
  ```

  {% /tab %}

{% /tabs %}

See the example app on GitHub to learn how to [receive the audio on your server](https://github.com/google-gemini/gemini-live-api-examples/blob/main/gemini-live-genai-python-sdk/gemini_live.py#L86-L98) and [play it in the browser](https://github.com/google-gemini/gemini-live-api-examples/blob/main/gemini-live-genai-python-sdk/frontend/media-handler.js#L145-L174).

## Receiving text  {% id="receiving-text" %}

Transcriptions for both user input and model output are available in the server
content.

{% tabs %}
  {% tab label="Python" %}
  ```python
  async for response in session.receive():
      content = response.server_content
      if content:
          if content.input_transcription:
              print(f"User: {content.input_transcription.text}")
          if content.output_transcription:
              print(f"Gemini: {content.output_transcription.text}")
  ```

  {% /tab %}

  {% tab label="JavaScript" %}
  ```js
  // Inside the onmessage callback
  const content = response.serverContent;
  if (content?.inputTranscription) {
    console.log('User:', content.inputTranscription.text);
  }
  if (content?.outputTranscription) {
    console.log('Gemini:', content.outputTranscription.text);
  }
  ```

  {% /tab %}

{% /tabs %}

## Handling tool calls  {% id="handling-tool-calls" %}

The API supports tool calling (function calling). When the model requests a tool
call, you must execute the function and send the response back.

{% tabs %}
  {% tab label="Python" %}
  ```python
  async for response in session.receive():
      if response.tool_call:
          function_responses = []
          for fc in response.tool_call.function_calls:
              # 1. Execute the function locally
              result = my_tool_function(**fc.args)
  
              # 2. Prepare the response
              function_responses.append(types.FunctionResponse(
                  name=fc.name,
                  id=fc.id,
                  response={"result": result}
              ))
  
          # 3. Send the tool response back to the session
          await session.send_tool_response(function_responses=function_responses)
  ```

  {% /tab %}

  {% tab label="JavaScript" %}
  ```js
  // Inside the onmessage callback
  if (response.toolCall) {
    const functionResponses = [];
    for (const fc of response.toolCall.functionCalls) {
      const result = myToolFunction(fc.args);
      functionResponses.push({
        name: fc.name,
        id: fc.id,
        response: { result }
      });
    }
    session.sendToolResponse({ functionResponses });
  }
  ```

  {% /tab %}

{% /tabs %}

## What's next  {% id="whats-next" %}

* Read the full Live API [Capabilities](/docs/live-api/capabilities) guide for key capabilities and configurations; including Voice Activity Detection and native audio features.
* Read the [Tool use](/docs/live-api/tools) guide to learn how to integrate Live API with tools and function calling.
* Read the [Session management](/docs/live-api/session-management) guide for managing long running conversations.
* Read the [Ephemeral tokens](/docs/live-api/ephemeral-tokens) guide for secure authentication in [client-to-server](/docs/live-api#implementation-approach) applications.
* For more information about the underlying WebSockets API, see the [WebSockets API reference](/api-reference/live).