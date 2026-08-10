# AWS FinOps Automation Toolkit

A production-grade collection of Python automation scripts and Infrastructure-as-Code templates designed to optimize cloud infrastructure spend, eliminate idle resources, and enforce resource governance using AWS Boto3.

## Repository Structure
* `scripts/auto_stop_dev.py`: Tag-driven automation script to gracefully shut down non-prod EC2 and RDS instances outside of business hours.
* `scripts/ebs_cleanup.py`: Scans and cleans up unattached (idle) EBS volumes accumulating storage charges.
* `lambda/auto_stop_lambda.py`: Serverless adaptation of the auto-stopper designed to run natively inside AWS Lambda.
* `terraform/main.tf`: Infrastructure-as-Code configuration provisioning secure IAM roles and execution policies.
* `security/iam-policy.json`: Least-privilege IAM policy reference document.

## Governance & Tagging Taxonomy
Resources managed by the scripts must utilize these metadata tags:
* `Environment`: Must be set to `dev`, `staging`, or `test`.
* `DoNotStop`: (Optional) Set to `true` to exempt specific critical resources.

## Safety Features
* **Dry-Run Mode:** Local execution scripts default to simulation mode (`DRY_RUN = True`) to prevent accidental changes.
* **Least-Privilege Security:** Restricts IAM roles to strict read and stop actions only.

## Usage
Run scripts locally or from an authenticated terminal session:
(bash)
python3 scripts/auto_stop_dev.py
python3 scripts/ebs_cleanup.py
