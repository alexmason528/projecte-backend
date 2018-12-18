from django.db import models
from django.contrib.postgres.fields import JSONField

# Create your models here.

from authentication.models import User


class Category(models.Model):
    name = models.CharField(max_length=256)
    path = models.CharField(max_length=256)
    parent = models.ForeignKey(
        'self',
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='children',
    )


class Item(models.Model):
    name = models.CharField(max_length=256)
    facts = JSONField()
    details = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Image(models.Model):
    obj = models.ImageField(upload_to="items/images")
    description = models.TextField()
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
