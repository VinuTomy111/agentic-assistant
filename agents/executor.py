import logging
from groq import Groq
from tools import AVAILABLE_TOOLS

class ExecutorAgent:
    def __init__(self, api_key: str):
        self.client = Groq(api_key=api_key)
        self.model = "openai/gpt-oss-120b"

    def execute_plan(self, plan: list, user_query: str) -> str:
        """
        Executes a sequence of steps planned by the Planner Agent.
        Calls the actual python tools and gathers their outputs.
        Then, synthesizes the final response.
        """
        execution_results = []
        
        if not plan:
            return "Planner did not generate any steps."
        
        # Step 1: Execute Tool Calls
        for step in plan:
             tool_name = step.get("tool")
             args = step.get("args", {})
             reasoning = step.get("reasoning", "")
             
             logging.info(f"Executing step {step.get('step_number')}: {tool_name} - Reason: {reasoning}")
             
             if tool_name and tool_name in AVAILABLE_TOOLS:
                 try:
                      # Unpack kwargs appropriately based on tool
                      tool_fn = AVAILABLE_TOOLS[tool_name]
                      result = tool_fn(**args)
                      execution_results.append(f"Tool `{tool_name}` output:\n{result}")
                 except Exception as e:
                      error_msg = f"Tool `{tool_name}` execution failed: {str(e)}"
                      logging.error(error_msg)
                      execution_results.append(error_msg)
             elif tool_name and tool_name.lower() != "none" and tool_name != "tool_name_or_none":
                 execution_results.append(f"Tool `{tool_name}` is not available.")
                 
        # Step 2: Synthesize Final Answer
        synthesis_prompt = """You are an intelligent Synthesizer Agent.
The user asked a query. Another agent laid out a plan and executed it using tools.
Below are the raw results from the tools.
Your task is to review the tool outputs and provide a final, cleanly formatted, and helpful answer to the user based ONLY on those execution results.
If there are no results, just answer the query naturally if you can, otherwise explain what failed.
"""
        
        compiled_results = "\n\n".join(execution_results)
        
        user_message = f"""
User Query: {user_query}

Execution Results:
{compiled_results}

Please formulate the final answer to the user.
"""
        
        try:
             response = self.client.chat.completions.create(
                 messages=[
                     {"role": "system", "content": synthesis_prompt},
                     {"role": "user", "content": user_message}
                 ],
                 model=self.model,
                 temperature=0.3
             )
             return response.choices[0].message.content or "No response synthesized."
        except Exception as e:
             error_msg = f"Failed to synthesize final answer: {str(e)}"
             logging.error(error_msg)
             return error_msg
