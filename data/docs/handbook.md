# Data Pipeline Pro Handbook

## Getting Started
Install with `uv add data-pipeline-pro`. You need Python 3.11 or higher.
Set your database connection string in `config.json` before running anything.

## Running a Pipeline
Pipelines run in three stages: extract, clean, transform.
Each stage writes its output to the `output/` folder.
Logs are written to `pipeline.log` in the project root.

## Scheduling
Pipelines can be scheduled with any cron-style scheduler.
A pipeline that fails will write an ERROR line to the log and exit with code 1.

## Support
Email support@example.com. Response time is up to 2 business days.
