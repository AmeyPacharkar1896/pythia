# 🔮 Pythia: The Oracle Filesystem

> *“Files that don't just store data—they generate it.”*

Pythia is an experimental "Generative Filesystem" that uses **Google Gemini 2.5** to create content on-the-fly. Instead of writing code or text manually, you simply create an empty file, rename it to your prompt (e.g., `Snake_Game.py`), and Pythia instantly fills it with the correct code or content.

It feels less like coding and more like summoning data from the void.

---

## ⚡ Features

* **Zero-UI Interface:** Operates entirely within your OS File Explorer. No separate app window required.
* **Instant Code Generation:** Create a file named `Calculator.py`, and it becomes a working calculator script.
* **Polyglot Support:** Detects file extensions to switch personalities:
    * `.py` → Python Engineer (Runnable code)
    * `.html` → Frontend Dev (Single-file website)
    * `.json` → Data Engineer (Mock data)
    * `.md` → Technical Writer (Documentation)
* **Context-Aware:** Understands the difference between a SQL query and a Javascript function based on the extension.
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

3. **Configure Environment:**
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
    python oracle_fs.py
    ```
    *The terminal will confirm: "👁️ THE ORACLE IS WATCHING..."*

2.  **The Magic Trick:**
    * Open your target folder (`Oracle_Files`).
    * **Right-Click > New > Text Document.**
    * **Rename** the file to your prompt.
        * *Example:* `A_story_about_a_glitched_computer.txt`
        * *Example:* `Login_Page_Dark_Mode.html`
    * Wait 1 second.
    * **Open the file.** The content has been generated.

---

## 📂 Supported Extensions

| Extension | Persona | Output Style |
| :--- | :--- | :--- |
| **.txt** | General Assistant | Plain text, direct answers. |
| **.py** | Python Engineer | Clean, runnable code. No markdown wrapper. |
| **.html** | Web Developer | Single-file HTML with embedded CSS. |
| **.json** | Data Scientist | Valid, structured JSON data. |
| **.md** | Tech Writer | Rich text with headers and lists. |
| **.sql** | DB Admin | Standard SQL queries. |

---

## 🔮 Roadmap

* [x] **v1.0:** Basic Watchdog & Extension Support.
* [ ] **v1.1 (Hive Mind):** RAG implementation. Files will be able to "read" other files in the directory to understand project context.
* [ ] **v1.2 (Living Files):** Support for editing a file to request changes (Conversational Editing).
* [ ] **v2.0 (The Forger):** Support for image generation (`.png`, `.jpg`).

---

## 📜 License

This project is open-source and available under the [MIT License](LICENSE).