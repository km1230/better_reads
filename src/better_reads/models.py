"""Better reads models."""
from datetime import datetime

from django.db import models

from better_reads import objects
from users.models import User


class Category(models.Model):
    """Book category model."""

    name = models.CharField(max_length=20)

    def __str__(self):
        """Show shelf name."""
        return self.name

    class JSONAPIMeta:
        """JSON:API meta information."""

        resource_name = "categories"


class Book(models.Model):
    """Book model for all books. Only admin can create/modify/delete."""

    title = models.CharField(max_length=50)
    author = models.CharField(max_length=20)
    category = models.ForeignKey(
        to=Category, on_delete=models.CASCADE, related_name="books"
    )
    description = models.CharField(max_length=200, blank=True)
    cover = models.ImageField(blank=True)

    def __str__(self):
        """Show book title."""
        return self.title

    class JSONAPIMeta:
        """JSON:API meta information."""

        resource_name = "books"


class Shelf(models.Model):
    """Shelf model owned by each user."""

    name = models.CharField(max_length=20)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="shelves")
    books = models.ManyToManyField(
        to=Book, blank=True, related_name="shelves", through="Shelfbook"
    )
    public = models.BooleanField(default=True)

    def is_owner(self, user):
        """Return whether the user is the owner."""
        return self.user == user

    class JSONAPIMeta:
        """JSON:API meta information."""

        resource_name = "shelves"


class Shelfbook(models.Model):
    """Book on the shelf."""

    shelf = models.ForeignKey(
        to=Shelf, on_delete=models.CASCADE, related_name="shelfbooks"
    )
    book = models.ForeignKey(
        to=Book, on_delete=models.CASCADE, related_name="shelfbooks"
    )
    status = models.CharField(
        max_length=10,
        choices=objects.ReadStatus.choices(),
        default=objects.ReadStatus.wish.value,
    )

    def is_owner(self, user):
        """Return whether the user is the owner."""
        return self.shelf.is_owner(user)

    class JSONAPIMeta:
        """JSON:API meta information."""

        resource_name = "shelfbooks"


class Review(models.Model):
    """Note created by a user for a book."""

    ratings = [(str(x), str(x)) for x in range(1, 6)]
    rate = models.CharField(max_length=1, choices=ratings, blank=True)
    content = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="notes")
    book = models.ForeignKey(to=Book, on_delete=models.CASCADE, related_name="notes")

    def is_owner(self, user):
        """Return whether the user is the owner."""
        return self.user == user

    class JSONAPIMeta:
        """JSON:API meta information."""

        resource_name = "reviews"
