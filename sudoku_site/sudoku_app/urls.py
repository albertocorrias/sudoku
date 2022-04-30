from django.urls import path

from . import views

app_name = 'sudoku_app'

urlpatterns = [
    path('', views.index, name='index'),
    path('new_puzzle', views.new_puzzle, name='new_puzzle'),
]
