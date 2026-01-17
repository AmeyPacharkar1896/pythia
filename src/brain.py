import google.generativeai as genai
from src.config import API_KEY
from src.prompts import PERSONAS, DEFAULT_PERSONA, GENERATE_TEMPLATE, REFACTOR_TEMPLATE, VISUALIZE_TEMPLATE
import time

# 🟢 CONFIG: Toggle this to True if you want to test without using API credits
MOCK_MODE = False 

if not MOCK_MODE:
    genai.configure(api_key=API_KEY)
    # Using 2.0-flash as the stable workhorse
    model = genai.GenerativeModel(
        'gemini-2.0-flash', 
        generation_config=genai.GenerationConfig(temperature=0.4)
    )

class Brain:
    def generate(self, filename, file_ext, context_str=""):
        if MOCK_MODE: return self._get_mock_content(filename, file_ext)

        persona = PERSONAS.get(file_ext, DEFAULT_PERSONA)
        full_prompt = GENERATE_TEMPLATE.format(
            system_instruction=persona,
            context_str=context_str,
            filename=filename,
            file_ext=file_ext
        )
        return self._call_ai(full_prompt, filename, action="generating logic")

    def refactor(self, filename, file_ext, content, instruction):
        if MOCK_MODE: return content + f"\n\n# REFACTORED: {instruction}"

        persona = PERSONAS.get(file_ext, DEFAULT_PERSONA)
        full_prompt = REFACTOR_TEMPLATE.format(
            system_instruction=persona,
            filename=filename,
            current_content=content,
            instructions=instruction
        )
        return self._call_ai(full_prompt, filename, action="refactoring")

    def visualize(self, target_filename, code_content):
        if MOCK_MODE: return f'graph TD;\nA["{target_filename}"] --> B["Mock Diagram"];'

        # 🟢 CLEANER
        full_prompt = VISUALIZE_TEMPLATE.format(
            target_filename=target_filename,
            code_content=code_content
        )
        return self._call_ai(full_prompt, target_filename, action="visualizing")

    def _call_ai(self, prompt, filename, action="processing"):
        """Helper to handle API calls with the robust retry logic."""
        max_retries = 3
        for attempt in range(max_retries):
            try:
                print(f"   🧠 Brain {action} for {filename}...")
                response = model.generate_content(prompt)
                return self._clean_text(response.text)
            
            except Exception as e:
                error_msg = str(e)
                if "429" in error_msg:
                    wait_time = 30 * (attempt + 1)
                    print(f"   ⏳ Rate limit hit. Cooling down for {wait_time}s...")
                    time.sleep(wait_time)
                else:
                    return f"# Error {action}: {e}"
        
        return "# Error: Failed after max retries."

    def _get_mock_content(self, filename, ext):
        print(f"   🤖 [MOCK] Generating fake content for {filename}...")
        if ext == ".py":
            return f"def main():\n    print('This is MOCK code for {filename}')\n\nif __name__ == '__main__':\n    main()"
        if ext == ".md":
            return f"# {filename}\nThis is mock documentation."
        if ext == ".html":
            return f"<html><body><h1>Mock {filename}</h1></body></html>"
        if ext == ".js":
            return f"console.log('Mock JS for {filename}');"
        return f"Mock content for {filename}"

    def _get_persona(self, ext):
        if ext == ".py": return "You are a Senior Python Engineer. Write clean, runnable code."
        if ext == ".html": return "You are a Frontend Developer. Write valid HTML5 with embedded CSS."
        if ext == ".css": return "You are a UI Designer. Write valid CSS rules."
        if ext == ".js": return "You are a JavaScript Expert. Write valid JS code."
        if ext == ".json": return "You are a Data Engineer. Output ONLY valid JSON."
        if ext == ".sql": return "You are a Database Admin. Write valid SQL queries."
        if ext == ".md": return "You are a Technical Writer. Use Markdown."
        return "You are a helpful AI assistant."

    def _clean_text(self, text):
        if text.startswith("```"):
            text = text.split("\n", 1)[1]
            if text.strip().endswith("```"):
                text = text.rsplit("```", 1)[0]
        return text