import os
from anthropic import Anthropic

client = Anthropic(
    base_url="https://go2llm.tech",
    api_key=os.environ["GO2LLM_API_KEY"],
)

msg = client.messages.create(
    model="claude-opus-5",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Привет"}],
)
print(msg.usage)  # у шлюза там ещё cost_usd
