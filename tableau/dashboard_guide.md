# Tableau Dashboard Guide

## Status

The Tableau dashboard is in progress. This repository contains a Tableau-ready CSV and a practical dashboard plan, but it does not include a completed workbook or published dashboard link.

## Data source

Connect Tableau Public or Tableau Desktop to:

`data/processed/ed_encounters_cleaned.csv`

Run `python src/data_analysis.py` first to create or refresh this file. The original Tableau-ready extract remains available as `data/processed/tableau_ed_encounters.csv`.

## Planned dashboard

Use a 1,200 × 750 pixel dashboard with these elements:

1. KPI cards for total encounters, average wait, median length of stay, and 72-hour revisit rate.
2. Line chart showing average wait time by arrival hour.
3. Bar chart comparing average wait time by facility.
4. Bar chart comparing 72-hour revisit rates by service line.
5. Filters for facility, month, service line, payer, and ESI acuity.

## Suggested calculated fields

```text
72-Hour Revisit Rate = AVG([Revisit 72h])
Average Wait = AVG([Wait Minutes])
Median Length of Stay = MEDIAN([Length Of Stay Minutes])
Wait Target Rate = AVG([Wait Target Met])
```

Format rates as percentages with one decimal place. Use the same burgundy accent color as the Python charts (`#6C2B3B`) for a consistent presentation.

