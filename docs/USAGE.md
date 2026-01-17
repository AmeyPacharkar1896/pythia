# 🎮 User Manual

Pythia operates using **File System Events**. You don't type commands in a terminal; you manipulate files in your `Oracle_Files` folder.

---

## ⚡ Mode 1: Creation (The Spark)
*Generate new code from scratch.*

1.  **Right-Click > New > Text Document.**
2.  **Rename** the file to your prompt, ending with the target extension.
    * *Example:* `Login_Page_Dark_Mode.html`
    * *Example:* `Calculus_Solver.py`
3.  **Wait 1 second.** Open the file to see the generated code.

---

## 🧠 Mode 2: Context (The Hive Mind)
*Pythia reads other files in the folder to understand your project.*

* **Example:**
    1.  Create `Theme.txt`: "Primary color is Neon Green."
    2.  Create `Style.css`.
    3.  Pythia reads `Theme.txt` and automatically uses Neon Green in the CSS.

---

## ✨ Mode 3: Conversational Editing (Refactor)
*Modify existing code using natural language comments.*

1.  Open any code file (e.g., `script.py`).
2.  Scroll to the bottom and add a comment starting with `UPDATE:`:
    ```python
    # UPDATE: Change the database from SQLite to PostgreSQL.
    ```
3.  **Save the file.**
4.  Pythia will rewrite the code to match your instruction and remove the comment.

---

## 🛡️ Mode 4: The Time Machine (Rollback)
*Undo mistakes instantly. Pythia creates a hidden backup every time it modifies a file.*

1.  If an update breaks your code, open the file.
2.  Add the rollback command at the bottom:
    ```python
    # ROLLBACK
    ```
3.  **Save.** The file will instantly revert to the version before the last update.

---

## 🎨 Mode 5: Visualization (The Vizier)
*Generate system diagrams from your code.*

1.  Ensure you have a code file (e.g., `Game_Logic.py`).
2.  Create a new empty file with the **same name** but `.mermaid` extension:
    * `Game_Logic.mermaid`
3.  Pythia will analyze the Python code and generate a Flowchart inside the `.mermaid` file.
4.  *Tip:* Use the "Mermaid Preview" extension in VS Code to view the graph.

---

## 📂 Supported Extensions & Personas

| Extension | Persona | Output |
| :--- | :--- | :--- |
| **.py** | Python Engineer | Clean, runnable scripts. |
| **.js** | JS Expert | Modern ES6+ JavaScript. |
| **.html** | Frontend Dev | HTML5 with embedded CSS. |
| **.css** | UI Designer | Responsive stylesheets. |
| **.sql** | DB Admin | Complex SQL queries. |
| **.json** | Data Engineer | Structured mock data. |
| **.md** | Tech Writer | Documentation and tutorials. |
| **.mermaid**| Systems Architect | Flowcharts & Diagrams. |
