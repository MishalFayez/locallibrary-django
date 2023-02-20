from django.urls import path
from . import views

urlpatterns = [
    path('book/', views.getBook),
    path('book/add/', views.addBook)
]
