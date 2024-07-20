from pydantic import BaseModel
from typing import Optional

class PDFRequest(BaseModel):
    folder: Optional[str] = None
    output_path: Optional[str] = None