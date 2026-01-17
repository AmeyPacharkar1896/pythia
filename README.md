# 🔮 Pythia: The Oracle Filesystem

> *“Files that don't just store data—they generate it.”*

Pythia is an experimental "Generative Filesystem" that uses **Google Gemini 2.5 Flash** to create content on-the-fly. Instead of writing code or text manually, you simply create an empty file, rename it to your prompt (e.g., `Snake_Game.py`), and Pythia instantly fills it with the correct code or content.

It feels less like coding and more like summoning data from the void.

---

## ⚡ Features

* **Zero-UI Interface:** Operates entirely within your OS File Explorer. No separate app window required.
* **Instant Code Generation:** Create a file named `Calculator.py`, and it becomes a working calculator script.
* **🧠 Hive Mind (RAG):** Powered by **ChromaDB**, Pythia has long-term memory. It reads and "memorizes" every file in your folder. A new file can reference variables, passwords, or logic from existing files automatically.
* **✨ Living Files (Conversational Editing):** "Talk" to your code. Add a comment like `# UPDATE: Switch to SQLite` inside a file, save it, and Pythia will rewrite the code to match your instruction.
* **Polyglot Support:** Detects file extensions to switch personalities:
    * `.py` → Python Engineer (Runnable code)
    * `.html` → Frontend Dev (Single-file website)
    * `.js` / `.css` → Web Stack Experts
    * `.json` → Data Engineer (Mock data)
    * `.md` → Technical Writer (Documentation)
* **Secure:** Uses `.env` for API key management.
* **Driverless:** Built on Python `watchdog`, requiring no kernel drivers or risky installations.

---

## 🛠️ Installation

### Prerequisites
* Python 3.8+
* A Google Gemini API Key (Free tier works perfectly)

### Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/AmeyPacharkar1896/pythia.git
    cd pythia
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure Environment:**
    * Make a copy of the example config:
        ```bash
        cp .env.example .env
        # On Windows Command Prompt: copy .env.example .env
        ```
    * Open `.env` and paste your `GEMINI_API_KEY`.
    * (Optional) Change the `TARGET_FOLDER` path.

---

## 🎮 How to Use

1.  **Run the Oracle:**
    ```bash
    python main.py
    ```
    *The terminal will confirm: "👁️ PYTHIA v2.0 IS ONLINE..."*

### Mode 1: Creation (The Spark)
* Open your target folder (`Oracle_Files`).
* **Right-Click > New > Text Document.**
* **Rename** it to your prompt (e.g., `Login_Page_Dark_Mode.html`).
* Wait 1 second.
* **Open the file.** The content has been generated.

### Mode 2: Context (The Hive Mind)
* Create a file `Config.txt` with some data (e.g., "App Color: Neon Blue").
* Create a new file `Styles.css`.
* Pythia will read `Config.txt` and automatically use "Neon Blue" in the generated CSS.

### Mode 3: Editing (The Refactor)
* Open an existing file (e.g., `script.py`).
* Scroll to the bottom and add a comment command:
    ```python
    # UPDATE: Change the database port to 8080.
    ```
* **Save the file.**
* Watch as Pythia rewrites the code in real-time to apply your change.

---

## 📂 Supported Extensions

| Extension | Persona | Output Style |
| :--- | :--- | :--- |
| **.txt** | General Assistant | Plain text, direct answers. |
| **.py** | Python Engineer | Clean, runnable code. No markdown wrapper. |
| **.html** | Web Developer | Single-file HTML with embedded CSS. |
| **.js** | JS Expert | Modern JavaScript/Node.js code. |
| **.css** | UI Designer | Clean CSS styles. |
| **.json** | Data Scientist | Valid, structured JSON data. |
| **.md** | Tech Writer | Rich text with headers and lists. |
| **.sql** | DB Admin | Standard SQL queries. |

---

## 🔮 Roadmap

* [x] **v1.0:** Basic Watchdog & Extension Support.
* [x] **v2.0 (Hive Mind):** RAG implementation with ChromaDB (Vector Memory).
* [x] **v2.1 (Living Files):** Conversational Editing (Refactoring via comments).
* [ ] **v2.2 (The Vizier):** Support for generating diagrams (`.mermaid`) from code.
* [ ] **v3.0 (The Forger):** Support for image generation (`.png`, `.jpg`).

---

## 📜 License

This project is open-source and available under the [MIT License](LICENSE).