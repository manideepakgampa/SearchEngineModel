# Project-1/edusearch/main/models.py
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from elasticsearch_dsl import Document, connections
from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.search import SearchVectorField


class EducationalResource(models.Model):
    RESOURCE_TYPES = (
        ('course', 'Online Course'),
        ('video', 'Video Tutorial'),
        ('paper', 'Research Paper'),
        ('book', 'E-Book'),
        ('tool', 'Learning Tool'),
    )
    
    DIFFICULTY_LEVELS = (
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    )

    # Core Fields
    title = models.CharField(max_length=500)
    url = models.URLField(unique=True)
    content = models.TextField(help_text="Cleaned text content from source")
    source = models.CharField(max_length=100, db_index=True)  # e.g., Coursera, YouTube
    resource_type = models.CharField(max_length=20, choices=RESOURCE_TYPES)
    
    # Metadata
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_LEVELS)
    duration = models.PositiveIntegerField(help_text="In minutes", null=True)
    rating = models.FloatField(null=True, blank=True)
    
    # NLP Fields
    keywords = models.JSONField(default=list, help_text="AI-generated keywords")
    entities = models.JSONField(default=list, help_text="Named entities from NLP")
    
    # System Fields
    created_at = models.DateTimeField(auto_now_add=True)
    last_scraped = models.DateTimeField(auto_now=True)
    is_verified = models.BooleanField(default=False)

    class Meta:
        indexes = [
            models.Index(fields=['title', 'source']),
            models.Index(fields=['resource_type', 'difficulty']),
        ]

    def _str_(self):
        return f"{self.source} - {self.title[:50]}"

class UserQuery(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    query_text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    filters_used = models.JSONField(default=dict)
    results_count = models.PositiveIntegerField()
    
    # NLP Analysis Cache
    semantic_vector = models.JSONField(null=True, help_text="BERT embeddings")
    query_entities = models.JSONField(default=list)

class UserInteraction(models.Model):
    INTERACTION_TYPES = (
        ('click', 'Resource Click'),
        ('save', 'Resource Saved'),
        ('rating', 'Rating Given'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    resource = models.ForeignKey(EducationalResource, on_delete=models.CASCADE)
    interaction_type = models.CharField(max_length=20, choices=INTERACTION_TYPES)
    metadata = models.JSONField(default=dict)  # e.g., rating value, timestamp
    created_at = models.DateTimeField(auto_now_add=True)

class RecommendationProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    preferred_topics = models.JSONField(default=list)
    learning_style = models.CharField(max_length=100, blank=True)
    difficulty_preference = models.CharField(
        max_length=20,
        choices=EducationalResource.DIFFICULTY_LEVELS,
        default='beginner'
    )
    last_updated = models.DateTimeField(auto_now=True)

# ElasticSearch Integration
@receiver(post_save, sender=EducationalResource)
def update_document(sender, instance=None, created=False, **kwargs):
    """Sync model with ElasticSearch index"""
    index = EducationalResourceIndex(
        meta={'id': instance.id},
        title=instance.title,
        content=instance.content,
        source=instance.source,
        resource_type=instance.resource_type,
        price=float(instance.price),
        difficulty=instance.difficulty,
        url=instance.url,
        keywords=instance.keywords,
        entities=instance.entities
    )
    index.save()

@receiver(post_delete, sender=EducationalResource)
def delete_document(sender, instance=None, **kwargs):
    """Delete document from ElasticSearch index"""
    EducationalResourceIndex(meta={'id': instance.id}).delete()

connections.create_connection(hosts=['localhost'])
class EducationalResource(models.Model):
    RESOURCE_TYPES = (
        ('course', 'Course'),
        ('video', 'Video'),
        ('paper', 'Research Paper'),
        ('book', 'E-Book'),
    )
    
    title = models.CharField(max_length=500)
    url = models.URLField(unique=True)
    content = models.TextField()
    source = models.CharField(max_length=100)
    resource_type = models.CharField(max_length=20, choices=RESOURCE_TYPES)
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    embeddings = models.JSONField(null=True)
    search_vector = SearchVectorField(null=True)
    
    class Meta:
        indexes = [
            GinIndex(fields=['search_vector']),
            models.Index(fields=['resource_type', 'source']),
        ]

    def __str__(self):
        return f"{self.source} - {self.title[:50]}"