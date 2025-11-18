from django.urls import path
from . import views

app_name = 'claude'

urlpatterns = [
    path('', views.ClaudeHomeView.as_view(), name='home'),
    path('upload/', views.JSONUploadView.as_view(), name='upload_json'),
    path('list/', views.list_entries, name='list_entries'),
    path('detail/<int:pk>/', views.DataEntryDetailView.as_view(), name='detail_entry'),
    path('delete-all/', views.DeleteAllDataView.as_view(), name='delete_all'),
]