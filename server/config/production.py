from dotenv import load_dotenv
import os

load_dotenv()

class ProductionConfig:
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "mysql+pymysql://root:Clave123@localhost/jcaproposals")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv("SECRET_KEY", "your-production-secret-key")
