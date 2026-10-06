from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("pergunta/<int:n>/", views.question, name="question"),
    path("resultado/", views.result, name="result"),
]
