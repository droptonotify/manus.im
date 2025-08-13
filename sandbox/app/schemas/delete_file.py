"""
File delete request
"""
from pydantic import BaseModel, Field
from typing import Optional


class FileDeleteRequest(BaseModel):
    """File delete request"""
    file: str = Field(..., description="Absolute file path")
