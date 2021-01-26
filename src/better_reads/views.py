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
    search_fields = ["title", "author", "category__name"]
    filterset_fields = ["category"]


class CategoryView(views.ModelViewSet):
    """Category viewset."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.DjangoModelPermissionsOrAnonReadOnly]
    search_fields = ["name"]
    filterset_fields = ["name"]


class ShelfView(views.ModelViewSet):
    """Shelf viewset."""

    queryset = Shelf.objects.all()
    serializer_class = ShelfSerializer
    search_fields = ["name", "user__id", "books__id"]
    filterset_fields = ["name", "user", "books"]

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
    permissions_classes = [permissions.DjangoModelPermissionsOrAnonReadOnly]
    search_fields = ["shelf__name", "book__title"]
    filterset_fields = ["shelf", "book", "shelf__user"]

    def get_queryset(self):
        """Public or self owned shelves."""
        return (
            super()
            .get_queryset()
            .filter(Q(shelf__public=True) | Q(shelf__user=self.request.user.id))
        )


class ReviewView(views.ModelViewSet):
    """Review viewset."""

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    search_fields = ["book__title", "user__email", "rate"]
    filterset_fields = ["book", "user", "rate"]

    def get_permissions(self):
        """Define permission upon actions."""
        if self.action == "list" or self.action == "retrieve":
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [IsObjectOwner]
        return [permission() for permission in permission_classes]
