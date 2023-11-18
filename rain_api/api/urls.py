from django.urls import path
from . import views

urlpatterns = [
    path("getprecip/", views.get_precip, name="GetPrecip"),
    path("checkdata/", views.check_data_exist, name="CheckData")
]