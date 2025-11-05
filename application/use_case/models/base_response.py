from typing import Optional
from pydantic import BaseModel, PrivateAttr


class BaseResponse(BaseModel):
    status: bool
    message: Optional[str] = None
    _status_code: str = PrivateAttr()