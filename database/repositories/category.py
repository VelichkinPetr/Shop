from database.repositories.base import BaseRepo
from models import Category


class CategoryRepo(BaseRepo):

   model = Category