from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("cash_flow.urls")),
    path("", include("investment_hub.urls")),
]
