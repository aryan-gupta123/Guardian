from django.urls import path
from . import views
from . import auth_views

urlpatterns = [
    # Homepage
    path('', views.homepage, name='homepage'),
    
    # Authentication Routes
    path('login/', auth_views.login_view, name='login'),
    path('signup/', auth_views.signup_view, name='signup'),
    path('logout/', auth_views.logout_view, name='logout'),
    path('dashboard/', auth_views.dashboard_view, name='dashboard'),
    
    # API Routes
    path('api/ingest/', views.ingest_transaction, name='ingest_transaction'),
    path('api/score/<int:transaction_id>/', views.score_transaction, name='score_transaction'),
    path('api/ml-score/', views.ml_score_transaction, name='ml_score_transaction'),
    path('api/agents/act/', views.agent_action, name='agent_action'),
    path('api/merchant/<int:merchant_id>/', views.get_merchant, name='get_merchant'),
    path('api/explain/<int:transaction_id>/', views.explain_transaction, name='explain_transaction'),
    path('api/high-risk/', views.get_high_risk_transactions, name='get_high_risk_transactions'),
]

