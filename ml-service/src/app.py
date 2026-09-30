"""
app.py
Phase 1f: FastAPI microservice exposing /predict for Spring Boot to call.
 
Run locally:
    uvicorn app:app --reload --port 8000
 
Test:
    curl -X POST http://localhost:8000/predict \
         -H "Content-Type: application/json" \
         -d '{"text": "I want to track my refund"}'
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
 
from predict import predict_ticket
 
app = FastAPI(title="Ticket Classification ML Service")
 
 
class TicketRequest(BaseModel):
    text: str
 
 
class TicketResponse(BaseModel):
    category: str
    confidence: float
    suggested_response: str | None = None
 
 
@app.get("/health")
def health():
    return {"status": "ok"}
 
 
@app.post("/predict", response_model=TicketResponse)
def predict(request: TicketRequest):
    if not request.text or not request.text.strip():
        raise HTTPException(status_code=400, detail="text field cannot be empty")
 
    result = predict_ticket(request.text)
    return result
 
