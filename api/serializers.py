from rest_framework import serializers

from authentication.models import User

from .models import Item, Category, Image


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
        fields = ('id', 'email', 'fullname')


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
        return {
            'id': obj.id,
            'facts': obj.facts,
            'name': obj.name,
            'category': SubCategorySerializer(obj.category).data,
            'user': ItemUserSerializer(obj.user).data,
            'details': obj.details,
        }
