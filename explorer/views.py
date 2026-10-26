from django.shortcuts import render
from django.db.models import Avg, Count
from django.db.models.functions import ExtractMonth

from .models import FlightRecord


def dashboard(request):
    total_flights = FlightRecord.objects.count()

    completed_flights = FlightRecord.objects.filter(
        is_cancelled=False
    ).count()

    cancelled_flights = FlightRecord.objects.filter(
        is_cancelled=True
    ).count()

    avg_arrival_delay = FlightRecord.objects.filter(
        is_cancelled=False
    ).aggregate(
        avg_delay=Avg("arrival_delay")
    )["avg_delay"]

    monthly_flights = (
        FlightRecord.objects
        .annotate(month=ExtractMonth("flight_date"))
        .values("month")
        .annotate(total=Count("id"))
        .order_by("month")
    )

    top_airlines = (
        FlightRecord.objects
        .values("marketing_carrier")
        .annotate(total=Count("id"))
        .order_by("-total")[:5]
    )

    top_routes = (
        FlightRecord.objects
        .values("origin", "destination")
        .annotate(total=Count("id"))
        .order_by("-total")[:5]
    )

    context = {
        "total_flights": total_flights,
        "completed_flights": completed_flights,
        "cancelled_flights": cancelled_flights,
        "avg_arrival_delay": avg_arrival_delay,
        "monthly_flights": monthly_flights,
        "top_airlines": top_airlines,
        "top_routes": top_routes,
    }

    return render(
        request,
        "explorer/dashboard.html",
        context
    )