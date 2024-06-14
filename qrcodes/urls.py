# qrcodes/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_qr, name='create_qr'),
    path('update/<str:edit_code>/', views.update_qr, name='update_qr'),
    path('success/<str:edit_code>/', views.success_page, name='success_page'),
    path('view/<str:edit_code>/', views.view_content, name='view_content'),
    path('instructions/<str:edit_code>/', views.instructions_page, name='instructions_page'),
]
