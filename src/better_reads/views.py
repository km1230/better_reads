"""Views for the better_reads app."""
from django.db.models import Q
from rest_framework import generics, permissions
from rest_framework_json_api import views

from .models import Book, Category, Review, Shelf, Shelfbook
from .serializers import (
    BookSerializer,
    CategorySerializer,
    ReviewSerializer,
    ShelfbookSerializer,
    ShelfSerializer,
)


class IsObjectOwner(permissions.BasePermission):
    """Custom permission to detect object owner."""

    def has_object_permission(self, request, view, obj):
        """Detect object owner."""
        return obj.is_owner(request.user)


class BookView(views.ModelViewSet):
    """Book viewset."""

    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.DjangoModelPermissionsOrAnonReadOnly]
    ordering = ["title"]


class CategoryView(views.ModelViewSet):
    """Category viewset."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.DjangoModelPermissionsOrAnonReadOnly]
    ordering = ["name"]


class ShelfView(views.ModelViewSet):
    """Shelf viewset."""

    queryset = Shelf.objects.all()
    serializer_class = ShelfSerializer

    def get_queryset(self):
        """Public or self owned shelves."""
        return super().get_queryset().filter(Q(public=True) | Q(user=self.request.user))

    def get_permissions(self):
        """Allow authenticated users to list & retrieve (their / public) shelves."""
        permission_classes = [permissions.IsAuthenticated]
        if self.action != "retrieve" and self.action != "list":
            permission_classes.append(IsObjectOwner)
        return [permissions() for permissions in permission_classes]


class ShelfbookView(views.ModelViewSet):
    """Books on shelf."""

    queryset = Shelfbook.objects.all()
    serializer_class = ShelfbookSerializer
    permission_classes = [permissions.IsAuthenticated, IsObjectOwner]

    def get_queryset(self):
        """Public or self owned shelves."""
        return (
            super()
            .get_queryset()
            .filter(Q(shelf__public=True) | Q(shelf__user=self.request.user))
        )


class ReviewView(views.ModelViewSet):
    """Review viewset."""

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get_permissions(self):
        """Define permission upon actions."""
        if self.action == "list" or self.action == "retrieve":
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [IsObjectOwner]
        return [permission() for permission in permission_classes]
