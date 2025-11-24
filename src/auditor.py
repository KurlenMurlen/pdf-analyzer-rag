from typing import Any, Dict, List, Optional
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_core.language_models import BaseChatModel
import re
import json
import logging

logger = logging.getLogger(__name__)

def clean_json_output(text: str) -> Any:
    """
    Cleans the LLM output to ensure it's valid JSON.
    Uses a brace counter to extract the first valid JSON object.
    """
    # If the input is not a string (e.g. AIMessage), get the content
    if hasattr(text, 'content'):
        text = text.content
    
    logger.info(f"DEBUG: Raw LLM Output:\n{text}")
        
    # Remove markdown code blocks
    text = re.sub(r'```json\s*', '', text)
    text = re.sub(r'```\s*', '', text)
    
    # Attempt to extract JSON using brace counting
    try:
        start_index = text.find('{')
        if start_index != -1:
            brace_count = 0
            for i, char in enumerate(text[start_index:], start=start_index):
                if char == '{':
                    brace_count += 1
                elif char == '}':
                    brace_count -= 1
                    if brace_count == 0:
                        # Found the matching closing brace
                        potential_json = text[start_index:i+1]
                        # Validate if it loads
                        return json.loads(potential_json) 
    except Exception as e:
        logger.warning(f"Brace counting extraction failed: {e}")

    # Fallback: Return raw text wrapped in a dict if JSON parsing fails
    # This handles cases where the LLM returns plain text (e.g. a summary) instead of JSON.
    return {"analysis_result": text}

class AuditorAgent:
    def __init__(self, llm: BaseChatModel, retriever):
        self.llm = llm
        self.retriever = retriever

    def format_docs(self, docs):
        return "\n\n".join([d.page_content for d in docs])

    def get_chain(self, system_prompt_text: str):
        # Define the prompt
        # We inject the user's system prompt directly.
        # We enforce JSON output in the system prompt instructions.
        
        full_system_prompt = f"""You are an expert AI Auditor.
        
        USER INSTRUCTIONS:
        {system_prompt_text}
        
        STRICT OUTPUT RULES:
        1. Output ONLY a valid JSON object.
        2. Use the exact field names requested in the User Instructions as JSON keys (e.g., if asked for 'budget', create a "budget" key).
        3. If multiple fields are requested, ensure they are SEPARATE keys in the JSON. Do NOT combine them.
        4. If the user requested a summary without specifying fields, use "summary" as the key.
        5. Do NOT include markdown formatting (no ```json).
        6. Do NOT include introductory text.
        """
        
        human_template = """Context information is below:
        
        --- START OF CONTEXT ---
        {context}
        --- END OF CONTEXT ---
        
        User Query: {query}
        
        Based on the context above, please answer the user query and return the result in JSON format."""
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", full_system_prompt),
            ("human", human_template)
        ])

        # Debug step to print context
        def debug_context(inputs):
            ctx = inputs['context']
            logger.info(f"DEBUG: Context Length: {len(ctx)} chars")
            return inputs

        # Define the chain using LCEL
        chain = (
            {
                "context": self.retriever | self.format_docs, 
                "query": RunnablePassthrough()
            }
            | RunnableLambda(debug_context)
            | prompt
            | self.llm
            | RunnableLambda(clean_json_output)
        )
        
        return chain

    def audit_project(self, query: str, system_prompt: str):
        """
        Runs the audit chain. 
        query: The specific question or instruction from the user.
        system_prompt: The persona or rules for the AI.
        """
        # Combine query and system_prompt for retrieval to ensure we find relevant sections
        # (e.g. if prompt asks for "Budget", we want to search for "Budget" in the docs)
        combined_search = f"{query}\n\nContext to look for: {system_prompt}"
        
        chain = self.get_chain(system_prompt)
        # We pass the combined search to the chain. 
        # The retriever will use it to find docs, and it will be passed as {query} to the prompt.
        result = chain.invoke(combined_search)
        return result

