from django.urls import path 
from . import views 

urlpatterns = [
    path('', views.getRoutes), 
    path('activities/', views.getActivities),
    path('activities/<str:pk>/', views.getActivity),
]
