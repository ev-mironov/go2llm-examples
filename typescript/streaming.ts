import OpenAI from "openai";

const client = new OpenAI({
  baseURL: "https://go2llm.tech/v1",
  apiKey: process.env.GO2LLM_API_KEY,
});

const stream = await client.chat.completions.create({
  model: "gpt-5.6-sol",
  stream: true,
  messages: [{ role: "user", content: "Сгенерируй SQL" }],
});

for await (const chunk of stream) {
  process.stdout.write(chunk.choices[0]?.delta?.content ?? "");
}
