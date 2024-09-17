import os

class Config:
    # Secret key for JWT encoding and decoding
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_secret_key_here'
    
    # Database configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'mysql://username:password@localhost/fruitsdb'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
