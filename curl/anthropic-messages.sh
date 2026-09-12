#!/usr/bin/env bash
# Anthropic Messages protocol. Note: no /v1 in the base URL for SDKs;
# here the full path is explicit.
set -euo pipefail
curl https://go2llm.tech/v1/messages \
  -H "x-api-key: YOUR_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "content-type: application/json" \
  -d '{"model":"claude-sonnet-5","max_tokens":120,"messages":[{"role":"user","content":"Ответь одним словом: работает"}]}'
