from sqlalchemy.orm import Session

from api.errors.Exceptions import HTTPError
from database.repositories import CategoryRepo
from schemas import CategoryRead, CategoryCreate, CategoryUpdate


class CategoryService:
    category_repo = CategoryRepo
    category_schema = CategoryRead

    @classmethod
    def create_category(cls,
                        db: Session,
                        category_data: CategoryCreate
    ) -> CategoryRead:
        new_product = cls.category_repo.create(db, category_data)
        return cls.category_schema.model_validate(new_product)

    @classmethod
    def get_category(cls,
                     db: Session,
                     category_id: int
    ) -> CategoryRead | None:
        category = cls.category_repo.get_by_id(db, category_id)
        if category is not None:
            return cls.category_schema.model_validate(category)
        return None


    @classmethod
    def list_categories(cls,
                        db: Session
    ) -> list[CategoryRead]:
        categories = cls.category_repo.get_all(db)
        categories_out = []
        for category in categories:
            categories_out.append(cls.category_schema.model_validate(category))
        return categories_out

    @classmethod
    def update_category(cls,
                        db: Session,
                        category_id: int,
                        category_data: CategoryUpdate
    ) -> CategoryRead | None:
        category = cls.category_repo.update(db, category_id, category_data)
        if category is not None:
            return cls.category_schema.model_validate(category)
        return None

    @classmethod
    def delete_category(cls,
                        db: Session,
                        category_id: int
    ) -> bool:
        product = cls.category_repo.get_by_id(db, category_id)
        if product is not None:
            cls.category_repo.delete_by_id(db, category_id)
            return True
        return False