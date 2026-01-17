# 🛠️ Installation Guide

## Prerequisites
* **Python 3.8+**
* A **Google Gemini API Key** (The free tier works perfectly).
    * [Get a key here](https://aistudio.google.com/app/apikey)

## Setup

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/AmeyPacharkar1896/pythia.git](https://github.com/AmeyPacharkar1896/pythia.git)
    cd pythia
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure Environment:**
    * Create a `.env` file in the root directory.
    * Add your API key:
        ```ini
        GEMINI_API_KEY=your_actual_api_key_here
        ```
    * *(Optional)* To change the folder Pythia watches, edit `src/config.py`.

## 🧪 Mock Mode (Offline Testing)
If you want to test the file system logic without using API credits, you can enable **Mock Mode**.

1. Open `src/brain.py`.
2. Set `MOCK_MODE = True`.
3. Pythia will now generate dummy content instantly, allowing you to test triggers like `# ROLLBACK` safely.

## 🚀 Running the Oracle
```bash
python main.py
```

You should see: "👁️ PYTHIA v2.0 IS ONLINE..."