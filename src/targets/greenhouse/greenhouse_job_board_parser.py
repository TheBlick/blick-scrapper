from bs4 import BeautifulSoup
import requests
import re
import time


class GreenhouseBoardParser:
    def __init__(self, logger):
        self.__logger = logger
        self.job_url_pattern = re.compile(r"(/jobs/\d+)|(\?gh_jid=\d+)")

    def extract_greenhouse_job_info(self, url):
        self.__logger.info(f"extracting job board info for url {url}")
        response = requests.get(url)
        if response.status_code != 200:
            self.__logger.info(
                f"Failed to retrieve the webpage: Status code {response.status_code}"
            )
            return []
        soup = BeautifulSoup(response.text, "html.parser")

        job_links = soup.find_all("a", href=self.job_url_pattern)
        job_info_list = []

        for job_link in job_links:
            job_url = f"https://boards.greenhouse.io{job_link.get('href')}"
            job_title = job_link.text.strip()
            location_tag = job_link.find_next_sibling("span", class_="location")
            job_location = (
                location_tag.text.strip() if location_tag else "Location not specified"
            )

            job_info_list.append(
                {"url": job_url, "title": job_title, "location": job_location}
            )

        return job_info_list

    def extract_embedded_job_info(self, url):
        self.__logger.info(f"extracting embedded job info for url {url}")
        response = requests.get(url)
        time.sleep(0.5)
        if response.status_code != 200:
            self.__logger.info(
                f"Failed to retrieve the webpage: Status code {response.status_code}"
            )
            return []
        soup = BeautifulSoup(response.text, "html.parser")

        job_links = soup.find_all("a", href=self.job_url_pattern)

        job_info_list = []

        for job_link in job_links:
            job_url = job_link.get("href")
            job_info_list.append(job_url)

        return job_info_list
