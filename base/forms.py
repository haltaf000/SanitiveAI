from django import forms
from .models import Client, IndustryPricing, Subscription, EnvironmentalMetric, Recommendation, CustomUser, DataSource, Alert, ActionItem, HistoricalData, DataIngestionJob, AnalysisResult, MachineLearningModel, ModelTrainingJob, ModelPrediction, DataAggregation, Goal, Progress, Document, Comment, UserInteraction

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = [
            'company_name', 
            'industry', 
            'contact_information', 
            'billing_details'
        ]


class IndustryPricingForm(forms.ModelForm):
    class Meta:
        model = IndustryPricing
        fields = [
            'industry',
            'price_tier1',
            'price_tier2',
            'price_tier3'            
        ]

class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = Subscription
        fields = [
            'client',
            'industry_pricing',
            'tier',
            'start_date',
            'end_date',
        ]


class EnvironmentalMetricForm(forms.ModelForm):
    class Meta:
        model = EnvironmentalMetric
        fields = [
            'client',
            'metric_type',
            'timestamp',
            'value',
        ]

class RecommendationForm(forms.ModelForm):
    class Meta:
        model = Recommendation
        fields = [
            'client',
            'category',
            'description',
            'strategy',
            'potential_impact',
            'specific_properties',
            'priority',
            'status',
        ]

class CustomUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = [
            'client',
            'role',
            'permissions',
        ]

class DataSourceForm(forms.ModelForm):
    class Meta:
        model = DataSource
        fields = [
            'client',
            'type',
            'configuration',
            'last_update',
        ]

class AlertForm(forms.ModelForm):
    class Meta:
        model = Alert
        fields = [
            'client',
            'user',
            'type',
            'message',
            'sent',
        ]

class ActionItemForm(forms.ModelForm):
    class Meta:
        model = ActionItem
        fields = [
            'recommendation',
            'description',
            'assignee',
            'due_date',
            'status',
        ]

class HistoricalDataForm(forms.ModelForm):
    class Meta:
        model = HistoricalData
        fields = [
            'client',
            'metric_type',
            'timestamp',
            'value',
            'source',
        ]

class DataIngestionJobForm(forms.ModelForm):
    class Meta:
        model = DataIngestionJob
        fields = [
            'client',
            'data_source',
            'status',
            'start_time',
            'end_time',
            'frequency',
            'next_run',
        ]

class AnalysisResultForm(forms.ModelForm):
    class Meta:
        model = AnalysisResult
        fields = [
            'client',
            'metric_type',
            'timestamp',
            'result',
        ]

class MachineLearningModelForm(forms.ModelForm):
    class Meta:
        model = MachineLearningModel
        fields = [
            'client',
            'metric_type',
            'model_name',
            'model_file',
            'creation_date',
            'last_updated',
            'status',
        ]

class ModelTrainingJobForm(forms.ModelForm):
    class Meta:
        model = ModelTrainingJob
        fields = [
            'client',
            'ml_model',
            'status',
            'start_time',
            'end_time',
        ]
        
class ModelPredictionForm(forms.ModelForm):
    class Meta:
        model = ModelPrediction
        fields = [
            'client',
            'ml_model',
            'prediction',
            'timestamp',
        ]

class DataAggregationForm(forms.ModelForm):
    class Meta:
        model = DataAggregation
        fields = [
            'client',
            'metric_type',
            'start_timestamp',
            'end_timestamp',
            'aggregated_value',
        ]

class GoalForm(forms.ModelForm):
    class Meta:
        model = Goal
        fields = [
            'client',
            'description',
            'start_date',
            'end_date',
            'progress',
            'status',
        ]

class ProgressForm(forms.ModelForm):
    class Meta:
        model = Progress
        fields = [
            'goal',
            'timestamp',
            'value',
        ]

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = [
            'client',
            'title',
            'file',
            'uploaded_by',
            'upload_date',
        ]

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = [
            'user',
            'document',
            'text',
            'timestamp',
        ]

class UserInteractionForm(forms.ModelForm):
    class Meta:
        model = UserInteraction
        fields = [
            'user',
            'interaction_type',
            'timestamp',
            'details',
        ]
