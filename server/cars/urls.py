from django.urls import path

# //////////////////////// VIEWS ///////////////
from .views import GetAvtoTypesView, GetMarkaWithTypeView

urlpatterns = [
    path("avtotype/", GetAvtoTypesView.as_view()),
    path("marka/", GetMarkaWithTypeView.as_view()),
]
