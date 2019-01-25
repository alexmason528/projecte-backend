from slugify import slugify

from django.shortcuts import get_object_or_404

from rest_framework import serializers

from authentication.models import User
from authentication.serializers import UserSerializer

from .models import Item, Category, Image, Estimation, Comment, WatchItem


class RecursiveField(serializers.Serializer):
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'path', 'parent', 'slug', 'translation')


class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')


class ImageUploadSerializer(serializers.Serializer):
    images = serializers.ListField(child=serializers.ImageField())

    def create(self, validated_data):
        return [
            Image.objects.create(obj=image) for image in validated_data.get('images')
        ]

    def to_representation(self, objects):
        return {
            'images': ImageSerializer(objects, many=True).data
        }


class ImageSerializer(serializers.ModelSerializer):
    description = serializers.CharField(required=False)

    class Meta:
        model = Image
        fields = '__all__'


class ItemUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'username')


class ItemEstimationSerializer(serializers.ModelSerializer):
    comment = serializers.CharField(required=False)

    class Meta:
        model = Estimation
        fields = ('id', 'value', 'item', 'user', 'comment')
        extra_kwargs = {
            'comment': {'write_only': True},
            'user': {'read_only': True}
        }

    def validate(self, data):
        super(ItemEstimationSerializer, self).validate(data)

        user = self.context['request'].user
        item = data.get('item')

        if item.user == user:
            raise serializers.ValidationError('Can not give estimation to own item.')

        if Estimation.objects.filter(user=user, item=data.get('item')).exists():
            raise serializers.ValidationError('User already gave estimation to this item.')

        return data

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user

        if 'comment' in validated_data:
            comment_content = validated_data.pop('comment')
            comment = Comment.objects.create(item=validated_data.get(
                'item'), user=user, content=comment_content)
            validated_data['comment'] = comment

        estimation = Estimation.objects.create(**validated_data)
        return estimation

    def to_representation(self, instance):
        res = super(ItemEstimationSerializer, self).to_representation(instance)
        if instance.comment:
            res['comment'] = CommentSerializer(instance.comment).data
        return res


class ItemReplySerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'item', 'content', 'parent')

    def validate(self, data):
        super(ItemReplySerializer, self).validate(data)

        parent = data.get('parent')

        if parent and parent.parent:
            raise serializers.ValidationError('Two levels of nested comments are not allowed.')

        return data

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user

        return super(ItemReplySerializer, self).create(validated_data)

    def to_representation(self, instance):
        return CommentSerializer(instance).data


class EstimationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estimation
        fields = ('id', 'item', 'value', 'user')
        read_only_fields = ('user', )


class CommentSerializer(serializers.ModelSerializer):
    estimation = EstimationSerializer()
    user = UserSerializer()
    children = RecursiveField(many=True)

    class Meta:
        model = Comment
        fields = ('id', 'item', 'user', 'content', 'children', 'parent', 'estimation')


class ItemImageSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    description = serializers.CharField(required=False, allow_null=True, allow_blank=True)


class ItemDetailSerializer(serializers.ModelSerializer):
    estimations = EstimationSerializer(many=True)
    user = UserSerializer()
    category = CategorySerializer()
    comments = CommentSerializer(many=True)

    class Meta:
        model = Item
        fields = ('id', 'name', 'facts', 'details', 'category', 'user', 'date', 'comments', 'estimations', 'slug')
        read_only_fields = ('slug',)

    def to_representation(self, instance):
        user = self.context['request'].user

        res = super(ItemDetailSerializer, self).to_representation(instance)
        res['in_watchlist'] = False if user.is_anonymous else user.watchlist.filter(item=instance).exists()
        res['images'] = ImageSerializer(instance.images, many=True).data

        return res


class ItemDetailUpdateSerializer(serializers.ModelSerializer):
    images = ItemImageSerializer(many=True)

    class Meta:
        model = Item
        fields = ('name', 'facts', 'details', 'category', 'images', 'slug')
        read_only_fields = ('slug',)

    def update(self, instance, validated_data):
        image_data = validated_data.pop('images', None)
        instance = super(ItemDetailUpdateSerializer, self).update(instance, validated_data)
        instance.slug = slugify('{}-{}'.format(instance.name, instance.id))
        instance.save()

        if not image_data:
            return instance

        images = []

        for image in image_data:
            obj = Image.objects.get(pk=image.get('id'))
            obj.description = image.get('description')
            obj.save()
            images.append(obj)

        instance.images.set(images)
        instance.save()

        return instance


class ItemListCreateSerializer(serializers.ModelSerializer):
    images = serializers.ListField(child=ItemImageSerializer())

    class Meta:
        model = Item
        fields = ('id', 'facts', 'name', 'category', 'details', 'images', 'slug')
        read_only_fields = ('slug',)

    def create(self, validated_data):
        images = []
        for image in validated_data.pop('images'):
            obj = get_object_or_404(Image, pk=image.get('id'))
            obj.description = image.get('description')
            obj.save()
            images.append(obj)

        validated_data['user'] = self.context['request'].user
        item = Item.objects.create(**validated_data)

        item.slug = slugify('{}-{}'.format(item.name, item.id))
        item.save()

        item.images.set(images)

        return item

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'name': instance.name,
            'slug': instance.slug,
            'images': ImageSerializer(instance.images, many=True).data,
            'estimations': EstimationSerializer(instance.estimations, many=True).data,
            'category': CategorySerializer(instance.category).data,
            'comments_count': instance.comments.count(),
        }


class WatchItemCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = WatchItem
        fields = ('id', 'item', 'user')
        read_only_fields = ('user',)

    def validate(self, data):
        item = data.get('item')
        user = self.context['request'].user

        if WatchItem.objects.filter(item=item, user=user).exists():
            raise serializers.ValidationError('This item is already in watchlist.')

        return data

    def create(self, validated_data):
        request = self.context['request']
        validated_data['user'] = request.user

        return super(WatchItemCreateSerializer, self).create(validated_data)


class WatchItemListSerializer(serializers.ModelSerializer):
    item = ItemListCreateSerializer()

    class Meta:
        model = WatchItem
        fields = ('id', 'item', 'user')

    def to_representation(self, instance):
        res = super(WatchItemListSerializer, self).to_representation(instance)
        return res.get('item')
