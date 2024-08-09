import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'mysql+pymysql://username:password@rds-endpoint.amazonaws.com/dbname')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
