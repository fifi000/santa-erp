from typing import List

from sqlmodel import Session, select
from fastapi import APIRouter, HTTPException, Depends, Query

from db.config import get_session
from db.models import Elf, Holiday, Item


router = APIRouter(
    prefix='/elves',
    tags=['elves']
)


@router.post('/', response_model=Elf)
async def create_elf(*, session: Session = Depends(get_session), elf: Elf):
    db_elf = Elf.model_validate(elf)
    session.add(db_elf)
    session.commit()
    session.refresh(db_elf)
    return db_elf
            

@router.get('/', response_model=List[Elf])
async def get_elves(
    *,
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=100, le=100)
):
    elves = session.exec(select(Elf).offset(offset).limit(limit)).all()
    return elves


@router.get('/{elf_id}', response_model=Elf)
async def get_elf(*, session: Session = Depends(get_session), elf_id: int):
    elf = session.get(Elf, elf_id)
    if not elf:
        raise HTTPException(status_code=404, detail='Elf not found')
    return elf


@router.patch('/{elf_id}', response_model=Elf)
async def update_elf(*, session: Session = Depends(get_session), elf_id: int, elf: Elf):
    db_elf = session.get(Elf, elf_id)
    if not db_elf:
        raise HTTPException(status_code=404, detail='Elf not found')
    
    elf_data = elf.model_dump(exclude_unset=True)
    for key, value in elf_data.items():
        setattr(db_elf, key, value)

    session.add(db_elf)
    session.commit()
    session.refresh(db_elf)
    return db_elf


@router.delete('/{elf_id}')
async def delete_elf(*, session: Session = Depends(get_session), elf_id: int):
    db_elf = session.get(Elf, elf_id)
    if not db_elf:
        raise HTTPException(status_code=404, detail='Elf not found')
    
    session.delete(db_elf)
    session.commit()
    return {'ok': True}
    
    
@router.post('/{elf_id}/holiday/', response_model=Elf)
async def asign_holiday(*, session: Session = Depends(get_session), elf_id: int, holiday: Holiday):
    db_elf = session.get(Elf, elf_id)
    if not db_elf:
        raise HTTPException(status_code=404, detail='Elf not found')
    
    db_elf.holidays.append(holiday)
    session.commit()
    session.refresh(db_elf)
    return db_elf


@router.post('/{elf_id}/items/{item_id}', response_model=Elf)
async def assign_item(*, session: Session = Depends(get_session), elf_id: int, item_id: int):
    db_elf = session.get(Elf, elf_id)    
    if not db_elf:
        raise HTTPException(status_code=404, detail='Elf not found')
    
    db_item = session.get(Item, item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail='Item not found')
    
    db_elf.items.append(db_item)
    session.commit()
    session.refresh(db_elf)
    return db_elf