-- 04_dashboard_stats.sql
-- Queries intended for dashboard cards and charts

-- Main dashboard KPI values
SELECT
    COUNT(*) AS total_flights,

    COUNT(*) FILTER (
        WHERE is_cancelled = FALSE
    ) AS completed_flights,

    COUNT(*) FILTER (
        WHERE is_cancelled = TRUE
    ) AS cancelled_flights,

    ROUND(
        AVG(arrival_delay) FILTER (
            WHERE is_cancelled = FALSE
        ),
        2
    ) AS avg_arrival_delay

FROM flights;


-- Flights by month
SELECT
    EXTRACT(MONTH FROM flight_date) AS month,
    COUNT(*) AS total_flights
FROM flights
GROUP BY month
ORDER BY month;


-- Monthly completed and cancelled flights
SELECT
    EXTRACT(MONTH FROM flight_date) AS month,

    COUNT(*) FILTER (
        WHERE is_cancelled = FALSE
    ) AS completed_flights,

    COUNT(*) FILTER (
        WHERE is_cancelled = TRUE
    ) AS cancelled_flights

FROM flights
GROUP BY month
ORDER BY month;


-- Average arrival delay by month
SELECT
    EXTRACT(MONTH FROM flight_date) AS month,

    ROUND(
        AVG(arrival_delay) FILTER (
            WHERE is_cancelled = FALSE
        ),
        2
    ) AS avg_arrival_delay

FROM flights
GROUP BY month
ORDER BY month;


-- Cancellation causes
SELECT
    cancellation_code,
    COUNT(*) AS total_cancellations
FROM flights
WHERE is_cancelled = TRUE
GROUP BY cancellation_code
ORDER BY total_cancellations DESC;


-- Total delay minutes by delay category
SELECT
    SUM(carrier_delay) AS carrier_delay_minutes,
    SUM(weather_delay) AS weather_delay_minutes,
    SUM(nas_delay) AS nas_delay_minutes,
    SUM(security_delay) AS security_delay_minutes,
    SUM(late_aircraft_delay) AS late_aircraft_delay_minutes
FROM flights
WHERE is_cancelled = FALSE;


-- Top 5 routes for dashboard
SELECT
    origin,
    destination,
    COUNT(*) AS total_flights
FROM flights
GROUP BY origin, destination
ORDER BY total_flights DESC
LIMIT 5;


-- Top airlines for dashboard
SELECT
    marketing_carrier,
    COUNT(*) AS total_flights,

    ROUND(
        AVG(arrival_delay) FILTER (
            WHERE is_cancelled = FALSE
        ),
        2
    ) AS avg_arrival_delay

FROM flights
GROUP BY marketing_carrier
ORDER BY total_flights DESC;


-- Top origin airports
SELECT
    origin,
    COUNT(*) AS total_departures
FROM flights
GROUP BY origin
ORDER BY total_departures DESC
LIMIT 10;