import os
import time
import google.generativeai as genai
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from dotenv import load_dotenv

# ================= CONFIGURATION =================
# 1. Load variables from .env file
load_dotenv()

# 2. Get variables safely
API_KEY = os.getenv("GEMINI_API_KEY")
TARGET_FOLDER = os.getenv("TARGET_FOLDER")

# 3. Safety Check
if not API_KEY:
    raise ValueError("❌ Error: GEMINI_API_KEY not found in .env file")

# Fallback if target folder isn't set
if not TARGET_FOLDER:
    TARGET_FOLDER = r"D:\Oracle_Files"
# =================================================

# Configure AI
genai.configure(api_key=API_KEY)

# CORRECTED MODEL NAME: gemini-1.5-flash is the current fast/free standard
model = genai.GenerativeModel('gemini-2.5-flash')

class OracleHandler(FileSystemEventHandler):
    def on_moved(self, event):
        """
        Triggered when a file is RENAMED.
        Event: New Text Document.txt -> Why is the sky blue.txt
        """
        if event.is_directory: return

        filename = os.path.basename(event.dest_path)
        file_path = event.dest_path

        # Filter out system files, temp files, or hidden files
        if filename.startswith(".") or filename.startswith("~"): return

        # === UNIVERSAL FILE FILTER ===
        # We only process extensions that make sense for text generation
        valid_extensions = ['.txt', '.py', '.js', '.html', '.css', '.md', '.json', '.csv', '.sql', '.sh']
        _, ext = os.path.splitext(filename)
        
        if ext.lower() not in valid_extensions:
            return  # Ignore images/exes to prevent corruption

        print(f"\n🔮 [DETECTED] Prompt: '{filename}'")
        self.fulfill_prophecy(file_path, filename)

    def fulfill_prophecy(self, file_path, filename):
        """Generates content and injects it into the file."""
        try:
            # Step 1: Write a "Loading" message immediately
            with open(file_path, "w", encoding="utf-8") as f:
                f.write("🔮 The Oracle is gazing into the void... please wait.")

            # Step 2: Determine Context based on Extension
            name, ext = os.path.splitext(filename)
            prompt = name.replace("_", " ") # Clean up underscores for better prompts

            system_instruction = "You are a helpful AI."
            
            if ext == ".py":
                system_instruction = "You are a Senior Python Engineer. Write ONLY valid, runnable Python code. Do not wrap in markdown blocks."
            elif ext == ".html":
                system_instruction = "You are a Frontend Developer. Write a single HTML file with embedded CSS. Do not wrap in markdown blocks."
            elif ext == ".json":
                system_instruction = "You are a Data Engineer. Output ONLY valid JSON data. Do not wrap in markdown blocks."
            elif ext == ".md":
                system_instruction = "You are a Technical Writer. Use rich Markdown formatting."
            elif ext == ".sql":
                system_instruction = "You are a Database Admin. Write a valid SQL query."

            print(f"   Thinking about: {prompt} ({ext})...")
            
            # Step 3: Ask the AI
            response = model.generate_content(
                f"{system_instruction} \n"
                f"The user created a file named '{filename}'. "
                f"Generate the full text content that belongs inside this file based on its name."
            )
            text = response.text

            # Step 4: Clean up Markdown Artifacts (Gemini sometimes adds ```python ... ```)
            # This ensures code files are instantly runnable
            if text.startswith("```"):
                # Remove the first line (e.g., ```python)
                text = text.split("\n", 1)[1]
                # Remove the last line (e.g., ```) if it exists
                if text.strip().endswith("```"):
                     text = text.rsplit("```", 1)[0]

            # Step 5: Overwrite the file with the result
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(text)
            
            print(f"✅ [SUCCESS] Prophecy written to disk.")

        except Exception as e:
            print(f"🛑 Error: {e}")
            # Write the error to the file so the user sees it inside Notepad
            try:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(f"Error consulting the Oracle: {e}")
            except:
                pass

if __name__ == "__main__":
    # Create the folder automatically if it doesn't exist
    if not os.path.exists(TARGET_FOLDER):
        os.makedirs(TARGET_FOLDER)
        print(f"📂 Created magic folder: {TARGET_FOLDER}")

    # Start the Watchdog
    event_handler = OracleHandler()
    observer = Observer()
    observer.schedule(event_handler, TARGET_FOLDER, recursive=False)
    observer.start()

    print(f"👁️  THE ORACLE IS WATCHING: {TARGET_FOLDER}")
    print("---------------------------------------------------")
    print("   INSTRUCTIONS:")
    print("   1. Go to the folder.")
    print("   2. Right-Click -> New -> Document.")
    print("   Supported extentions: \n\t1. .txt\n\t2. .py\n\t3. .html\n\t4. .json\n\t5. .md\n\t6. .sql")
    print("   3. RENAME it to your prompt (e.g., 'Snake_Game.py').")
    print("   4. Wait 1 second.")
    print("   5. Open it.")
    print("---------------------------------------------------")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print("\n💤 The Oracle sleeps.")
    observer.join()