-- 02_route_analysis.sql
-- Route-level analysis

-- Top 10 routes by total number of flights
SELECT
    origin,
    destination,
    COUNT(*) AS total_flights
FROM flights
GROUP BY origin, destination
ORDER BY total_flights DESC
LIMIT 10;


-- Route statistics for every route
SELECT
    origin,
    destination,

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
    ) AS avg_arrival_delay,

    ROUND(
        AVG(departure_delay) FILTER (
            WHERE is_cancelled = FALSE
        ),
        2
    ) AS avg_departure_delay,

    ROUND(
        100.0 *
        COUNT(*) FILTER (
            WHERE is_cancelled = TRUE
        )
        / COUNT(*),
        2
    ) AS cancellation_rate

FROM flights
GROUP BY origin, destination
ORDER BY total_flights DESC;


-- Example route analysis: ANC -> SEA
SELECT
    origin,
    destination,

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
    ) AS avg_arrival_delay,

    ROUND(
        AVG(departure_delay) FILTER (
            WHERE is_cancelled = FALSE
        ),
        2
    ) AS avg_departure_delay,

    ROUND(
        AVG(air_time) FILTER (
            WHERE is_cancelled = FALSE
        ),
        2
    ) AS avg_air_time

FROM flights
WHERE origin = 'ANC'
AND destination = 'SEA'
GROUP BY origin, destination;


-- Monthly statistics for ANC -> SEA
SELECT
    EXTRACT(MONTH FROM flight_date) AS month,

    COUNT(*) AS total_flights,

    ROUND(
        AVG(arrival_delay) FILTER (
            WHERE is_cancelled = FALSE
        ),
        2
    ) AS avg_arrival_delay,

    COUNT(*) FILTER (
        WHERE is_cancelled = TRUE
    ) AS cancelled_flights

FROM flights
WHERE origin = 'ANC'
AND destination = 'SEA'
GROUP BY month
ORDER BY month;