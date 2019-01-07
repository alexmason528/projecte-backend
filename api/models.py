from django.db import models
from django.db.models import Avg
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

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name


class Item(models.Model):
    name = models.CharField(max_length=256)
    facts = JSONField()
    details = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='items')
    date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return self.name

    @property
    def average_estimation(self):
        return self.estimations.all().aggregate(average_estimation=Avg('value')).get('average_estimation')

    @property
    def estimation_count(self):
        return len(self.estimations.all())


class Image(models.Model):
    obj = models.ImageField(upload_to="items/images")
    description = models.TextField(blank=True, null=True)
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

    def __str__(self):
        return '{} - {}'.format(self.item, self.user)


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
