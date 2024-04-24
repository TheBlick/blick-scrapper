import requests
from requests.models import Response
from io import BytesIO

class ApiInteractor():
    def __init__(self):
        pass

    def get(self, url):
        try:
            response = requests.get(url)
            return response
        except requests.exceptions.RequestException as e:
            print(f'Error in requesting url {url}: {e}')
            error_response = Response()
            error_response.status_code = 500
            error_response._content = b'Error requesting url'
            return error_response
    
if __name__ == '__main__':
    api_interactor = ApiInteractor()
    response = api_interactor.get('https://boards.greenhouse.io/remotecom/jobs/5757553003')
    print(response.text)