import asyncio

from fastmcp import Client

async def test_server():
    # Test already running Currency MCP server (port 9999)
    async with Client("http://localhost:9999/sse") as client:
        # List available tools
        tools = await client.list_tools()
        for tool in tools:
            print(f"--- 🛠️ Tool found: {tool.name} ---")
        # Call get_exchange_rate tool
        print("--- 🪛 Calling get_exchange_rate tool for USD to EUR ---")
        result = await client.call_tool("get_exchange_rate", {"currency_from": "USD", "currency_to": "EUR"})
        print(f"--- ✅ Success: {result[0].text} ---")

if __name__ == "__main__":
    asyncio.run(test_server())