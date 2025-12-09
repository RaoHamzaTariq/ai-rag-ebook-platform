from pydantic import BaseModel

class UserContext(BaseModel):
    page_no: int
    highlighted_text:str | None = None
    chapter_no: int | None = None
