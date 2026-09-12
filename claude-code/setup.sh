#!/usr/bin/env bash
# ANTHROPIC_AUTH_TOKEN, not ANTHROPIC_API_KEY: if the machine has ever been
# logged into a personal claude.ai account, ANTHROPIC_API_KEY can lose to the
# stored login and the request silently goes to api.anthropic.com instead.
set -euo pipefail
unset ANTHROPIC_API_KEY
export ANTHROPIC_BASE_URL=https://go2llm.tech
export ANTHROPIC_AUTH_TOKEN=YOUR_API_KEY
export ANTHROPIC_MODEL=claude-sonnet-5
claude
