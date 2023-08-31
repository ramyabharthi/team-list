from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('team_list/', views.team_list, name='team_list'),
    path('add_team/', views.add_team, name='add_team'),
    path('delete_team/', views.delete_team, name='delete_team'),
    path('get_team_data/', views.get_team_data, name='get_team_data'),
    path('update_team/', views.update_team, name='update_team'),
    path('team_report/', views.team_report, name='team_report'),

]