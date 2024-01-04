from typing import Optional

from sqlmodel import SQLModel, Field


class UserDB(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    username: str = Field(unique=True, nullable=False)
    hashed_password: str = Field(nullable=False)
    
    email: Optional[str] = Field(default=None)
    disabled: Optional[str] = Field(default=None)



