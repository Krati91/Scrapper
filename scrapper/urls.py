from django.urls import path
from . import views

app_name = 'scrapper'
urlpatterns = [
    path('',views.show_list,name='show-list'),
    path('collect-structured-data/',views.collect_structured_data,name='collect_structured_data'),
    path('collect-structured-data/categorize-url/',views.categorize_url,name="categorize_url")
]