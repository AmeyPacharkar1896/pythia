import os
import time
import google.generativeai as genai
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from dotenv import load_dotenv

# ================= CONFIGURATION =================
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
TARGET_FOLDER = os.getenv("TARGET_FOLDER")

# Safety Checks
if not API_KEY:
    print("\n🛑 CONFIGURATION ERROR: .env file missing or empty.")
    print("Please rename .env.example to .env and add your API key.")
    exit(1)

if not TARGET_FOLDER:
    # Default to Desktop if not set
    desktop = os.path.join(os.path.expanduser("~"), "Desktop")
    TARGET_FOLDER = os.path.join(desktop, "Oracle_Files")
# =================================================

# Configure AI
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash')

class OracleHandler(FileSystemEventHandler):
    def on_moved(self, event):
        """Triggered when a file is RENAMED."""
        if event.is_directory: return
        self._process_event(event)

    def on_created(self, event):
        """Triggered when a file is SAVED (VS Code)."""
        time.sleep(0.5) # Wait for write to finish
        self._process_event(event)

    def _process_event(self, event):
        """Standardized event processor."""
        filename = os.path.basename(event.src_path)
        file_path = event.src_path
        
        # Handle rename events where dest_path exists
        if hasattr(event, 'dest_path'):
            filename = os.path.basename(event.dest_path)
            file_path = event.dest_path

        # Filter system files
        if filename.startswith(".") or filename.startswith("~"): return

        # Validate Extension
        valid_extensions = ['.txt', '.py', '.js', '.html', '.css', '.md', '.json', '.csv', '.sql', '.sh']
        _, ext = os.path.splitext(filename)
        if ext.lower() not in valid_extensions: return

        # Check if file is empty (we only fill empty files)
        try:
            if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
                return
        except OSError:
            return

        print(f"\n🔮 [DETECTED] Prompt: '{filename}'")
        self.fulfill_prophecy(file_path, filename)

    # 🧠 NEW FUNCTION: THE HIVE MIND (RAG)
    def get_hive_context(self, current_file_path):
        """
        Scans the folder for OTHER files and reads them to build context.
        """
        context_data = ""
        folder = os.path.dirname(current_file_path)
        
        # List all files in the directory
        try:
            files_in_folder = os.listdir(folder)
        except FileNotFoundError:
            return ""

        for file in files_in_folder:
            path = os.path.join(folder, file)
            
            # Skip the file we are currently generating (don't read yourself!)
            if path == current_file_path:
                continue
            
            # Skip system files or directories
            if file.startswith(".") or os.path.isdir(path):
                continue

            # Only read text-based files
            valid_read_exts = ['.txt', '.md', '.py', '.json', '.html', '.css', '.js', '.sql']
            _, ext = os.path.splitext(file)
            if ext.lower() not in valid_read_exts:
                continue

            try:
                # Read the file content
                with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    # Only add if it's not empty and not too huge (limit to 20k chars per file)
                    if content.strip() and len(content) < 20000:
                        context_data += f"\n--- FILE: {file} ---\n{content}\n"
            except Exception:
                continue # Skip files we can't read
        
        return context_data

    def fulfill_prophecy(self, file_path, filename):
        try:
            # 1. Loading Message
            with open(file_path, "w", encoding="utf-8") as f:
                f.write("🔮 The Oracle is consulting the Hive Mind...")

            # 2. Get Context from Sibling Files
            hive_context = self.get_hive_context(file_path)
            
            print_msg = f"   Thinking about: {filename}..."
            if hive_context:
                print_msg = f"   🧠 Hive Mind Active: Reading other files..."
            print(print_msg)

            # 3. Build the Prompt
            name, ext = os.path.splitext(filename)
            prompt = name.replace("_", " ")

            system_instruction = "You are an intelligent file system."
            if ext == ".py": system_instruction = "You are a Python Expert. Write ONLY valid code."
            elif ext == ".md": system_instruction = "You are a Technical Writer. Use Markdown."
            elif ext == ".html": system_instruction = "You are a Web Developer. Write valid HTML."
            elif ext == ".json": system_instruction = "You are a Data Engineer. Output valid JSON."
            
            # THE RAG PROMPT
            full_prompt = (
                f"{system_instruction}\n"
                f"You are operating inside a folder. Here are the other files in this folder:\n"
                f"{hive_context}\n"
                f"--------------------------------------------------\n"
                f"Based on the context above (if relevant), generate the content for a new file named '{filename}'.\n"
                f"Task: {prompt}\n"
                f"Be direct. Do not include markdown blocks like ```python."
            )

            # 4. Generate
            response = model.generate_content(full_prompt)
            text = response.text

            # 5. Clean & Save
            if text.startswith("```"):
                text = text.split("\n", 1)[1]
                if text.strip().endswith("```"):
                     text = text.rsplit("```", 1)[0]

            with open(file_path, "w", encoding="utf-8") as f:
                f.write(text)
            
            print(f"✅ [SUCCESS] Written to {filename}")

        except Exception as e:
            print(f"🛑 Error: {e}")
            try:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(f"Error consulting the Oracle: {e}")
            except:
                pass

if __name__ == "__main__":
    if not os.path.exists(TARGET_FOLDER):
        os.makedirs(TARGET_FOLDER)
        print(f"📂 Created magic folder: {TARGET_FOLDER}")

    event_handler = OracleHandler()
    observer = Observer()
    observer.schedule(event_handler, TARGET_FOLDER, recursive=False)
    observer.start()

    print(f"👁️  PYTHIA v1.1 (Hive Mind) IS WATCHING: {TARGET_FOLDER}")
    print("---------------------------------------------------")
    print("   INSTRUCTIONS:")
    print("   1. Create context files (e.g. 'Project_Specs.txt')")
    print("   2. Create a new file (e.g. 'Generate_Code.py')")
    print("   3. Watch the AI connect the dots.")
    print("---------------------------------------------------")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print("\n💤 The Oracle sleeps.")
    observer.join()