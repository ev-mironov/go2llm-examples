# go2llm-examples

Working integration examples for [go2llm](https://go2llm.tech) — a single API
gateway to current AI models with Anthropic- and OpenAI-compatible endpoints.

Every example in this repo is a complete, runnable file. Copy one, set your key,
run it.

## What this is

go2llm exposes two wire protocols on one key and one balance:

| Protocol | Endpoint | Base URL to configure |
|---|---|---|
| Anthropic Messages | `POST /v1/messages` | `https://go2llm.tech` (no `/v1`) |
| OpenAI Chat Completions | `POST /v1/chat/completions` | `https://go2llm.tech/v1` |
| Image generation | `POST /v1/images/generations` | `https://go2llm.tech/v1` |

Two public endpoints need no key at all:

```bash
curl https://go2llm.tech/v1/models     # published models, modalities, endpoints
curl https://go2llm.tech/api/pricing   # public per-model pricing + catalog version
```

`GET /v1/models` is the source of truth for model IDs. Anything in this README
is a snapshot; that endpoint is live.

**Not available:** Responses API (`/v1/responses`), embeddings, image edits,
video, audio. Text endpoints reject images, PDFs and binary input with
`400 unsupported_content_type`.

## Quick start

Get a key at [go2llm.tech](https://go2llm.tech). Keys look like `gk_sk_...`.
Registration credits $1 to the balance, which is enough for a first request
without topping up.

```bash
export GO2LLM_API_KEY=gk_sk_your_key_here
```

### curl — Anthropic Messages

```bash
curl https://go2llm.tech/v1/messages \
  -H "x-api-key: $GO2LLM_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "content-type: application/json" \
  -d '{"model":"claude-sonnet-5","max_tokens":120,
       "messages":[{"role":"user","content":"Reply with one word: works"}]}'
```

### curl — OpenAI Chat Completions

```bash
curl https://go2llm.tech/v1/chat/completions \
  -H "Authorization: Bearer $GO2LLM_API_KEY" \
  -H "content-type: application/json" \
  -d '{"model":"gpt-5.6-sol","max_tokens":120,
       "messages":[{"role":"user","content":"Reply with one word: works"}]}'
```

### Python — OpenAI SDK

```python
from openai import OpenAI

client = OpenAI(
    api_key="YOUR_API_KEY",
    base_url="https://go2llm.tech/v1",
)

response = client.chat.completions.create(
    model="gpt-5.6-sol",
    messages=[{"role": "user", "content": "Reply: OK"}],
)

print(response.choices[0].message.content)
```

### Python — Anthropic SDK

```python
import os
from anthropic import Anthropic

client = Anthropic(
    base_url="https://go2llm.tech",
    api_key=os.environ["GO2LLM_API_KEY"],
)

msg = client.messages.create(
    model="claude-opus-5",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello"}],
)

print(msg.usage)  # includes cost_usd for this request
```

### TypeScript — OpenAI SDK, streaming

```typescript
import OpenAI from "openai";

const client = new OpenAI({
  baseURL: "https://go2llm.tech/v1",
  apiKey: process.env.GO2LLM_API_KEY,
});

const stream = await client.chat.completions.create({
  model: "gpt-5.6-sol",
  stream: true,
  messages: [{ role: "user", content: "Generate SQL" }],
});

for await (const chunk of stream) {
  process.stdout.write(chunk.choices[0]?.delta?.content ?? "");
}
```

### JavaScript — Anthropic SDK

```javascript
import Anthropic from "@anthropic-ai/sdk";

const client = new Anthropic({
  apiKey: "YOUR_API_KEY",
  baseURL: "https://go2llm.tech",
});

const response = await client.messages.create({
  model: "claude-sonnet-5",
  max_tokens: 120,
  messages: [{ role: "user", content: "Say OK" }],
});

console.log(response.content);
```

### Claude Code

```bash
export ANTHROPIC_BASE_URL=https://go2llm.tech
export ANTHROPIC_AUTH_TOKEN=YOUR_API_KEY
export ANTHROPIC_MODEL=claude-sonnet-5
claude
```

**Use `ANTHROPIC_AUTH_TOKEN`, not `ANTHROPIC_API_KEY`.** If the machine already
has a Claude Code login (claude.ai or Anthropic Console), `ANTHROPIC_API_KEY` can
lose to the stored credential, the request never reaches `ANTHROPIC_BASE_URL`,
and you get a 401 that looks like a bad key. `ANTHROPIC_AUTH_TOKEN` always
authenticates against the configured base URL.

Note the base URL has **no** `/v1` — the SDK appends the path itself.

### OpenCode — `opencode.json`

```json
{
  "provider": {
    "go2llm": {
      "npm": "@ai-sdk/openai-compatible",
      "name": "go2llm",
      "options": { "baseURL": "https://go2llm.tech/v1" },
      "models": { "claude-sonnet-5": {}, "gpt-5.6-sol": {} }
    }
  }
}
```

```bash
opencode run "..." -m go2llm/claude-sonnet-5
```

### Image generation

`Idempotency-Key` is required for image requests: 8–128 printable ASCII
characters, body up to 20 MiB, `response_format: "url"`.

```bash
curl https://go2llm.tech/v1/images/generations \
  -H "Authorization: Bearer $GO2LLM_API_KEY" \
  -H "Idempotency-Key: project-20260911-image-001" \
  -H "content-type: application/json" \
  -d '{"model":"gpt-image-2","prompt":"Minimal diagram of an API gateway",
       "n":1,"size":"1024x1024","quality":"standard","response_format":"url"}'
```

## Tool compatibility

Honest status, not a checkbox table:

| Tool | Protocol | Status |
|---|---|---|
| Claude Code | Anthropic Messages | Verified with a live request |
| OpenCode | OpenAI Chat Completions | Verified with a live request |
| Kilo Code | OpenAI Chat Completions | Per documentation, not tested by us |
| Cline / Roo Code / Continue.dev / Aider | OpenAI Chat Completions | Works if the client accepts a custom base URL |
| **Codex CLI** | — | **Does not connect.** See below |

### Why Codex CLI does not work

Current Codex CLI versions configure custom providers through `model_providers`
in `~/.codex/config.toml`, and only support `wire_api = "responses"` — the OpenAI
Responses API format. `wire_api = "chat"` is rejected by Codex itself as no
longer supported. go2llm has no `/v1/responses` endpoint, so Codex gets a `404`.

Use a Chat Completions client (Cline, Aider, Continue, OpenCode, Roo Code) or an
Anthropic Messages client (Claude Code) instead.

## Pricing

There used to be a price table here. It went stale, quoted four model IDs that
no longer exist, and understated several real prices — which is exactly what a
hand-maintained table does between edits. Read the catalogue instead:

```bash
./python/pricing_table.py              # every published model, cheapest blended first
./python/pricing_table.py anthropic    # filter by family or model id
```

The script needs no key and no dependencies, and it prints the catalogue version
and timestamp it read, so you always know how fresh the answer is. The raw
document is `GET /api/pricing`; image models appear there too, billed per image
rather than per token.

### How to compare the numbers properly

A coding agent's billed token profile is roughly 10% input, 5% output, 85% cache
reads, because the agent resubmits its whole context every turn. So the number
that decides your bill is the blended price, not the input column:

```
blended = in × 0.10 + out × 0.05 + cache × 0.85
```

`pricing_table.py` sorts by exactly that, using the weights the catalogue itself
publishes in `comparisonProfile` — so the ranking you see is the ranking the
gateway used, not one we invented for the README. A provider that looks cheapest
on input alone routinely lands mid-table once cache reads are counted.

## Billing behavior

- Pay-as-you-go only. No subscriptions, no packages, no monthly minimum.
- The gateway reserves an estimated cost before the call, charges the actual
  cost afterwards, and releases the remainder. **The balance never goes below zero.**
- Every response carries `usage.cost_usd` — including the final usage block of an
  SSE stream.

## Per-key controls

Each key can carry a dollar quota, an allow-list of models, an IP allow-list, an
expiry date, and a rate limit (20 RPM by default). A key with quota `0` has no
separate limit — its spend is bounded only by the account balance.

## Error codes

| HTTP | `error.code` | What to do |
|---|---|---|
| 400 | `invalid_request` | Check JSON and required fields |
| 400 | `unsupported_content_type` | Remove image/audio/video/PDF from a text request |
| 400 | `model_protocol_mismatch` | Take the endpoint from `GET /v1/models` |
| 401 | `no-key` | Pass a valid key |
| 402 | `insufficient_balance` | Top up, or lower `max_tokens` |
| 403 | `model` / `inactive` / `expired` / `ip` | Check the key's settings |
| 404 | `model_not_found` | Copy the exact model ID from `GET /v1/models` |
| 409 | `idempotency_conflict` | Do not reuse an `Idempotency-Key` for a different body |
| 429 | `quota` / `rate_limit` | Check quota; honor `Retry-After` |
| 502 | `upstream_unavailable` | Retry a safe text request with backoff |
| 503 | `product_paused` / `no_eligible_route` | Check `/status`, retry later |

Errors carry `error.type`, `error.code`, `error.message`, `error.request_id`.

Two cases worth special handling in your client:

- A `404` on `/v1/responses` means protocol incompatibility, not a key problem.
- A media request that failed with `ambiguous_upstream_result` **must not** be
  retried automatically — the upstream may have accepted it.

## Streaming and fallback

Availability depends on external providers. Before the response begins, the
gateway may use a compatible fallback route on permitted error classes.
**After the first byte or the first valid SSE event, no switching happens** — and
a stream cannot be safely retried once you have received a valid chunk, because
the model has already started producing output.

## Repository layout

```
curl/         anthropic-messages.sh, openai-chat-completions.sh,
              list-models.sh, images.sh
python/       openai_sdk.py, anthropic_sdk.py, pricing_table.py
typescript/   streaming.ts
javascript/   anthropic.js
claude-code/  setup.sh
opencode/     opencode.json
```

## Standalone snippets

Single-file answers to the problems people hit first. Each one runs on its own
and works against any compatible endpoint, not only ours.

- [429 `rate_limit_error`: Retry-After before backoff, with full jitter](https://gist.github.com/ev-mironov/798e9f5cb57a756719d48faac1ad43c4)
- [401 `authentication_error` / `invalid x-api-key`: separate the six causes](https://gist.github.com/ev-mironov/aeb46e8c2c5eae909a0c39dbf0b7b60e)
- [n8n: importable HTTP Request workflow, because the OpenAI node has no Base URL field](https://gist.github.com/ev-mironov/67adba860b083d668f80d74e4ac7e27e)
- [Custom base URL in Claude Code, OpenCode, Zed, Continue.dev, Roo/Kilo Code, Open WebUI](https://gist.github.com/ev-mironov/c29b1c07696f482d8e60e003986f7f31)

## Links

- Site: https://go2llm.tech
- Docs: https://go2llm.tech/docs
- Pricing: https://go2llm.tech/pricing
- Status: https://go2llm.tech/status
- Error reference: https://go2llm.tech/en/errors
- Client setup guides: https://go2llm.tech/tools
- Support: support@go2llm.tech · Telegram `@go2llm_support`

## License

MIT. See [LICENSE](LICENSE).
````

---
