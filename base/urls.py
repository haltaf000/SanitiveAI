from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import DataIngestionView

router = DefaultRouter()
router.register(r'users', views.CustomUserViewSet)
router.register(r'clients', views.ClientViewSet)
router.register(r'environmental-metrics', views.EnvironmentalMetricViewSet)
router.register(r'recommendations', views.RecommendationViewSet)
router.register(r'data-sources', views.DataSourceViewSet)
router.register(r'alerts', views.AlertViewSet)
router.register(r'action-items', views.ActionItemViewSet)
router.register(r'historical-data', views.HistoricalDataViewSet)
router.register(r'data-ingestion-jobs', views.DataIngestionJobViewSet)
router.register(r'industry-pricing', views.IndustryPricingViewSet)
router.register(r'analysis-results', views.AnalysisResultViewSet)
router.register(r'machine-learning-models', views.MachineLearningModelViewSet)
router.register(r'model-training-jobs', views.ModelTrainingJobViewSet)
router.register(r'model-predictions', views.ModelPredictionViewSet)
router.register(r'data-aggregations', views.DataAggregationViewSet)
router.register(r'goals', views.GoalViewSet)
router.register(r'progresses', views.ProgressViewSet)
router.register(r'documents', views.DocumentViewSet)
router.register(r'comments', views.CommentViewSet)
router.register(r'user-interactions', views.UserInteractionViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api/ingest_data/', DataIngestionView.as_view(), name='ingest_data'),
    path('api/register/', views.register, name='register'),

]
