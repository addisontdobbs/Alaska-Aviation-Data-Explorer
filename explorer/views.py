import csv

from django.conf import settings
from django.core.paginator import Paginator
from django.db.models import Avg, Count, Q
from django.db.models.functions import ExtractMonth
from django.shortcuts import render

from .models import FlightRecord


AIRLINE_NAMES = {
    "AS": "Alaska Airlines",
    "DL": "Delta",
    "UA": "United",
    "AA": "American",
    "HA": "Hawaiian",
}

MONTH_NAMES = [
    "",
    "Jan",
    "Feb",
    "Mar",
    "Apr",
    "May",
    "Jun",
    "Jul",
    "Aug",
    "Sep",
    "Oct",
    "Nov",
    "Dec",
]


def get_flight_stats():
    completed = FlightRecord.objects.filter(is_cancelled=False)

    return {
        "total_flights": FlightRecord.objects.count(),
        "completed_flights": completed.count(),
        "cancelled_flights": FlightRecord.objects.filter(
            is_cancelled=True
        ).count(),
        "avg_arrival_delay": completed.aggregate(
            avg=Avg("arrival_delay")
        )["avg"],
    }


def dashboard(request):
    stats = get_flight_stats()

    monthly_flights = (
        FlightRecord.objects
        .annotate(month=ExtractMonth("flight_date"))
        .values("month")
        .annotate(total=Count("id"))
        .order_by("month")
    )

    month_labels = [
        MONTH_NAMES[row["month"]]
        for row in monthly_flights
    ]

    month_counts = [
        row["total"]
        for row in monthly_flights
    ]

    top_airlines = (
        FlightRecord.objects
        .values("marketing_carrier")
        .annotate(total=Count("id"))
        .order_by("-total")[:5]
    )

    airline_labels = [
        AIRLINE_NAMES.get(
            row["marketing_carrier"],
            row["marketing_carrier"]
        )
        for row in top_airlines
    ]

    airline_counts = [
        row["total"]
        for row in top_airlines
    ]

    top_routes = (
        FlightRecord.objects
        .values("origin", "destination")
        .annotate(total=Count("id"))
        .order_by("-total")[:5]
    )

    airport_codes = set(
        FlightRecord.objects
        .values_list("origin", flat=True)
        .distinct()
    ) | set(
        FlightRecord.objects
        .values_list("destination", flat=True)
        .distinct()
    )

    airport_data = []
    airport_csv = settings.BASE_DIR / "data" / "alaska_airports.csv"

    if airport_csv.exists():
        with open(
            airport_csv,
            newline="",
            encoding="utf-8"
        ) as csvfile:

            for row in csv.DictReader(csvfile):
                code = row.get("code")

                if code not in airport_codes:
                    continue

                try:
                    latitude = float(row["latitude"])
                    longitude = float(row["longitude"])
                except (ValueError, TypeError, KeyError):
                    continue

                airport_data.append({
                    "code": code,
                    "name": row.get("airport_name", ""),
                    "city": row.get("city", ""),
                    "latitude": latitude,
                    "longitude": longitude,
                })

    return render(
        request,
        "explorer/dashboard.html",
        {
            **stats,
            "month_labels": month_labels,
            "month_counts": month_counts,
            "airline_labels": airline_labels,
            "airline_counts": airline_counts,
            "top_routes": top_routes,
            "airport_data": airport_data,
        }
    )


def flights(request):
    queryset = FlightRecord.objects.all()

    search = request.GET.get("search", "").strip()
    airline = request.GET.get("airline", "").strip()
    origin = request.GET.get("origin", "").strip()
    destination = request.GET.get("destination", "").strip()
    status = request.GET.get("status", "").strip()

    try:
        rows_per_page = int(request.GET.get("rows", 10))
    except ValueError:
        rows_per_page = 10

    if rows_per_page not in (10, 25, 50):
        rows_per_page = 10

    if search:
        queryset = queryset.filter(
            Q(marketing_carrier__icontains=search)
            | Q(operating_carrier__icontains=search)
            | Q(origin__icontains=search)
            | Q(destination__icontains=search)
            | Q(tail_number__icontains=search)
        )

    if airline:
        queryset = queryset.filter(
            marketing_carrier=airline
        )

    if origin:
        queryset = queryset.filter(
            origin=origin
        )

    if destination:
        queryset = queryset.filter(
            destination=destination
        )

    if status == "completed":
        queryset = queryset.filter(
            is_cancelled=False
        )

    elif status == "cancelled":
        queryset = queryset.filter(
            is_cancelled=True
        )

    queryset = queryset.order_by(
        "-flight_date",
        "marketing_carrier",
        "marketing_flight_number"
    )

    paginator = Paginator(
        queryset,
        rows_per_page
    )

    page_obj = paginator.get_page(
        request.GET.get("page")
    )

    airlines = (
        FlightRecord.objects
        .values_list("marketing_carrier", flat=True)
        .distinct()
        .order_by("marketing_carrier")
    )

    origins = (
        FlightRecord.objects
        .values_list("origin", flat=True)
        .distinct()
        .order_by("origin")
    )

    destinations = (
        FlightRecord.objects
        .values_list("destination", flat=True)
        .distinct()
        .order_by("destination")
    )

    return render(
        request,
        "explorer/flights.html",
        {
            **get_flight_stats(),

            "page_obj": page_obj,
            "result_count": paginator.count,
            "rows_per_page": rows_per_page,

            "airlines": airlines,
            "origins": origins,
            "destinations": destinations,

            "search": search,
            "selected_airline": airline,
            "selected_origin": origin,
            "selected_destination": destination,
            "selected_status": status,
        }
    )