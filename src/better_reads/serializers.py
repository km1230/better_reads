"""Serializers for better_reads app."""
from rest_framework_json_api import serializers

from .models import Book, Category, Note, Shelf, Shelfbook


class BookSerializer(serializers.ModelSerializer):
    """Book serializer."""

    class Meta:
        """Meta of book serializer."""

        model = Book
        fields = ["id", "title", "author", "category", "cover"]


class CategorySerializer(serializers.ModelSerializer):
    """Category serializer."""

    class Meta:
        """Meta of category serializer."""

        model = Category
        fields = ["id", "name"]


class ShelfSerializer(serializers.ModelSerializer):
    """Shelf serializer."""

    class Meta:
        """Meta of shelf serializer."""

        model = Shelf
        read_only_fields = ["user"]
        fields = ["id", "name", "books", "public"] + read_only_fields

    def create(self, validated_data):
        """Add request.user upon shelf creation."""
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)


class ShelfbookSerializer(serializers.ModelSerializer):
    """Shelf-book through table serializer."""

    class Meta:
        """Meta of shelfbook serializer."""

        model = Shelfbook
        fields = ["id", "shelf", "book", "status"]


class NoteSerializer(serializers.ModelSerializer):
    """Notes serializer."""

    class Meta:
        """Meta of note serializer."""

        model = Note
        read_only_fields = ["user"]
        fields = ["id", "rate", "content", "created_at", "book"] + read_only_fields

    def validate_book(self, book):
        """Do not allow to update book."""
        if self.instance is not None and self.instance.book != book:
            raise serializers.ValidationError("You cannot update this field.")
        return book

    def create(self, validated_data):
        """Add request.user upon note creation."""
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)
