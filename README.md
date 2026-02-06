# 🤖 Career-Bot: AI-Powered Job Application Assistant
[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)](https://streamlit.io/)
[![ScaleDown](https://img.shields.io/badge/ScaleDown.ai-Token_Optimized-blueviolet?style=for-the-badge)](https://scaledown.xyz)

**Career-Bot** is a high-performance full-stack tool designed to bridge the gap between wordy job descriptions and candidate resumes. By leveraging **LLM Context Compression** via ScaleDown.ai, the assistant extracts core technical pillars from JDs and provides actionable, line-by-line resume improvements.



## ✨ Key Features
* **Hybrid Input Handling:** Supports both standard `JSON` and `Multipart Form-Data` for resilient copy-pasting of long texts.
* **Token Optimization:** Reduces API latency and costs by filtering out "corporate fluff" using the `ScaleDownCompressor`.
* **Resume Gap Analysis:** Specifically identifies missing technical stacks (e.g., Python, FastAPI, AWS) based on the JD.
* **Async Processing:** Built with Python’s `async/await` to handle multiple requests without blocking.

---

## 🚀 Installation & Setup

### 1. Clone the Repository
```bash
git clone [https://github.com/Swastika-311/career-bot.git](https://github.com/Swastika-311/career-bot.git)
cd career-bot
```

🚀 **Installation & Setup**
1. Clone the Repository
   ```bash
   git clone https://github.com/Swastika-311/career-bot.git
   cd career-bot
   ```
2. Create a Virtual Environment (Recommended)
   This keeps your project dependencies isolated and clean.
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```
   ```bash
   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Install Dependencies
   ```bash
   pip install -r requirements.txt
   ```
4. Configure Environment Variables
   Create a file named **.env.api** in the root directory and add your key:
   ```text
   SCALEDOWN_API_KEY="your_actual_api_key_here"
   ```
   
### 🚀 How to Run the Application
This project requires two terminals to be running simultaneously:
1. Start the Backend (API)
Open a terminal, activate your venv, and run:
```bash
python -m uvicorn app:app --reload
```
The API will be live at http://127.0.0.1:8000
2. Start the Frontend (UI)
Open a second terminal, activate your venv, and run:
```bash
python -m streamlit run frontend.py
```
The UI will open automatically in your browser at: http://localhost:8501

---

## 🔌 API Endpoints
The backend is fully documented via **Swagger UI**. Once the backend is running, visit `http://127.0.0.1:8000/docs` to test:

* **`POST /summarize-jd`**: Converts raw job descriptions into 5 technical pillars.
* **`POST /resume-tips`**: Compares JD summary vs. Resume for gap analysis.

*While the Streamlit UI is provided for the best user experience, the FastAPI endpoints remain fully exposed and documented for programmatic integration.*

---

📂 **Project Structure**

**career-bot**/

├── **app.py**              	# Main FastAPI application & logic

|:--- **frontend.py**         # Streamlit Frontend UI

├── **.env.api**    	        # (Ignored by Git) Your private API keys

├── **.gitignore**    	        # Prevents sensitive files from being uploaded

├── **requirements.txt**    	# Project dependencies

├── **venv/**               	# (Ignored by Git) Virtual environment

└── **README.md**           	# Project documentation

---

🔧 **Technical Challenges Overcome**

* **Handling Multi-line Strings:** Solved the common JSON 422 Unprocessable Entity error by implementing Form-Data support, allowing users to paste raw text with newlines directly.

* **API Timeouts:** Integrated logic to handle 504 Gateway Timeouts from external AI services during heavy processing tasks.

* **Environment Synchronization:** Managed VS Code interpreter conflicts to ensure seamless virtual environment integration.

---
