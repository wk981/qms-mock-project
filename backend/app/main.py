"""FastAPI application for the greeting service."""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from .greeting import hello


class GreetRequest(BaseModel):
    name: str


class GreetResponse(BaseModel):
    greeting: str


app = FastAPI(title="Hello App", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/api/greet", response_model=GreetResponse)
def greet(request: GreetRequest) -> GreetResponse:
    """Generate a greeting for the given name."""
    try:
        greeting_text = hello(request.name)
        return GreetResponse(greeting=greeting_text)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/health")
def health_check() -> dict:
    """Health check endpoint."""
    return {"status": "ok"}
