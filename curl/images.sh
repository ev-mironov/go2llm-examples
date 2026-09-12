#!/usr/bin/env bash
# Idempotency-Key makes a retry safe: the same key returns the same image
# instead of generating — and charging for — a second one.
set -euo pipefail
curl https://go2llm.tech/v1/images/generations \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Idempotency-Key: project-20260911-image-001" \
  -H "content-type: application/json" \
  -d '{"model":"gpt-image-2","prompt":"Минималистичная схема API-шлюза","n":1,"size":"1024x1024","quality":"standard","response_format":"url"}'
