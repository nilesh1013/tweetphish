from django.db import models

# Create your models here.
class TweetUrls(models.Model):
    url = models.URLField(max_length=2000, blank=True, null=True, unique=True)
    phish_url = models.BooleanField(default=False)
    users = models.TextField(blank=True, null=True)
    tags = models.TextField(blank=True, null=True)
    which_phish = models.CharField(blank=True, null=True, max_length=100)
    full_url = models.URLField(max_length=2000, blank=True, null=True)
    query_keyword = models.CharField(max_length=100, blank=True, null=True)
    user_keyword = models.CharField(max_length=100, blank=True, null=True)