from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("estoque/", views.stock, name="stock"),
    path("adicionar-pedido/", views.add_order, name="add_order"),
    path("adicionar-produto/", views.add_product, name="add_product"),
    path("update_order/<int:order_id>/", views.update_order, name="update_order"),
    path("delete_order/<int:order_id>/", views.delete_order, name="delete_order"),
    path("update_stock/<int:order_id>/", views.update_stock, name="update_stock"),
]
