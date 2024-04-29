from bs4 import BeautifulSoup
from api_interactor import ApiInteractor
from data_transformer import DataTransformer

connections = {
    'app-title': 'position_name',
    'location': 'location',
    'company-name': 'company',
}

class Scrapper():
    def __init__(self, db) -> None:
        self.__api = ApiInteractor()
        self.db = db

    def get(self, url):
        response = self.__api.get(url)
        return response
    
    def scrape_landing_job(self, job_record):
        job_url = job_record.get('url')
        response = self.get(job_url)
        html_doc = response.text

        soup = BeautifulSoup(html_doc, 'html.parser')
        fields = connections.items()

        for html_class,psql_field in fields:
            html = soup.find(class_=html_class)
            job_record['processed_at'] = DataTransformer.get_current_time()
            if html:
                info = html.text.replace('\n', '').strip()
                job_record[psql_field] = info
            else:
                job_record[psql_field] = None

        return job_record

if __name__ == '__main__':
    scrapper = Scrapper(None)
    response = scrapper.get('https://boards.greenhouse.io/remotecom/jobs/5757553003')
    html_doc = response.text

    soup = BeautifulSoup(html_doc, 'html.parser')
    fields = connections.items()
    # print(soup.prettify())
    for html_class,psql_field in fields:
        html = soup.find(class_=html_class)
        info = html.text.replace('\n', '').strip()
        print(f'{html_class} >> {psql_field}: {info}')