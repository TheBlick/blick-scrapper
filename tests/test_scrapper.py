import pytest
from src.scrapper import Scrapper
from unittest.mock import patch

class TestScrapper():
    class DummyHttpResponse:
        def __init__(self, status_code, job_name, location, company):
            self.status_code = status_code
            self.text = """ <html>
                <head></head>
                <body>
                    <div class="app-title">{job_name}</div>
                    <div class="location">{location}</div>
                    <div class="company-name">{company}</div>
                </body>
            </html> """.format(job_name=job_name, location=location, company=company)
            self.text = self.text.encode('utf-8')

    def test_get_should_pass_when_url_is_valid(self):
        scrapper = Scrapper(None)
        response = scrapper.get('https://boards.greenhouse.io/remotecom/jobs/5757553003')
        assert response.status_code == 200

    def test_get_should_pass_when_url_is_invalid(self):
        scrapper = Scrapper(None)
        response = scrapper.get('https://this.url.doesnt.exist/fails')
        assert response.status_code != 200

    @patch('src.scrapper.Scrapper.get')
    @pytest.mark.parametrize("job_name, location, company", [
        ('Software Engineer', 'Remote', 'Remote.com'),
        ('Data Scientist', 'Glovo', 'Glovo.com'),
        ('Product Manager', 'CloudFare', 'CloudFare.com'),
    ])
    def test_scrape_landing_job_should_pass_when_html_is_scrapped(self, mock_http_response, job_name, location, company):
        mock_http_response.return_value = self.DummyHttpResponse(200, job_name, location, company)
        scrapper = Scrapper(None)
        job_record = {
            'url': 'https://a-job-url.com'
        }
        result = scrapper.scrape_landing_job(job_record)
        assert result['position_name'] == job_name
        assert result['location'] == location
        assert result['company'] == company