from typing import List

from sqlmodel import Session, select
from fastapi import APIRouter, HTTPException, Depends, Query

from db.models import Item
from db.config import get_session


router = APIRouter(
    prefix='/items',
    tags=['items']
)


@router.post('/', response_model=Item, )
async def create_item(*, session: Session = Depends(get_session), item: Item):
    db_item = Item.model_validate(item)

    session.add(db_item)
    session.commit()
    session.refresh(db_item)
    return db_item


@router.get('/', response_model=List[Item])
async def get_items(
    *,
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=100, le=100)
):
    items = session.exec(select(Item).offset(offset).limit(limit)).all()
    return items


@router.get('/{item_id}', response_model=Item)
async def get_item(*, session: Session = Depends(get_session), item_id: int):
    db_item = session.get(Item, item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail='Item not found')

    return db_item


@router.patch('/{item_id}', response_model=Item)
async def update_item(*, session: Session = Depends(get_session), item_id: int, item: Item):
    db_item = session.get(Item, item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail='Item not found')
    
    db_item_data = item.model_dump(exclude_unset=True)
    for key, value in db_item_data.items():
        setattr(db_item, key, value)
    
    session.add(db_item)
    session.commit()
    session.refresh(db_item)
    return db_item  


@router.delete('/{item_id}', response_model=Item)
async def delete_item(*, session: Session = Depends(get_session), item_id: int):
    db_item = session.get(Item, item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail='Item not found')
    
    session.delete(db_item)
    session.commit()
    return {'ok': True}

