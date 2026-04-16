import json
import logging
from groq import Groq
from tools import TOOL_DESCRIPTIONS

class PlannerAgent:
    def __init__(self, api_key: str):
        self.client = Groq(api_key=api_key)
        self.model = "llama3-8b-8192" # Or an appropriate groq model like "mixtral-8x7b-32768"
        
    def plan(self, user_query: str, short_term_context: str, long_term_context: str) -> list:
        """
        Receives the user query and contexts, and breaks it down into actionable steps.
        Returns a list of dictionaries with step definition.
        """
        system_prompt = f"""You are an intelligent Planner Agent. 
Your job is to break down the user's request into a sequence of tool execution steps to fulfill the user's goal.
You have access to the following tools:
{TOOL_DESCRIPTIONS}

If the user request can be answered directly using the context provided or general knowledge (safely), you can emit a step to use no tools and just supply an answer.
Otherwise, formulate a plan.
Return ONLY valid JSON in the format:
{{
   "plan": [
      {{
         "step_number": 1,
         "tool": "tool_name_or_none",
         "args": {{ "arg1": "value1" }},
         "reasoning": "Why this tool is useful"
      }}
   ]
}}
"""
        
        user_message = f"""
Current User Request: {user_query}

Short Term Context:
{short_term_context}

Relevant Long Term Memory:
{long_term_context}
"""
        try:
             response = self.client.chat.completions.create(
                 messages=[
                     {"role": "system", "content": system_prompt},
                     {"role": "user", "content": user_message}
                 ],
                 model=self.model,
                 response_format={"type": "json_object"},
                 temperature=0.0
             )
             raw_content = response.choices[0].message.content
             plan_data = json.loads(raw_content)
             return plan_data.get("plan", [])
        except Exception as e:
             logging.error(f"Planner failed to create plan: {str(e)}")
             return []
