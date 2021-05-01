from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("handleForm", views.handleForm, name="handleForm"),
    path("newPage", views.newPage, name="newPage"),
    path("randomPage", views.randomPage, name="randomPage"),
    path("editPage", views.editPage, name="editPage"),
    path("<str:title>", views.page, name="page")
]
