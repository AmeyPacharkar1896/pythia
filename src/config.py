import os
from dotenv import load_dotenv

# Load env variables once
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
TARGET_FOLDER = os.getenv("TARGET_FOLDER")
DB_PATH = "./pythia_memory" 

# Validation
if not API_KEY:
    raise ValueError("🛑 API Key missing! Check your .env file.")

if not TARGET_FOLDER:
    # Default to Desktop
    desktop = os.path.join(os.path.expanduser("~"), "Desktop")
    TARGET_FOLDER = os.path.join(desktop, "Oracle_Files")

# Ensure folders exist
if not os.path.exists(TARGET_FOLDER):
    os.makedirs(TARGET_FOLDER)
    print(f"📂 Created target folder: {TARGET_FOLDER}")