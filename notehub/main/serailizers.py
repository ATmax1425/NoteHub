from rest_framework import serializers
from .models import Document, Tag

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']

class DocumentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Document
        fields = [
            'id', 'title', 'description', 'author', 'file_url',
            'file_size', 'file_type', 'tags', 'created_at', 'updated_at'
        ]
