from pydantic import BaseModel

class Token_Info(BaseModel):
    token_type : str
    access_token : str
    refres_token : str | None = None