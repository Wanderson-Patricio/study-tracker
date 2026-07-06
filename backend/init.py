from sqlite_orm import DatabaseContextManager
from sqlite_orm.model import Model

from .model import ModelRegistry
from .constants import DATABASE_NAME
from .backend import Backend


def create_table(db_manager: DatabaseContextManager, model_class: Model) -> None:
    if not db_manager.table_exists(model_class.__tablename__):
        session = db_manager.get_session(model_class)
        session.create_table().execute()


def init_database(model_registry: ModelRegistry) -> None:
    classes = model_registry._registry.values()
    with DatabaseContextManager(DATABASE_NAME) as db_manager:
        for model_class in classes:
            create_table(db_manager, model_class)


def init_backend() -> Backend:
    model_registry = ModelRegistry()

    init_database(model_registry)
    
    return Backend(DATABASE_NAME, model_registry)