from django.urls import path
from . import views

urlpatterns = [
    path('', views.compose_view, name='compose'),
    path('compose/', views.compose_view, name='compose'),
    path('sent/', views.sent_view, name='sent'),
    path('sent/<int:pk>/', views.email_detail_view, name='email_detail'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
]
