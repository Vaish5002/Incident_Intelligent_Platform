from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Investigation(Base):
    __tablename__ = "investigations"

    id = Column(Integer, primary_key=True, index=True)

    repo_url = Column(String)

    incident_description = Column(String)

    status = Column(String)

    severity = Column(String)

    root_cause = Column(String)