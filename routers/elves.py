from typing import List

from sqlmodel import Session, select
from fastapi import HTTPException, Depends, Query

from .config import app
from db.config import get_session
from db.models import Elf, Holiday


@app.post('/elves/', response_model=Elf)
async def create_elf(*, session: Session = Depends(get_session), elf: Elf):
    db_elf = Elf.model_validate(elf)
    session.add(db_elf)
    session.commit()
    session.refresh(db_elf)
    return db_elf
            

@app.get('/elves/', response_model=List[Elf])
async def get_elves(
    *,
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=100, le=100)
):
    elves = session.exec(select(Elf).offset(offset).limit(limit)).all()
    return elves


@app.get('/elves/{elf_id}', response_model=Elf)
async def get_elf(*, session: Session = Depends(get_session), elf_id: int):
    elf = session.get(Elf, elf_id)
    if not elf:
        raise HTTPException(status_code=404, detail='Elf not found')
    return elf


@app.patch('/elves/{elf_id}', response_model=Elf)
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


@app.delete('/elves/{elf_id}')
async def delete_elf(*, session: Session = Depends(get_session), elf_id: int):
    db_elf = session.get(Elf, elf_id)
    if not db_elf:
        raise HTTPException(status_code=404, detail='Elf not found')
    
    session.delete(db_elf)
    session.commit()
    return {'ok': True}
    
    
@app.post('/elves/{elf_id}/holiday/', response_model=Elf)
async def asign_holiday(*, session: Session = Depends(get_session), elf_id: int, holiday: Holiday):
    db_elf = session.get(Elf, elf_id)
    if not db_elf:
        raise HTTPException(status_code=404, detail='Elf not found')
    
    db_elf.holidays.append(holiday)
    session.commit()
    session.refresh(db_elf)
    return db_elf
