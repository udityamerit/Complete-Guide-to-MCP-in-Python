from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
import asyncio
import traceback
import json
import os
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI



BASE_DIR = Path(__file__).parent

env_path = BASE_DIR / ".env"

print("=" * 60)
print("Current Working Directory:", os.getcwd())
print("Script Directory:", BASE_DIR)
print("Looking for .env at:", env_path)
print("=" * 60)

load_dotenv(env_path)

api_key = os.getenv("OPENAI_API_KEY")

print("API Key Loaded:", bool(api_key))

if not api_key:
    raise ValueError(
        f"OPENAI_API_KEY not found.\n"
        f"Expected .env file at:\n{env_path}"
    )



server_path = BASE_DIR / "server.py"

print("Server Path:", server_path)
print("Server Exists:", server_path.exists())

if not server_path.exists():
    raise FileNotFoundError(
        f"server.py not found at:\n{server_path}"
    )

server_params = StdioServerParameters(
    command="uv",
    args=["run", str(server_path)]
)



async def run(query):

    try:

        print("\nStarting stdio_client...")

        async with stdio_client(server_params) as (read, write):

            print("Client connected successfully.")

            async with ClientSession(read, write) as session:

                print("Initializing MCP Session...")

                await session.initialize()

                print("Session Initialized Successfully")

             

                tools_result = await session.list_tools()

                print("\nAvailable Tools:")

                for tool in tools_result.tools:
                    print(f"  - {tool.name}")

                

                openai_tools = []

                for tool in tools_result.tools:

                    openai_tools.append(
                        {
                            "type": "function",
                            "function": {
                                "name": tool.name,
                                "description": tool.description,
                                "parameters": tool.inputSchema,
                            },
                        }
                    )

                client = OpenAI(api_key=api_key)

                messages = [
                    {
                        "role": "user",
                        "content": query,
                    }
                ]

                print("\nSending Query:")
                print(query)


                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=messages,
                    tools=openai_tools,
                    tool_choice="auto",
                )

                assistant_message = response.choices[0].message

                messages.append(assistant_message)

              

                if assistant_message.tool_calls:

                    print("\nTool Call Requested")

                    for tool_call in assistant_message.tool_calls:

                        tool_name = tool_call.function.name

                        arguments = json.loads(
                            tool_call.function.arguments
                        )

                        print("\nExecuting Tool:", tool_name)
                        print("Arguments:", arguments)

                        result = await session.call_tool(
                            tool_name,
                            arguments=arguments
                        )

                        tool_output = result.content[0].text

                        print("Tool Output:", tool_output)

                        messages.append(
                            {
                                "role": "tool",
                                "tool_call_id": tool_call.id,
                                "content": tool_output,
                            }
                        )

                    

                    response = client.chat.completions.create(
                        model="gpt-4o",
                        messages=messages,
                    )

                    return response.choices[0].message.content

                else:

                    return assistant_message.content

    except Exception as e:

        print("\n" + "=" * 60)
        print("ERROR OCCURRED")
        print("=" * 60)

        print("Error Type:", type(e).__name__)
        print("Error Message:", str(e))

        traceback.print_exc()

        return None



if __name__ == "__main__":

    query = "What's the weather in California?"

    result = asyncio.run(run(query))

    print("\n" + "=" * 60)
    print("FINAL RESPONSE")
    print("=" * 60)

    print(result)

