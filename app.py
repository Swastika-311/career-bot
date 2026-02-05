from fastapi import FastAPI, Form, Request, HTTPException
from pydantic import BaseModel
from scaledown.compressor.scaledown_compressor import ScaleDownCompressor
from dotenv import load_dotenv
from typing import Optional
import os

load_dotenv(".env.api")

app=FastAPI()

compressor=ScaleDownCompressor(
    target_model='gpt-4o', rate='auto', api_key=os.getenv("SCALEDOWN_API_KEY")
)

class JobRequest(BaseModel):
    job_description: str

class ResumeRequest(BaseModel):
    job_summary: str
    resume_text: str

@app.post("/summarize-jd")
async def summarize_job_description(request:Request, job_description: Optional[str]=Form(None)):
    prompt="Summarize this description into 4-5 bullet points covering skills, experience and responsibilities"
    context=job_description
    if not context:
        try:
            body=await request.json()
            context=body.get(job_description)
        except:
            pass
    if not context:
        raise HTTPException(status_code=422, detail="No job description provided")
    summarized_text=compressor.compress(context=context, prompt=prompt)
    return {"summary":summarized_text.content}

@app.post("/resume-tips")
async def resume_tips(request:Request, job_summary:Optional[str]=Form(None), resume_text:Optional[str]=Form(None)):
    prompt="Give 4-5 specific actionable improvements to make this resume better for the job"
    job_data=job_summary
    resume_data=resume_text
    if not job_data or not resume_data:
        try:
            body=await Request.json()
            job_data=job_data or body.get(job_summary)
            resume_data= resume_data or body.get(resume_text)
        except:
            pass
        if not job_data or not resume_data:
            raise HTTPException(status_code=422, detail="Job summary and resume both are required.")
    context=f"Job summary:{job_data}\nResume:{resume_data}"
    refine_resume_tips=compressor.compress(context=context, prompt=prompt)
    return {"tips":refine_resume_tips.content}


    