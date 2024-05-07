import enum
from sqlalchemy import Column, BigInteger, String, DateTime, Enum
from sqlalchemy.sql import func # https://stackoverflow.com/questions/13370317/sqlalchemy-default-datetime
from db.db_config import Base


class JobMatch(enum.Enum):
    direct_match    = 1
    indirect_match  = 2

class Job(Base):
    __tablename__   = 'jobs_test'
    __table_args__  = {"schema": "landing", "extend_existing": True}

    job_id          = Column(BigInteger, primary_key=True)
    target_name     = Column(String(length=255), primary_key=True)
    company_name    = Column(String(length=255), primary_key=True)
    url             = Column(String(length=255))
    origin_url      = Column(String(length=255), primary_key=True)
    origin_category = Column(String(length=255))
    category        = Column(String, default='job_posting')
    match           = Column(Enum(JobMatch, schema='landing'))
    title           = Column(String(length=255))
    location        = Column(String(length=255))
    scraped_at      = Column(DateTime(timezone=True), server_default=func.now())
    processed_at    = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())
    status          = Column(String)