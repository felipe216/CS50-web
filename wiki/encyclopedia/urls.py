from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.render_wiki, name="render_wiki"),
    path("edit/<str:title>", views.edit, name="edit"),
    path("search/", views.search, name="search"),
    path("create", views.create, name="create"),
    path("random", views.random, name="random")
]
