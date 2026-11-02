
from django.db import models


class SportType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Address(models.Model):
    city = models.CharField(max_length=100)
    street = models.CharField(max_length=150)
    building_number = models.CharField(max_length=20)
    postal_code = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f"{self.street} {self.building_number}, {self.city}"


class SportCenter(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    address = models.OneToOneField(
        Address,
        on_delete=models.CASCADE,
        related_name="sport_center"
    )

    def __str__(self):
        return self.name


class Court(models.Model):
    sport_center = models.ForeignKey(
        SportCenter,
        on_delete=models.CASCADE,
        related_name="courts"
    )
    sport_type = models.ForeignKey(
        SportType,
        on_delete=models.PROTECT,
        related_name="courts"
    )
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price_per_hour = models.DecimalField(max_digits=8, decimal_places=2)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} - {self.sport_center.name}"


class OpeningHours(models.Model):
    class Weekday(models.IntegerChoices):
        MONDAY = 0, "Monday"
        TUESDAY = 1, "Tuesday"
        WEDNESDAY = 2, "Wednesday"
        THURSDAY = 3, "Thursday"
        FRIDAY = 4, "Friday"
        SATURDAY = 5, "Saturday"
        SUNDAY = 6, "Sunday"

    sport_center = models.ForeignKey(
        SportCenter,
        on_delete=models.CASCADE,
        related_name="opening_hours"
    )
    weekday = models.IntegerField(choices=Weekday.choices)
    open_time = models.TimeField()
    close_time = models.TimeField()

    def __str__(self):
        return f"{self.sport_center.name} - {self.get_weekday_display()}"
