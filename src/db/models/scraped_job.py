import enum
from sqlalchemy import Column, BigInteger, String, DateTime, Enum
from sqlalchemy.sql import func # https://stackoverflow.com/questions/13370317/sqlalchemy-default-datetime
from db.db_config import Base

class ScrappedJob(Base):
    __tablename__   = 'scraped_jobs'
    __table_args__  = {"schema": "processed", "extend_existing": True}

    target_name     = Column(String(length=255), primary_key=True)
    company_name    = Column(String(length=255), primary_key=True)
    job_id          = Column(BigInteger, primary_key=True)
    location        = Column(String(length=255), nullable=True)
    company         = Column(String(length=255), nullable=True)
    position_name   = Column(String(length=255), nullable=True)
    scraped_at      = Column(DateTime(timezone=True), server_default=func.now())
    processed_at    = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"ScrappedJob(target_name={self.target_name}, company={self.company_name}, job_id={self.job_id}, location={self.location}, company_name={self.company_name}, position_name={self.position_name}, scraped_at={self.scraped_at}, processed_at={self.processed_at})"