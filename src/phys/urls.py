from django.urls import path
from . import views

app_name = 'phys'

urlpatterns = [
    path('phys/list/', views.phys_data_list, name='phys_data_list'),
    path('phys/list/<kidsProfileId>', views.phys_data_list, name='phys_data_list'),
    path('phys/data_add/', views.phys_data_add, name='phys_data_add'),
    path('phys/data_edit/<dataPostId>', views.phys_data_edit, name='phys_data_edit'),
    path('phys/data_delete/', views.phys_data_delete, name='phys_data_delete'),
    path('phys/graph/', views.graph_page_display, name='graph_page_display'),
    path('phys/graph/<kidsProfileId>', views.graph_page_display, name='graph_page_display'),
    path('data/graph_imaga/', views.graph_image_display, name='graph_image_display'),
    path('data/graph_imaga/<kidsProfileId>', views.graph_image_display, name='graph_image_display'),
]
