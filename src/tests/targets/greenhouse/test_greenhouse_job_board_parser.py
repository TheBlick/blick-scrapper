import unittest
from unittest.mock import patch, MagicMock

from targets.greenhouse.greenhouse_job_board_parser import GreenhouseBoardParser


class TestGreenhouseBoardParser(unittest.TestCase):
    def setUp(self):
        # Setup a logger
        self.logger = MagicMock()
        self.parser = GreenhouseBoardParser(self.logger)

    @patch("requests.get")
    def test_extract_greenhouse_job_info(self, mock_get):
        with open(
            "tests/targets/greenhouse/fixtures/board_page_with_several_placements.html",
            "r",
        ) as file:
            html_content = file.read()

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = html_content
        mock_get.return_value = mock_response

        # Call the method under test
        url = "https://boards.greenhouse.io/remotecom"
        job_info = self.parser.extract_greenhouse_job_info(url)

        assert len(job_info) == 8
        assert job_info[1] == {
            "url": "https://boards.greenhouse.io/fixture_board_company/jobs/4362194005",
            "title": "Geospatial Data Scientist",
            "location": "LATAM - Remote",
        }

        mock_get.assert_called_once_with(url)


if __name__ == "__main__":
    unittest.main()
