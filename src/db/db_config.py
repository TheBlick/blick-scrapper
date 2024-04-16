from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Database:
    def __init__(self, db_url):
        self.engine = create_engine(db_url, echo=True)
        self.Session = sessionmaker(bind=self.engine)

    @classmethod
    def psql_conn_string(self, host, username, password, port, db_name):
        conn_string = f'postgresql+psycopg2://{username}:{password}@{host}:{port}/{db_name}'
        return conn_string
    
    def create_tables(self):
        Base.metadata.create_all(self.engine)