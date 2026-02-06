# 📄 Project Documentation: Career-Bot Full-Stack Technical Specs

## 1. Executive Summary
**Career-Bot** is a full-stack AI-driven career assistant that optimizes the job application process. Unlike standard GPT-wrappers, it utilizes a decoupled architecture—separating a **Streamlit-based UI** from a **FastAPI backend**—and incorporates a dedicated **Context Compression Layer** via ScaleDown.ai to ensure cost-efficient and high-accuracy results.

---

## 2. System Architecture & Data Flow
The system is built on a "Client-Server" model designed for scalability and separation of concerns.



### Workflow:
1.  **Client Layer (Streamlit):** The user interacts with a multi-tab interface. Input is collected via text areas and forwarded as a `POST` request using the `requests` library.
2.  **API Gateway (FastAPI):** The backend receives the data through specialized endpoints (`/summarize-jd` or `/resume-tips`).
3.  **Optimization (The ScaleDown Layer):** * Raw job descriptions are sent to the `ScaleDownCompressor`.
    * Linguistic "noise" (e.g., "Our office has a ping-pong table") is stripped away.
    * Technical requirements (e.g., "3 years of React experience") are prioritized.
4.  **Inference Engine:** The AI processes only the "signal-rich" data to generate summaries or career tips.
5.  **Response:** The UI receives a JSON response and renders it using Markdown for a clean user experience.

---

## 3. Component Specification

### 🖥️ Frontend (ui.py / frontend.py)
* **State Management:** Uses Streamlit's session handling for real-time interaction.
* **Navigation:** Implements a Tabbed Interface to separate "JD Summarization" from "Resume Gap Analysis."
* **API Integration:** Configurable backend URL in the sidebar allows the UI to point to local or cloud-hosted versions of the API.

### ⚙️ Backend (app.py)
* **POST /summarize-jd:** Converts unstructured job postings into 5 technical pillars.
* **POST /resume-tips:** Performs a cross-referential analysis between a JD and a Resume.
* **Hybrid Validation:** Uses `Pydantic` for JSON and `python-multipart` for resilient Form-Data handling.

---

## 4. Engineering Challenges & Solutions

### A. The "Copy-Paste" Resiliency
**Challenge:** Users often copy text with hidden formatting characters or newlines, causing standard JSON payloads to fail with `422 Unprocessable Entity`.
**Solution:** Switched to **Multi-part Form-Data** for text ingestion. This allows the API to accept raw "messy" text directly from the UI without requiring complex client-side sanitization.

### B. Token Economy (Cost Engineering)
**Challenge:** High-volume LLM requests are expensive.
**Solution:** By implementing **ScaleDown.ai**, the system compresses job descriptions before they reach the LLM. This saves ~30-40% on token costs per request, making the application sustainable for production-scale usage.



### C. UI/UX "Ghost" Crashes
**Challenge:** If the backend (FastAPI) is down, the UI provides no feedback to the user.
**Solution:** Integrated **Status Code Validation** in the frontend. The UI now checks for `200 OK` responses and displays user-friendly error messages (e.g., `st.error`) if the backend is unreachable.

---

## 5. Technology Stack
* **Frontend UI:** Streamlit
* **Backend API:** FastAPI
* **Production Server:** Uvicorn (ASGI)
* **Context Optimization:** ScaleDown.ai
* **Asynchronous Tasks:** Python `asyncio` & `httpx`
* **Environment Logic:** Python-Dotenv

---

## 6. Deployment & Future Roadmap
* **Current State:** Localhost deployment with separate environments for Frontend and Backend.
* **V2.0 (The File Layer):** Integration of `PyMuPDF` to allow direct `.pdf` resume uploads.
* **V2.1 (The Analysis Layer):** A visual "Skill Match" chart comparing JD requirements vs. Resume skills.
* **V3.0 (Cloud):** Dockerization of both layers for deployment on AWS/GCP.

---
*Documentation Version: 1.1 - Revised Feb 2026*