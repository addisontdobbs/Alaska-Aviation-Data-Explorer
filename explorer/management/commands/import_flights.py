import csv
from pathlib import Path

from django.core.management.base import BaseCommand
from explorer.models import FlightRecord


class Command(BaseCommand):
    help = "Import Alaska aviation flight records from CSV"

    def handle(self, *args, **options):
        project_root = Path(__file__).resolve().parents[3]
        csv_path = project_root / "data" / "alaska_flights_2025.csv"

        if not csv_path.exists():
            self.stdout.write(
                self.style.ERROR(
                    f"CSV file not found: {csv_path}"
                )
            )
            return

        self.stdout.write("Starting flight import...")

        FlightRecord.objects.all().delete()

        flights = []

        with open(csv_path, newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                flights.append(
                    FlightRecord(
                        marketing_carrier=row["marketing_carrier"],
                        marketing_flight_number=self.to_int(
                            row["marketing_flight_number"]
                        ),
                        operating_carrier=row["operating_carrier"],
                        operating_flight_number=self.to_int(
                            row["operating_flight_number"]
                        ),
                        origin=row["origin"],
                        destination=row["destination"],
                        flight_date=row["flight_date"],
                        day_of_week=self.to_int(row["day_of_week"]),

                        scheduled_departure=self.to_int(
                            row["scheduled_departure"]
                        ),
                        actual_departure=self.to_int(
                            row["actual_departure"]
                        ),
                        scheduled_arrival=self.to_int(
                            row["scheduled_arrival"]
                        ),
                        actual_arrival=self.to_int(
                            row["actual_arrival"]
                        ),

                        scheduled_elapsed_time=self.to_int(
                            row["scheduled_elapsed_time"]
                        ),
                        actual_elapsed_time=self.to_int(
                            row["actual_elapsed_time"]
                        ),

                        departure_delay=self.to_int(
                            row["departure_delay"]
                        ),
                        arrival_delay=self.to_int(
                            row["arrival_delay"]
                        ),

                        wheels_off=self.to_int(row["wheels_off"]),
                        wheels_on=self.to_int(row["wheels_on"]),

                        tail_number=row["tail_number"],

                        taxi_out=self.to_int(row["taxi_out"]),
                        taxi_in=self.to_int(row["taxi_in"]),
                        air_time=self.to_int(row["air_time"]),

                        cancellation_code=row["cancellation_code"],

                        carrier_delay=self.to_int(
                            row["carrier_delay"]
                        ),
                        weather_delay=self.to_int(
                            row["weather_delay"]
                        ),
                        nas_delay=self.to_int(
                            row["nas_delay"]
                        ),
                        security_delay=self.to_int(
                            row["security_delay"]
                        ),
                        late_aircraft_delay=self.to_int(
                            row["late_aircraft_delay"]
                        ),

                        is_cancelled=self.to_bool(
                            row["is_cancelled"]
                        ),
                    )
                )

        FlightRecord.objects.bulk_create(
            flights,
            batch_size=1000
        )

        self.stdout.write(
            self.style.SUCCESS(
                f"Imported {len(flights)} flight records."
            )
        )

    def to_int(self, value):
        if value is None or value == "":
            return None

        try:
            return int(float(value))
        except ValueError:
            return None

    def to_bool(self, value):
        return str(value).lower() in [
            "true",
            "1",
            "yes"
        ]