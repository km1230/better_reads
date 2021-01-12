"""Views for the better_reads app."""
from django.db.models import Q
from rest_framework import generics, permissions
from rest_framework_json_api import views

from .models import Book, Category, Note, Shelf, Shelfbook
from .serializers import (
    BookSerializer,
    CategorySerializer,
    NoteSerializer,
    ShelfbookSerializer,
    ShelfSerializer,
)


class IsObjectOwner(permissions.BasePermission):
    """Custom permission to detect object owner."""

    def has_object_permission(self, request, view, obj):
        """Detect object owner."""
        return request.user == obj.user


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
    permission_classes = [permissions.IsAuthenticated, IsObjectOwner]

    def get_queryset(self):
        """Public or self owned shelves."""
        return super().get_queryset().filter(Q(public=True) | Q(user=self.request.user))


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


class NoteView(views.ModelViewSet):
    """Note viewset."""

    queryset = Note.objects.all()
    serializer_class = NoteSerializer

    def get_permissions(self):
        """Define permission upon actions."""
        if self.action == "list" or self.action == "retrieve":
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [IsObjectOwner]
        return [permission() for permission in permission_classes]
