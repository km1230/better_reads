"""Serializers for better_reads app."""
from rest_framework_json_api import serializers

from users.serializers import UserSerializer

from .models import Book, Category, Review, Shelf, Shelfbook


class CategorySerializer(serializers.ModelSerializer):
    """Category serializer."""

    class Meta:
        """Meta of category serializer."""

        model = Category
        fields = ["id", "name"]


class BookSerializer(serializers.ModelSerializer):
    """Book serializer."""

    class Meta:
        """Meta of book serializer."""

        model = Book
        fields = ["id", "title", "author", "description", "category", "cover"]

    included_serializers = {"category": CategorySerializer}


class ShelfSerializer(serializers.ModelSerializer):
    """Shelf serializer."""

    class Meta:
        """Meta of shelf serializer."""

        model = Shelf
        read_only_fields = ["user", "books"]
        fields = ["id", "name", "public"] + read_only_fields

    def create(self, validated_data):
        """Add request.user upon shelf creation."""
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)

    included_serializers = {"books": BookSerializer, "user": UserSerializer}


class ShelfbookSerializer(serializers.ModelSerializer):
    """Shelf-book through table serializer."""

    class Meta:
        """Meta of shelfbook serializer."""

        model = Shelfbook
        fields = ["id", "shelf", "book", "status"]

    included_serializers = {"shelf": ShelfSerializer, "books": BookSerializer}

    def validate_shelf(self, shelf):
        """Validate the requesting user is the owner of the shelf."""
        if self.context["request"].user != shelf.user:
            raise serializers.ValidationError(
                "You have no permission to modify this shelf."
            )
        return shelf


class ReviewSerializer(serializers.ModelSerializer):
    """Notes serializer."""

    class Meta:
        """Meta of note serializer."""

        model = Review
        read_only_fields = ["user"]
        fields = ["id", "rate", "content", "created_at", "book"] + read_only_fields

    included_serializers = {"book": BookSerializer, "user": UserSerializer}

    def validate_book(self, book):
        """Do not allow to update book."""
        if self.instance is not None and self.instance.book != book:
            raise serializers.ValidationError("You cannot update this field.")
        return book

    def create(self, validated_data):
        """Add request.user upon note creation."""
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)
