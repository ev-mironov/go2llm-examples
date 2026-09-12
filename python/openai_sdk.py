from openai import OpenAI

client = OpenAI(
    api_key="YOUR_API_KEY",
    base_url="https://go2llm.tech/v1",
)

response = client.chat.completions.create(
    model="gpt-5.6-sol",
    messages=[{"role": "user", "content": "Ответь: OK"}],
)

print(response.choices[0].message.content)
