import os
from dotenv import load_dotenv

load_dotenv()

class Config:

    DEFAULT_ADMIN_EMAIL = os.getenv('DEFAULT_ADMIN_EMAIL')
    DEFAULT_ADMIN_PASSWORD = os.getenv('DEFAULT_ADMIN_PASSWORD')
    SECRET_KEY = os.getenv('FLASK_SECRET_KEY', 'fcffc4521d166bf48b3e1f2ac30ac9ef6fc417cace089c6a')
    #MYSQL_USER=pinness
    #MYSQL_PWD=devPiness231
    #MYSQL_HOST=18.207.202.233
    #MYSQL_DB=Healtigrity
    #SQLALCHEMY_DATABASE_URI =mysql+mysqldb://pinness:devPiness231@18.207.202.233/Healtigrity
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqldb://pinness:devPiness231@18.207.202.233/Healtigrity'