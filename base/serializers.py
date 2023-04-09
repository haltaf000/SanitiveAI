from .models import ( CustomUser, Client, EnvironmentalMetric, Recommendation, DataSource, Alert, ActionItem, HistoricalData, IndustryPricing, 
                     DataIngestionJob, AnalysisResult, MachineLearningModel, ModelTrainingJob, ModelPrediction, DataAggregation, Goal, Progress,
                     Document, Comment, UserInteraction)
from rest_framework import serializers

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}
        
    def create(self, validated_data):
        client = Client.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            company_name=validated_data['company_name'],
            industry=validated_data['industry'],
            contact_information=validated_data['contact_information'],
            billing_details=validated_data['billing_details'],
        )
        return client
         
class EnvironmentalMetricSerializer(serializers.ModelSerializer):
    class Meta:
        model = EnvironmentalMetric
        fields = '__all__'

class RecommendationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recommendation
        fields = '__all__'
        
        
class DataSourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataSource
        fields = '__all__'

class AlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alert
        fields = '__all__'
        
        
class ActionItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActionItem
        fields = '__all__'

class HistoricalDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoricalData
        fields = '__all__'
        
class IndustryPricingSerializer(serializers.ModelSerializer):
    class Meta:
        model = IndustryPricing
        fields = '__all__'
        
        
class DataIngestionJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataIngestionJob
        fields = '__all__'

class AnalysisResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnalysisResult
        fields = '__all__'

class MachineLearningModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = MachineLearningModel
        fields = '__all__'

class ModelTrainingJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModelTrainingJob
        fields = '__all__'

class ModelPredictionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModelPrediction
        fields = '__all__'

class DataAggregationSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataAggregation
        fields = '__all__'

class GoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goal
        fields = '__all__'

class ProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Progress
        fields = '__all__'

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

class UserInteractionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInteraction
        fields = '__all__'
        
