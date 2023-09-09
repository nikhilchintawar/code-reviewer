import os


# Load the environment variables from the .env file
def load_env():
    with open(".env") as f:
        for line in f:
            key, value = line.strip().split("=")
            os.environ[key] = value
