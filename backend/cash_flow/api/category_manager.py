from django.shortcuts import get_object_or_404

from ..helpers import norm_str
from ..models import Category

class CategoryManager:
    queryset = Category.objects.all()

    def __init__(self, user):
        self.user = user
        self.category_by_name = {norm_str(cat.name): cat for cat in self.queryset}
    
    def get_category_by_name(self, name):
        """
        Retrieve a category by its name.
        """
        return self.category_by_name.get(norm_str(name))

    def create_category(self, name, is_approved=False):
        """
        Create a new category with the given name and type.
        """
        category = self.get_category_by_name(name)
        if category:
            return category
        category = Category.objects.create(name=name, is_approved=is_approved)
        return category

    def update_category(self, category_id, name=None, is_approved=None):
        """
        Update an existing category by ID.
        Example:
        update_category(category_id=1, name='Updated Salary', is_approved='INCOME')
        """
        category = get_object_or_404(Category, id=category_id)
        if name is not None:
            category.name = name
        if is_approved is not None:
            category.is_approved = is_approved
        category.save()
        return category

    def delete_category(self, category_id):
        """
        Delete a category by ID.
        """
        category = get_object_or_404(Category, id=category_id)
        category.delete()