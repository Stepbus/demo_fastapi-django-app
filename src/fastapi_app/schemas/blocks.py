from datetime import datetime

from pydantic import BaseModel


class BlockSchema(BaseModel):
    id: int
    currency: str
    provider: str
    block_number: int
    created_at: datetime | None
    stored_at: datetime

    class Config:
        from_attributes = True
