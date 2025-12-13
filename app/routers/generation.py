from fastapi import APIRouter, BackgroundTasks
from pydantic import BaseModel
from app.services.image_service import image_service
from app.services.tripo_service import tripo_service  # <--- NEW IMPORT
import uuid

router = APIRouter()

class GenerationRequest(BaseModel):
    prompt: str 

@router.post("/generate-full-pipeline")
async def generate_pipeline(request: GenerationRequest, background_tasks: BackgroundTasks):
    job_id = str(uuid.uuid4())
    
    def run_hybrid_pipeline(jid, user_prompt):
        print(f"\n🚀 STARTING FIBO -> TRIPO PIPELINE (Job {jid})")
        
        # 1. FIBO (Phase 1)
        image_url = image_service.generate_single_image(user_prompt)
        
        if not image_url:
            print("❌ Pipeline Stopped at Phase 1 (Fibo)")
            return

        # 2. TRIPO (Phase 2)
        print(f"--- PHASE 2: TRIPO 3D CONVERSION ---")
        glb_url = tripo_service.generate_3d_model(image_url)

        if glb_url:
            print(f"\n✨ SUCCESS!")
            print(f"   🖼️ Input Image: {image_url}")
            print(f"   📦 Final 3D Model: {glb_url}")
        else:
            print("❌ Pipeline Stopped at Phase 2 (Tripo)")

    background_tasks.add_task(run_hybrid_pipeline, job_id, request.prompt)
    
    return {
        "message": "Hybrid Pipeline started (Fibo -> Tripo).",
        "job_id": job_id
    }