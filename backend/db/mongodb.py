
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import os

load_dotenv()

username = os.getenv("MONGO_USER")
password = os.getenv("MONGO_PASSWORD")

def initialize_mongodb_python_client(username: str, password: str) -> MongoClient:
    """Connects to MongoDB and returns a client"""
    uri = f"mongodb+srv://{username}:{password}@githubrecruiter.jtrl9bm.mongodb.net/?retryWrites=true&w=majority&appName=GitHubRecruiter"

    # Create a new client and connect to the server
    client = MongoClient(uri, server_api=ServerApi('1'))

    # Send a ping to confirm a successful connection
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)

    return client