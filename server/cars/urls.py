from django.urls import path

# //////////////////////// VIEWS ///////////////
from .views import (
    GetAvtoTypesView,
    GetMarkaWithTypeView,
    GetModelsWithMarkaView,
    GetColorsView,
    GetCountriesView,
    GetFuelsView,
    AddCarView,
    UploadCarImageView,
    GetAllCarsView,
    GetCarByIDView,
    GetUserCarsFDraftView,
    GetUserCarsPublished,
)

urlpatterns = [
    path("avtotype/", GetAvtoTypesView.as_view()),
    path("marka/", GetMarkaWithTypeView.as_view()),
    path("models/", GetModelsWithMarkaView.as_view()),
    path("colors/", GetColorsView.as_view()),
    path("countries/", GetCountriesView.as_view()),
    path("fuel/", GetFuelsView.as_view()),
    path("upload/", AddCarView.as_view()),
    path("upload/image/", UploadCarImageView.as_view()),
    path("car/<uuid:pk>/", GetCarByIDView.as_view()),
    path("cars/", GetAllCarsView.as_view()),
    path("user/cars/draft/", GetUserCarsFDraftView.as_view()),
    path("user/cars/published/", GetUserCarsPublished.as_view()),
]
