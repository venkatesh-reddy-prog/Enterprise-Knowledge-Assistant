from fastapi import FastAPI

app = FastAPI(title="Enterprise Knowledge Assistant - Query Service")

@app.get("/")
def root():
    return {"message": "Query Service Running 🚀"}

@app.post("/ask")
def ask_question(question: str):
    return {
        "question": question,
        "answer": "Mock AI response from Enterprise Knowledge Assistant."
    }