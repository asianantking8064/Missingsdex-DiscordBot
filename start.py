import os
import subprocess

# Set environment variables as needed
os.environ["BALLSDEXBOT_DB_URL"] = "postgres://ballsdex:defaultballsdexpassword@localhost:5432/ballsdex"
# os.environ["BALLSDEXBOT_REDIS_URL"] = "redis://localhost"  # Uncomment if needed

# Install dependencies first
subprocess.run(["poetry", "install"], check=True)

# Run the bot using poetry
subprocess.run(["poetry", "run", "python3", "-m", "ballsdex", "--dev"])