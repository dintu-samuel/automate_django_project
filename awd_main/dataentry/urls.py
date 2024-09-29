
from django.urls import path
from . import views

urlpatterns = [
    path('import-data/',views.importdata,name="import_data"),
    path('export-data/',views.exportdata,name="export_data")
]
