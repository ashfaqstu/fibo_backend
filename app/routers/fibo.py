from fastapi import APIRouter

router = APIRouter()

@router.get("/structured")
def get_structured_prompt():
    return {"message": "FIBO Structured Prompt Endpoint"}

@router.post("/render")
def render_fibo_image():
    return {"message": "FIBO Render Endpoint"}