from django.urls import path, include
from .views import ItemView, AuctionView
from rest_framework import routers

router = routers.DefaultRouter()
router.register('auction', AuctionView)
router.register('items', ItemView)

urlpatterns = [
  path("", include(router.urls))
  # path("auction/<int:pk>/", AuctionUpdateView.as_view()),
]
