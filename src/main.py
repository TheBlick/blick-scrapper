import os
from time import sleep
from db.db_config import Database
from db.models.job import Job

class Main:
    def __init__(self):
        print('Main started')
        db = Database(
            Database.psql_conn_string(
                host='postgres',
                username=os.getenv('POSTGRES_USER'),
                password=os.getenv('POSTGRES_PASSWORD'),
                port='5432',
                db_name=os.getenv('POSTGRES_DB')
            )
        )
        db.create_tables()

if __name__ == "__main__":
    main = Main()
    # sleep (20)