from rest_framework import serializers
from .models import Category, Report


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "description"]


class ReportSerializer(serializers.ModelSerializer):
    reporter = serializers.ReadOnlyField(source="reporter.username")

    class Meta:
        model = Report
        fields = [
            "id",
            "title",
            "description",
            "latitude",
            "longitude",
            "status",
            "votes",
            "reporter",
            "category",
            "created_at",
            "updated_at",
        ]
