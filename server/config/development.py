from dotenv import load_dotenv
import os

load_dotenv()

class DevelopmentConfig:
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "mysql+pymysql://root:Clave123@localhost/jcaproposals")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv("SECRET_KEY", "your-development-secret-key")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your_super_secret_key")

