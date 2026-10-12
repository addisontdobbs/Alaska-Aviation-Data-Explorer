-- 01_basic_analysis.sql
-- General statistics for the Alaska Aviation Data Explorer

-- Total Alaska-related flights
SELECT
    COUNT(*) AS total_flights
FROM flights;


-- Completed vs cancelled flights
SELECT
    is_cancelled,
    COUNT(*) AS total_flights
FROM flights
GROUP BY is_cancelled
ORDER BY is_cancelled;


-- Dataset date range
SELECT
    MIN(flight_date) AS first_date,
    MAX(flight_date) AS last_date
FROM flights;


-- Number of airlines
SELECT
    COUNT(DISTINCT marketing_carrier) AS total_airlines
FROM flights;


-- Number of unique airports appearing in the dataset
SELECT
    COUNT(DISTINCT airport_code) AS total_airports
FROM (
    SELECT origin AS airport_code
    FROM flights

    UNION

    SELECT destination AS airport_code
    FROM flights
) airports;


-- Average departure and arrival delay
-- Cancelled flights are excluded because they use placeholder values
SELECT
    ROUND(
        AVG(departure_delay) FILTER (
            WHERE is_cancelled = FALSE
        ),
        2
    ) AS avg_departure_delay,

    ROUND(
        AVG(arrival_delay) FILTER (
            WHERE is_cancelled = FALSE
        ),
        2
    ) AS avg_arrival_delay
FROM flights;


-- Cancellation rate
SELECT
    COUNT(*) AS total_flights,

    COUNT(*) FILTER (
        WHERE is_cancelled = TRUE
    ) AS cancelled_flights,

    ROUND(
        100.0 *
        COUNT(*) FILTER (
            WHERE is_cancelled = TRUE
        )
        / COUNT(*),
        2
    ) AS cancellation_rate
FROM flights;