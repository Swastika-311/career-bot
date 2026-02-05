🤖 **Career-Bot: AI-Powered Job Application Assistant**
Career-Bot is a high-performance backend API designed to bridge the gap between wordy job descriptions and candidate resumes. 
By leveraging LLM Context Compression via ScaleDown.ai, the assistant extracts core technical pillars from JDs and provides actionable, line-by-line resume improvements.

✨ **Key Features**
**Hybrid Input Handling:** Supports both standard JSON and Multipart Form-Data for easy copy-pasting of long texts in Swagger UI.

**Token Optimization:** Reduces API latency and costs by filtering out "corporate fluff" using the ScaleDownCompressor.

**Resume Gap Analysis:** Specifically identifies missing technical stacks (e.g., Python, FastAPI, AWS) based on the JD.

**Async Processing:** Built with Python’s async/await to handle multiple requests without blocking.

🚀 **Installation & Setup**
1. Clone the Repository
   ```bash
   git clone https://github.com/Swastika-311/career-bot.git
   cd career-bot
   ```
2. Create a Virtual Environment (Recommended)
   This keeps your project dependencies isolated and clean.
   ```bash
   python -m venev venv
   venv\Scripts\activate
    
   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```
4. Install Dependencies
   ```bash
   pip install -r requirements.txt
   ```
5. Configure Environment Variables
   Create a file named **.env.api** in the root directory and add your key:
   ```text
   SCALEDOWN_API_KEY="your_actual_api_key_here"
   ```

🛠️ **Usage**
1. Start the Server:
```Bash
python -m uvicorn app:app --reload
```
2. Access the API Documentation: Open your browser to http://127.0.0.1:8000/docs.

**Endpoints**
* **POST /summarize-jd:** Enter a long job description to get a concise 5-point technical summary.
* **POST /resume-tips:** Enter both a JD summary and your resume text to receive 4-5 actionable improvements.

📂 **Project Structure**

**career-bot**/

├── **app.py**              	# Main FastAPI application & logic

├── **.env.api**    	        # (Ignored by Git) Your private API keys

├── **.gitignore**    	        # Prevents sensitive files from being uploaded

├── **requirements.txt**    	# Project dependencies

├── **venv/**               	# (Ignored by Git) Virtual environment

└── **README.md**           	# Project documentation

🔧 **Technical Challenges Overcome**
* **Handling Multi-line Strings:** Solved the common JSON 422 Unprocessable Entity error by implementing Form-Data support, allowing users to paste raw text with newlines directly into the API.
* **API Timeouts:** Integrated logic to handle 504 Gateway Timeouts from external AI services during heavy processing tasks.
