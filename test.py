from dotenv import load_dotenv
import asyncio

load_dotenv()
from src.agents.multi_agent.flow import app


async def main():
    while True:
        prompt = ""
        name = ""
        response = await app.ainvoke(
            input={
                "messages": [
                    {"role": "user", "content": input("Enter your message: ")},
                ],
            },
            config={
                "configurable": {
                    "thread_id": "1",
                }
            },
        )
        print("====================")
        print(response["messages"][-1].content)


if __name__ == "__main__":
    asyncio.run(main())
