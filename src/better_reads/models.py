"""Better reads models."""
from datetime import datetime

from django.db import models

from users.models import User


class Category(models.Model):
    """Book category model."""

    name = models.CharField(max_length=20)

    def __str__(self):
        """Show shelf name."""
        return self.name


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


class Shelf(models.Model):
    """Shelf model owned by each user."""

    name = models.CharField(max_length=20)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="shelves")
    books = models.ManyToManyField(
        to=Book, blank=True, related_name="shelves", through="Shelfbook"
    )
    public = models.BooleanField(default=True)


class Shelfbook(models.Model):
    """extras attributes for books on shelf."""

    shelf = models.ForeignKey(Shelf, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    options = [("WI", "Wish"), ("RI", "Reading"), ("RD", "Read")]
    status = models.CharField(max_length=2, choices=options, default=("WI"))


class Note(models.Model):
    """Note created by a user for a book."""

    ratings = [(str(x), str(x)) for x in range(1, 6)]
    rate = models.CharField(max_length=1, choices=ratings, blank=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="notes")
    book = models.ForeignKey(to=Book, on_delete=models.CASCADE, related_name="notes")
