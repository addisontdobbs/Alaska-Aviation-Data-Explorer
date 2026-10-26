from django.db import models
from django.contrib.auth.models import User


class FlightRecord(models.Model):
    marketing_carrier = models.CharField(max_length=5)
    marketing_flight_number = models.IntegerField(null=True, blank=True)

    operating_carrier = models.CharField(max_length=5, blank=True)
    operating_flight_number = models.IntegerField(null=True, blank=True)

    origin = models.CharField(max_length=5)
    destination = models.CharField(max_length=5)

    flight_date = models.DateField()
    day_of_week = models.IntegerField(null=True, blank=True)

    scheduled_departure = models.IntegerField(null=True, blank=True)
    actual_departure = models.IntegerField(null=True, blank=True)

    scheduled_arrival = models.IntegerField(null=True, blank=True)
    actual_arrival = models.IntegerField(null=True, blank=True)

    scheduled_elapsed_time = models.IntegerField(null=True, blank=True)
    actual_elapsed_time = models.IntegerField(null=True, blank=True)

    departure_delay = models.IntegerField(null=True, blank=True)
    arrival_delay = models.IntegerField(null=True, blank=True)

    wheels_off = models.IntegerField(null=True, blank=True)
    wheels_on = models.IntegerField(null=True, blank=True)

    tail_number = models.CharField(max_length=20, blank=True)

    taxi_out = models.IntegerField(null=True, blank=True)
    taxi_in = models.IntegerField(null=True, blank=True)
    air_time = models.IntegerField(null=True, blank=True)

    cancellation_code = models.CharField(
        max_length=5,
        blank=True
    )

    carrier_delay = models.IntegerField(null=True, blank=True)
    weather_delay = models.IntegerField(null=True, blank=True)
    nas_delay = models.IntegerField(null=True, blank=True)
    security_delay = models.IntegerField(null=True, blank=True)
    late_aircraft_delay = models.IntegerField(null=True, blank=True)

    is_cancelled = models.BooleanField(default=False)

    def __str__(self):
        return (
            f"{self.flight_date} - "
            f"{self.marketing_carrier} "
            f"{self.origin} to {self.destination}"
        )


class SavedRoute(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="saved_routes"
    )

    origin = models.CharField(max_length=5)
    destination = models.CharField(max_length=5)

    name = models.CharField(
        max_length=100,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.origin} to {self.destination}"


class FlightNote(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="flight_notes"
    )

    flight = models.ForeignKey(
        FlightRecord,
        on_delete=models.CASCADE,
        related_name="notes"
    )

    title = models.CharField(max_length=150)
    content = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title