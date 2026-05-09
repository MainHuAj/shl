from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
from app.agent import run_agent
import time



app =FastAPI()

class Message(BaseModel):
    role:str
    content:str

class ChatRequest(BaseModel):
    messages : list[Message]

class Recommendation(BaseModel):
    name:str
    url:str
    test_type:str

class ChatResponse(BaseModel):
    reply:str
    recommendations:list[Recommendation]
    end_of_conversation : bool




@app.post("/chat",response_model=ChatResponse)
def chat(request:ChatRequest):
    start = time.time()
    try:
        
        messages = [{"role":m.role , "content":m.content} for m in request.messages]
        response = run_agent(messages)
        elapsed = time.time() - start
        print(f"REQUEST TIME: {elapsed:.2f}s")
        return ChatResponse(
            reply=response["reply"],
            recommendations=response["recommendations"],
            end_of_conversation=response["end_of_conversation"]
        )
    except Exception as e:
        raise HTTPException(
            status_code= 500,
            detail=str(e)
        )
@app.get("/health")
def health():
    return {"status":"ok"}