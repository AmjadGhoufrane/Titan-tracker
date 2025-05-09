# FA-Titans

A data collection and analytics application for tracking Titan-class ships in EVE Online.

## Overview

FA-Titans is an Azure Function App that periodically collects statistics about Titan-class ships in EVE Online using the zKillboard API. The application stores this information in a MySQL database for historical tracking and analysis. This data can then be fed to any data analysis software (Power-Bi,Tableau, etc) for further use.

## Requirements

- Python 3.x
- Azure Functions Core Tools
- PyMySQL
- Requests library

## Setup

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Configure database connection in `common/env.py`
4. Run locally: `func start`
5. Deploy to Azure: `func azure functionapp publish <app-name>`

## Schedule

The application runs daily at 1:00 AM UTC to collect the latest Titan statistics.

## Data Collected

- Monthly ship and ISK statistics
- Top characters involved in Titan kills
- Top corporations and alliances with Titan activity
- Most active solar systems for Titan engagements