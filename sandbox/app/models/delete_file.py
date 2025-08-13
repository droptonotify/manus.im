"""
File delete result
"""
from typing import Optional

class FileDeleteResult:
    """File delete result"""
    def __init__(self, file: str, deleted: bool, message: Optional[str] = None):
        self.file = file
        self.deleted = deleted
        self.message = message
        
    def model_dump(self):
        """Convert to dict for API response"""
        return {
            'file': self.file,
            'deleted': self.deleted,
            'message': self.message
        }
