import logging
import os

from dotenv import load_dotenv
from google.adk.agents import LlmAgent
from google.adk.tools.agent_tool import AgentTool
from google.adk.agents.remote_a2a_agent import RemoteA2aAgent, AGENT_CARD_WELL_KNOWN_PATH

logger = logging.getLogger(__name__)
logging.basicConfig(format="[%(levelname)s]: %(message)s", level=logging.INFO)

load_dotenv()

SYSTEM_INSTRUCTION = (
    "You are a helpful travel assistant. You help users plan trips, recommend places, "
    "and answer travel-related questions. "
    "Whenever a user asks about currency exchange rates or money conversions, "
    "delegate the request to the 'currency_agent' sub-agent."
)

CURRENCY_AGENT_URL = os.getenv("CURRENCY_AGENT_URL", "http://localhost:10000")

logger.info(
    "--- 🔗 Connecting to Remote A2A Currency Agent at %s... ---",
    CURRENCY_AGENT_URL,
)

currency_remote_agent = RemoteA2aAgent(
    name="currency_agent",
    agent_card=f"{CURRENCY_AGENT_URL}{AGENT_CARD_WELL_KNOWN_PATH}",
    description="An agent that can help with currency conversions and exchange rates.",
)

logger.info("--- 🤖 Creating ADK Travel Agent... ---")

root_agent = LlmAgent(
    model="gemini-3.7-flash",
    name="travel_agent",
    description="A travel assistant that can help plan trips and convert currencies via the remote currency agent.",
    instruction=SYSTEM_INSTRUCTION,
    tools=[AgentTool(agent=currency_remote_agent)],
)
