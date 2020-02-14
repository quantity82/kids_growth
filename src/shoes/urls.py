from django.urls import path
from . import views

app_name = 'shoes'

urlpatterns = [
    path('shoes/list/', views.shoes_data_list, name='shoes_data_list'),
    path('shoes/list/<kidsProfileId>', views.shoes_data_list, name='shoes_data_list'),
    path('shoes/data_add/', views.shoes_data_add, name='shoes_data_add'),
    path('shoes/data_edit/<shoesDataId>', views.shoes_data_edit, name='shoes_data_edit'),
    path('shoes/data_delete/<shoesDataId>', views.shoes_data_delete, name='shoes_data_delete'),
]
