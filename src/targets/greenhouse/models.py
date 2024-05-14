import re
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, validator

from targets.greenhouse.constants import *


class JobPosting(BaseModel):
    url: str

    def dict(self, *args, **kwargs) -> dict:
        return {
            "url": self.url,
            "origin_url": self.url,
            "origin_category": JOB_POSTING_CATEGORY,
            "target_name": "greenhouse",
            "company_name": re.search(JOB_POSTING_REGEX_PATTERN, self.url).group(1),
            "job_id": re.search(JOB_POSTING_REGEX_PATTERN, self.url).group(2),
            "title": None,  # TODO - add something to make this schema generic to all models
            "location": None,
        }


class JobPostingFromBoard(BaseModel):
    url: str
    origin_url: str
    title: str
    location: str

    def dict(self, *args, **kwargs) -> dict:
        return {
            "url": self.url,
            "origin_url": self.origin_url,
            "origin_category": JOB_BOARD_CATEGORY,
            "target_name": "greenhouse",
            "company_name": re.search(JOB_BOARD_REGEX_PATTERN, self.origin_url).group(
                1
            ),
            "job_id": re.search(JOB_POSTING_REGEX_PATTERN, self.url).group(2),
            "title": self.title,
            "location": self.location,
        }
