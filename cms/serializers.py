from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Category, Article

User = get_user_model()


class UserSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name']


class CategorySerializer(serializers.ModelSerializer):
    article_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'created_at', 'article_count']
        read_only_fields = ['id', 'created_at', 'article_count']


class ArticleListSerializer(serializers.ModelSerializer):
    author = UserSummarySerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    excerpt = serializers.CharField(read_only=True)

    class Meta:
        model = Article
        fields = [
            'id',
            'title',
            'slug',
            'author',
            'category',
            'excerpt',
            'status',
            'reading_time',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'slug', 'author', 'reading_time', 'created_at', 'updated_at']


class ArticleDetailSerializer(serializers.ModelSerializer):
    author = UserSummarySerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    rendered_content = serializers.CharField(read_only=True)
    excerpt = serializers.CharField(read_only=True)

    class Meta:
        model = Article
        fields = [
            'id',
            'title',
            'slug',
            'author',
            'category',
            'content',
            'rendered_content',
            'excerpt',
            'status',
            'reading_time',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'slug', 'author', 'reading_time', 'created_at', 'updated_at']


class ArticleWriteSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Article
        fields = [
            'id',
            'title',
            'slug',
            'author',
            'category',
            'content',
            'status',
            'reading_time',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'slug', 'author', 'created_at', 'updated_at']
