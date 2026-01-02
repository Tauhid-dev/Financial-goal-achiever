# Financial Goal Achiever

## Environment + OCI

Copy the example environment file and fill in the required values:

```bash
cp .env.example .env
# Edit .env and set DATABASE_URL, JWT_SECRET, and any other needed variables
```

The OCI bootstrap script (`scripts/oci_bootstrap.sh`) expects the `.env.example` file at the repository root. It will copy it to `.env` if the latter is missing and then prompt you to edit the required variables.

## Development

...
