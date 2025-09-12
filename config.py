from dotenv import load_dotenv
from os import getenv


load_dotenv()


class Config:
    DEBUG = getenv("DEBUG")
    SECRET_KEY = getenv("SECRET_KEY")
