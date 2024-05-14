UNKOWN_CATEGORY_NAME = "Unknown"

JOB_POSTING_CATEGORY = "job_posting"
JOB_POSTING_REGEX_PATTERN = r"https://boards.greenhouse.io/([^/]+)/jobs/(\d+)"

JOB_BOARD_CATEGORY = "job_board"
JOB_BOARD_REGEX_PATTERN = r"https://boards.greenhouse.io/([^/\?\s]+)/?$"

EMBED_JOB_BOARD_CATEGORY = "embed_job_board"
EMBED_JOB_REGEX_PATTERN = (
    r"https://boards.greenhouse.io/embed/job_board\?for=([^\&\s]+)"
)
