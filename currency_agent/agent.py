import logging
import os

from dotenv import load_dotenv
from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, SseServerParams

logger = logging.getLogger(__name__)

load_dotenv()

SYSTEM_INSTRUCTION = (
    'You are a specialized assistant for currency conversions. '
    "Your sole purpose is to use the 'get_exchange_rate' tool to answer questions about currency exchange rates. "
    'If the user asks about anything other than currency conversion or exchange rates, '
    'politely state that you cannot help with that topic and can only assist with currency-related queries. '
    'Do not attempt to answer unrelated questions or use tools for other purposes.'
)

def create_agent() -> LlmAgent:
    """Constructs the ADK currency conversion agent."""
    logger.info("--- 🔧 Loading MCP tools from MCP Server... ---")
    logger.info("--- 🤖 Creating ADK Currency Agent... ---")
    return LlmAgent(
        model='gemini-2.0-flash-001',   
        name='currency_agent',
        description="An agent that can help with currency conversions",
        instruction=SYSTEM_INSTRUCTION,
        tools=[
            MCPToolset(
                connection_params=SseServerParams(
                    url=os.getenv('MCP_SERVER_URL', 'http://localhost:3000/sse')
                )
            )
        ],
    )
