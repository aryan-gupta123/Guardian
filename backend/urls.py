from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'merchants', views.MerchantViewSet)
router.register(r'transactions', views.TransactionViewSet)

urlpatterns = [
    path('ingest/', views.IngestView.as_view(), name='ingest'),
    path('score/', views.ScoreView.as_view(), name='score'),
    path('agents/act/', views.AgentActionView.as_view(), name='agent-action'),
    path('', include(router.urls)),
]

