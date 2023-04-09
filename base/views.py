from rest_framework import viewsets
from django.contrib.auth import authenticate, login, logout
from rest_framework.permissions import IsAuthenticated
from .models import (CustomUser, Client, EnvironmentalMetric, Recommendation, DataSource, Alert, ActionItem, HistoricalData, IndustryPricing, 
                     DataIngestionJob, AnalysisResult, MachineLearningModel, ModelTrainingJob, ModelPrediction, DataAggregation, Goal, Progress,
                     Document, Comment, UserInteraction)
from .serializers import (CustomUserSerializer, ClientSerializer, EnvironmentalMetricSerializer,
                          RecommendationSerializer, DataSourceSerializer, AlertSerializer,
                          ActionItemSerializer, HistoricalDataSerializer, IndustryPricingSerializer,
                          DataIngestionJobSerializer, AnalysisResultSerializer, MachineLearningModelSerializer,
                          ModelTrainingJobSerializer, ModelPredictionSerializer, DataAggregationSerializer, 
                          GoalSerializer, ProgressSerializer, DocumentSerializer, CommentSerializer, UserInteractionSerializer)

from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from .utils import data_ingestion
from rest_framework import views, status
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]

class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated]

class EnvironmentalMetricViewSet(viewsets.ModelViewSet):
    queryset = EnvironmentalMetric.objects.all()
    serializer_class = EnvironmentalMetricSerializer
    permission_classes = [IsAuthenticated]

class RecommendationViewSet(viewsets.ModelViewSet):
    queryset = Recommendation.objects.all()
    serializer_class = RecommendationSerializer
    permission_classes = [IsAuthenticated]

class DataSourceViewSet(viewsets.ModelViewSet):
    queryset = DataSource.objects.all()
    serializer_class = DataSourceSerializer
    permission_classes = [IsAuthenticated]

class AlertViewSet(viewsets.ModelViewSet):
    queryset = Alert.objects.all()
    serializer_class = AlertSerializer
    permission_classes = [IsAuthenticated]

class ActionItemViewSet(viewsets.ModelViewSet):
    queryset = ActionItem.objects.all()
    serializer_class = ActionItemSerializer
    permission_classes = [IsAuthenticated]

class HistoricalDataViewSet(viewsets.ModelViewSet):
    queryset = HistoricalData.objects.all()
    serializer_class = HistoricalDataSerializer
    permission_classes = [IsAuthenticated]


class IndustryPricingViewSet(viewsets.ModelViewSet):
    queryset = IndustryPricing.objects.all()
    serializer_class = IndustryPricingSerializer

class DataIngestionJobViewSet(viewsets.ModelViewSet):
    queryset = DataIngestionJob.objects.all()
    serializer_class = DataIngestionJobSerializer
    permission_classes = [IsAuthenticated]

class AnalysisResultViewSet(viewsets.ModelViewSet):
    queryset = AnalysisResult.objects.all()
    serializer_class = AnalysisResultSerializer
    permission_classes = [IsAuthenticated]

class MachineLearningModelViewSet(viewsets.ModelViewSet):
    queryset = MachineLearningModel.objects.all()
    serializer_class = MachineLearningModelSerializer
    permission_classes = [IsAuthenticated]

class ModelTrainingJobViewSet(viewsets.ModelViewSet):
    queryset = ModelTrainingJob.objects.all()
    serializer_class = ModelTrainingJobSerializer
    permission_classes = [IsAuthenticated]

class ModelPredictionViewSet(viewsets.ModelViewSet):
    queryset = ModelPrediction.objects.all()
    serializer_class = ModelPredictionSerializer
    permission_classes = [IsAuthenticated]

class DataAggregationViewSet(viewsets.ModelViewSet):
    queryset = DataAggregation.objects.all()
    serializer_class = DataAggregationSerializer
    permission_classes = [IsAuthenticated]

class GoalViewSet(viewsets.ModelViewSet):
    queryset = Goal.objects.all()
    serializer_class = GoalSerializer
    permission_classes = [IsAuthenticated]

class ProgressViewSet(viewsets.ModelViewSet):
    queryset = Progress.objects.all()
    serializer_class = ProgressSerializer
    permission_classes = [IsAuthenticated]

class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = [IsAuthenticated]

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

class UserInteractionViewSet(viewsets.ModelViewSet):
    queryset = UserInteraction.objects.all()
    serializer_class = UserInteractionSerializer
    permission_classes = [IsAuthenticated]

@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    serializer = CustomUserSerializer(data=request.data)
    if serializer.is_valid():
        user = get_user_model().objects.create_user(
            username=serializer.validated_data['username'],
            password=serializer.validated_data['password']
        )
        return Response({"detail": "User registered successfully"}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class DataIngestionView(views.APIView):
    parser_classes = [MultiPartParser]

    def post(self, request, format=None):
        data_file = request.FILES.get('data_file', None)
        if not data_file:
            return Response({"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            data = data_ingestion.load_data(data_file.temporary_file_path())
            # Process and store the ingested data as required, and then return the response
            return Response({"success": "Data processed successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class RegisterView(views.APIView):
    def post(self, request):
        serializer = ClientSerializer(data=request.data)
        if serializer.is_valid():
            client = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class LoginView(views.APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_401_UNAUTHORIZED)

class LogoutView(views.APIView):
    def post(self, request):
        logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)