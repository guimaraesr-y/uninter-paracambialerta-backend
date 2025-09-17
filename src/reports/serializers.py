from rest_framework import serializers

from src.location.serializers import LocationSerializer
from .models import Category, Report


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "description"]


class ReportSerializer(serializers.ModelSerializer):
    reporter = serializers.ReadOnlyField(source="reporter.username")
    location = LocationSerializer()
    category = CategorySerializer()
    upvotes_count = serializers.ReadOnlyField()
    downvotes_count = serializers.ReadOnlyField()

    class Meta:
        model = Report
        fields = [
            "id",
            "title",
            "description",
            "status",
            "upvotes_count",
            "downvotes_count",
            "reporter",
            "location",
            "category",
            "created_at",
            "updated_at",
        ]
