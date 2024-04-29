import enum
from sqlalchemy import Column, BigInteger, String, DateTime, Enum
from sqlalchemy.sql import func # https://stackoverflow.com/questions/13370317/sqlalchemy-default-datetime
from db.db_config import Base

class JobMatch(enum.Enum):
    direct_match    = 1
    indirect_match  = 2

class Job(Base):
    __tablename__   = 'jobs'
    __table_args__  = {"schema": "landing", "extend_existing": True}

    url             = Column(String(length=255))
    category        = Column(String, default='job_posting')
    match           = Column(Enum(JobMatch, schema='landing'))
    target_name     = Column(String(length=255), primary_key=True)
    company_name    = Column(String(length=255), primary_key=True)
    job_id          = Column(BigInteger, primary_key=True)
    scraped_at      = Column(DateTime(timezone=True), server_default=func.now())
    processed_at    = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())
    status          = Column(String)

    def __repr__(self):
        return f"Job(url={self.url}, category={self.category}, match={self.match}, target_name={self.target_name}, company_name={self.company_name}, job_id={self.job_id}, scraped_at={self.scraped_at}, processed_at={self.processed_at}, status={self.status})"