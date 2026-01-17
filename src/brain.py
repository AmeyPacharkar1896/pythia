import google.generativeai as genai
from src.config import API_KEY

genai.configure(api_key=API_KEY)
# Using a slightly higher temperature for creativity, but strict prompts
model = genai.GenerativeModel(
    'gemini-2.5-flash',
    generation_config=genai.GenerationConfig(temperature=0.4)
)

class Brain:
    def generate(self, filename, file_ext, context_str=""):
        system_instruction = self._get_persona(file_ext)
        prompt_topic = filename.replace("_", " ").replace(file_ext, "")

        # 🚀 UPGRADED PROMPT: Forces the AI to convert data into code
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

        try:
            print(f"   🧠 Brain generating logic for {filename}...")
            response = model.generate_content(full_prompt)
            return self._clean_text(response.text)
        except Exception as e:
            return f"# Error generating content: {e}"

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
        # Removes markdown fences (```) so code is runnable
        if text.startswith("```"):
            text = text.split("\n", 1)[1]
            if text.strip().endswith("```"):
                text = text.rsplit("```", 1)[0]
        return text

    def refactor(self, filename, file_ext, current_content, instructions):
        """Rewrites an existing file based on user comments."""
        
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

        try:
            print(f"   🧠 Brain refactoring {filename}...")
            response = model.generate_content(full_prompt)
            return self._clean_text(response.text)
        except Exception as e:
            return f"# Error refactoring content: {e}"