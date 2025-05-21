from django.urls import path
from .views import RegisterView, FileUploadView, FileDeleteView
from rest_framework_simplejwt.views import TokenObtainPairView

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', TokenObtainPairView.as_view()),
    path('files/', FileUploadView.as_view()),
    path('files/<int:pk>/', FileDeleteView.as_view()),
]
