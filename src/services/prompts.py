# src/prompts.py

# 🎭 SYSTEM PERSONAS
# Maps file extensions to specific AI roles
PERSONAS = {
    ".py": "You are a Senior Python Engineer. Write clean, runnable code, including error handling where appropriate.",
    ".html": "You are a Frontend Developer. Write valid HTML5 with embedded CSS for a modern, responsive look.",
    ".css": "You are a UI Designer. Write clean, modular CSS rules.",
    ".js": "You are a JavaScript Expert. Write valid, modern ES6+ code.",
    ".json": "You are a Data Engineer. Output ONLY valid, strictly structured JSON data.",
    ".sql": "You are a Database Administrator. Write efficient, valid SQL queries.",
    ".md": "You are a Technical Writer. Use Markdown with clear headers, lists, and code blocks.",
    ".mermaid": "You are a Systems Architect. You specialize in visualizing logic."
}

DEFAULT_PERSONA = "You are a helpful AI assistant."

# 📝 TASK TEMPLATES

# 1. Generation (Creating new files)
GENERATE_TEMPLATE = """
{system_instruction}
--------------------------------------------------
CONTEXT (Background Information):
{context_str}
--------------------------------------------------
TASK: Write the code for a file named '{filename}'.
INSTRUCTIONS:
1. Use the variables/data from the CONTEXT above if relevant.
2. You MUST write valid {file_ext} code. Do NOT just copy the context text.
3. Example: If context says 'Port: 80', your Python code should be 'PORT = 80'.
4. Output ONLY the code. No markdown formatting (no ```).
"""

# 2. Refactoring (Editing existing files)
REFACTOR_TEMPLATE = """
{system_instruction}
--------------------------------------------------
TASK: The user wants to modify the file '{filename}'.
1. Read the CURRENT CONTENT below.
2. Follow the USER INSTRUCTIONS at the bottom.
3. Rewrite the FULL file with the changes applied.
4. REMOVE the user's instruction comment from the final output.
5. Output ONLY the code. No markdown.
--------------------------------------------------
CURRENT CONTENT:
{current_content}
--------------------------------------------------
USER INSTRUCTIONS:
{instructions}
"""

# 3. Visualization (Mermaid Diagrams)
VISUALIZE_TEMPLATE = """
You are a Systems Architect. Your goal is to visualize code logic.
--------------------------------------------------
TASK: Analyze the code below and generate a Mermaid.js diagram.
INSTRUCTIONS:
1. Use 'graph TD' (Top-Down) for flowcharts.
2. IMPORTANT: Wrap ALL node text in double quotes to prevent syntax errors.
   - BAD:  A[Start (Init)]
   - GOOD: A["Start (Init)"]
3. Keep it simple and high-level (show relationships, not every line of code).
4. Output ONLY the mermaid code. No markdown blocks.
--------------------------------------------------
CODE TO ANALYZE ({target_filename}):
{code_content}
"""