from fastapi import FastAPI

from app.api.runbooks import router as runbooks_router


app = FastAPI(
    title="OpsPilot AI",
    description="AI-powered runbook knowledge assistant",
    version="0.1.0",
)


@app.get("/")
def home():
    return {"message": "Welcome to OpsPilot AI!"}


@app.get("/health")
def health_check():
    return {
        "status": "UP",
        "application": "OpsPilot AI",
    }


app.include_router(runbooks_router)