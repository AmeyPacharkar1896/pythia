import google.generativeai as genai
from src.config import API_KEY
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
        # 1. Check for Mock Mode
        if MOCK_MODE:
            return self._get_mock_content(filename, file_ext)

        # 2. Real AI Logic
        system_instruction = self._get_persona(file_ext)
        full_prompt = (
            f"{system_instruction}\n"
            f"--------------------------------------------------\n"
            f"CONTEXT (Background Information):\n{context_str}\n"
            f"--------------------------------------------------\n"
            f"TASK: Write the code for a file named '{filename}'.\n"
            f"INSTRUCTIONS:\n"
            f"1. Use the variables/data from the CONTEXT above if relevant.\n"
            f"2. You MUST write valid {file_ext} code. Do NOT just copy the context text.\n"
            f"3. Example: If context says 'Port: 80', your Python code should be 'PORT = 80'.\n"
            f"4. Output ONLY the code. No markdown formatting (no ```)."
        )

        return self._call_ai(full_prompt, filename, action="generating logic")

    def refactor(self, filename, file_ext, current_content, instructions):
        # 1. Check for Mock Mode
        if MOCK_MODE:
            return current_content + f"\n\n# REFACTORED: {instructions}"

        # 2. Real AI Logic
        system_instruction = self._get_persona(file_ext)
        full_prompt = (
            f"{system_instruction}\n"
            f"--------------------------------------------------\n"
            f"TASK: The user wants to modify the file '{filename}'.\n"
            f"1. Read the CURRENT CONTENT below.\n"
            f"2. Follow the USER INSTRUCTIONS at the bottom.\n"
            f"3. Rewrite the FULL file with the changes applied.\n"
            f"4. REMOVE the user's instruction comment from the final output.\n"
            f"5. Output ONLY the code. No markdown.\n"
            f"--------------------------------------------------\n"
            f"CURRENT CONTENT:\n{current_content}\n"
            f"--------------------------------------------------\n"
            f"USER INSTRUCTIONS:\n{instructions}\n"
        )

        return self._call_ai(full_prompt, filename, action="refactoring")

    def visualize(self, target_filename, code_content):
        # 1. Check for Mock Mode
        if MOCK_MODE:
            return f'graph TD;\nA["{target_filename}"] --> B["Mock Diagram"];'

        # 2. Real AI Logic
        full_prompt = (
            f"You are a Systems Architect. Your goal is to visualize code logic.\n"
            f"--------------------------------------------------\n"
            f"TASK: Analyze the code below and generate a Mermaid.js diagram.\n"
            f"INSTRUCTIONS:\n"
            f"1. Use 'graph TD' (Top-Down) for flowcharts.\n"
            f"2. IMPORTANT: Wrap ALL node text in double quotes to prevent syntax errors.\n"
            f"   - BAD:  A[Start (Init)]\n"
            f"   - GOOD: A[\"Start (Init)\"]\n"
            f"3. Keep it simple and high-level (show relationships, not every line of code).\n"
            f"4. Output ONLY the mermaid code. No markdown blocks.\n"
            f"--------------------------------------------------\n"
            f"CODE TO ANALYZE ({target_filename}):\n{code_content}\n"
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