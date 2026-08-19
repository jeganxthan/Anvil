from openai import AsyncOpenAI
import asyncio
import os


async def main():

    client = AsyncOpenAI(
        base_url="https://integrate.api.nvidia.com/v1",
        api_key=os.environ["NVIDIA_NIM_API_KEY"],
    )

    response = await client.chat.completions.create(
        model="meta/llama-3.3-70b-instruct",
        messages=[
            {
                "role": "user",
                "content": "Say hello in one sentence.",
            }
        ],
        temperature=0.2,
        top_p=0.7,
        max_tokens=32,
        stream=False,
    )

    print(response.choices[0].message.content)


if __name__ == "__main__":
    asyncio.run(main())