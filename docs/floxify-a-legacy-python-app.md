# Floxify a legacy Python app in 5 steps

A short guide based on floxifying AppDirect, a Flask app from 2020.

## The problem in one sentence

Old Python apps quietly depend on things nobody wrote down: a Python version, system libraries, and services like a database. A new laptop, a new CI image, or a newer Python breaks them.

What broke in AppDirect on a fresh machine:

| What | Symptom | Hidden assumption |
| --- | --- | --- |
| Two pins that never existed (`MarkupSafe==3.2.0`, `psycopg2-binary==3.4`) | `pip install` fails | Nobody had rebuilt from scratch in years |
| `requests 2.22` on Python 3.12+ | Crash on startup: `No module named 'urllib3.packages.six.moves'` | "Python" meant Python 3.11 or older |
| Database host `postgresql-service` | Database routes fail locally | You're always inside the Kubernetes cluster |
| Dockerfile on `ubuntu:22.04` | Only works because 22.04 ships Python 3.10 | The base image's Python version |

## The 5 steps

**1. Initialize.** In the project folder, run `flox init`. It creates a `.flox/` folder that holds the environment definition. Flox may detect `requirements.txt` and offer to set up Python for you.

**2. Pin what the app actually needs.** Find packages with `flox search`, then install them:

```bash
flox install python311 postgresql_16
```

This records the exact versions in `.flox/env/manifest.lock`. Nothing is installed into your system; `which python` points into `/nix/store`.

**3. Keep the app's own packages where they belong.** A short hook in the manifest creates a Python virtual environment inside the Flox environment and runs `pip install -r requirements.txt`. Flox locks the layer pip can't reach (Python itself, Postgres, system libraries); pip still manages the Python libraries.

**4. Add services and settings.** Postgres becomes a Flox service, and settings like `DB_HOST=localhost` become environment variables in the manifest. The code keeps its Kubernetes default, so production doesn't change.

**5. Commit and share.** Commit the `.flox/` folder. Now onboarding is:

```bash
git clone <repo> && cd <repo>
flox activate -s
python app/app.py
```

The same environment runs in CI through Flox's GitHub Actions, and `flox containerize` can build a container image from it for production.

## Is it better? An honest answer

**Better:**
- The Python version is declared and locked, not assumed.
- The database runs as part of the environment: one command, no Docker, no cluster.
- The same definition works on macOS and Linux, on laptops and in CI.
- Upgrades become reviewable: moving to Python 3.13 is a diff to the lockfile, not a surprise.

**Not fixed by Flox:**
- The bad pins in `requirements.txt` still had to be fixed by hand.
- Python libraries still come from pip. You could go further and use Nix-built Python packages, but for a legacy app with old pins, pip inside Flox is the practical choice.
- The old dependencies are still old. Flox makes them reproducible; upgrading them is still real work, though now it's safer work.

## How to explain it to someone in 20 seconds

> A Dockerfile tells a machine what to do and hopes the result matches. Flox writes down exactly what this app needs, from Python to Postgres, and gives every machine exactly that.
