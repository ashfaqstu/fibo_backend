from pydantic import BaseModel

class PromptRequest(BaseModel):
    user_text: str

class FiboStructure(BaseModel):
    category: str
    description: str
    style: str
class RenderRequest(BaseModel):
    strucure: FiboStructure
class ImageResponse(BaseModel):
    image_url: str
    status: str
