from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini
from src.agents.tools import search_knowledge_base
from google.genai import types

system_prompt = """
# =================================================================================================
# TODO: HACKATHON CHALLENGE (Pillar 1: Completeness)
#
# The current system prompt provides a basic persona. Your challenge is to enhance it to make the
# agent more robust, reliable, and aligned with specific use cases (e.g., a medical assistant,
# a customer service bot, a technical support agent).
#
# REQUIREMENTS:
#   1. PERSONA: Give the agent a more specific and detailed persona. Consider:
#      - What is its role (e.g., "You are a highly experienced medical assistant...")?
#      - What are its core competencies or areas of expertise?
#      - What is its tone and communication style (e.g., "...always respond with empathy and clarity.")?
#   2. STRICT INSTRUCTIONS:
#      - Add explicit rules or constraints to guide the agent's behavior.
#      - How should it handle ambiguous queries? What if information is missing?
#      - Should it ask clarifying questions? Should it refuse to answer certain types of questions?
#      - Emphasize the importance of using the `search_knowledge_base` tool and citing sources.
#
# HINT: Think about edge cases and how a human expert in this persona would behave.
# =================================================================================================

You are a helpful AI assistant.
Your knowledge comes exclusively from the documents provided to you via the "search_knowledge_base" tool.
You must ALWAYS use the "search_knowledge_base" tool to find information before answering any question.
Do not rely on any prior knowledge."""

model_config = Gemini(
    model="gemini-2.0-flash-lite",
)

agent_config = Agent(
    import os

app_name = os.getenv("APP_NAME", "GenAI-RAG").lower().replace(' ', '_')
name=f"{app_name}_agent",
    model=model_config,
    instruction=system_prompt,
    generate_content_config=types.GenerateContentConfig(temperature=0),
    tools=[search_knowledge_base],
)