from django.db import models
from django.contrib.auth.models import AbstractUser, Permission
from django.utils import timezone
import datetime

# Pricing    
class IndustryPricing(models.Model):
    industry = models.CharField(max_length=255, unique=True)
    price_tier1 = models.DecimalField(max_digits=10, decimal_places=2)
    price_tier2 = models.DecimalField(max_digits=10, decimal_places=2)
    price_tier3 = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.industry
    
    def tier1_price(self):
        return self.price_tier1

    def tier2_price(self):
        return self.price_tier2

    def tier3_price(self):
        return self.price_tier3
    
    def get_price_for_tier(self, tier):
        price_mapping = {1: self.price_tier1, 2: self.price_tier2, 3: self.price_tier3}
        return price_mapping.get(tier, None)

    def update_tier_price(self, tier, new_price):
        price_mapping = {1: 'price_tier1', 2: 'price_tier2', 3: 'price_tier3'}
        tier_price_field = price_mapping.get(tier)
        if tier_price_field:
            setattr(self, tier_price_field, new_price)
            self.save()
        else:
            raise ValueError("Invalid tier")

    def get_clients(self):
        return Client.objects.filter(industry=self.industry)



# Clients
class Client(models.Model):
    company_name = models.CharField(max_length=255)
    industry = models.CharField(max_length=255)
    contact_information = models.TextField()
    billing_details = models.TextField()
    industry_pricing = models.ForeignKey(IndustryPricing, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.company_name
    
    def get_total_spend(self):
        total_spend = 0
        subscriptions = self.subscription_set.all()
        for subscription in subscriptions:
            if subscription.industry_pricing:
                if subscription.tier == 1:
                    total_spend += subscription.industry_pricing.price_tier1
                elif subscription.tier == 2:
                    total_spend += subscription.industry_pricing.price_tier2
                elif subscription.tier == 3:
                    total_spend += subscription.industry_pricing.price_tier3
        return total_spend
    
    @property
    def total_spend(self):
        total_spend = 0
        subscriptions = self.subscription_set.all()
        for subscription in subscriptions:
            total_spend += subscription.industry_pricing.get_price_for_tier(subscription.tier)
        return total_spend
    
    def total_metric_value(self, metric_type):
        metrics = self.environmentalmetric_set.filter(metric_type=metric_type)
        total_value = sum(metric.value for metric in metrics)
        return total_value
    
    def total_historical_data_value(self, metric_type):
        historical_data = self.historicaldata_set.filter(metric_type=metric_type)
        total_value = sum(data.value for data in historical_data)
        return total_value
    
    def due_action_items(self):
        due_items = self.actionitem_set.filter(status="pending")
        return due_items

    def overdue_action_items(self):
        overdue_items = self.actionitem_set.filter(status="pending", due_date__lt=timezone.now())
        return overdue_items
    
    def total_goals(self):
        return self.goal_set.count()
    
    def completed_goals(self):
        return self.goal_set.filter(status="completed").count()

    def progress_percentage(self):
        progress = self.progress_set.last()
        if progress:
            return (progress.value / self.target_value) * 100
        return 0

    def get_active_subscription(self):
        today = timezone.now().date()
        active_subscriptions = self.subscription_set.filter(start_date__lte=today, end_date__gte=today)
        return active_subscriptions.first()
    
    def has_active_tier(self, tier):
        active_subscription = self.get_active_subscription()
        if active_subscription:
            return active_subscription.tier == tier
        return False
    
    def get_active_alerts(self):
        return self.alert_set.filter(sent__gte=timezone.now() - datetime.timedelta(days=30)).order_by('-sent')

    def get_documents_by_type(self, document_type):
        return self.document_set.filter(type=document_type)
    
    def get_documents_by_status(self, status):
        return self.document_set.filter(status=status)
    
    

# Environmental Metrics
class EnvironmentalMetric(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    metric_type = models.CharField(max_length=255)
    timestamp = models.DateTimeField()
    value = models.FloatField()
    
    def __str__(self):
        return f"{self.client.company_name} - {self.metric_type}"
    
    @classmethod
    def create_metric(cls, client, metric_type, value):
        new_metric = cls(client=client, metric_type=metric_type, value=value, timestamp=timezone.now())
        new_metric.save()
        return new_metric

# Recommendations
class Recommendation(models.Model):
    CATEGORY_CHOICES = [
        ('carbon_footprint', 'Carbon Footprint'),
        ('waste_reduction', 'Waste Reduction'),
        ('energy_efficiency', 'Energy Efficiency'),
        ('water_conservation', 'Water Conservation')
    ]
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    category = models.CharField(max_length=255, choices=CATEGORY_CHOICES)
    description = models.TextField()
    strategy = models.TextField()
    potential_impact = models.TextField()
    specific_properties = models.JSONField(null=True, blank=True)
    priority = models.IntegerField()
    status = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.client.company_name} - {self.get_category_display()}"
    
    def update_status(self, new_status):
        self.status = new_status
        self.save()
        
    

# Users
class CustomUser(AbstractUser):
    client = models.ForeignKey(Client, null=True, blank=True, on_delete=models.CASCADE)
    role = models.CharField(max_length=255)
    permissions = models.ManyToManyField(Permission, blank=True)

    def __str__(self):
        return self.username
    

# Data Sources
class DataSource(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    type = models.CharField(max_length=255)
    configuration = models.TextField()
    last_update = models.DateTimeField()
    
    def update_last_update(self):
        self.last_update = timezone.now()
        self.save()


# Alerts and Notifications
class Alert(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    type = models.CharField(max_length=255)
    message = models.TextField()
    sent = models.DateTimeField()
    
    @classmethod
    def create_alert(cls, client, user, alert_type, message):
        new_alert = cls(client=client, user=user, type=alert_type, message=message, sent=timezone.now())
        new_alert.save()
        return new_alert

# Action Items
class ActionItem(models.Model):
    recommendation = models.ForeignKey(Recommendation, on_delete=models.CASCADE)
    description = models.TextField()
    assignee = models.CharField(max_length=255)
    due_date = models.DateTimeField()
    status = models.CharField(max_length=255)
    
    def update_status(self, new_status):
        self.status = new_status
        self.save()

# Historical Data
class HistoricalData(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    metric_type = models.CharField(max_length=255)
    timestamp = models.DateTimeField()
    value = models.FloatField()
    source = models.TextField()
    
    @classmethod
    def create_historical_data(cls, client, metric_type, timestamp, value, source):
        new_historical_data = cls(client=client, metric_type=metric_type, timestamp=timestamp, value=value, source=source)
        new_historical_data.save()
        return new_historical_data
    
class DataIngestionJob(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    data_source = models.ForeignKey(DataSource, on_delete=models.CASCADE)
    status = models.CharField(max_length=255)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True, blank=True)
    frequency = models.DurationField()
    next_run = models.DateTimeField()
    
    def schedule_next_run(self):
        self.next_run = timezone.now() + self.frequency
        self.save()
        
    def mark_complete(self):
        self.status = "Completed"
        self.end_time = timezone.now()
        self.schedule_next_run()
        self.save()


class AnalysisResult(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    metric_type = models.CharField(max_length=255)
    timestamp = models.DateTimeField()
    result = models.JSONField()
    
    @classmethod
    def create_analysis_result(cls, client, metric_type, result):
        new_analysis_result = cls(client=client, metric_type=metric_type, result=result, timestamp=timezone.now())
        new_analysis_result.save()
        return new_analysis_result

class MachineLearningModel(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    metric_type = models.CharField(max_length=255)
    model_name = models.CharField(max_length=255)
    model_file = models.FileField(upload_to='models/')
    creation_date = models.DateTimeField()
    last_updated = models.DateTimeField()
    status = models.CharField(max_length=255)
    
    def update_status(self, new_status):
        self.status = new_status
        self.save()

class ModelTrainingJob(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    ml_model = models.ForeignKey(MachineLearningModel, on_delete=models.CASCADE)
    status = models.CharField(max_length=255)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True, blank=True)
    
    def update_status_and_times(self, new_status, start_time=None, end_time=None):
        self.status = new_status
        if start_time:
            self.start_time = start_time
        if end_time:
            self.end_time = end_time
        self.save()

class ModelPrediction(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    ml_model = models.ForeignKey(MachineLearningModel, on_delete=models.CASCADE)
    metric_type = models.CharField(max_length=255)
    timestamp = models.DateTimeField()
    value = models.FloatField()
    
    
    @classmethod
    def create_model_prediction(cls, client, ml_model, metric_type, value):
        new_model_prediction = cls(client=client, ml_model=ml_model, metric_type=metric_type, value=value, timestamp=timezone.now())
        new_model_prediction.save()
        return new_model_prediction
        
        
class ModelEvaluation(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    ml_model = models.ForeignKey(MachineLearningModel, on_delete=models.CASCADE)
    metric_type = models.CharField(max_length=255)
    timestamp = models.DateTimeField()
    value = models.FloatField()
    
    
class DataAggregation(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    metric_type = models.CharField(max_length=255)
    aggregation_type = models.CharField(max_length=255)
    timestamp = models.DateTimeField()
    value = models.FloatField()

class Goal(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    metric_type = models.CharField(max_length=255)
    target_value = models.FloatField()
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=255)
    
    def update_status(self, new_status):
        self.status = new_status
        self.save()
        
    

class Progress(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    goal = models.ForeignKey(Goal, on_delete=models.CASCADE)
    timestamp = models.DateTimeField()
    value = models.FloatField()
    status = models.CharField(max_length=255)
    
    def update_status_and_value(self, new_status, new_value):
        self.status = new_status
        self.value = new_value
        self.save()

class Document(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    type = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='documents/')
    upload_date = models.DateTimeField()
    
    

class Comment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    recommendation = models.ForeignKey(Recommendation, on_delete=models.CASCADE, null=True, blank=True)
    action_item = models.ForeignKey(ActionItem, on_delete=models.CASCADE, null=True, blank=True)
    timestamp = models.DateTimeField()
    content = models.TextField()
    
    
    def __str__(self):
        return f"{self.user.username} - {self.content}"
    
    
    @classmethod
    def create_comment(cls, user, recommendation, action_item, content):
        new_comment = cls(user=user, recommendation=recommendation, action_item=action_item, timestamp=timezone.now(), content=content)
        new_comment.save()
        return new_comment
        
        
    
        
class UserInteraction(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    interaction_type = models.CharField(max_length=255)
    timestamp = models.DateTimeField()
    details = models.JSONField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.interaction_type}"
    
    @classmethod
    def create_user_interaction(cls, user, interaction_type, details=None):
        new_user_interaction = cls(user=user, interaction_type=interaction_type, timestamp=timezone.now(), details=details)
        new_user_interaction.save()
        return new_user_interaction
    
    
class Notification(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    notification_type = models.CharField(max_length=255)
    timestamp = models.DateTimeField()
    details = models.JSONField(null=True, blank=True)
    is_read = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.user.username} - {self.notification_type}"
    
    @classmethod
    def create_notification(cls, user, notification_type, details=None):
        new_notification = cls(user=user, notification_type=notification_type, timestamp=timezone.now(), details=details)
        new_notification.save()
        return new_notification
    
    def mark_as_read(self):
        self.is_read = True
        self.save()
        
        
class UserSettings(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    settings_type = models.CharField(max_length=255)
    settings = models.JSONField()
    
    def __str__(self):
        return f"{self.user.username} - {self.settings_type}"
    
    @classmethod
    def create_user_settings(cls, user, settings_type, settings):
        new_user_settings = cls(user=user, settings_type=settings_type, settings=settings)
        new_user_settings.save()
        return new_user_settings
        
    def update_settings(self, new_settings):
        self.settings = new_settings
        self.save()
        
        
        
#subscription
class Subscription(models.Model):
    client = models.OneToOneField(Client, on_delete=models.CASCADE)
    industry_pricing = models.ForeignKey(IndustryPricing, on_delete=models.SET_NULL, null=True)
    tier = models.PositiveSmallIntegerField(choices=[(1, 'Tier 1'), (2, 'Tier 2'), (3, 'Tier 3')])
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"{self.client.company_name} - {self.industry_pricing.industry} - Tier {self.tier}"

    def renew_subscription(self):
        self.start_date = self.end_date
        self.end_date = self.start_date + datetime.timedelta(days=30)
        self.save()
        
class UserSubscription(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    subscription_type = models.CharField(max_length=255)
    subscription = models.JSONField()
    
    def __str__(self):
        return f"{self.user.username} - {self.subscription_type}"
    
    @classmethod
    def create_user_subscription(cls, user, subscription_type, subscription):
        new_user_subscription = cls(user=user, subscription_type=subscription_type, subscription=subscription)
        new_user_subscription.save()
        return new_user_subscription
        
    def update_subscription(self, new_subscription):
        self.subscription = new_subscription
        self.save()
