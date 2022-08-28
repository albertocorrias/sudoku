from django.urls import path, include

from . import views

app_name = 'sudoku_app'

urlpatterns = [
    path('', views.index, name='index'),
    path('new_puzzle_from_diff_level_change', views.new_puzzle_from_diff_level_change, name='new_puzzle_from_diff_level_change'),
    path('new_puzzle', views.new_puzzle, name='new_puzzle'),
    path('<int:puzzle_id>', views.new_specific_puzzle, name='new_specific_puzzle'),
    path('accounts/', include('django.contrib.auth.urls')),
]
