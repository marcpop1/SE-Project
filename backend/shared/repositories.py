from typing import Optional, TypeVar, Generic, Type

from fastapi import HTTPException
from sqlalchemy.orm import Session


T = TypeVar('T')


class BaseRepository(Generic[T]):

    def __init__(self, model: Type[T], session: Session):
        self.model = model
        self.session = session

    def save(self, entity: T) -> T:
        self.session.add(entity)
        self.session.commit()
        self.session.refresh(entity)
        return entity

    def update(self, entity: T) -> T:
        self.session.merge(entity)
        self.session.commit()
        self.session.refresh(entity)
        return entity

    def delete(self, entity: T) -> None:
        self.session.delete(entity)
        self.session.commit()

    def find_by_id(self, id: int) -> Optional[T]:
        entity = self.session.query(self.model).filter(self.model.id == id).first()
        if not entity:
            raise HTTPException(status_code=404, detail=f"Entity with id {id} not found")
        return entity

    def find_all(self) -> list[T]:
        return self.session.query(self.model).all()
