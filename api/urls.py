from django.urls import path
from . import views
from knox import views as knox_views


urlpatterns = [
    # API for notes
    # get and create notes
    path('notes/', views.notes),
    # fetch, update and delete note by id
    path('notes/<int:pk>/', views.note),
    # get note by user
    path('notes/user', views.notes_by_user),
    # search notes
    path('notes/search', views.search_notes),

    # API for users auth
    # get user detail
    path('users/user/', views.get_user),
    # user login
    path('users/login/', views.login_api),
    # user register
    path('users/register/', views.register_api),
    # user logout
    path('users/logout/', knox_views.LogoutView.as_view()),
    # user logout all tokens
    path('users/logoutAll/', knox_views.LogoutAllView.as_view()),
]
