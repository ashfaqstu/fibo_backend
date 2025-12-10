import json
import requests
import os
import copy
from app.core.config import settings

class MultiviewService:
    BASE_URL = "https://engine.prod.bria-api.com/v2/image/generate"

    def _get_base_structure(self, subject: str):
        """
        Defines the MASTER structure. 
        We will NOT change the object description between views.
        This forces the AI to keep the geometry as stable as possible.
        """
        return {
            # STATIC description (Notice we don't say "rotated" here)
            "short_description": f"A technical studio photo of a {subject}.", 
            "objects": [
                {
                    "description": f"A {subject} with identical structure.",
                    "location": "center",
                    "relationship": "Primary subject.",
                    "relative_size": "large within frame",
                    "shape_and_color": "Identical structure, uniform color.", 
                    "texture": "Smooth, clean material.",
                    "appearance_details": "Symmetrical design.",
                    # We remove 'orientation' here to let the Camera control the view
                }
            ],
            "background_setting": "Solid white background.",
            "lighting": {
                "conditions": "Studio lighting",
                "direction": "Front",
                "shadows": "Minimal"
            },
            "aesthetics": {
                "composition": "Centered",
                "color_scheme": "Neutral",
                "mood_atmosphere": "Technical",
                "consistency_requirements": "Geometry must match exactly."
            },
            # We initialize this, but will update it in the loop
            "photographic_characteristics": {
                "camera_angle": "Front view", 
                "lens_focal_length": "50mm",
                "depth_of_field": "Deep focus",
                "focus": "Sharp focus"
            },
            "style_medium": "photograph",
            "context": "3D asset generation reference.", 
            "artistic_style": "realistic"
        }

    def generate_views(self, subject: str, request_id: str):
        # We generate 8 views
        angles = [0, 45, 90, 135, 180, 225, 270, 315]
        saved_paths = []
        
        base_path = os.getcwd()
        save_dir = os.path.join(base_path, "assets_storage", request_id, "views")
        os.makedirs(save_dir, exist_ok=True)

        headers = {
            "api_token": settings.BRIA_API_KEY,
            "Content-Type": "application/json"
        }

        print(f"🚀 Starting Strict Multi-View Generation for: {subject}")

        # 1. Get the Master JSON template
        base_prompt = self._get_base_structure(subject)
        
        # 2. Variable to hold the 'Anchor' image URL (0 degree)
        anchor_url = None

        for angle in angles:
            # Create a Deep Copy so we don't mess up the template
            current_prompt = copy.deepcopy(base_prompt)
            
            # 3. ONLY change the Camera Angle string
            # This is the "Disentangled Control" Bria is famous for
            current_prompt["photographic_characteristics"]["camera_angle"] = f"Turntable view, rotated {angle} degrees."

            # Prepare Payload
            payload = {
                "structured_prompt": json.dumps(current_prompt),
                "aspect_ratio": "1:1",
                "sync": True,
                "seed": 42, # CRITICAL: Keep seed constant
                "variation_strength": 0
            }

            # For angles other than 0, we can try to use the 0-degree image as a weak reference
            if anchor_url and angle > 0:
                payload["image_url"] = anchor_url
                payload["image_strength"] = 0.30 # Keep low to allow rotation, but high enough to keep color

            try:
                response = requests.post(self.BASE_URL, headers=headers, json=payload)
                
                if response.status_code != 200:
                    print(f"   ⚠️ Error on {angle}°: {response.text}")
                    continue

                result = response.json()
                img_url = result["result"]["image_url"]
                
                # If this is the first image, save it as the Anchor
                if angle == 0:
                    anchor_url = img_url
                    print("   ⚓ Anchor Image Locked.")

                # Download
                img_data = requests.get(img_url).content
                filename = os.path.join(save_dir, f"{angle}.png")
                with open(filename, "wb") as f:
                    f.write(img_data)
                
                saved_paths.append(filename)
                print(f"   ✅ Saved {angle}° view")

            except Exception as e:
                print(f"   ❌ Exception on {angle}°: {str(e)}")
        
        return saved_paths

multiview_service = MultiviewService()