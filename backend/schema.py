from pydantic import BaseModel


class UserOut(BaseModel):
    id: str
    full_name: str
    preferred_name: str | None
    c4k_id: str
    role: str
    is_active: bool
