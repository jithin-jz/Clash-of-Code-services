import os
import json
import logging

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from curriculum import get_skill_blueprint
from sandbox import verify_challenge

logger = logging.getLogger(__name__)

from config import settings
from llm_factory import LLMFactory

class AutoGenerator:
    def __init__(self):
        # We don't initialize a single LLM here anymore, 
        # as we might switch providers per request or on fallback.
        pass

    def _get_system_prompt(self):
        return """You are an expert Coding Mentor for absolute beginners.
Your task is to generate a fun, encouraging, and clear Python coding challenge.

CRITICAL REQUIREMENTS:
1. FOCUS: {topic}
2. CONCEPTS: {concepts}
3. DIFFICULTY: {difficulty}
4. FORMAT: You MUST output ONLY valid JSON. No conversational text.
5. SCHEMA:
{{
  "title": "Concise Technical Title",
  "slug": "lvl-{level}-short-name",
  "description": "Clear and direct instructions. What needs to be done.",
  "initial_code": "The starting code provided to the user. Use newlines.",
  "test_code": "Pytest-style assertions in check(scope) format. Use newlines, NO semicolons.",
  "reference_solution": "Simple solution. Use newlines.",
  "xp_reward": 50
}}

RULES:
- Level 1 MUST be a simple print task or basic calculation.
- Use clear, direct English.
- NEVER use semicolons to separate statements in 'test_code' or 'initial_code'.
- ALWAYS use actual newlines (`\\n` in JSON) for multiple statements.

TESTING INSTRUCTION (CRITICAL):
- The `test_code` MUST define a function named `check(scope)`.
- `scope` is a dictionary containing the user's defined variables and functions.
- DO NOT just write asserts at the top level. Wrap them in `check(scope)`.
- Correct Syntax Example:
  ```python
  def check(scope):
      assert 'var' in scope
      assert scope['var'] == 10
  ```
- Incorrect Syntax (DO NOT DO THIS):
  ```python
  import sys; def check(scope): pass
  ```
""";


    def generate_level(self, level_number: int, retry_count=0, user_id: int = None):
        blueprint = get_skill_blueprint(level_number)
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", self._get_system_prompt()),
            ("human", "Generate challenge for Level {level} using the blueprint.")
        ])
        
        # Generation Logic with Fallback
        result_content = None
        
        try:
            # 1. Try Primary LLM
            try:
                llm = LLMFactory.get_llm()
                chain = prompt | llm | StrOutputParser()
                response = chain.invoke({
                    "level": level_number,
                    "topic": blueprint["topic"],
                    "concepts": ", ".join(blueprint["concepts"]),
                    "difficulty": blueprint["difficulty"]
                })
                result_content = response
            except Exception as e:
                logger.warning(f"Primary LLM failed: {e}. Attempting fallback...")
                # 2. Try Fallback LLM
                llm = LLMFactory.get_fallback_llm()
                chain = prompt | llm | StrOutputParser()
                response = chain.invoke({
                    "level": level_number,
                    "topic": blueprint["topic"],
                    "concepts": ", ".join(blueprint["concepts"]),
                    "difficulty": blueprint["difficulty"]
                })
                result_content = response

            if not result_content:
                raise Exception("Both Primary and Fallback LLMs failed.")

            # Clean and Parse
            import re
            # Find the first { and last }
            match = re.search(r'(\{.*\})', result_content, re.DOTALL)
            if match:
                content = match.group(1)
            else:
                content = result_content.replace("```json", "").replace("```", "").strip()

            # Remove potential non-printable characters or literal newlines that break JSON
            # But keep valid spaces/newlines if they are escaped. 
            # Actually, standard json.loads handles escaped newlines.
            # It's the literal ones inside strings that are the problem.
            # We can't safely regex replace all newlines without breaking the structure.
            # But we can replace literal newlines that are NOT preceded by a backslash in a string... tricky.
            # Simpler: just replace common culprits if they are not escaped.
            
            try:
                # strict=False allows control characters like newlines in strings
                challenge_data = json.loads(content, strict=False)
            except json.JSONDecodeError as je:
                logger.warning(f"JSON Parse Error: {je}. Attempting aggressive cleanup...")
                # Cleanup: remove actual control characters except whitespace
                content = "".join(char for char in content if ord(char) >= 32 or char in "\n\r\t")
                challenge_data = json.loads(content, strict=False)

            # --- ENSURE NO BLANK REQUIRED FIELDS ---
            if not challenge_data.get("initial_code"):
                challenge_data["initial_code"] = "# Write your Python code here\n"
            if not challenge_data.get("title"):
                challenge_data["title"] = f"Level {level_number} Challenge"

            # --- NAMESPACE THE SLUG ---
            import uuid
            import re
            short_id = str(uuid.uuid4())[:8]
            raw_slug = challenge_data.get("slug", f"lvl-{level_number}")
            raw_slug = re.sub(r'[^a-zA-Z0-9-]', '', raw_slug.lower())
            
            if user_id:
                challenge_data["slug"] = f"{raw_slug}-u{user_id}-{short_id}"
            else:
                challenge_data["slug"] = f"{raw_slug}-{short_id}"

            # --- DOUBLE-LOOP VALIDATION ---
            logger.info(f"Validating Level {level_number} for User {user_id}...")
            verification = verify_challenge(
                challenge_data["reference_solution"], 
                challenge_data["test_code"]
            )
            
            is_ok = verification.get("passed", False)
            error = verification.get("error", "")
            
            # --- MODIFIED: ALLOW BYPASS IF PISTON IS DEAD ---
            if is_ok:
                logger.info(f"Level {level_number} VERIFIED.")
                return challenge_data
            elif "Sandbox not ready" in error or "Piston Error" in error:
                logger.warning(f"Piston Unavailable ({error}). Accepting Level {level_number} WITHOUT runtime verification.")
                return challenge_data
            else:
                logger.warning(f"Verification FAILED for Level {level_number}: {error}")
                if retry_count < 3:
                    logger.info(f"Retrying Level {level_number} (Attempt {retry_count + 1})...")
                    return self.generate_level(level_number, retry_count + 1, user_id)
                else:
                    raise Exception(f"Failed to generate a valid level after {retry_count} retries.")

        except Exception as e:
            logger.error(f"Error generating Level {level_number}: {str(e)}")
            if retry_count < 3:
                 return self.generate_level(level_number, retry_count + 1, user_id)
            raise

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    gen = AutoGenerator()
    data = gen.generate_level(1)
    print(json.dumps(data, indent=2))
