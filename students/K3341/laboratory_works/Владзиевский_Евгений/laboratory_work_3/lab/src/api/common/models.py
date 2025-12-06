from pydantic import BaseModel



class ErrorDetails(BaseModel):
    msg: str

class Error(BaseModel):
    detail: list[ErrorDetails]
