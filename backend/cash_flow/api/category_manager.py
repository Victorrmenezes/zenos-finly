from django.shortcuts import get_object_or_404
from ..models import Category

class CategoryManager:
    
    @classmethod
    def get_category_by_name(cls, name):
        """
        Retrieve a category by its name.
        """
        category = Category.objects.filter(name=name).first()
        return category

    def create_category(self, name, is_income=True):
        """
        Create a new category with the given name and type.
        Example:
        create_category(name='Salary', type='INCOME')
        """
        category_type = 'INCOME' if is_income else 'EXPENSE'
        category = self.get_category_by_name(name)
        if category:
            return category
        category = Category.objects.create(name=name, type=category_type)
        return category

    def update_category(self, category_id, name=None, type=None):
        """
        Update an existing category by ID.
        Example:
        update_category(category_id=1, name='Updated Salary', type='INCOME')
        """
        category = get_object_or_404(Category, id=category_id)
        if name is not None:
            category.name = name
        if type is not None:
            category.type = type
        category.save()
        return category

    def delete_category(self, category_id):
        """
        Delete a category by ID.
        """
        category = get_object_or_404(Category, id=category_id)
        category.delete()