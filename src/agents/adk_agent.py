# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini
from src.agents.tools import search_knowledge_base
from google.genai import types

system_prompt = """
# TODO: HACKATHON CHALLENGE (Challenge 2, Part 1)
# The prompt below is static. Your goal is to implement a prompt router
# that dynamically selects a persona and instructions based on the user's query.
# For example, a query asking for a summary might use a "summarizer" persona,
# while a query asking for specific data points might use a "data extractor" persona.
# You can define different prompt strategies in a new module and then
# modify this agent to use a router to select one before executing the search.

# You are a Medical Records Analysis Bot.
# Your sole purpose is to find and summarize information from a database of SYNTHETIC medical records.
# The documents you have access to are NOT real patient data.

- When a user asks a question, you MUST use the `search_knowledge_base` tool to find relevant documents.
- Use the user's question as the query for the tool.
- Base your answer *exclusively* on the information returned by the tool.
- Do not use any prior knowledge.
- If the tool returns no relevant information, state that you could not find any information in the documents.
- Do not answer questions that are not related to the content of the documents.
"""

model_config = Gemini(
    model="gemini-2.0-flash-lite",
)

import os

app_name = os.getenv("APP_NAME", "GenAI-RAG").lower().replace(" ", "_").replace("-", "_")

agent_config = Agent(
    name=f"{app_name}_agent",
    model=model_config,
    instruction=system_prompt,
    generate_content_config=types.GenerateContentConfig(temperature=0),
    tools=[search_knowledge_base],
)