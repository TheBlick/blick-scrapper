from unittest.mock import patch

from src.api_interactor import ApiInteractor

class TestApiInteractor:
    class DummyHttpResponse:
        def __init__(self, status_code, content):
            self.status_code = status_code
            self.text = content.encode()

    def test_get_should_pass_when_url_is_valid(self):
        expected_result = TestApiInteractor.DummyHttpResponse(200, 'Success')

        api_interactor = ApiInteractor()
        response = api_interactor.get('https://boards.greenhouse.io/remotecom/jobs/5757553003')

        assert response.status_code == expected_result.status_code

    def test_get_should_fail_when_url_is_valid(self):
        expected_result = TestApiInteractor.DummyHttpResponse(500, 'Error requesting url')

        api_interactor = ApiInteractor()
        response = api_interactor.get('https://some-job-url.com')

        assert response.status_code == expected_result.status_code
        assert response._content == expected_result.text