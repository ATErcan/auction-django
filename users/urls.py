from django.urls import path
from users.views import RegisterView, UserUpdateView


urlpatterns = [
  path('register/', RegisterView.as_view()),
  path('user/<int:pk>/', UserUpdateView.as_view()),
]
