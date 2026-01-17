# src/config.py
import os
from dotenv import load_dotenv

load_dotenv()

# 🔑 Secrets
API_KEY = os.getenv("GEMINI_API_KEY")

# ⚙️ Settings
MOCK_MODE = False
MODEL_NAME = "gemini-2.0-flash" 
TEMPERATURE = 0.4
MAX_RETRIES = 3
RETRY_DELAY_BASE = 30

# 📂 Filesystem
TARGET_FOLDER = "D:/Oracle_Files"
BACKUP_FOLDER = ".pythia_history"
DB_PATH = "pythia_memory"  

# 📝 Extensions
VALID_EXTENSIONS = [
    '.txt', '.py', '.js', '.html', '.css', 
    '.md', '.json', '.sql', '.mermaid'
]