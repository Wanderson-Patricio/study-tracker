from sqlite_orm import Model, DatabaseContextManager
from sqlite_orm.selector import Count
from contextlib import contextmanager
from typing import Any, Generator, List, Union


ID_LIKE = Union[int, str]


class Controller:
    def __init__(self, db_name: str, model: Model) -> None:
        self.__db_name = db_name
        self.__model = model
        self.__db_manager = DatabaseContextManager(self.__db_name)

    @contextmanager
    def _session(self) -> Generator[Any, None, None]:
        with self.__db_manager as db_manager:
            yield db_manager.get_session(self.__model)

    def list(self, *, limit: int = 10, offset: int = 0, **filters) -> List[Model]:
        with self._session() as session:
            return (
                session.select()
                .all()
                .where(**filters)
                .limit(limit)
                .offset(offset)
                .to_model()
                .execute()
            )
        
    def get_by_id(self, id: ID_LIKE) -> Model:
        with self._session() as session:
            return (
                session.select()
                .first()
                .where(self.__model.id == id)
                .to_model()
                .execute()    
            )
        
    def get_by_field(self, field_name: str, value: Any) -> List[Model]:
        with self._session() as session:
            return (
                session.select()
                .all()
                .where(getattr(self.__model, field_name) == value)
                .to_model()
                .execute()
            )
        
    def create(self, model_instance: Model) -> ID_LIKE:
        with self._session() as session:
            return (
                session
                .insert(model_instance)
                .execute()
            )

    def update(self, *, id: ID_LIKE, **data) -> ID_LIKE:
        with self._session() as session:
            (
                session
                .update()
                .set(**data)
                .where(self.__model.id == id)
                .execute()
            )

            return id
        
    def delete(self, id: ID_LIKE) -> None:
        with self._session() as session:
            (
                session
                .delete()
                .where(self.__model.id == id)
                .execute()
            )

    def total_itens(self) -> int:
        with self._session() as session:
            total_object = (
                session
                .select(Count(self.__model).As("total"))
                .first()
                .to_model()
                .execute()
            )
            return total_object.total
    