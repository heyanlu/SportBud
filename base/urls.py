from django.urls import path 
from . import views

urlpatterns = [
    path('', views.activities, name='activities'),
    path('activity/<str:pk>/', views.activity, name='activity'),
    path('create-activity/', views.createActivity, name='create-activity'),
    path('update-activity/<str:pk>/', views.updateActivity, name='update-activity'),
    path('delete-activity/<str:pk>/', views.deleteActivity, name='delete-activity'),
    # path('registration-confirmation/<str:pk>/', views.registrationConfirmation, name='registration-confirmation'),


]