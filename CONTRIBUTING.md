# Contributing

## Workflow

1. Create a focused branch from `main` using a descriptive name such as `feat/add-viewership-mart` or `fix/ad-revenue-grain`.
2. Keep each pull request scoped to one outcome and link its issue when one exists.
3. Follow the project layers: one source per staging model, reusable joins and business logic in `intermediate`, and BI-facing facts and dimensions in `marts`.

## dbt expectations

- Use `ref()` and `source()` for model dependencies; do not hard-code warehouse relations.
- Document new models and material columns in schema YAML.
- Add data tests for primary keys, required fields, relationships, and important business rules.
- For SQL, macro, snapshot, or test changes, run a targeted check such as `dbt build --select +<model_name>+` before opening a pull request.
- For configuration-only changes, run `dbt parse`.

## Pull requests

Use the pull request template to describe the data-contract impact, validation performed, and any rollout or backfill required. Request review from the automatically assigned code owner.

## Commit messages

Use concise Conventional Commit-style messages, for example `feat: add advertiser spend mart` or `fix: preserve programme grain`.

## Security

Do not commit passwords, tokens, private keys, or customer data. Report vulnerabilities privately as described in [SECURITY.md](SECURITY.md).
