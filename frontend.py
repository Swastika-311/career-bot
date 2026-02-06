import streamlit as st
import requests

st.set_page_config(page_title="Career Chatbot", page_icon="🤖")

st.title("🤖 Career Chatbot")
st.markdown("Optimize your Job Applications using AI compression.")

# Sidebar for API Configuration
with st.sidebar:
    st.header("Settings")
    api_url = st.text_input("API URL", value="http://127.0.0.1:8000")

# Tabs for different features
tab1, tab2 = st.tabs(["Summarize JD", "Resume Tips"])

with tab1:
    jd_input = st.text_area("Paste Job Description here:", height=300)
    if st.button("Summarize"):
        if jd_input:
            # We use 'data' for Form-Data, which matches our hybrid backend
            response = requests.post(f"{api_url}/summarize-jd", data={"job_description": jd_input})
            if response.status_code == 200:
                st.success("Summary Generated!")
                st.write(response.json().get("summary"))
            else:
                st.error("Failed to connect to API.")

with tab2:
    col1, col2 = st.columns(2)
    with col1:
        sum_input = st.text_area("Job Summary:", height=200)
    with col2:
        res_input = st.text_area("Your Resume:", height=200)
    
    if st.button("Get Tips"):
        if sum_input and res_input:
            response = requests.post(
                f"{api_url}/resume-tips", 
                data={"job_summary": sum_input, "resume_text": res_input}
            )
            if response.status_code == 200:
                st.info("Actionable Tips:")
                st.write(response.json().get("tips"))