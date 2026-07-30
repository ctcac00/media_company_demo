# MediaCo — Media Analytics Demo

A dbt project showcasing full media analytics for MediaCo, built with the SDD (Spec-Driven Development) framework.

## What's included

- **Content performance** — viewership ratings, audience reach by programme, channel, and time slot
- **Advertising revenue** — ad impressions, CPM, revenue by show, daypart, and advertiser
- **Digital & streaming (MediaCo Streaming)** — VOD views, unique users, completion rates
- **Audience analytics** — demographics, reach, and engagement across linear TV + digital

## Stack

- **Warehouse:** Snowflake
- **Transformation:** dbt (Fusion engine)
- **Orchestration:** dbt Platform
- **Source data:** dbt seeds (realistic UK media sample data)

## Project structure

```
models/
├── staging/      — raw → typed, renamed, one source per model
├── intermediate/ — business logic, joins, spine tables
└── marts/        — fact and dimension tables for BI consumption
seeds/            — sample source data (CSV)
specs/            — requirements, design, and review documents
```

## Getting started

```bash
dbt deps
dbt seed
dbt build
```
