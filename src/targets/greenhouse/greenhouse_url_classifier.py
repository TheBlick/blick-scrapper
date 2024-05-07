import re 

from misc.utils import strip_non_numeric

from targets.greenhouse.greenhouse_job_board_parser import GreenhouseBoardParser
from targets.greenhouse.models import JobPosting, JobPostingFromBoard
from targets.greenhouse.constants import *

class GreenhouseUrlClassifier:
    def __init__(self, logger):
        self.__logger = logger
        self.job_board_parser = GreenhouseBoardParser(logger)

    def __match_url_to_category(self, url, pattern):
        if  re.compile(pattern).match(url):
            return True
        return False

    def classify_urls_to_dict(self, url_list):
        #TODO Add another step to add job postings inside the job boards
        classification_list = []
        for url in url_list:
            
            if self.__match_url_to_category(url=url, pattern=JOB_BOARD_REGEX_PATTERN):
                for job_board_dict in self.job_board_parser.extract_greenhouse_job_info(url):
                    model = JobPostingFromBoard(url=job_board_dict.get('url'), origin_url=url, title=job_board_dict.get('title'), location=job_board_dict.get('location'))
                    classification_list.append(model.dict())

            # if category == EMBED_JOB_BOARD_CATEGORY:        
            #     for job_board_url in self.job_board_parser.extract_embedded_job_info(url):
                    

            if self.__match_url_to_category(url=url, pattern=JOB_POSTING_REGEX_PATTERN):
                model = JobPosting(url=url)
                classification_list.append(model.dict())
                
        return classification_list
