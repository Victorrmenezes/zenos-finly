from django.urls import path
from . import views

urlpatterns = [
    path("investment/", views.home, name="home"),
    path("instrument_list/", views.instrument_list, name="instrument_list"),
    path("portfolio_list/", views.portfolio_list, name="portfolio_list"),
    path("record_list/", views.record_list, name="record_list"),
]
