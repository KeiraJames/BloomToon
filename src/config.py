import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Environment variables (use dotenv or set manually)
MONGO_URI = os.getenv("MONGO_URI")
PLANTNET_API_KEY = os.getenv("PLANTNET_API_KEY")

# Database and Collection Names
DB_NAME = "plants"
COLLECTION_NAME = "c1"

