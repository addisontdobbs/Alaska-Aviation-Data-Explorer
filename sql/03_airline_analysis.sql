-- 03_airline_analysis.sql
-- Airline-level statistics

-- Overall airline statistics
SELECT
    marketing_carrier,

    COUNT(*) AS total_flights,

    COUNT(*) FILTER (
        WHERE is_cancelled = FALSE
    ) AS completed_flights,

    COUNT(*) FILTER (
        WHERE is_cancelled = TRUE
    ) AS cancelled_flights,

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
    ) AS avg_arrival_delay,

    ROUND(
        100.0 *
        COUNT(*) FILTER (
            WHERE is_cancelled = FALSE
        )
        / COUNT(*),
        2
    ) AS completion_rate,

    ROUND(
        100.0 *
        COUNT(*) FILTER (
            WHERE is_cancelled = TRUE
        )
        / COUNT(*),
        2
    ) AS cancellation_rate

FROM flights
GROUP BY marketing_carrier
ORDER BY total_flights DESC;


-- Monthly flight counts by airline
SELECT
    marketing_carrier,
    EXTRACT(MONTH FROM flight_date) AS month,
    COUNT(*) AS total_flights

FROM flights
GROUP BY marketing_carrier, month
ORDER BY marketing_carrier, month;


-- Average delay by airline and month
SELECT
    marketing_carrier,
    EXTRACT(MONTH FROM flight_date) AS month,

    ROUND(
        AVG(arrival_delay) FILTER (
            WHERE is_cancelled = FALSE
        ),
        2
    ) AS avg_arrival_delay

FROM flights
GROUP BY marketing_carrier, month
ORDER BY marketing_carrier, month;


-- Cancellation totals by airline
SELECT
    marketing_carrier,
    COUNT(*) AS cancelled_flights
FROM flights
WHERE is_cancelled = TRUE
GROUP BY marketing_carrier
ORDER BY cancelled_flights DESC;