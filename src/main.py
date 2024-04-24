import os
import json
from time import sleep
from colors import COLORS
from db.db_config import Database
from db.models.job import Job
from db.models.scraped_job import ScrappedJob
from scrapper import Scrapper

class Main:
    def __init__(self):
        print('Main started')
        self.db = Database(
            Database.psql_conn_string(
                host='postgres',
                username=os.getenv('POSTGRES_USER'),
                password=os.getenv('POSTGRES_PASSWORD'),
                port='5432',
                db_name=os.getenv('POSTGRES_DB')
            )
        )
        self.db.create_tables()
        self.scrapper = Scrapper(self.db)

    def scrape_landing_jobs(self, SourceTable, TargetTable):
        records = self.db.retrieve_not_processed_records(SourceTable)
        target_cols = TargetTable.__table__.columns.keys()

        inserted_count = 0
        for job_record in records:
            scrapped_job = self.scrapper.scrape_landing_job(job_record)
            self.db.update_processed_at(SourceTable, scrapped_job)

            filtered_scrapped_job = {key: value for key, value in job_record.items() if key in target_cols}
            inserted_count += self.db.insert_record(TargetTable, filtered_scrapped_job)

            if inserted_count % 500 == 0 and inserted_count != 0:
                print(f'{COLORS['GREEN']}Inserted {inserted_count} records sucessfully already ...{COLORS['WHITE']}')
        
        if inserted_count % 500 != 0 and inserted_count != 0:
            print(f'{COLORS['YELLOW']}Inserted {inserted_count} records in total!{COLORS['WHITE']}')

if __name__ == "__main__":
    main = Main()
    main.scrape_landing_jobs(Job, ScrappedJob)
    # records = main.scrapper.scrape_landing_jobs(Job)
    # return_code = main.db.update_processed_at(Job, records[0])
    # print(return_code)
    # print(records)