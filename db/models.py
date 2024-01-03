from enum import Enum
from datetime import date
from typing import List, Optional

from sqlmodel import SQLModel, Field, Relationship


# Helpers 
class HolidayType(Enum):
    PATERNITY_LEAVE = 1
    VACATION = 2
    SICK_LEAVE = 3
    OTHER = 4


# Models
class Item(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    description: Optional[str] = Field(default=None)

    elf_id: Optional[int] = Field(default=None, foreign_key="elf.id")
    elf: Optional["Elf"] = Relationship(back_populates="items")


class Holiday(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    start_date: date = Field(default=None)
    end_date: date = Field(default=None)
    type: HolidayType = Field(default=None)
    description: Optional[str] = Field(default=None)

    elf_id: Optional[int] = Field(default=None, foreign_key="elf.id")
    elf: Optional["Elf"] = Relationship(back_populates="holidays")


class Elf(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(default=None)
    items: List[Item] = Relationship(back_populates="elf")
    holidays: List[Holiday] = Relationship(back_populates="elf")

