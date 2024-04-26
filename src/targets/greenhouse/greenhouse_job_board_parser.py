from bs4 import BeautifulSoup
import requests
import re
import time 

class GreenhouseBoardParser:
    def __init__(self):
        self.job_url_pattern = re.compile(r"(/jobs/\d+)|(\?gh_jid=\d+)")
            
    def extract_greenhouse_job_info(self, url):
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Failed to retrieve the webpage: Status code {response.status_code}")
            return []
        soup = BeautifulSoup(response.text, 'html.parser')
        job_links = soup.find_all('a', href=self.job_url_pattern)

        job_info_list = []

        for job_link in job_links:
            job_url = f"https://boards.greenhouse.io{job_link.get('href')}"
            job_info_list.append(job_url)

        return job_info_list

    def extract_embedded_job_info(self, url):
        response = requests.get(url)
        time.sleep(0.5)
        if response.status_code != 200:
            print(f"Failed to retrieve the webpage: Status code {response.status_code}")
            return []
        soup = BeautifulSoup(response.text, 'html.parser')
        job_links = soup.find_all('a', href=self.job_url_pattern)

        job_info_list = []

        for job_link in job_links:
            job_url = job_link.get('href')
            job_info_list.append(job_url)

        return job_info_list