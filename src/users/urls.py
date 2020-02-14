from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('', views.mypage, name='mypage'),
    path('signup/', views.signup, name='signup'),
    path('mypage/', views.mypage, name='mypage'),
    path('login/', views.login_mypage.as_view(), name='login'),
    path('logout/', views.logout.as_view(), name='logout'),
    path('kids_profile_add/', views.kids_profile_add, name='kids_profile_add'),
    path('kids_profile_edit/<kidsProfileId>', views.kids_profile_edit, name='kids_profile_edit'),
    path('kids_profile_delete/<kidsProfileId>', views.kids_profile_delete, name='kids_profile_delete'),
]
