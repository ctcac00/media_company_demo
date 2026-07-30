output "project_id" {
  description = "dbt Cloud project ID."
  value       = dbtcloud_project.media_company_demo.id
}

output "development_environment_id" {
  description = "dbt Cloud Development environment ID."
  value       = dbtcloud_environment.development.environment_id
}

output "production_environment_id" {
  description = "dbt Cloud Production environment ID."
  value       = dbtcloud_environment.production.environment_id
}

output "ci_environment_id" {
  description = "dbt Cloud CI environment ID."
  value       = dbtcloud_environment.ci.environment_id
}

output "snowflake_connection_id" {
  description = "dbt Cloud Snowflake global connection ID."
  value       = dbtcloud_global_connection.snowflake.id
}

output "production_credential_id" {
  description = "dbt Cloud Snowflake production credential ID."
  value       = dbtcloud_snowflake_credential.production.credential_id
}

output "ci_credential_id" {
  description = "dbt Cloud Snowflake CI credential ID."
  value       = dbtcloud_snowflake_credential.ci.credential_id
}

output "daily_production_build_job_id" {
  description = "Daily Production dbt build job ID."
  value       = dbtcloud_job.daily_production_build.id
}

output "demo_source_data_state_build_job_id" {
  description = "Demo Source Data State Build job ID."
  value       = dbtcloud_job.demo_source_data_state_build.id
}

output "slim_ci_job_id" {
  description = "Slim CI job ID."
  value       = dbtcloud_job.slim_ci.id
}
