
from django.db import models
from django.conf import settings
from courts.models import Court


class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile"
    )
    phone = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.user.username


class Review(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reviews"
    )
    court = models.ForeignKey(
        Court,
        on_delete=models.CASCADE,
        related_name="reviews"
    )
    rating = models.PositiveSmallIntegerField()
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.court.name}"


class Favorite(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="favorites"
    )
    court = models.ForeignKey(
        Court,
        on_delete=models.CASCADE,
        related_name="favorites"
    )

    class Meta:
        unique_together = ("user", "court")

    def __str__(self):
        return f"{self.user.username} - {self.court.name}"
