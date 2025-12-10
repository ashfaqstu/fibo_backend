from fastapi import APIRouter
router = APIRouter()

@router.post("/generate")
def generate_3d_model():
    return {"message": "3d Generation workflow ready"}
