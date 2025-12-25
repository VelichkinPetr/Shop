from sqlalchemy.orm import Session

from database.repositories import ProductRepo, CategoryRepo
from models import Review
from schemas import ProductRead, ProductCreate, ProductUpdate, ReviewCreate, ReviewRead


class ProductService:

    product_repo = ProductRepo
    product_schema = ProductRead
    category_repo = CategoryRepo
    review_schema = ReviewRead

    @classmethod
    def create_product(cls,
           db: Session,
           product_data: ProductCreate
    ) -> ProductRead:
        new_product = cls.product_repo.create(db, product_data)
        return cls.product_schema.model_validate(new_product)

    @classmethod
    def get_by_filter(cls,
            db: Session,
            category_id: str = None,
            min_price: int = None,
            max_price: int = None,
            limit: int = 20,
            offset: int = 0
    ) -> list[ProductRead]:
        products = cls.product_repo.get_by_filter(db, category_id, min_price, max_price, limit, offset)
        products_out = []
        for product in products:
            products_out.append(cls.product_schema.model_validate(product))
        return products_out

    @classmethod
    def get_product(cls,
            db: Session,
            product_id: int,
    ) -> ProductRead | None:
        product = cls.product_repo.get_by_id(db, product_id)
        if product is not None:
            return cls.product_schema.model_validate(product)
        return None

    @classmethod
    def update_product(cls,
           db: Session,
           product_id: int,
           product_data: ProductUpdate
    ) -> ProductRead | None:
        product = cls.product_repo.get_by_id(db, product_id)
        if product is not None:
            updated_product = cls.product_repo.update(db, product_id, product_data)
            return cls.product_schema.model_validate(updated_product)
        return None

    @classmethod
    def add_category(cls,
            db: Session,
            product_id: int,
            category_id: int
    ) -> ProductRead | None:
        product = cls.product_repo.get_by_id(db, product_id)
        category = cls.category_repo.get_by_id(db, category_id)
        if product is not None and category is not None:
            new_product = cls.product_repo.add_category(db, product, category)
            return new_product
        return None

    @classmethod
    def add_review(cls,
            db: Session,
            profile_id: int,
            product_id: int,
            review_data: ReviewCreate
    ) -> ProductRead | None:
        product = cls.product_repo.get_by_id(db, product_id)
        if product is not None:
            new_review = Review(**review_data.model_dump(), product_id = product_id, profile_id = profile_id)
            updated_product = cls.product_repo.add_review(db, product, new_review)
            return cls.product_schema.model_validate(updated_product)
        return None

    @classmethod
    def get_reviews(cls,
                    db: Session,
                    product_id: int
    ) -> list[ReviewRead] | None:
        product = cls.product_repo.get_by_id(db, product_id)
        if product is not None:
            reviews = product.reviews
            reviews_out = []
            for review in reviews:
                reviews_out.append(cls.review_schema.model_validate(review))
            return reviews_out
        return None

    @classmethod
    def delete_product(cls,
               db: Session,
               product_id: int,
    ) -> bool:
        product = cls.product_repo.get_by_id(db, product_id)
        if product is not None:
            cls.product_repo.delete_by_id(db, product_id)
            return True
        return False