#!/usr/bin/env bash
set -euo pipefail
curl https://go2llm.tech/v1/chat/completions \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "content-type: application/json" \
  -d '{"model":"gpt-5.6-sol","max_tokens":120,"messages":[{"role":"user","content":"Ответь одним словом: работает"}]}'
