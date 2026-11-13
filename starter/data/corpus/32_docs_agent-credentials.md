> ## AI Agent Context
> Get the complete documentation index at: https://aistudio.google.com/llms.txt
> Use this file to discover all available pages.
> For the full documentation in a single file, fetch: https://aistudio.google.com/llms-full.txt

# Credentials in managed agents  {% id="credentials" %}

Credentials are server-managed secrets that let your agents reach third-party
services without the secret ever entering the agent's environment. You store a
credential once, reference it by ID, and the egress proxy resolves and injects
it at request time.

Secret values are write-only. Once stored, they are never returned by any
endpoint, so a compromised agent cannot read back the tokens it is using.

The primary place you use a credential is the network allowlist on
[`environment.network`](/docs/agent-environment). Store the secret
first:

{% tabs %}
  {% tab filename="credentials_in_managed_agents.py" label="Python" %}
  ```py
  from google import genai
  
  client = genai.Client(http_options={"api_version": "v1beta"})
  
  credential = client.credentials.create(
      id="github-production",
      type="bearer_token",
      token="ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
  )
  
  print(f"Credential ID: {credential.id}, Status: {credential.status}")
  ```

  {% /tab %}

  {% tab filename="credentials_in_managed_agents.js" label="JavaScript" %}
  ```javascript
  import { GoogleGenAI } from "@google/genai";
  
  const client = new GoogleGenAI({ httpOptions: { apiVersion: "v1beta" } });
  
  const credential = await client.credentials.create({
      id: "github-production",
      type: "bearer_token",
      token: "ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
  });
  
  console.log(`Credential ID: ${credential.id}, Status: ${credential.status}`);
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
      "google.golang.org/genai/interactions/models/credentials"
      "google.golang.org/genai/interactions/models/operations"
  )
  
  func main() {
      ctx := context.Background()
      client, err := genai.NewClient(ctx, &genai.ClientConfig{HTTPOptions: genai.HTTPOptions{APIVersion: "v1beta"}})
      if err != nil {
          log.Fatal(err)
      }
  
      res, err := client.Credentials.Create(ctx, operations.CreateCredentialRequest{
          Body: credentials.NewCredentialCreateParams(credentials.HTTPBearerConfig{
              ID:    "github-production",
              Token: "ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
          }),
      })
      if err != nil {
          log.Fatal(err)
      }
  
      fmt.Printf("Credential ID: %s, Status: %v\n", res.Credential.ID, res.Credential.GetStatus())
  }
  ```

  {% /tab %}

  {% tab label="REST" %}
  ```shell
  curl -X POST "https://generativelanguage.googleapis.com/v1beta/credentials" \
  -H "Content-Type: application/json" \
  -H "x-goog-api-key: $GEMINI_API_KEY" \
  -d '{
      "id": "github-production",
      "type": "bearer_token",
      "token": "ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
  }'
  ```

  {% /tab %}

  {% tab label="CLI" %}
  ```bash
  gemini-api credentials create --body '{
    "id": "github-production",
    "type": "bearer_token",
    "token": "ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
  }'
  ```

  {% /tab %}

{% /tabs %}

Then attach it to the domain it authenticates:

{% tabs %}
  {% tab filename="credentials_in_managed_agents.py" label="Python" %}
  ```py
  interaction = client.interactions.create(
      agent="antigravity-preview-09-2026",
      input="Triage the open issues in my-org/my-repo.",
      environment={
          "type": "remote",
          "network": {
              "allowlist": [
                  {"domain": "api.github.com", "credential": "github-production"},
                  {"domain": "*"},
              ]
          },
      },
  )
  ```

  {% /tab %}

  {% tab filename="credentials_in_managed_agents.js" label="JavaScript" %}
  ```javascript
  const interaction = await client.interactions.create({
      agent: "antigravity-preview-09-2026",
      input: "Triage the open issues in my-org/my-repo.",
      environment: {
          type: "remote",
          network: {
              allowlist: [
                  { domain: "api.github.com", credential: "github-production" },
                  { domain: "*" },
              ],
          },
      },
  });
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
              Input: interactions.NewInteractionsInput("Triage the open issues in my-org/my-repo."),
              Environment: genai.Ptr(interactions.NewCreateAgentInteractionEnvironment(interactions.Environment{
                  Network: genai.Ptr(interactions.NewNetwork(interactions.EnvironmentNetworkEgressAllowlist{
                      Allowlist: genai.Ptr(interactions.NewAllowlist([]interactions.AllowlistEntry{
                          {Domain: "api.github.com", Credential: genai.Ptr("github-production")},
                          {Domain: "*"},
                      })),
                  })),
              })),
          }),
      })
      if err != nil {
          log.Fatal(err)
      }
  
      fmt.Println(res.Interaction.GetOutputText())
  }
  ```

  {% /tab %}

  {% tab label="REST" %}
  ```shell
  curl -X POST "https://generativelanguage.googleapis.com/v1beta/interactions" \
  -H "Content-Type: application/json" \
  -H "x-goog-api-key: $GEMINI_API_KEY" \
  -d '{
      "agent": "antigravity-preview-09-2026",
      "input": "Triage the open issues in my-org/my-repo.",
      "environment": {
          "type": "remote",
          "network": {
              "allowlist": [
                  { "domain": "api.github.com", "credential": "github-production" },
                  { "domain": "*" }
              ]
          }
      }
  }'
  ```

  {% /tab %}

  {% tab label="CLI" %}
  ```bash
  gemini-api agent run "Triage the open issues in my-org/my-repo." \
    --agent antigravity-preview-09-2026 \
    --body '{
      "environment": {
        "type": "remote",
        "network": {"allowlist": [
          {"domain": "api.github.com", "credential": "github-production"},
          {"domain": "*"}
        ]}
      }
    }'
  ```

  {% /tab %}

{% /tabs %}

The agent now makes authenticated requests to `api.github.com`, and the token
never exists inside the sandbox.

## Credential types  {% id="credential-types" %}

Every credential has a `type` that determines which fields it accepts and how
the proxy applies it.

| Type | Use case | Behavior |
| :--- | :--- | :--- |
| `bearer_token` | Personal access tokens, bot tokens, static API keys | The proxy injects the token as a request header. No refresh logic. |
| `oauth2` | OAuth apps and user-delegated flows | The proxy exchanges the refresh token for access tokens and refreshes them as they expire. |
| `environment_variable` | Client SDKs that read secrets from the process environment | The agent's environment receives a placeholder. The proxy substitutes the real secret on outbound requests. |

## Use credentials in the network allowlist  {% id="network-allowlist" %}

Add `credential` to an allowlist rule and the proxy authenticates every
outbound request to that domain. This is the recommended way to give an agent
access to a private API, a private repository, or a private bucket.

You can mix authenticated and unauthenticated rules in the same allowlist:

{% tabs %}
  {% tab filename="use_credentials_in_the_network_allowlist.py" label="Python" %}
  ```py
  interaction = client.interactions.create(
      agent="antigravity-preview-09-2026",
      input="Sync the open Jira issues into the tracking sheet in my repo.",
      environment={
          "type": "remote",
          "sources": [
              {
                  "type": "repository",
                  "source": "https://github.com/your-org/backend",
                  "target": "/backend-app",
              }
          ],
          "network": {
              "allowlist": [
                  {"domain": "github.com", "credential": "github-production"},
                  {"domain": "api.atlassian.com", "credential": "jira-oauth"},
                  {"domain": "*.googleapis.com"},
              ]
          },
      },
  )
  ```

  {% /tab %}

  {% tab filename="use_credentials_in_the_network_allowlist.js" label="JavaScript" %}
  ```javascript
  const interaction = await client.interactions.create({
      agent: "antigravity-preview-09-2026",
      input: "Sync the open Jira issues into the tracking sheet in my repo.",
      environment: {
          type: "remote",
          sources: [
              {
                  type: "repository",
                  source: "https://github.com/your-org/backend",
                  target: "/backend-app",
              },
          ],
          network: {
              allowlist: [
                  { domain: "github.com", credential: "github-production" },
                  { domain: "api.atlassian.com", credential: "jira-oauth" },
                  { domain: "*.googleapis.com" },
              ],
          },
      },
  });
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
              Input: interactions.NewInteractionsInput("Sync the open Jira issues into the tracking sheet in my repo."),
              Environment: genai.Ptr(interactions.NewCreateAgentInteractionEnvironment(interactions.Environment{
                  Sources: []interactions.Source{
                      {
                          Type:   interactions.SourceTypeRepository.ToPointer(),
                          Source: genai.Ptr("https://github.com/your-org/backend"),
                          Target: genai.Ptr("/backend-app"),
                      },
                  },
                  Network: genai.Ptr(interactions.NewNetwork(interactions.EnvironmentNetworkEgressAllowlist{
                      Allowlist: genai.Ptr(interactions.NewAllowlist([]interactions.AllowlistEntry{
                          {Domain: "github.com", Credential: genai.Ptr("github-production")},
                          {Domain: "api.atlassian.com", Credential: genai.Ptr("jira-oauth")},
                          {Domain: "*.googleapis.com"},
                      })),
                  })),
              })),
          }),
      })
      if err != nil {
          log.Fatal(err)
      }
  
      fmt.Println(res.Interaction.GetOutputText())
  }
  ```

  {% /tab %}

  {% tab label="REST" %}
  ```shell
  curl -X POST "https://generativelanguage.googleapis.com/v1beta/interactions" \
  -H "Content-Type: application/json" \
  -H "x-goog-api-key: $GEMINI_API_KEY" \
  -d '{
      "agent": "antigravity-preview-09-2026",
      "input": "Sync the open Jira issues into the tracking sheet in my repo.",
      "environment": {
          "type": "remote",
          "sources": [
              {
                  "type": "repository",
                  "source": "https://github.com/your-org/backend",
                  "target": "/backend-app"
              }
          ],
          "network": {
              "allowlist": [
                  { "domain": "github.com", "credential": "github-production" },
                  { "domain": "api.atlassian.com", "credential": "jira-oauth" },
                  { "domain": "*.googleapis.com" }
              ]
          }
      }
  }'
  ```

  {% /tab %}

{% /tabs %}

Because the proxy resolves the credential per request, an `oauth2` credential
refreshes its access token transparently. A long-running interaction does not
break when the access token expires.

### Combining `credential` and `transform` {% id="credential-and-transform" %}

Allowlist rules also accept an inline
[`transform`](/docs/agent-environment#private-sources) object that sets headers
directly on the rule. Both mechanisms are applied by the egress proxy on the
wire, so in both cases the header value never exists inside the sandbox. Both
fields can appear on the same rule.

| Rule configuration | Behavior |
| :--- | :--- |
| `credential` only | The proxy resolves the credential and injects its header on every request to the domain. |
| `transform` only | Static header injection. The headers you write are sent as-is. |
| Both | The credential is applied first, then `transform` merges on top. An explicit `transform` header wins if both set the same key. |
| Neither | The domain is allowed and no headers are injected. |

A credential is worth using when you want to store a secret once and reference
it from every environment, agent, and trigger in your project, and when you want
access token refresh and rotation handled for you. An inline `transform` fits
when the value belongs to a single call, for example a token you generate
yourself right before creating the interaction.

Combining the two is common. The credential carries the authentication header
and `transform` adds whatever else the upstream service expects on the same
request:

```json
{
    "domain": "api.atlassian.com",
    "credential": "jira-oauth",
    "transform": {
        "X-Atlassian-Workspace": "my-workspace-id"
    }
}
```

To move a secret out of an inline `transform` and into a credential, store it
with `POST /credentials`, replace the auth header in `transform` with
`"credential": "<id>"`, and leave the rest of the `transform` object alone.

## Use credentials with MCP servers  {% id="mcp-servers" %}

Remote MCP servers take the same `credential` field. Set it on an `mcp_server`
tool and the proxy injects the auth header into every request to that server:

{% tabs %}
  {% tab filename="use_credentials_with_mcp_servers.py" label="Python" %}
  ```py
  interaction = client.interactions.create(
      agent="antigravity-preview-09-2026",
      input="Create a new issue in my-org/my-repo",
      environment="remote",
      tools=[{
          "type": "mcp_server",
          "name": "github",
          "url": "https://api.githubcopilot.com/mcp",
          "credential": "github-production",
      }],
  )
  ```

  {% /tab %}

  {% tab filename="use_credentials_with_mcp_servers.js" label="JavaScript" %}
  ```javascript
  const interaction = await client.interactions.create({
      agent: "antigravity-preview-09-2026",
      input: "Create a new issue in my-org/my-repo",
      environment: "remote",
      tools: [{
          type: "mcp_server",
          name: "github",
          url: "https://api.githubcopilot.com/mcp",
          credential: "github-production",
      }],
  });
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
              Input: interactions.NewInteractionsInput("Create a new issue in my-org/my-repo"),
              Environment: genai.Ptr(interactions.NewCreateAgentInteractionEnvironment(interactions.Environment{
                  Network: genai.Ptr(interactions.NewNetwork(interactions.EnvironmentNetworkEgressAllowlist{
                      Allowlist: genai.Ptr(interactions.NewAllowlist([]interactions.AllowlistEntry{
                          {Domain: "api.githubcopilot.com", Credential: genai.Ptr("github-production")},
                      })),
                  })),
              })),
              Tools: []interactions.Tool{
                  interactions.NewTool(interactions.MCPServer{
                      Name: genai.Ptr("github"),
                      URL:  genai.Ptr("https://api.githubcopilot.com/mcp"),
                  }),
              },
          }),
      })
      if err != nil {
          log.Fatal(err)
      }
  
      fmt.Println(res.Interaction.GetOutputText())
  }
  ```

  {% /tab %}

  {% tab label="REST" %}
  ```shell
  curl -X POST "https://generativelanguage.googleapis.com/v1beta/interactions" \
  -H "Content-Type: application/json" \
  -H "x-goog-api-key: $GEMINI_API_KEY" \
  -d '{
      "agent": "antigravity-preview-09-2026",
      "input": "Create a new issue in my-org/my-repo",
      "environment": "remote",
      "tools": [
          {
              "type": "mcp_server",
              "name": "github",
              "url": "https://api.githubcopilot.com/mcp",
              "credential": "github-production"
          }
      ]
  }'
  ```

  {% /tab %}

{% /tabs %}

`credential` and `headers` follow the same precedence rule as the allowlist.
The credential is applied first and `headers` merges on top, so an explicit
header wins if both set the same key:

```json
{
    "type": "mcp_server",
    "name": "jira",
    "url": "https://jira.atlassian.com/mcp",
    "credential": "jira-oauth",
    "headers": {
        "X-Atlassian-Workspace": "my-workspace-id"
    }
}
```

To move a secret out of inline `headers` and into a credential, store it with
`POST /credentials` and replace the auth entry in `headers` with `credential`.
Keep the other headers where they are.

## Use credentials as environment variables  {% id="environment-variables" %}

Some client libraries read secrets from the process environment rather than
accepting them as request headers. Socket-mode and long-polling clients are the
common case.

Bind an `environment_variable` credential to a variable name under
`environment.env`:

{% tabs %}
  {% tab filename="use_credentials_as_environment_variables.py" label="Python" %}
  ```py
  interaction = client.interactions.create(
      agent="antigravity-preview-09-2026",
      input="Run the sync script and check notifications.",
      environment={
          "type": "remote",
          "env": {
              "NODE_ENV": "production",
              "SLACK_BOT_TOKEN": {"credential": "slack-bot-token"},
          },
      },
  )
  ```

  {% /tab %}

  {% tab filename="use_credentials_as_environment_variables.js" label="JavaScript" %}
  ```javascript
  const interaction = await client.interactions.create({
      agent: "antigravity-preview-09-2026",
      input: "Run the sync script and check notifications.",
      environment: {
          type: "remote",
          env: {
              NODE_ENV: "production",
              SLACK_BOT_TOKEN: { credential: "slack-bot-token" },
          },
      },
  });
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
              Input: interactions.NewInteractionsInput("Run the sync script and check notifications."),
              Environment: genai.Ptr(interactions.NewCreateAgentInteractionEnvironment(interactions.Environment{
                  Env: genai.Ptr(interactions.NewEnv(map[string]interactions.EnvVar{
                      "NODE_ENV":        {Value: genai.Ptr("production")},
                      "SLACK_BOT_TOKEN": {Credential: genai.Ptr("slack-bot-token")},
                  })),
              })),
          }),
      })
      if err != nil {
          log.Fatal(err)
      }
  
      fmt.Println(res.Interaction.GetOutputText())
  }
  ```

  {% /tab %}

  {% tab label="REST" %}
  ```shell
  curl -X POST "https://generativelanguage.googleapis.com/v1beta/interactions" \
  -H "Content-Type: application/json" \
  -H "x-goog-api-key: $GEMINI_API_KEY" \
  -d '{
      "agent": "antigravity-preview-09-2026",
      "input": "Run the sync script and check notifications.",
      "environment": {
          "type": "remote",
          "env": {
              "NODE_ENV": "production",
              "SLACK_BOT_TOKEN": { "credential": "slack-bot-token" }
          }
      }
  }'
  ```

  {% /tab %}

  {% tab label="CLI" %}
  ```bash
  gemini-api agent run "Run the sync script and check notifications." \
    --agent antigravity-preview-09-2026 \
    --body '{
      "environment": {
        "type": "remote",
        "env": {"NODE_ENV": "production", "SLACK_BOT_TOKEN": {"credential": "slack-bot-token"}}
      }
    }'
  ```

  {% /tab %}

{% /tabs %}

`env` accepts literal strings and credential references side by side. A literal
string is injected into the container as a normal plaintext variable.

A credential reference is not. The variable receives the placeholder
`__GEMINI_CRED_<credential-id>__`, and the proxy swaps in the real secret only
for outbound requests going to a domain in the credential's `trusted_domains`. A
request to any other domain is rejected, so the secret never leaves the
perimeter and the placeholder is not sent in its place.

Caution: Literal values are injected as plain text and are readable by anything running in the sandbox, including the agent itself. Use them for configuration like `NODE_ENV`, not for secrets. A secret belongs in a credential, which is the only form that gets a placeholder and on-the-wire substitution.

Set `trusted_domains` on every `environment_variable` credential. It is the
control that scopes where the secret can be used.

## Create a credential  {% id="create-a-credential" %}

Every create request needs a `type`, plus whichever fields that type requires.

When calling REST directly, all field names use snake_case. Sending a camelCase
field returns a `400`.

### Bearer token  {% id="bearer-token" %}

A bearer token credential needs only `token`:

{% tabs %}
  {% tab filename="bearer_token.py" label="Python" %}
  ```py
  credential = client.credentials.create(
      id="github-production",
      type="bearer_token",
      token="ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
  )
  ```

  {% /tab %}

  {% tab filename="bearer_token.js" label="JavaScript" %}
  ```javascript
  const credential = await client.credentials.create({
      id: "github-production",
      type: "bearer_token",
      token: "ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
  });
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
      "google.golang.org/genai/interactions/models/credentials"
      "google.golang.org/genai/interactions/models/operations"
  )
  
  func main() {
      ctx := context.Background()
      client, err := genai.NewClient(ctx, &genai.ClientConfig{HTTPOptions: genai.HTTPOptions{APIVersion: "v1beta"}})
      if err != nil {
          log.Fatal(err)
      }
  
      res, err := client.Credentials.Create(ctx, operations.CreateCredentialRequest{
          Body: credentials.NewCredentialCreateParams(credentials.HTTPBearerConfig{
              ID:    "github-production",
              Token: "ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
          }),
      })
      if err != nil {
          log.Fatal(err)
      }
  
      fmt.Printf("Created credential: %s\n", res.Credential.ID)
  }
  ```

  {% /tab %}

  {% tab label="REST" %}
  ```shell
  curl -X POST "https://generativelanguage.googleapis.com/v1beta/credentials" \
  -H "Content-Type: application/json" \
  -H "x-goog-api-key: $GEMINI_API_KEY" \
  -d '{
      "id": "github-production",
      "type": "bearer_token",
      "token": "ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
  }'
  ```

  {% /tab %}

  {% tab label="CLI" %}
  ```bash
  gemini-api credentials create --body '{
    "id": "github-production",
    "type": "bearer_token",
    "token": "ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
  }'
  ```

  {% /tab %}

{% /tabs %}

The response returns metadata only, never the token:

```json
{
  "id": "github-production",
  "type": "bearer_token",
  "status": "active",
  "create_time": "2026-07-15T10:00:00.000000000Z",
  "update_time": "2026-07-15T10:00:00.000000000Z"
}
```

By default the proxy sends `Authorization: Bearer <token>`. Override
`header_name` and `prefix` to target a service that expects something else:

{% tabs %}
  {% tab filename="bearer_token.py" label="Python" %}
  ```py
  credential = client.credentials.create(
      id="my-api-key",
      type="bearer_token",
      token="key_xxxxxxxxxxxx",
      header_name="x-goog-api-key",
      prefix="",
  )
  ```

  {% /tab %}

  {% tab filename="bearer_token.js" label="JavaScript" %}
  ```javascript
  const credential = await client.credentials.create({
      id: "my-api-key",
      type: "bearer_token",
      token: "key_xxxxxxxxxxxx",
      header_name: "x-goog-api-key",
      prefix: "",
  });
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
      "google.golang.org/genai/interactions/models/credentials"
      "google.golang.org/genai/interactions/models/operations"
  )
  
  func main() {
      ctx := context.Background()
      client, err := genai.NewClient(ctx, &genai.ClientConfig{HTTPOptions: genai.HTTPOptions{APIVersion: "v1beta"}})
      if err != nil {
          log.Fatal(err)
      }
  
      res, err := client.Credentials.Create(ctx, operations.CreateCredentialRequest{
          Body: credentials.NewCredentialCreateParams(credentials.HTTPBearerConfig{
              ID:         "my-api-key",
              Token:      "key_xxxxxxxxxxxx",
              HeaderName: genai.Ptr("x-goog-api-key"),
              Prefix:     genai.Ptr(""),
          }),
      })
      if err != nil {
          log.Fatal(err)
      }
  
      fmt.Printf("Created credential: %s\n", res.Credential.ID)
  }
  ```

  {% /tab %}

  {% tab label="REST" %}
  ```shell
  curl -X POST "https://generativelanguage.googleapis.com/v1beta/credentials" \
  -H "Content-Type: application/json" \
  -H "x-goog-api-key: $GEMINI_API_KEY" \
  -d '{
      "id": "my-api-key",
      "type": "bearer_token",
      "token": "key_xxxxxxxxxxxx",
      "header_name": "x-goog-api-key",
      "prefix": ""
  }'
  ```

  {% /tab %}

  {% tab label="CLI" %}
  ```bash
  gemini-api credentials create --body '{
    "id": "my-api-key",
    "type": "bearer_token",
    "token": "key_xxxxxxxxxxxx",
    "header_name": "x-goog-api-key",
    "prefix": ""
  }'
  ```

  {% /tab %}

{% /tabs %}

This configuration produces the header `x-goog-api-key: key_xxxxxxxxxxxx`.

The following table shows how `header_name` and `prefix` combine:

| Configuration | Injected header |
| :--- | :--- |
| `{"token": "ghp_xxx"}` | `Authorization: Bearer ghp_xxx` |
| `{"token": "sk_live_xxx"}` | `Authorization: Bearer sk_live_xxx` |
| `{"token": "key_xxx", "header_name": "x-goog-api-key", "prefix": ""}` | `x-goog-api-key: key_xxx` |
| `{"token": "mytoken", "header_name": "X-API-Token", "prefix": ""}` | `X-API-Token: mytoken` |

### OAuth2  {% id="oauth2" %}

An OAuth2 credential requires `client_id`, `client_secret`, `refresh_token`,
and `token_url`. The `scopes` field is optional:

{% tabs %}
  {% tab filename="oauth2.py" label="Python" %}
  ```py
  credential = client.credentials.create(
      id="jira-oauth",
      type="oauth2",
      client_id="my-client-id",
      client_secret="my-client-secret",
      token_url="https://auth.atlassian.com/oauth/token",
      refresh_token="rt_xxxxxxxxxxxxxxxxxxxx",
      scopes=["read:jira-work", "write:jira-work"],
  )
  ```

  {% /tab %}

  {% tab filename="oauth2.js" label="JavaScript" %}
  ```javascript
  const credential = await client.credentials.create({
      id: "jira-oauth",
      type: "oauth2",
      client_id: "my-client-id",
      client_secret: "my-client-secret",
      token_url: "https://auth.atlassian.com/oauth/token",
      refresh_token: "rt_xxxxxxxxxxxxxxxxxxxx",
      scopes: ["read:jira-work", "write:jira-work"],
  });
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
      "google.golang.org/genai/interactions/models/credentials"
      "google.golang.org/genai/interactions/models/operations"
  )
  
  func main() {
      ctx := context.Background()
      client, err := genai.NewClient(ctx, &genai.ClientConfig{HTTPOptions: genai.HTTPOptions{APIVersion: "v1beta"}})
      if err != nil {
          log.Fatal(err)
      }
  
      res, err := client.Credentials.Create(ctx, operations.CreateCredentialRequest{
          Body: credentials.NewCredentialCreateParams(credentials.OAuth2Config{
              ID:           "jira-oauth",
              ClientID:     "my-client-id",
              ClientSecret: "my-client-secret",
              TokenURL:     "https://auth.atlassian.com/oauth/token",
              RefreshToken: "rt_xxxxxxxxxxxxxxxxxxxx",
              Scopes:       []string{"read:jira-work", "write:jira-work"},
          }),
      })
      if err != nil {
          log.Fatal(err)
      }
  
      fmt.Printf("Created OAuth2 credential: %s\n", res.Credential.ID)
  }
  ```

  {% /tab %}

  {% tab label="REST" %}
  ```shell
  curl -X POST "https://generativelanguage.googleapis.com/v1beta/credentials" \
  -H "Content-Type: application/json" \
  -H "x-goog-api-key: $GEMINI_API_KEY" \
  -d '{
      "id": "jira-oauth",
      "type": "oauth2",
      "client_id": "my-client-id",
      "client_secret": "my-client-secret",
      "token_url": "https://auth.atlassian.com/oauth/token",
      "refresh_token": "rt_xxxxxxxxxxxxxxxxxxxx",
      "scopes": ["read:jira-work", "write:jira-work"]
  }'
  ```

  {% /tab %}

  {% tab label="CLI" %}
  ```bash
  gemini-api credentials create --body '{
    "id": "jira-oauth",
    "type": "oauth2",
    "client_id": "my-client-id",
    "client_secret": "my-client-secret",
    "token_url": "https://auth.atlassian.com/oauth/token",
    "refresh_token": "rt_xxxxxxxxxxxxxxxxxxxx",
    "scopes": ["read:jira-work", "write:jira-work"]
  }'
  ```

  {% /tab %}

{% /tabs %}

Creating an OAuth2 credential performs a live token exchange against
`token_url` to confirm the configuration works. The credential is stored only
if the provider returns a successful token response containing an
`access_token`. Both JSON and form-urlencoded responses are accepted.

This means you need a valid, unexpired refresh token at creation time. If the
provider rejects the exchange, the error is returned to you:

```json
{
  "error": {
    "message": "OAuth token validation failed with HTTP 403: {\"error\":\"unauthorized_client\",\"error_description\":\"refresh_token is invalid\"}",
    "code": "invalid_request"
  }
}
```

Once stored, the proxy refreshes access tokens as they expire. If the provider
rotates refresh tokens and returns a new one during a refresh, the new token
replaces the stored one automatically.

### Environment variable  {% id="environment-variable" %}

An `environment_variable` credential requires `value` and `injection_location`:

{% tabs %}
  {% tab filename="environment_variable.py" label="Python" %}
  ```py
  credential = client.credentials.create(
      id="slack-bot-token",
      type="environment_variable",
      value="xoxb-xxxxxxxxxxxx-xxxxxxxxxxxx",
      trusted_domains=["*.slack.com", "slack.com"],
      injection_location="header",
  )
  ```

  {% /tab %}

  {% tab filename="environment_variable.js" label="JavaScript" %}
  ```javascript
  const credential = await client.credentials.create({
      id: "slack-bot-token",
      type: "environment_variable",
      value: "xoxb-xxxxxxxxxxxx-xxxxxxxxxxxx",
      trusted_domains: ["*.slack.com", "slack.com"],
      injection_location: "header",
  });
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
      "google.golang.org/genai/interactions/models/credentials"
      "google.golang.org/genai/interactions/models/operations"
  )
  
  func main() {
      ctx := context.Background()
      client, err := genai.NewClient(ctx, &genai.ClientConfig{HTTPOptions: genai.HTTPOptions{APIVersion: "v1beta"}})
      if err != nil {
          log.Fatal(err)
      }
  
      res, err := client.Credentials.Create(ctx, operations.CreateCredentialRequest{
          Body: credentials.NewCredentialCreateParams(credentials.EnvironmentVariableConfig{
              ID:                "slack-bot-token",
              Value:             "xoxb-xxxxxxxxxxxx-xxxxxxxxxxxx",
              TrustedDomains:    []string{"*.slack.com", "slack.com"},
              InjectionLocation: credentials.NewEnvironmentVariableConfigInjectionLocation(credentials.InjectionLocationEnumHeader),
          }),
      })
      if err != nil {
          log.Fatal(err)
      }
  
      fmt.Printf("Created environment variable credential: %s\n", res.Credential.ID)
  }
  ```

  {% /tab %}

  {% tab label="REST" %}
  ```shell
  curl -X POST "https://generativelanguage.googleapis.com/v1beta/credentials" \
  -H "Content-Type: application/json" \
  -H "x-goog-api-key: $GEMINI_API_KEY" \
  -d '{
      "id": "slack-bot-token",
      "type": "environment_variable",
      "value": "xoxb-xxxxxxxxxxxx-xxxxxxxxxxxx",
      "trusted_domains": ["*.slack.com", "slack.com"],
      "injection_location": "header"
  }'
  ```

  {% /tab %}

  {% tab label="CLI" %}
  ```bash
  gemini-api credentials create --body '{
    "id": "slack-bot-token",
    "type": "environment_variable",
    "value": "xoxb-xxxxxxxxxxxx-xxxxxxxxxxxx",
    "trusted_domains": ["*.slack.com", "slack.com"],
    "injection_location": "header"
  }'
  ```

  {% /tab %}

{% /tabs %}

The `injection_location` field tells the proxy where in the outbound request to
substitute the secret. It accepts `header`, `query`, or `body`, either as a
single string or as an array when a service needs more than one:

```json
"injection_location": ["header", "query"]
```

Substitution happens only in the locations you list. A request that carries the
placeholder anywhere else is rejected rather than sent on.

To bind the credential to a variable name, see
[Use credentials as environment variables](/docs/agent-credentials#environment-variables).

### Generated IDs  {% id="generated-ids" %}

The `id` field is optional. Omit it and the service generates a UUID:

```json
{
  "id": "9e545973-4330-49bb-9a44-930cea9fbe3c",
  "type": "bearer_token",
  "status": "active",
  "create_time": "2026-07-15T10:00:00.000000000Z",
  "update_time": "2026-07-15T10:00:00.000000000Z"
}
```

Supply your own ID when you want a stable, readable reference to use across
interactions. Since the ID appears in the resource path, prefer lowercase
alphanumerics with hyphens or underscores.

## List credentials  {% id="list-credentials" %}

List the credentials belonging to your project. Use pagination parameters to
control the response batch size.

{% tabs %}
  {% tab filename="list_credentials.py" label="Python" %}
  ```py
  response = client.credentials.list(page_size=10)
  for credential in response.credentials:
      print(f"Credential ID: {credential.id}, Type: {credential.type}")
  ```

  {% /tab %}

  {% tab filename="list_credentials.js" label="JavaScript" %}
  ```javascript
  const response = await client.credentials.list({ page_size: 10 });
  for (const credential of response.credentials) {
      console.log(`Credential ID: ${credential.id}, Type: ${credential.type}`);
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
  
      res, err := client.Credentials.List(ctx, operations.ListCredentialsRequest{
          PageSize: genai.Ptr(10),
      })
      if err != nil {
          log.Fatal(err)
      }
  
      for _, cred := range res.CredentialListResponse.Credentials {
          fmt.Printf("Credential ID: %s, Type: %v\n", cred.ID, cred.GetType())
      }
  }
  ```

  {% /tab %}

  {% tab label="REST" %}
  ```shell
  curl -X GET "https://generativelanguage.googleapis.com/v1beta/credentials?page_size=10" \
  -H "x-goog-api-key: $GEMINI_API_KEY"
  ```

  {% /tab %}

  {% tab label="CLI" %}
  ```bash
  gemini-api credentials list --page-size 10
  ```

  {% /tab %}

{% /tabs %}

The response contains metadata only:

```json
{
  "credentials": [
    {
      "id": "github-production",
      "type": "bearer_token",
      "status": "active",
      "create_time": "2026-07-15T10:00:00.000000000Z",
      "update_time": "2026-07-15T10:00:00.000000000Z"
    },
    {
      "id": "jira-oauth",
      "type": "oauth2",
      "status": "active",
      "create_time": "2026-07-15T10:05:00.000000000Z",
      "update_time": "2026-07-15T10:05:00.000000000Z"
    }
  ],
  "next_page_token": "Cj...5aE="
}
```

Pass `next_page_token` back as `page_token` to fetch the next page. The field
is omitted when there are no further results.

| Parameter | Type | Description |
| :--- | :--- | :--- |
| `page_size` | integer | Maximum number of credentials per page. |
| `page_token` | string | Token from the `next_page_token` of a previous response. |

## Get a credential  {% id="get-a-credential" %}

Retrieve metadata for a specific credential by its ID.

{% tabs %}
  {% tab filename="get_a_credential.py" label="Python" %}
  ```py
  credential = client.credentials.get(id="github-production")
  print(f"Credential ID: {credential.id}, Status: {credential.status}")
  ```

  {% /tab %}

  {% tab filename="get_a_credential.js" label="JavaScript" %}
  ```javascript
  const credential = await client.credentials.get("github-production");
  console.log(`Credential ID: ${credential.id}, Status: ${credential.status}`);
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
  
      res, err := client.Credentials.Get(ctx, operations.GetCredentialRequest{
          ID: "github-production",
      })
      if err != nil {
          log.Fatal(err)
      }
  
      fmt.Printf("Credential ID: %s, Status: %v\n", res.Credential.ID, res.Credential.GetStatus())
  }
  ```

  {% /tab %}

  {% tab label="REST" %}
  ```shell
  curl -X GET "https://generativelanguage.googleapis.com/v1beta/credentials/github-production" \
  -H "x-goog-api-key: $GEMINI_API_KEY"
  ```

  {% /tab %}

  {% tab label="CLI" %}
  ```bash
  gemini-api credentials get github-production
  ```

  {% /tab %}

{% /tabs %}

The response looks similar to the following:

```json
{
  "id": "github-production",
  "type": "bearer_token",
  "status": "active",
  "create_time": "2026-07-15T10:00:00.000000000Z",
  "update_time": "2026-08-01T14:30:00.000000000Z"
}
```

Requesting a credential that does not exist returns `404`:

```json
{
  "error": {
    "message": "Result not found.; GetCredential call failed",
    "code": "not_found"
  }
}
```

## Rotate a credential  {% id="rotate-a-credential" %}

Replace a secret without touching any allowlist rule, tool definition, or
environment variable that references it. Rotation takes effect on the next
proxy resolution.

The request must include `type`, plus the fields you want to change. Fields you
omit keep their current values.

Rotate a bearer token:

{% tabs %}
  {% tab filename="rotate_a_credential.py" label="Python" %}
  ```py
  credential = client.credentials.update(
      id="github-production",
      type="bearer_token",
      token="ghp_new_xxxxxxxxxxxxxxxxxxxx",
  )
  ```

  {% /tab %}

  {% tab filename="rotate_a_credential.js" label="JavaScript" %}
  ```javascript
  const credential = await client.credentials.update("github-production", {
      type: "bearer_token",
      token: "ghp_new_xxxxxxxxxxxxxxxxxxxx",
  });
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
      "google.golang.org/genai/interactions/models/credentials"
      "google.golang.org/genai/interactions/models/operations"
  )
  
  func main() {
      ctx := context.Background()
      client, err := genai.NewClient(ctx, &genai.ClientConfig{HTTPOptions: genai.HTTPOptions{APIVersion: "v1beta"}})
      if err != nil {
          log.Fatal(err)
      }
  
      res, err := client.Credentials.Update(ctx, operations.UpdateCredentialRequest{
          ID: "github-production",
          Body: credentials.NewCredentialUpdate(credentials.HTTPBearerUpdateConfig{
              Token: genai.Ptr("ghp_new_xxxxxxxxxxxxxxxxxxxx"),
          }),
      })
      if err != nil {
          log.Fatal(err)
      }
  
      fmt.Printf("Updated credential %s at %v\n", res.Credential.ID, res.Credential.GetUpdateTime())
  }
  ```

  {% /tab %}

  {% tab label="REST" %}
  ```shell
  curl -X PATCH "https://generativelanguage.googleapis.com/v1beta/credentials/github-production" \
  -H "Content-Type: application/json" \
  -H "x-goog-api-key: $GEMINI_API_KEY" \
  -d '{
      "type": "bearer_token",
      "token": "ghp_new_xxxxxxxxxxxxxxxxxxxx"
  }'
  ```

  {% /tab %}

  {% tab label="CLI" %}
  ```bash
  gemini-api credentials update github-production --body '{"type": "bearer_token", "token": "ghp_new_xxxxxxxxxxxxxxxxxxxx"}'
  ```

  {% /tab %}

{% /tabs %}

Rotate an OAuth2 refresh token:

{% tabs %}
  {% tab filename="rotate_a_credential.py" label="Python" %}
  ```py
  credential = client.credentials.update(
      id="jira-oauth",
      type="oauth2",
      refresh_token="rt_new_xxxxxxxxxxxxxxxxxxxx",
  )
  ```

  {% /tab %}

  {% tab filename="rotate_a_credential.js" label="JavaScript" %}
  ```javascript
  const credential = await client.credentials.update("jira-oauth", {
      type: "oauth2",
      refresh_token: "rt_new_xxxxxxxxxxxxxxxxxxxx",
  });
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
      "google.golang.org/genai/interactions/models/credentials"
      "google.golang.org/genai/interactions/models/operations"
  )
  
  func main() {
      ctx := context.Background()
      client, err := genai.NewClient(ctx, &genai.ClientConfig{HTTPOptions: genai.HTTPOptions{APIVersion: "v1beta"}})
      if err != nil {
          log.Fatal(err)
      }
  
      res, err := client.Credentials.Update(ctx, operations.UpdateCredentialRequest{
          ID: "jira-oauth",
          Body: credentials.NewCredentialUpdate(credentials.OAuth2UpdateConfig{
              RefreshToken: genai.Ptr("rt_new_xxxxxxxxxxxxxxxxxxxx"),
          }),
      })
      if err != nil {
          log.Fatal(err)
      }
  
      fmt.Printf("Updated credential %s at %v\n", res.Credential.ID, res.Credential.GetUpdateTime())
  }
  ```

  {% /tab %}

  {% tab label="REST" %}
  ```shell
  curl -X PATCH "https://generativelanguage.googleapis.com/v1beta/credentials/jira-oauth" \
  -H "Content-Type: application/json" \
  -H "x-goog-api-key: $GEMINI_API_KEY" \
  -d '{
      "type": "oauth2",
      "refresh_token": "rt_new_xxxxxxxxxxxxxxxxxxxx"
  }'
  ```

  {% /tab %}

  {% tab label="CLI" %}
  ```bash
  gemini-api credentials update jira-oauth --body '{"type": "oauth2", "refresh_token": "rt_new_xxxxxxxxxxxxxxxxxxxx"}'
  ```

  {% /tab %}

{% /tabs %}

The response reflects the new `update_time`:

```json
{
  "id": "jira-oauth",
  "type": "oauth2",
  "status": "active",
  "create_time": "2026-07-15T10:05:00.000000000Z",
  "update_time": "2026-08-01T14:30:00.000000000Z"
}
```

A credential's `type` is fixed at creation. To change it, delete the credential
and create a new one.

## Delete a credential  {% id="delete-a-credential" %}

Delete a credential and its stored secret when it is no longer needed.

{% tabs %}
  {% tab filename="delete_a_credential.py" label="Python" %}
  ```py
  client.credentials.delete(id="github-production")
  ```

  {% /tab %}

  {% tab filename="delete_a_credential.js" label="JavaScript" %}
  ```javascript
  await client.credentials.delete("github-production");
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
  
      _, err = client.Credentials.Delete(ctx, operations.DeleteCredentialRequest{
          ID: "github-production",
      })
      if err != nil {
          log.Fatal(err)
      }
  }
  ```

  {% /tab %}

  {% tab label="REST" %}
  ```shell
  curl -X DELETE "https://generativelanguage.googleapis.com/v1beta/credentials/github-production" \
  -H "x-goog-api-key: $GEMINI_API_KEY"
  ```

  {% /tab %}

  {% tab label="CLI" %}
  ```bash
  gemini-api credentials delete github-production
  ```

  {% /tab %}

{% /tabs %}

A successful delete returns an empty object:

```json
{}
```

Any allowlist rule, tool, or environment variable still referencing the ID will
fail to resolve, so update those first.

## Field reference  {% id="field-reference" %}

Fields common to every credential:

| Field | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `id` | string | No | Unique identifier. Generated as a UUID when omitted. |
| `type` | string | Yes | One of `bearer_token`, `oauth2`, `environment_variable`. |
| `status` | string | Read-only | Current status of the credential. |
| `create_time` | string | Read-only | RFC 3339 creation timestamp. |
| `update_time` | string | Read-only | RFC 3339 timestamp of the last update. |

Fields for `bearer_token`:

| Field | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `token` | string | Yes | Write-only. The token value. |
| `header_name` | string | No | Header to inject. Defaults to `Authorization`. |
| `prefix` | string | No | Value prefix. Defaults to `Bearer`. Set to `""` for none. |

Fields for `oauth2`:

| Field | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `client_id` | string | Yes | OAuth2 client ID. |
| `client_secret` | string | Yes | Write-only. OAuth2 client secret. |
| `refresh_token` | string | Yes | Write-only. Refresh token used to obtain access tokens. |
| `token_url` | string | Yes | Provider token endpoint. |
| `scopes` | array | No | OAuth scopes to request. |

Fields for `environment_variable`:

| Field | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `value` | string | Yes | Write-only. The secret value. |
| `injection_location` | string or array | Yes | Where to substitute the secret. One or more of `header`, `query`, `body`. |
| `trusted_domains` | array | No | Domain patterns authorized for substitution. |

## Errors  {% id="errors" %}

Errors return a JSON object with a `message` and a `code`:

```json
{
  "error": {
    "message": "Credential 'github-production' already exists.; CreateCredential call failed",
    "code": "aborted"
  }
}
```

| HTTP status | `code` | Cause |
| :--- | :--- | :--- |
| 400 | `invalid_request` | Missing required field, unknown field, unsupported `type`, or a failed OAuth2 validation. |
| 404 | `not_found` | No credential with that ID. |
| 409 | `aborted` | A credential with that ID already exists. |

Unknown fields are rejected rather than ignored, and the error names the field:

```json
{
  "error": {
    "message": "Unknown parameter 'headerName'. Did you mean 'header_name'?",
    "code": "invalid_request"
  }
}
```

## What's next  {% id="whats-next" %}

*   [Environments](/docs/agent-environment): Learn how agents run code and persist files.
*   [Agents Overview](/docs/agents): Learn about the core concepts of managed agents.
*   [Building Custom Agents](/docs/custom-agents): Define your own agents using `AGENTS.md` and `SKILL.md`.