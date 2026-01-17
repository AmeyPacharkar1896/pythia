import time
import google.generativeai as genai
from typing import Optional, Dict, Any
from src.config import API_KEY, MOCK_MODE, MODEL_NAME, TEMPERATURE, MAX_RETRIES, RETRY_DELAY_BASE
from src.prompts import PERSONAS, DEFAULT_PERSONA, GENERATE_TEMPLATE, REFACTOR_TEMPLATE, VISUALIZE_TEMPLATE
from src.logger import logger

if not MOCK_MODE:
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel(
        MODEL_NAME, 
        generation_config=genai.GenerationConfig(temperature=TEMPERATURE)
    )

class Brain:
    def generate(self, filename: str, file_ext: str, context_str: str = "") -> str:
        if MOCK_MODE: return self._get_mock_content(filename, file_ext)

        persona: str = PERSONAS.get(file_ext, DEFAULT_PERSONA)
        full_prompt: str = GENERATE_TEMPLATE.format(
            system_instruction=persona,
            context_str=context_str,
            filename=filename,
            file_ext=file_ext
        )
        return self._call_ai(full_prompt, filename, action="generating logic")

    def refactor(self, filename: str, file_ext: str, content: str, instruction: str) -> str:
        if MOCK_MODE: return content + f"\n\n# REFACTORED: {instruction}"

        persona: str = PERSONAS.get(file_ext, DEFAULT_PERSONA)
        full_prompt: str = REFACTOR_TEMPLATE.format(
            system_instruction=persona,
            filename=filename,
            current_content=content,
            instructions=instruction
        )
        return self._call_ai(full_prompt, filename, action="refactoring")

    def visualize(self, target_filename: str, code_content: str) -> str:
        if MOCK_MODE: return f'graph TD;\nA["{target_filename}"] --> B["Mock Diagram"];'

        full_prompt: str = VISUALIZE_TEMPLATE.format(
            target_filename=target_filename,
            code_content=code_content
        )
        return self._call_ai(full_prompt, target_filename, action="visualizing")

    def _call_ai(self, prompt: str, filename: str, action: str = "processing") -> str:
        for attempt in range(MAX_RETRIES):
            try:
                logger.info(f"   🧠 Brain {action} for {filename}...")
                response = model.generate_content(prompt)
                return self._clean_text(response.text)
            except Exception as e:
                error_msg = str(e)
                if "429" in error_msg:
                    wait: int = RETRY_DELAY_BASE * (attempt + 1)
                    logger.warning(f"   ⏳ Rate limit. Cooling down for {wait}s...")
                    time.sleep(wait)
                else:
                    return f"# Error {action}: {e}"
        return "# Error: Failed after max retries."

    def _get_mock_content(self, filename: str, ext: str) -> str:
        logger.info(f"   🤖 [MOCK] Generating fake content for {filename}...")
        if ext == ".py":
            return f"def main():\n    print('Mock code for {filename}')\n\nif __name__ == '__main__':\n    main()"
        if ext == ".md":
            return f"# {filename}\nThis is mock documentation."
        if ext == ".html":
            return f"<html><body><h1>Mock {filename}</h1></body></html>"
        if ext == ".js":
            return f"console.log('Mock JS for {filename}');"
        return f"Mock content for {filename}"

    def _clean_text(self, text: str) -> str:
        if text.startswith("```"):
            parts = text.split("\n", 1)
            if len(parts) > 1:
                text = parts[1]
            if text.strip().endswith("```"):
                text = text.rsplit("```", 1)[0]
        return text