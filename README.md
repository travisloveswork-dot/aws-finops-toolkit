# aws-finops-toolkit-
Automate AWS cloud cost savings using Python. Features tag-driven non-production auto-stoppage, dry-run safety, and least-privilege security.


# AWS FinOps Automation Toolkit

A collection of production-grade Python scripts designed to optimize cloud infrastructure spend, enforce resource governance, and automate cost-saving operations using AWS Boto3.

## Features Included
* **Tag-Based Non-Production Auto-Stopper (`scripts/auto_stop_dev.py`):** Automatically shuts down idle development, testing, and staging resources (EC2 and RDS) outside of business hours based on resource tags rather than hardcoded IDs.

## Tagging Governance
For the automation scripts to recognize and manage resources, they must be tagged accordingly:
* `Environment`: Must be set to `dev`, `staging`, or `test`.
* `DoNotStop`: (Optional) Set to `true` to override and exempt a specific resource from automation.

## Safety & Security Features
* **Dry-Run Mode:** Defaults to a simulation mode (`DRY_RUN = True`) that outputs target resources to the console without issuing live API shutdown commands.
* **Least-Privilege IAM:** Designed to run with minimal required permissions (see `security/iam-policy.json`).

## Usage
Run the auto-stopper script from an authenticated terminal session:
(bash)
python3 scripts/auto_stop_dev.py
