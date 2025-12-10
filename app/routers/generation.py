from fastapi import APIRouter, BackgroundTasks
from pydantic import BaseModel
from app.services.multiview_service import multiview_service
import uuid

router = APIRouter()

class GenerationRequest(BaseModel):
    prompt: str # e.g. "wooden crate"

@router.post("/generate-views")
async def generate_multiview_images(request: GenerationRequest):
    """
    Trigger the 8-angle generation.
    Returns a Job ID so the frontend knows where to look later.
    """
    # Create a unique ID for this job
    job_id = str(uuid.uuid4())
    
    # Run the heavy generation directly (for now)
    # In a real app, use BackgroundTasks, but let's keep it simple to debug
    paths = multiview_service.generate_views(request.prompt, job_id)
    
    return {
        "message": "Views generated successfully",
        "job_id": job_id,
        "view_count": len(paths),
        "local_paths": paths
    }