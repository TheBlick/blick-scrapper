import requests

class GoogleSearch:
    def __init__(self, logger, api_key, cse_id):
        self.__logger = logger
        self.api_key = api_key
        self.cse_id = cse_id

    def google_search(self, search_term, start_page):
        self.__logger.info(f"searching for term {search_term} in page {start_page}")
        search_url = "https://www.googleapis.com/customsearch/v1"
        params = {
            "q": search_term,
            "cx": self.cse_id,
            "key": self.api_key,
            "start": start_page,
        }
        response = requests.get(search_url, params=params)
        self.__logger.info(f"Google response status {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            return result

    def get_urls(self, data):
        url_list = []
        for item in data["items"]:
            if item.get("link"):
                url_list.append(item["link"])
        return url_list

    def fetch_urls(self, search_term, start_page):
        results = self.google_search(search_term, start_page)
        return self.get_urls(results)
