from django.urls import path

# //////////////////////// VIEWS ///////////////
from .views import (
    GetAvtoTypesView,
    GetMarkaWithTypeView,
    GetModelsWithMarkaView,
    GetColorsView,
    GetCountriesView,
    GetFuelsView,
    CarView,
    CarImageView,
    GetAllCarsView,
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
    
    # post
    path("car/upload/", CarView.as_view()),
    # get put patch delete
    path("car/<uuid:pk>/", CarView.as_view()),
    
    path("car/image/upload/", CarImageView.as_view()),
    path("car/image/<uuid:pk>/", CarImageView.as_view()),
    
    path("cars/", GetAllCarsView.as_view()),
    path("user/cars/draft/", GetUserCarsFDraftView.as_view()),
    path("user/cars/published/", GetUserCarsPublished.as_view()),
]
