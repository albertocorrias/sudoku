from django.urls import path

from . import views

app_name = 'sudoku_app'

urlpatterns = [
    path('/', views.index, name='index'),
    path('/new_puzzle', views.new_puzzle, name='new_puzzle'),
    path('/<int:puzzle_id>', views.new_specific_puzzle, name='new_spec_puzzle'),
]
