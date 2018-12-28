from django.db import models
from django.contrib.postgres.fields import JSONField

# Create your models here.

from authentication.models import User


class Category(models.Model):
    name = models.CharField(max_length=256)
    slug = models.CharField(max_length=256)
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
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='items')
    date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date']


class Image(models.Model):
    obj = models.ImageField(upload_to="items/images")
    description = models.TextField()
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='images')


class Comment(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    parent = models.ForeignKey(
        'self',
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='children',
    )


class Estimation(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='estimations')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='estimations')
    value = models.FloatField(null=True, blank=True)
    comment = models.OneToOneField(Comment, null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        unique_together = ('item', 'user')


class WatchItem(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='watchlist')
    date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date']
        unique_together = ('item', 'user')
