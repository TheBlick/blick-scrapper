import re 

from utils import strip_non_numeric

from greenhouse_job_board_parser import GreenhouseBoardParser

UNKOWN_CATEGORY_NAME = 'Unknown'
JOB_POSTING_CATEGORY = 'job_posting'
JOB_BOARD_CATEGORY = 'job_board'
EMBED_JOB_BOARD_CATEGORY = 'embed_job_board'

class GreenhouseUrlClassifier:
    def __init__(self):
        self.job_board_parser = GreenhouseBoardParser()
        self.patterns = {
            'job_posting': re.compile(r"https:\/\/boards\.greenhouse\.io\/[^\/]+\/jobs\/\d+"),
            'job_board': re.compile(r"https:\/\/boards\.greenhouse\.io\/[^\/?]+(?:\?.*)?$"),
            'embed_job_board': re.compile(r"https:\/\/boards\.greenhouse\.io\/embed\/job_board\?for=[^&]+")
        }

    def classify_url_list(self, url_list):
        """
        Classify each URL based on the predefined regex patterns.

        Returns:
            dict: A dictionary mapping each URL to its classification.
        """
        classification_list = []
        for url in url_list:
            category = self._match_category(url)
            classifications = {'url': url,
                    'category': category}
            classification_list.append(classifications)
        return classification_list

    def _match_single_category(self, url, category):
        """
        Determine the category of a URL based on regex patterns.

        Args:
            url (str): The URL to classify.

        Returns:
            str: The classification of the URL.
        """
        pattern = self.patterns.get(category)
        if pattern.match(url):
            return True
        return False


    def instantiate_single_url(self, url, category, origin_url=None):
        if category == EMBED_JOB_BOARD_CATEGORY:
            company_name =  origin_url.split('=')[-1][0], #TODO arrumar essa lógica, usar um regex pra puxar o valor sem ser esse split fraco
        else:
            company_name = url.split('/')[-3], #TODO mesmo de cima

        row = {'url': url,
                'origin_url': origin_url,
                'origin_category': category,
                'target_name': 'greenhouse',
                'company_name': company_name,
                'job_id': strip_non_numeric(url.split('/')[-1])
                }
        return row


    def handle_google_results(self, url_list):
        #TODO Add another step to add job postings inside the job boards
        classification_list = []
        for url in url_list:
            if self._match_single_category(url, JOB_BOARD_CATEGORY):
                for job_board_url in self.job_board_parser.extract_greenhouse_job_info(url):
                    classification_list.append(self.instantiate_single_url(job_board_url, JOB_BOARD_CATEGORY, url))

            elif self._match_single_category(url, EMBED_JOB_BOARD_CATEGORY):
                for job_board_url in self.job_board_parser.extract_embedded_job_info(url):
                    classification_list.append(self.instantiate_single_url(job_board_url, EMBED_JOB_BOARD_CATEGORY, url))

            elif self._match_single_category(url, JOB_POSTING_CATEGORY):
                classification_list.append(self.instantiate_single_url(url, JOB_POSTING_CATEGORY))            

        return classification_list
