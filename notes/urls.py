from django.urls import path
from . import views

urlpatterns = [
    path('notes/', views.add_notes, name='add_notes'),  # Update the URL pattern to '/notes/'
    path('delete_note/', views.delete_note, name='delete_note'),
    path('edit_notes/<int:note_id>/', views.edit_notes, name='edit_notes'),
    path('get_notes/', views.get_notes, name='get_notes'),

]