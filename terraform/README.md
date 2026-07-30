# Media Company Demo Terraform

This directory manages dbt platform resources for the Media Company Demo:

- dbt Cloud project
- Snowflake global connection
- Snowflake deployment credentials using a sensitive keypair variable
- Development, CI, and Production environments
- Daily Production `dbt build` job
- PR-triggered Slim CI `dbt build --select state:modified+` job
- Demo source data state build job

## Prerequisites

Create or identify the Snowflake account, database, warehouse, role, and user before running Terraform. The Snowflake role needs permission to create schemas in the target database.

Set `dbt_access_url` to your dbt Cloud access URL, for example `https://cloud.getdbt.com`. Use a dbt Cloud service token, not a personal access token.

Copy `terraform.tfvars.example` to `terraform.tfvars` for local use, then fill in account-specific values. Provide `snowflake_private_key_path` through a secure local variable mechanism. Do not commit private keys, service tokens, Terraform state, plans, crash logs, or `*.tfvars` files containing secrets.
