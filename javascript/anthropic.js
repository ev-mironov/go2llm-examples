import Anthropic from "@anthropic-ai/sdk";

const client = new Anthropic({
  apiKey: "YOUR_API_KEY",
  baseURL: "https://go2llm.tech",
});

const response = await client.messages.create({
  model: "claude-sonnet-5",
  max_tokens: 120,
  messages: [{ role: "user", content: "Скажи OK" }],
});

console.log(response.content);
