import os

import unittest
from unittest.mock import patch, MagicMock

from targets.greenhouse.greenhouse_url_classifier import GreenhouseUrlClassifier


def build_test_base_path():
    return "/".join(os.path.dirname(os.path.realpath(__file__)).split("/"))


class TestGreenhouseUrlClassifier(unittest.TestCase):
    def setUp(self):
        self.mock_logger = MagicMock()
        self.mock_engine = MagicMock()
        self.batch_size = 5
        self.classifier = GreenhouseUrlClassifier(logger=self.mock_logger)

    def test_should_classify_job_postings_regex_pattern(self):
        result = self.classifier.classify_urls_to_dict(
            [
                "https://boards.greenhouse.io/random_company/jobs/123",
                "https://boards.greenhouse.io/another_company/jobs/321",
                "https://testesteste",
            ]
        )

        expected_result = [
            {
                "url": "https://boards.greenhouse.io/random_company/jobs/123",
                "origin_url": "https://boards.greenhouse.io/random_company/jobs/123",
                "origin_category": "job_posting",
                "target_name": "greenhouse",
                "company_name": "random_company",
                "job_id": "123",
                "title": None,
                "location": None,
            },
            {
                "url": "https://boards.greenhouse.io/another_company/jobs/321",
                "origin_url": "https://boards.greenhouse.io/another_company/jobs/321",
                "origin_category": "job_posting",
                "target_name": "greenhouse",
                "company_name": "another_company",
                "job_id": "321",
                "title": None,
                "location": None,
            },
        ]
        assert result == expected_result

    def test_should_not_classify_job_postings_that_do_not_match_regex_pattern(self):
        result = self.classifier.classify_urls_to_dict(["https://testesteste"])

        expected_result = []
        assert result == expected_result

    def test_should_approve_merge_when_it_is_compliant(self):
        with (
            patch(
                "targets.greenhouse.greenhouse_url_classifier.GreenhouseBoardParser.extract_greenhouse_job_info"
            ) as parser,
            patch("targets.greenhouse.greenhouse_job_board_parser.requests") as req,
        ):
            parser.return_value = [
                {
                    "url": "https://boards.greenhouse.io/fixture_board_company/jobs/4362194005",
                    "title": "Geospatial Data Scientist",
                    "location": "LATAM - Remote",
                }
            ]

            urls = self.classifier.classify_urls_to_dict(
                [
                    "https://boards.greenhouse.io/companyname",
                    "https://boards.greenhouse.io/random_company/jobs/123",
                ]
            )
            parser.assert_called_once_with("https://boards.greenhouse.io/companyname")
            assert urls == [
                {
                    "url": "https://boards.greenhouse.io/fixture_board_company/jobs/4362194005",
                    "origin_url": "https://boards.greenhouse.io/companyname",
                    "origin_category": "job_board",
                    "target_name": "greenhouse",
                    "company_name": "companyname",
                    "job_id": "4362194005",
                    "title": "Geospatial Data Scientist",
                    "location": "LATAM - Remote",
                },
                {
                    "url": "https://boards.greenhouse.io/random_company/jobs/123",
                    "origin_url": "https://boards.greenhouse.io/random_company/jobs/123",
                    "origin_category": "job_posting",
                    "target_name": "greenhouse",
                    "company_name": "random_company",
                    "job_id": "123",
                    "title": None,
                    "location": None,
                },
            ]


if __name__ == "__main__":
    unittest.main()
