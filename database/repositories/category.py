from database.repositories import BaseRepo
from models import Category


class CategoryRepo(BaseRepo):

   model = Category