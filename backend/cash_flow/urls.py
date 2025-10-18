from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("invoices/", views.invoices, name="invoices"),
    path("adicionar-pedido/", views.add_transaction, name="add_transaction"),
    path("adicionar-produto/", views.add_product, name="add_product"),
    path("update_transaction/<int:transaction_id>/", views.update_transaction, name="update_transaction"),
    path("delete_transaction/<int:transaction_id>/", views.delete_transaction, name="delete_transaction"),
    path("update_stock/<int:transaction_id>/", views.update_stock, name="update_stock"),
]
