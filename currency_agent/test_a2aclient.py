"""Direct A2A client for testing purposes."""

import asyncio
import os
import traceback

import httpx

from a2a.client import A2ACardResolver, ClientConfig, create_client
from a2a.helpers import display_agent_card, new_text_message
from a2a.types import Role, SendMessageRequest

AGENT_URL = os.getenv("AGENT_URL", "http://localhost:10000")


async def get_agent_card():
    """Get the agent card."""
    print(f"🔄 Fetching the agent card at {AGENT_URL}")

    async with httpx.AsyncClient() as httpx_client:
        resolver = A2ACardResolver(
            httpx_client=httpx_client,
            base_url=AGENT_URL,
        )
        public_agent_card = await resolver.get_agent_card()
        print("✅ Successfully fetched the agent card")
    return public_agent_card


async def send_message(text_query: str) -> None:
    """
    Send a text query to the agent and print the response.
    """
    public_agent_card = await get_agent_card()

    print("🔄 Initializing a non-streaming client")
    config = ClientConfig(streaming=False)
    client = await create_client(agent=public_agent_card, client_config=config)

    message = new_text_message(text_query, role=Role.ROLE_USER)
    print("Sending request:")
    request = SendMessageRequest(message=message)
    print(request)

    print("Response:")
    async for chunk in client.send_message(request):
        print(chunk)
    await client.close()


async def main() -> None:
    """Main function"""
       
    try:
        public_agent_card = await get_agent_card()
        display_agent_card(public_agent_card)
        await send_message("how much is 100 USD in GBP?")
    except Exception as e:
        traceback.print_exc()
        print(f"--- ❌ An error occurred: {e} ---")
        print("Ensure the agent server is running.")


if __name__ == "__main__":
    asyncio.run(main())
