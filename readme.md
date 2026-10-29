# AppDirect README

AppDirect is a sample Python Flask application used to test various technologies. This application is meant to be containerized and run in a Kubernetes Pod. The *yaml* directory contains a simple deployment yaml.

The application provides output to stdout and can be obtained via `kubectl logs <pod name>` if running in Kubernetes. This is the standard flask output.

This repository also includes a Github Action workflow to deploy to an EC2 instance for testing. Have fun!!!!!

## Getting started with Flox (recommended)

One command gives you the right Python, all the Python packages, and a local Postgres database:

```bash
flox activate --start-services     # or: flox activate -s
python app/app.py
```

Then open http://localhost:5000 and try:

| Route | What it does |
| --- | --- |
| `/test` | Simple health check |
| `/sql-check` | Lists databases on the Postgres server |
| `/sql-create` | Creates the `appdirectdb` database and table |
| `/sql-add` | Adds a timestamped row |
| `/sql-show` | Shows all rows |
| `/msg` | Shows the `PAGE_MESSAGE` environment variable |

You need Flox installed ([install guide](https://flox.dev/docs/install-flox/)). You do **not** need Python, Postgres, or Docker installed on your machine.

### What the environment provides

| Piece | Version | Why |
| --- | --- | --- |
| Python | 3.11 | This app's dependencies (`requests 2.22`, `Flask 1.1`) break on Python 3.12 and newer |
| PostgreSQL | 16 | Runs locally as a Flox service; data stays in `.flox/cache` |
| Python packages | from `requirements.txt` | Installed into a virtual environment inside the Flox environment |

The exact versions are locked in `.flox/env/manifest.lock`, so every laptop and CI runner gets the same environment.

## Getting started without Flox (the old way)

1. Install Python **3.11 or older** (newer versions crash on startup).
2. Install Postgres, or have access to a Kubernetes cluster with a `postgresql-service`.
3. Create a virtual environment and run `pip install -r requirements.txt`.
4. If Postgres isn't at `postgresql-service`, set `DB_HOST` (for example `export DB_HOST=localhost`).
5. Run `python app/app.py`.

## Configuration

| Variable | Default | Purpose |
| --- | --- | --- |
| `DB_HOST` | `postgresql-service` | Postgres host. The default matches the Kubernetes service; Flox sets it to `localhost` |
| `PAGE_MESSAGE` | none | Text shown by the `/msg` route |
