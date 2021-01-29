from rest_framework import serializers
from rest_framework.decorators import permission_classes

from .models import *


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.CharField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), write_only=True)

    class Meta:
        model = Comment
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

    def _get_image_url(self, obj):
        request = self.context.get('request')
        image_objs = obj.images.all()
        imgs = []
        for image_obj in image_objs:
            if image_obj is not None and image_obj.image:
                url = image_obj.image.url
                if request is not None:
                    url = request.build_absolute_uri(url)
                imgs.append(url)
        if imgs == []:
            return None
        else:
            return imgs

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['image'] = self._get_image_url(instance)
        representation['categories'] = CategorySerializer(instance.categories.all(), many=True).data
        representation['comments'] = CommentSerializer(instance.comments.all(), many=True).data
        return representation


class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        exclude = ('description',)

    def _get_image_url(self, obj):
        request = self.context.get('request')
        image_objs = obj.images.all()
        imgs = []
        for image_obj in image_objs:
            if image_obj is not None and image_obj.image:
                url = image_obj.image.url
                if request is not None:
                    url = request.build_absolute_uri(url)
                imgs.append(url)
        if imgs == []:
            return None
        else:
            return imgs

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['image'] = self._get_image_url(instance)
        representation['categories'] = CategorySerializer(instance.categories.all(), many=True).data
        return representation


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class CreateUpdateProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('title', 'description', 'price', 'categories')


