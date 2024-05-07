import json 
import logging 
from dotenv import load_dotenv

from search_engines.google.google import GoogleSearch

from targets.greenhouse.greenhouse_url_classifier import GreenhouseUrlClassifier
from configuration.configuration import ConfigurationHelper
from db.db_config import DatabaseInteractor

from db.models.job import Job

load_dotenv()
logging.basicConfig(
    format="[%(levelname)s] [%(asctime)s][%(filename)-15s][%(lineno)4d] : %(message)s",
    level=logging.INFO,
)
logging.getLogger("sqlalchemy").setLevel(logging.WARNING)
log = logging.getLogger()

config = ConfigurationHelper(log)

rdbms_interactor = DatabaseInteractor(log, config.database_uri)
rdbms_interactor.create_tables()
classifier = GreenhouseUrlClassifier(logger=log)

fetcher = GoogleSearch(logger=log, api_key=config.google_api_key, cse_id=config.google_cse_id)


search_term = 'site:https://boards.greenhouse.io/ "Data Engineer" "remote" "latam"'
urls = fetcher.fetch_urls(search_term=search_term, start_page=1)

test_data = classifier.classify_urls_to_dict(urls)
rdbms_interactor.insert_data_to_rdbms(Job, test_data)