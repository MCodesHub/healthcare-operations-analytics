# Data Dictionary

All records and values in this project are synthetic.

| Field | Type | Definition |
|---|---|---|
| encounter_id | string | Synthetic unique visit identifier |
| facility_id | integer | Synthetic facility key |
| arrival_datetime | datetime | Simulated ED arrival time in 2024 |
| age | integer | Simulated patient age |
| sex | category | Simulated recorded sex |
| race_ethnicity | category | Simulated demographic category |
| zip_code | string | Inland Empire ZIP code used for geographic context |
| payer | category | Simulated primary payer group |
| esi_acuity | integer | Emergency Severity Index, 1 (most urgent) to 5 |
| service_line | category | Clinical service grouping |
| primary_diagnosis | category | High-level simulated diagnosis |
| wait_minutes | integer | Arrival-to-provider proxy |
| treatment_minutes | integer | Simulated treatment duration |
| length_of_stay_minutes | integer | Total simulated ED duration |
| disposition | category | Visit outcome |
| revisit_72h | boolean | Simulated revisit within 72 hours |
| satisfaction_score | decimal | Simulated 1–5 rating |
| facility_name | category | Synthetic facility name |
| city | category | Facility city |
| facility_type | category | General facility classification |
| arrival_date | date | Date portion of the arrival timestamp |
| arrival_hour | integer | Arrival hour from 0 through 23 |
| day_of_week | category | Day name derived from arrival time |
| month | string | Arrival month in YYYY-MM format |
| shift | category | Night, day, or evening arrival period |
| age_group | category | Age band used for grouped analysis |
| door_to_provider_target_met | boolean | Whether the original 30-minute wait target flag was met |
| los_target_met | boolean | Whether the original four-hour length-of-stay target flag was met |
| wait_target_met | boolean | Refreshed 30-minute wait target flag created by the Python analysis |
