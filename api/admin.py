from django.contrib import admin
from projecte.admin import admin as projecte_admin

from .models import Category, Item, Image, Comment, Estimation, WatchItem


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    list_display_links = ('id', 'name', 'slug')
    readonly_fields = ('id',)


class ItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'average_estimation', 'estimation_count', 'user', 'category', 'date')
    list_display_links = ('id', 'name')
    readonly_fields = ('id',)


class ImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'item', 'obj')
    list_display_links = ('id', 'item')
    readonly_fields = ('id',)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'item', 'user', 'parent')
    list_display_links = ('id', 'item')
    readonly_fields = ('id',)


class EstimationAdmin(admin.ModelAdmin):
    list_display = ('id', 'item', 'user', 'value')
    list_display_links = ('id', 'item')
    readonly_fields = ('id',)


class WatchItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'item', 'user', 'date')
    list_display_links = ('id', 'item')
    readonly_fields = ('id',)


projecte_admin.register(Category, CategoryAdmin)
projecte_admin.register(Item, ItemAdmin)
projecte_admin.register(Image, ImageAdmin)
projecte_admin.register(Comment, CommentAdmin)
projecte_admin.register(Estimation, EstimationAdmin)
projecte_admin.register(WatchItem, WatchItemAdmin)
