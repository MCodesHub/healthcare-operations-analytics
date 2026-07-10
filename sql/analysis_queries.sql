-- Inland Empire Emergency Department Operations Analysis
-- These queries use the ed_encounters table imported from the processed CSV.
-- The optional facilities table contains facility_id and facility_name.

USE healthcare_analytics;

-- 1. Preview the data and review the available columns.
SELECT *
FROM ed_encounters
LIMIT 10;

-- 2. Filter for encounters with waits longer than 60 minutes.
SELECT encounter_id, facility_name, arrival_datetime, service_line, wait_minutes
FROM ed_encounters
WHERE wait_minutes > 60
ORDER BY wait_minutes DESC;

-- 3. Calculate the main operational performance indicators.
SELECT
    COUNT(*) AS total_encounters,
    ROUND(AVG(wait_minutes), 1) AS average_wait_minutes,
    MIN(wait_minutes) AS minimum_wait_minutes,
    MAX(wait_minutes) AS maximum_wait_minutes,
    ROUND(AVG(length_of_stay_minutes), 1) AS average_length_of_stay,
    SUM(revisit_72h) AS total_72h_revisits,
    ROUND(100 * AVG(revisit_72h), 1) AS revisit_rate_percent
FROM ed_encounters;

-- 4. Compare encounter volume and wait times across facilities.
SELECT
    facility_name,
    COUNT(*) AS total_encounters,
    ROUND(AVG(wait_minutes), 1) AS average_wait_minutes,
    ROUND(AVG(length_of_stay_minutes), 1) AS average_length_of_stay
FROM ed_encounters
GROUP BY facility_name
ORDER BY average_wait_minutes DESC;

-- 5. Use CASE to group waits into easy-to-understand categories.
SELECT
    CASE
        WHEN wait_minutes <= 30 THEN '30 minutes or less'
        WHEN wait_minutes <= 60 THEN '31 to 60 minutes'
        ELSE 'More than 60 minutes'
    END AS wait_category,
    COUNT(*) AS total_encounters,
    ROUND(100 * COUNT(*) / (SELECT COUNT(*) FROM ed_encounters), 1) AS percent_of_encounters
FROM ed_encounters
GROUP BY wait_category
ORDER BY total_encounters DESC;

-- 6. Compare service lines while excluding very small groups with HAVING.
SELECT
    service_line,
    COUNT(*) AS total_encounters,
    ROUND(AVG(wait_minutes), 1) AS average_wait_minutes,
    ROUND(100 * AVG(revisit_72h), 1) AS revisit_rate_percent
FROM ed_encounters
GROUP BY service_line
HAVING COUNT(*) >= 100
ORDER BY revisit_rate_percent DESC;

-- 7. Join encounters to the facility lookup table.
SELECT
    f.facility_name,
    f.city,
    COUNT(e.encounter_id) AS total_encounters,
    ROUND(AVG(e.wait_minutes), 1) AS average_wait_minutes
FROM ed_encounters AS e
JOIN facilities AS f
    ON e.facility_id = f.facility_id
GROUP BY f.facility_name, f.city
ORDER BY total_encounters DESC;

-- 8. Use a CTE to identify the shifts with above-average wait times.
WITH shift_waits AS (
    SELECT
        shift,
        COUNT(*) AS total_encounters,
        AVG(wait_minutes) AS average_wait_minutes
    FROM ed_encounters
    GROUP BY shift
)
SELECT
    shift,
    total_encounters,
    ROUND(average_wait_minutes, 1) AS average_wait_minutes
FROM shift_waits
WHERE average_wait_minutes > (SELECT AVG(wait_minutes) FROM ed_encounters)
ORDER BY average_wait_minutes DESC;

