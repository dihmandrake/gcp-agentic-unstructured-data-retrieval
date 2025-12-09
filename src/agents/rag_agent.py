import vertexai
from vertexai.generative_models import GenerativeModel, Part, Tool, FunctionDeclaration
from src.agents.tools import search_knowledge_base
from src.shared.logger import setup_logger

logger = setup_logger(__name__)

class RAGAgent:
    """
    A Gemini-powered Agent for querying with a Search Tool, following ADK patterns with
    manual tool definition for Vertex AI SDK compatibility.
    """
    def __init__(self, project_id: str, vertex_ai_region: str, model_name: str = "gemini-2.0-flash-lite"):
        # 1. Initialize Vertex AI with a specific GCP region
        vertexai.init(project=project_id, location=vertex_ai_region)
        
        # 2. Manually define the tool as per Vertex AI SDK requirements
        search_tool = Tool(
            function_declarations=[
                FunctionDeclaration(
                    name="search_knowledge_base",
                    description="Searches the knowledge base to find information and answer user questions.",
                    parameters={
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "A detailed search query crafted from the user's question to find relevant information."
                            }
                        },
                        "required": ["query"]
                    }
                )
            ]
        )
        
        # 3. Initialize Model with Tools
        system_instruction = """You are a helpful AI assistant for the Nelly Hackathon.
Your knowledge comes exclusively from the "search_knowledge_base" tool.
ALWAYS use the "search_knowledge_base" tool to find information before answering.
If the user asks about "Nelly", "proposals", or "hackathons", you MUST search the knowledge base first.
Do not refuse to answer; try to search first."""

        self.model = GenerativeModel(
            model_name,
            tools=[search_tool],
            system_instruction=system_instruction
        )
        
        # 4. Start Chat Session
        self.chat = self.model.start_chat()
        logger.info(f"RAGAgent initialized with {model_name} model.")

    def ask(self, question: str) -> str:
        """
        Sends a query to the agent and returns the natural language response.
        """
        logger.info(f"User question: {question}")
        response = self.chat.send_message(question)
        
        # Gemini 2.0 might return Text + FunctionCall. We must find the function call part.
        function_call = None
        for part in response.candidates[0].content.parts:
            if part.function_call:
                function_call = part.function_call
                break
        
        # If we found a tool call, execute it
        if function_call:
            logger.info(f"Model called tool: {function_call.name} with args: {function_call.args}")
            
            if function_call.name == "search_knowledge_base":
                tool_result = search_knowledge_base(query=function_call.args["query"])
                
                # Send the tool result back to the model
                response = self.chat.send_message(
                    Part.from_function_response(
                        name="search_knowledge_base",
                        response={"content": tool_result}
                    )
                )

        # Now it is safe to get the final answer
        final_response = response.text
        logger.info(f"Agent final response: {final_response}")
        return final_response