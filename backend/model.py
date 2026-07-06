from sqlite_orm.model import Model
from sqlite_orm.field import UUID, Integer, String, DateTime, ForeignKey, Boolean, Date


class ModelRegistry:
    _registry = {}

    @classmethod
    def register(cls, model_class: Model) -> None:
        cls._registry[model_class.__name__] = model_class
        return model_class

    @classmethod
    def get_model(cls, table_name: str) -> Model:
        return cls._registry.get(table_name)
    
    def __str__(self) -> str:
        return f"ModelRegistry(models={[cls.__name__ for cls in self._registry.values()]})"


@ModelRegistry.register
class Exam(Model):
    __tablename__ = "Exams"

    id = UUID()
    name = String(max_length=255, nullable=False)
    target_date = DateTime(nullable=False)
    created_at = DateTime(nullable=False)


@ModelRegistry.register
class Discipline(Model):
    __tablename__ = "Disciplines"

    id = UUID()
    name = String(max_length=255, nullable=False)
    created_at = DateTime(nullable=False)
    exam_id = UUID(
        primary_key=False,
        foreign_key=ForeignKey(
            reference_table="Exams",
            reference_field="id",
            on_delete="CASCADE",
            on_update="SET NULL"
        ), 
        nullable=False
    )


@ModelRegistry.register
class Content(Model):
    __tablename__ = "Contents"

    id = UUID()
    name = String(max_length=255, nullable=False)
    created_at = DateTime(nullable=False)
    is_completed = Boolean(nullable=False)
    completed_at = DateTime(nullable=True)

    discipline_id = UUID(
        primary_key=False,
        foreign_key=ForeignKey(
            reference_table="Disciplines",
            reference_field="id",
            on_delete="CASCADE",
            on_update="SET NULL"
        ), 
        nullable=False
    )


@ModelRegistry.register
class Folder(Model):
    __tablename__ = "Folders"

    id = UUID()
    name = String(max_length=50, nullable=False)

    content_id = UUID(
        primary_key=False,
        foreign_key=ForeignKey(
            reference_table="Contents",
            reference_field="id",
            on_delete="CASCADE",
            on_update="SET NULL"
        ), 
        nullable=False
    )


@ModelRegistry.register
class MaterialLink(Model):
    __tablename__ = "MaterialLinks"

    id = UUID()
    name = String(max_length=255, nullable=False)
    url = String(max_length=255, nullable=False)

    folder_id = UUID(
        primary_key=False,
        foreign_key=ForeignKey(
            reference_table="Folders",
            reference_field="id",
            on_delete="CASCADE",
            on_update="SET NULL"
        ), 
        nullable=False
    )


@ModelRegistry.register
class PracticeTest(Model):
    __tablename__ = "PracticeTests"

    id = UUID()
    identifier_name = String(max_length=255, nullable=False)
    url = String(max_length=255, nullable=False)
    attempt_date = Date(nullable=False)

    total_questions = Integer(nullable=False)
    correct_answers = Integer(nullable=False)

    discipline_id = UUID(
        primary_key=False,
        foreign_key=ForeignKey(
            reference_table="Disciplines",
            reference_field="id",
            on_delete="CASCADE",
            on_update="SET NULL"
        ), 
        nullable=False
    )