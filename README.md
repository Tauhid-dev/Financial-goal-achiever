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

## Frontend Development

To run the frontend locally:

1. Copy the example environment file:
   ```bash
   cp frontend/.env.example frontend/.env
   ```
2. Install dependencies and start the dev server:
   ```bash
   cd frontend
   npm install
   npm run dev
   ```
