from rest_framework import serializers

from authentication.models import User
from authentication.serializers import UserSerializer

from .models import Item, Category, Image, Estimation, Comment


class RecursiveField(serializers.Serializer):
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class CategorySerializer(serializers.ModelSerializer):
    children = RecursiveField(many=True)

    class Meta:
        model = Category
        fields = ('id', 'name', 'path', 'children')


class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')


class ImageSerializer(serializers.ModelSerializer):
    obj = serializers.ImageField()
    description = serializers.CharField()

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


class EstimationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estimation
        fields = ('id', 'item', 'value', 'user')
        extra_kwargs = {
            'user': {'read_only': True},
        }


class CommentSerializer(serializers.ModelSerializer):
    estimation = EstimationSerializer()
    user = UserSerializer()
    children = RecursiveField(many=True)

    class Meta:
        model = Comment
        fields = ('id', 'item', 'user', 'content', 'children', 'estimation')


class ItemSerializer(serializers.ModelSerializer):
    images = serializers.ListField(child=serializers.ImageField())
    descriptions = serializers.ListField(child=serializers.CharField())

    class Meta:
        model = Item
        fields = ('id', 'facts', 'name', 'category', 'details', 'images', 'descriptions')

    def validate(self, data):
        super(ItemSerializer, self).validate(data)

        images = data.get('images')
        descriptions = data.get('descriptions')

        if len(images) != len(descriptions):
            raise serializers.ValidationError('All images require descriptions.')

        return data

    def create(self, validated_data):
        images = validated_data.pop('images')
        descriptions = validated_data.pop('descriptions')
        validated_data['user'] = self.context['request'].user
        item = Item.objects.create(**validated_data)

        for ind, image in enumerate(images):
            Image.objects.create(obj=image, description=descriptions[ind], item=item)

        return item

    def to_representation(self, obj):
        user = self.context['request'].user

        return {
            'id': obj.id,
            'facts': obj.facts,
            'name': obj.name,
            'details': obj.details,
            'date': obj.date,
            'images': ImageSerializer(obj.image_set, many=True).data,
            'category': SubCategorySerializer(obj.category).data,
            'user': ItemUserSerializer(obj.user).data,
            'estimations': EstimationSerializer(obj.estimations, many=True).data,
            'comments': CommentSerializer(obj.comments, many=True).data,
            'in_watchlist': user.watchlist.filter(item=obj).exists(),
        }
