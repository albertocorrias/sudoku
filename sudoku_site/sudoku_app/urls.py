from django.urls import path, include

from . import views

app_name = 'sudoku_app'

urlpatterns = [
    path('home/', views.home,name="home"),
    path('', views.index, name='index'),
    path('index/', views.index, name='index'),
    path('new_puzzle_from_diff_level_change', views.new_puzzle_from_diff_level_change, name='new_puzzle_from_diff_level_change'),
    path('new_puzzle', views.new_puzzle, name='new_puzzle'),
    path('<int:puzzle_id>', views.new_specific_puzzle, name='new_specific_puzzle'),
    path('sign_up/', views.sign_up,name='sign_up'),
    path('user/<int:user_id>/', views.user_page, name="user_page"),
    path('record_successful_puzzle/', views.record_successful_puzzle, name="record_successful_puzzle"),
]
